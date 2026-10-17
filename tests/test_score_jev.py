import importlib.util
import json
from pathlib import Path

import httpx

from system1.eval.ledger import CostLedger
from system1.routers.jev import JevClient


def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sj = load_script("score_jev")


def row(task, rnd, visible_pass, exec_id="e1", attempt=0):
    return {"run_id": "r", "exec_id": exec_id, "checkpoint_id": f"{task}/a{attempt}/r{rnd}", "task_id": task,
            "benchmark": "mbpp+", "attempt": attempt, "round": rnd, "task_shown": "Write f.",
            "code": "def f():\n    return 1\n", "visible_report": "ok" if visible_pass else "AssertionError",
            "visible_pass": visible_pass, "thinking": "I will return 1.", "jev_telemetry": {"visible_pass_fraction": 1.0},
            "prev_code": None if rnd == 1 else "def f():\n    return 0\n",
            "prev_report": None if rnd == 1 else "AssertionError"}


def make_run(tmp_path):
    run = tmp_path / "runs" / "r"
    store = CostLedger(run / "trajectories.jsonl")
    for r in (row("A", 1, True), row("B", 1, False, "e2"), row("B", 2, True, "e2")):
        store.append_obj(r)
    return run


def api(model="jev-1.13.0", fail_on=None, calls=None):
    def handler(request):
        body = json.loads(request.content)
        n = len(calls) if calls is not None else 0
        if calls is not None:
            calls.append(body)
        if fail_on is not None and fail_on(body, n):
            return httpx.Response(400, json={"error": "bad"})
        answers = {q: {"type": "noul", "noul": 0.3} for q in body["questions"]}
        return httpx.Response(200, json={"model": model, "answers": answers,
                                         "usage": {"input_tokens": 100, "output_tokens": 5}})
    return handler


def client(run, handler, **kw):
    return JevClient(api_key="k", transport=httpx.MockTransport(handler), sleep=lambda s: None,
                     ledger=CostLedger(run / sj.LEDGER), max_retries=0, **kw)


def last(run, name=sj.SCORES):
    rows, _ = CostLedger(run / name).read()
    return {(r["checkpoint_id"], r["arm"]): r for r in rows}, rows


def test_scores_every_checkpoint_in_both_arms_without_labels(tmp_path):
    run = make_run(tmp_path)
    calls = []
    assert sj.score_run(run, client(run, api(calls=calls)), log=lambda *a: None) == 0
    recs, rows = last(run)
    assert len(rows) == 6 and {r["status"] for r in rows} == {"ok"}
    assert all("hidden" not in json.dumps(c) for c in calls)  # the requests never carry labels
    meta = json.loads((run / sj.META).read_text())
    assert meta["model_version"] == "jev-1.13.0" and meta["protocol"]["byte_budget"] == 56_000
    assert meta["sessions"][0]["outcome"] == "finished"


def test_resume_rescores_only_checkpoints_with_a_failed_arm(tmp_path):
    run = make_run(tmp_path)
    # The trace arm of B/a0/r2 fails once (a 400 is not retried).
    fail = lambda body, n: "thinking" in body["state"] and body["state"].get("previous_code") is not None
    assert sj.score_run(run, client(run, api(fail_on=fail)), log=lambda *a: None) == 1
    calls = []
    assert sj.score_run(run, client(run, api(calls=calls)), log=lambda *a: None) == 0
    assert len(calls) == 2  # both arms of B/a0/r2, nothing else
    recs, rows = last(run)
    assert recs[("B/a0/r2", "base+history+trace")]["status"] == "ok" and len(rows) == 8


def test_refuses_another_scoring_protocol(tmp_path):
    run = make_run(tmp_path)
    assert sj.score_run(run, client(run, api()), log=lambda *a: None) == 0
    out = []
    assert sj.score_run(run, client(run, api(), byte_budget=28_000), log=out.append) == 2
    assert "differs in: byte_budget" in out[0]


def test_stops_on_a_new_model_version_across_sessions(tmp_path):
    run = make_run(tmp_path)
    assert sj.score_run(run, client(run, api()), limit=1, log=lambda *a: None) == 0
    out = []
    assert sj.score_run(run, client(run, api(model="jev-1.14.0")), log=out.append) == 1
    assert any("model changed" in line for line in out)
    assert json.loads((run / sj.META).read_text())["sessions"][-1]["outcome"] == "model_changed"


def test_token_guard_stops_before_more_calls(tmp_path):
    run = make_run(tmp_path)
    calls = []
    assert sj.score_run(run, client(run, api(calls=calls)), max_input_tokens=150, log=lambda *a: None) == 1
    assert len(calls) == 2  # one checkpoint (two arms, 200 tokens), then the guard


def test_repeat_sample_sends_the_same_requests_again(tmp_path):
    run = make_run(tmp_path)
    calls = []
    assert sj.score_run(run, client(run, api(calls=calls)), repeat=2, log=lambda *a: None) == 0
    first, _ = last(run)
    again, rows = last(run, sj.REPEAT)
    assert len(rows) == 4 and len(calls) == 10
    assert all(r["request_sha256"] == first[k]["request_sha256"] for k, r in again.items())
    assert sj.score_run(run, client(run, api(calls=calls)), repeat=2, log=lambda *a: None) == 0
    assert len(calls) == 10  # nothing left to score
