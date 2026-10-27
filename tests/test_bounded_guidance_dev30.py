"""Offline checks for the frozen development batch; no model or Azure calls."""

import asyncio
import hashlib
import json
import sys
from argparse import Namespace
from pathlib import Path

import httpx
import pytest

from system1.bounded_guidance import (DEV30_PLANNER_INSTRUCTIONS, dev30_plan_messages,
                                      run_pair, validate_plan)
from system1.bounded_guidance_dev30 import (DEBUG_TASKS, MANIFEST_PATH, MAX_PAIRS, load_manifest,
                                           select_tasks)
from system1.eval.exclusions import load_exclusions
from system1.eval.split import load_split
from system1.loop.tasks import TaskSpec, load_tasks

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from analyze_bounded_guidance_dev30 import analyze
from preflight_bounded_guidance_planner import PREFLIGHT_INSTRUCTIONS
from grade_bounded_guidance import generation_is_gradable
from run_bounded_guidance import (DEV30_TASKS_FILE, MockAdviser, MockVisible,
                                  MockWorker, RecordingWorkerClient, validate_pilot_limits)
from system1.eval.ledger import CostLedger


def test_fixed_selection_and_successful_preflight_prompt():
    manifest, digest = load_manifest()
    assert len(manifest["tasks"]) == len(set(manifest["tasks"])) == MAX_PAIRS == 30
    assert manifest["tasks"] == select_tasks()
    assert not set(DEBUG_TASKS) & set(manifest["tasks"])
    split, exclusions, tasks = load_split()["benchmarks"], load_exclusions()["tasks"], load_tasks()
    for tid in manifest["tasks"]:
        assert tid in split[tasks[tid].benchmark]["dev"] and tid not in exclusions
    assert digest == hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest()
    assert DEV30_PLANNER_INSTRUCTIONS == PREFLIGHT_INSTRUCTIONS
    task = TaskSpec("Mock/1", "mock", "Check x.", "f", (), "mock", "")
    prompt = dev30_plan_messages(task, "def f(x): return x", "visible pass")[0]["content"]
    assert prompt.startswith(PREFLIGHT_INSTRUCTIONS)
    assert "Task and visible examples:" in prompt
    assert validate_plan("No clear defect is evident; check boundary cases.")


def test_dev30_limits_are_exact_and_no_partial_batch():
    args = Namespace(split="dev", attempts=1, tasks_file=DEV30_TASKS_FILE, limit=0,
                     limit_usd=0.60, max_frontier_requests=30,
                     max_worker_http_requests=180, max_wall_seconds=5400)
    validate_pilot_limits(args)
    for change in ({"limit": 1}, {"limit_usd": 0.61}, {"max_frontier_requests": 31},
                   {"max_worker_http_requests": 181}, {"max_wall_seconds": 5401}):
        with pytest.raises(SystemExit):
            validate_pilot_limits(Namespace(**(vars(args) | change)))


def test_unequal_effective_continuation_caps_stop_before_branches():
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return messages[0]["content"]
        def __call__(self, text):
            return {"input_ids": text.split()}

    class Worker(MockWorker):
        tokenizer = Tokenizer()
        think_cap = 10
        code_tokens = 2
        max_model_len = 0

    task = TaskSpec("Mock/1", "mock", "Implement add_one(x).", "add_one",
                    ({"kind": "assert", "source": "assert add_one(1) == 2"},), "mock", "")
    worker, adviser = Worker(), MockAdviser()
    # The guided prompt has more tokens; this context ceiling keeps the control
    # at 10 but would silently lower the guided cap without the integrity check.
    from system1.bounded_guidance import continuation_messages
    base = continuation_messages(task, "def add_one(x): return x", "visible fail")
    worker.max_model_len = len(base[0]["content"].split()) + worker.code_tokens + 16 + worker.think_cap
    with pytest.raises(RuntimeError, match="unequal or exhausted"):
        asyncio.run(run_pair(task, 0, worker, MockVisible(), adviser,
                             require_equal_continuation_caps=True))
    assert worker.calls == 1 and adviser.calls == 1


def test_task_accounting_keeps_failure_and_unstarted_tasks(tmp_path):
    manifest, digest = load_manifest()
    run = tmp_path / "run"
    run.mkdir()
    (run / "run_meta.json").write_text(json.dumps({"protocol": {
        "pilot_profile": "dev30-v1", "task_ids": manifest["tasks"],
        "task_file_sha256": digest, "split": "dev", "attempts": 1}}))
    tid = manifest["tasks"][0]
    (run / "failures.jsonl").write_text(json.dumps({"task_id": tid,
        "error_type": "ReadTimeout", "error": "timed out"}) + "\n")
    summary, rows = analyze(run, manifest, digest)
    assert summary["task_status_counts"] == {"infrastructure_failed": 1, "not_started": 29}
    assert rows[0]["task_id"] == tid and rows[0]["status"] == "infrastructure_failed"
    assert summary["paired_results"] is None
    assert summary["request_counts"] == {"qwen_http": 0, "frontier": 0}


def test_invalid_delivery_pair_remains_in_paired_results(tmp_path):
    manifest, digest = load_manifest()
    run = tmp_path / "run"
    run.mkdir()
    (run / "run_meta.json").write_text(json.dumps({"protocol": {
        "pilot_profile": "dev30-v1", "task_ids": manifest["tasks"],
        "task_file_sha256": digest, "split": "dev", "attempts": 1}}))
    tid, pair_id = manifest["tasks"][0], "pair1"
    code = "def f(): return 1\n"
    sha = hashlib.sha256(code.encode()).hexdigest()
    rows = [{"checkpoint_id": f"{tid}/a0/{arm}/r2", "code": code}
            for arm in ("control", "guidance")]
    pair = {"pair_id": pair_id, "task_id": tid, "benchmark": "humaneval+",
            "attempt": 0, "first_visible_pass": False,
            "advice_delivery": "invalid", "plan_call_id": "plan1", "rows": rows,
            "final_checkpoint_ids": {arm: f"{tid}/a0/{arm}/r2" for arm in ("control", "guidance")}}
    plan = {"pair_id": pair_id, "task_id": tid, "call_id": "plan1",
            "delivery_status": "invalid"}
    labels = [{"pair_id": pair_id, "task_id": tid, "arm": arm, "checkpoint_id": f"{tid}/a0/{arm}/r2",
               "code_sha256": sha, "passed": arm == "guidance"}
              for arm in ("control", "guidance")]
    for name, records in (("pairs.jsonl", [pair]), ("plans.jsonl", [plan]),
                          ("bounded_hidden_labels.jsonl", labels),
                          ("ledger.jsonl", [{"task_id": tid, "component": "frontier",
                                               "usd_reported": 0.004}])):
        (run / name).write_text("".join(json.dumps(x) + "\n" for x in records))
    summary, task_rows = analyze(run, manifest, digest)
    assert summary["delivery_status_counts"] == {"invalid": 1}
    assert summary["paired_results"]["rescues"] == 1
    assert summary["paired_results"]["population"] == "graded_subset_only"
    assert task_rows[0]["status"] == "graded"
    assert summary["cost"]["frontier_recorded_or_computed_usd"] == 0.004


def test_raw_qwen_exchange_has_one_attempt_and_a_hard_ceiling(tmp_path):
    def respond(request):
        return httpx.Response(200, json={"choices": [{"text": "ok"}],
                                         "usage": {"prompt_tokens": 2, "completion_tokens": 1}})
    async def exercise():
        async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:
            logger = RecordingWorkerClient(client, CostLedger(tmp_path / "exchanges.jsonl"), 1)
            logger.task_id = "T"
            response = await logger.post("https://example.test/v1/completions",
                                         json={"prompt": "p"}, timeout=1)
            assert response.status_code == 200
            with pytest.raises(RuntimeError, match="ceiling"):
                await logger.post("https://example.test/v1/completions",
                                  json={"prompt": "again"}, timeout=1)
    asyncio.run(exercise())
    exchanges = [json.loads(x) for x in (tmp_path / "exchanges.jsonl").read_text().splitlines()]
    assert len(exchanges) == 1 and exchanges[0]["task_id"] == "T"
    assert exchanges[0]["request_body"] == {"prompt": "p"}
    assert exchanges[0]["response_body"]["usage"]["completion_tokens"] == 1


def test_stopped_dev30_grades_completed_pairs_without_resuming_generation():
    meta = {"protocol": {"pilot_profile": "dev30-v1"},
            "sessions": [{"status": "stopped"}]}
    assert generation_is_gradable(meta, real=True)
    assert not generation_is_gradable(meta, real=False)
    meta["protocol"]["pilot_profile"] = None
    assert not generation_is_gradable(meta, real=True)
