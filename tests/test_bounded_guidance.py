"""Protocol and safety checks; all actors are mocked and no code is executed."""

import asyncio
import sys
import httpx
from argparse import Namespace
from dataclasses import replace
from pathlib import Path

import pytest

from system1.bounded_guidance import InvalidPlan, plan_messages, run_pair, validate_plan
from system1.loop.tasks import TaskSpec
from system1.eval.ledger import CostLedger
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from run_bounded_guidance import (BoundedAdviser, MockAdviser, MockVisible, MockWorker,
                                  PILOT_TASKS_FILE, run, validate_pilot_limits)
from grade_bounded_guidance import final_units
from analyze_bounded_guidance import stats, task_bootstrap


TASK = TaskSpec("Mock/1", "mock", "Implement add_one(x).", "add_one",
                ({"kind": "assert", "source": "assert add_one(1) == 2"},), "mock", "")


def test_shared_draft_and_branch_isolation():
    worker, visible, adviser = MockWorker(), MockVisible(), MockAdviser()
    pair = asyncio.run(run_pair(TASK, 0, worker, visible, adviser))
    assert worker.calls == 3  # one shared and one continuation per arm
    assert adviser.calls == 1
    assert pair.rows[0]["arm"] == "shared" and pair.rows[0]["round"] == 1
    assert {(r["arm"], r["round"]) for r in pair.rows[1:]} == {("control", 2), ("guidance", 2)}
    assert not pair.final["control"]["visible_pass"] and pair.final["guidance"]["visible_pass"]
    assert pair.rows[1]["prompt_sha256"] != pair.rows[2]["prompt_sha256"]
    control = next(r for r in pair.rows if r["arm"] == "control")
    assert pair.rows[0]["code_sha256"] == control["code_sha256"]
    assert "Advice from a separate assistant" not in control["prompt_messages"][0]["content"]
    assert all("hidden" not in str(row).lower() for row in pair.rows)


def test_first_visible_pass_still_receives_the_same_budgeted_intervention():
    class FirstPassWorker(MockWorker):
        async def generate(self, *args, **kwargs):
            g = await super().generate(*args, **kwargs)
            return replace(g, code="def add_one(x):\n    return x + 1\n")

    worker, adviser = FirstPassWorker(), MockAdviser()
    pair = asyncio.run(run_pair(TASK, 0, worker, MockVisible(), adviser))
    assert worker.calls == 3 and adviser.calls == 1
    assert pair.plan is not None and len(pair.rows) == 3
    assert pair.rows[0]["visible_pass"]


def test_plan_bounds_and_invalid_delivery_remains_in_treatment():
    instruction = plan_messages(TASK, "def add_one(x): return x", "visible fail")[0]["content"]
    assert "120 whitespace-separated words and 900 characters" in instruction
    assert "after trimming leading and trailing whitespace" in instruction
    assert validate_plan("  Check the edge case.  ") == "Check the edge case."
    assert validate_plan("x" * 900) == "x" * 900
    assert len(validate_plan("word " * 120).split()) == 120
    for bad in (None, "", "word " * 121, "x" * 901, "```python\nx=1\n```"):
        with pytest.raises(InvalidPlan):
            validate_plan(bad)

    class BadAdviser(MockAdviser):
        def ask(self, *args, **kwargs):
            return replace(super().ask(*args, **kwargs), content="```python\nx=1\n```")

    worker, saved = MockWorker(), []
    pair = asyncio.run(run_pair(TASK, 0, worker, MockVisible(), BadAdviser(), on_advice=saved.append))
    assert worker.calls == 3 and len(pair.rows) == 3
    assert pair.plan["delivery_status"] == "invalid"
    assert pair.plan["invalid_reason"] == "adviser response contains a code fence"
    assert saved == [pair.plan]
    assert pair.final["control"]["prompt_messages"] == pair.final["guidance"]["prompt_messages"]


@pytest.mark.parametrize("content,finish,expected", [
    ("Check the edge case.", "stop", "delivered"),
    ("word " * 121, "stop", "invalid"),
    ("", "stop", "invalid"),
    ("Check the edge case.", "length", "invalid"),
    (None, "stop", "invalid"),  # reasoning-only response has no visible content
])
def test_advice_response_classes(content, finish, expected):
    class Adviser(MockAdviser):
        def ask(self, *args, **kwargs):
            return replace(super().ask(*args, **kwargs), content=content, finish_reason=finish)

    pair = asyncio.run(run_pair(TASK, 0, MockWorker(), MockVisible(), Adviser()))
    assert pair.plan["delivery_status"] == expected
    if expected == "invalid":
        assert pair.final["control"]["prompt_messages"] == pair.final["guidance"]["prompt_messages"]
    else:
        assert pair.final["control"]["prompt_messages"] != pair.final["guidance"]["prompt_messages"]


def test_reasoning_only_provider_response_is_saved_and_charged(tmp_path):
    response_body = {"id": "fake-id", "model": "anthropic/claude-sonnet-5.5",
        "choices": [{"finish_reason": "stop", "message": {"content": None,
                     "reasoning": "internal text is not advice"}}],
        "usage": {"prompt_tokens": 50, "completion_tokens": 30, "cost": 0.0004,
                  "completion_tokens_details": {"reasoning_tokens": 30}}}

    class Client:
        def post(self, url, json):
            self.request = json
            return httpx.Response(200, json=response_body)

    adviser = BoundedAdviser.__new__(BoundedAdviser)
    adviser.client = Client()
    adviser.ledger = CostLedger(tmp_path / "ledger.jsonl")
    adviser.exchanges = CostLedger(tmp_path / "exchanges.jsonl")
    adviser.limit_usd = 0.01
    adviser.p_in, adviser.p_out = 2.0, 10.0
    adviser.prices = {}
    adviser.usd_for = lambda prices, model, inp, out: 0.0004
    reply = adviser.ask([{"role": "user", "content": "task"}], task_id="T", sample=0)
    assert reply.content is None and reply.finish_reason == "stop"
    exchange = adviser.exchanges.read()[0][0]
    assert exchange["response_body"]["choices"][0]["message"]["reasoning"] == "internal text is not advice"
    assert exchange["request_body"]["max_tokens"] == 512
    assert "Authorization" not in str(exchange)
    assert adviser.ledger.read()[0][0]["usd_reported"] == 0.0004


@pytest.mark.parametrize("change,expected", [
    ({"usage": {}}, "missing usage"),
    ({"choices": [{"finish_reason": "unknown", "message": {"content": "Fix x."}}]}, "finish reason"),
    ({"model": "other/model"}, "returned model"),
    ({"provider": "other"}, "returned provider"),
    ({"choices": [{"finish_reason": "stop", "message": {"content": ["Fix x."]}}]}, "non-string content"),
])
def test_provider_integrity_failures_log_and_stop(tmp_path, change, expected):
    body = {"model": "anthropic/claude-sonnet-5.5",
            "choices": [{"finish_reason": "stop", "message": {"content": "Fix x."}}],
            "usage": {"prompt_tokens": 50, "completion_tokens": 30, "cost": 0.0004}}
    body.update(change)

    class Client:
        def post(self, url, json):
            return httpx.Response(200, json=body)

    adviser = BoundedAdviser.__new__(BoundedAdviser)
    adviser.client = Client()
    adviser.ledger = CostLedger(tmp_path / "ledger.jsonl")
    adviser.exchanges = CostLedger(tmp_path / "exchanges.jsonl")
    adviser.limit_usd = 0.01
    adviser.p_in, adviser.p_out = 2.0, 10.0
    adviser.prices = {}
    adviser.usd_for = lambda prices, model, inp, out: 0.0004
    with pytest.raises(RuntimeError, match=expected):
        adviser.ask([{"role": "user", "content": "task"}], task_id="T", sample=0)
    assert len(adviser.ledger.read()[0]) == len(adviser.exchanges.read()[0]) == 1


def test_reported_spend_violation_stops_after_charge_is_logged(tmp_path):
    body = {"model": "anthropic/claude-sonnet-5.5",
            "choices": [{"finish_reason": "stop", "message": {"content": "Fix x."}}],
            "usage": {"prompt_tokens": 50, "completion_tokens": 30, "cost": 0.02}}

    class Client:
        def post(self, url, json):
            return httpx.Response(200, json=body)

    adviser = BoundedAdviser.__new__(BoundedAdviser)
    adviser.client = Client()
    adviser.ledger = CostLedger(tmp_path / "ledger.jsonl")
    adviser.exchanges = CostLedger(tmp_path / "exchanges.jsonl")
    adviser.limit_usd = 0.01
    adviser.p_in, adviser.p_out = 2.0, 10.0
    adviser.prices = {}
    adviser.usd_for = lambda prices, model, inp, out: 0.0004
    with pytest.raises(RuntimeError, match="spending violation"):
        adviser.ask([{"role": "user", "content": "task"}], task_id="T", sample=0)
    assert adviser.ledger.read()[0][0]["usd_reported"] == 0.02
    assert len(adviser.exchanges.read()[0]) == 1


def test_grader_rejects_code_hash_mismatch_and_paired_bootstrap_keeps_tasks():
    pair = asyncio.run(run_pair(TASK, 0, MockWorker(), MockVisible(), MockAdviser()))
    stored = {"pair_id": pair.pair_id, "task_id": TASK.task_id, "benchmark": TASK.benchmark,
              "attempt": 0, "rows": pair.rows,
              "final_checkpoint_ids": {a: r["checkpoint_id"] for a, r in pair.final.items()}}
    assert len(final_units([stored])) == 2
    pair.rows[-1]["code_sha256"] = "tampered"
    with pytest.raises(ValueError, match="code hash mismatch"):
        final_units([stored])
    records = [{"task_id": "A", "control_pass": False, "guidance_pass": True,
                "first_visible_pass": False},
               {"task_id": "A", "control_pass": False, "guidance_pass": True,
                "first_visible_pass": False},
               {"task_id": "B", "control_pass": True, "guidance_pass": False,
                "first_visible_pass": False}]
    assert stats(records)["paired_delta"] == pytest.approx(1 / 3)
    assert task_bootstrap(records, draws=1000) == [-1.0, 1.0]


def test_real_mode_rejects_missing_approval_before_any_client_is_created():
    with pytest.raises(SystemExit, match="operator-approved"):
        asyncio.run(run(Namespace(mock=False, real=True, operator_approved=False, limit_usd=None)))


def test_frontier_guard_rejects_unaffordable_call_before_http(tmp_path):
    adviser = BoundedAdviser.__new__(BoundedAdviser)
    adviser.ledger = CostLedger(tmp_path / "ledger.jsonl")
    adviser.limit_usd = 0.0001
    adviser.p_in, adviser.p_out = 2.0, 10.0
    with pytest.raises(RuntimeError, match="spend guard"):
        adviser.ask([{"role": "user", "content": "shown task only"}], task_id="T", sample=0)
    assert adviser.ledger.read()[0] == []


def test_pilot_caps_and_frozen_label_independent_sample():
    import json
    from collections import Counter
    from system1.eval.split import load_split
    from system1.loop.tasks import load_tasks

    args = Namespace(split="dev", attempts=1, tasks_file=PILOT_TASKS_FILE,
                     limit_usd=1.5, max_frontier_requests=120,
                     max_worker_http_requests=720, max_wall_seconds=9000)
    validate_pilot_limits(args)
    for change in ({"limit_usd": 1.51}, {"max_wall_seconds": 9001},
                   {"max_worker_http_requests": 721}, {"max_frontier_requests": 121}):
        with pytest.raises(SystemExit):
            validate_pilot_limits(Namespace(**(vars(args) | change)))
    sample = json.loads((Path(__file__).resolve().parents[1] / PILOT_TASKS_FILE).read_text())["tasks"]
    assert len(sample) == len(set(sample)) == 120
    split = load_split()["benchmarks"]
    tasks = load_tasks()
    assert all(tid in split[tasks[tid].benchmark]["dev"] for tid in sample)
    assert Counter(tasks[tid].benchmark for tid in sample) == {"humaneval+": 36, "mbpp+": 84}
