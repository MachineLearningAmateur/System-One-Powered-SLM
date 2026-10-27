"""Protocol and safety checks; all actors are mocked and no code is executed."""

import asyncio
import sys
from argparse import Namespace
from dataclasses import replace
from pathlib import Path

import pytest

from system1.bounded_guidance import InvalidPlan, run_pair, validate_plan
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


def test_plan_bounds_stop_pair_without_silent_control_fallback():
    assert validate_plan("  Check the edge case.  ") == "Check the edge case."
    for bad in (None, "", "word " * 121, "x" * 901, "```python\nx=1\n```"):
        with pytest.raises(InvalidPlan):
            validate_plan(bad)

    class BadAdviser(MockAdviser):
        def ask(self, *args, **kwargs):
            return replace(super().ask(*args, **kwargs), content="```python\nx=1\n```")

    worker = MockWorker()
    with pytest.raises(InvalidPlan):
        asyncio.run(run_pair(TASK, 0, worker, MockVisible(), BadAdviser()))
    assert worker.calls == 1


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
