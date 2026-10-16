"""Loop runner, driver, labels, grader rules and run telemetry (no Docker, no GPU)."""

import argparse
import asyncio
import importlib.util
import json
from pathlib import Path

import httpx
import numpy as np
import pytest

from system1.eval.labels import LabelError, code_sha, load_labelled
from system1.eval.ledger import CostLedger
from system1.features.telemetry import cheap_features
from system1.loop import monitor
from system1.loop.generate import Generation
from system1.loop.runner import (
    AttemptFailed,
    RunContext,
    complete_executions,
    execution_is_complete,
    run_attempt,
    to_scoring_checkpoint,
)
from system1.loop.sandbox import SandboxError, VisibleRunner
from system1.loop.tasks import TaskSpec, format_test_report

OK = {"status": "ok", "stage": None, "error_type": None, "message": None}


class FakeVisible:
    def __init__(self, visible_seq, fail_on_call=None):
        self.visible_seq = list(visible_seq)
        self.fail_on_call = fail_on_call
        self.calls = 0

    def protocol(self):
        return {"visible_image_id": "sha256:test"}

    def run(self, code, tests, timeout):
        self.calls += 1
        if self.calls == self.fail_on_call:
            raise SandboxError("no reply")
        statuses = self.visible_seq.pop(0) if self.visible_seq else ["pass"] * len(tests)
        return {"execution": OK, "runner": "test",
                "results": [{"status": s, "error_type": None if s == "pass" else "AssertionError", "message": "m"}
                            for s in statuses]}


class FakeGen:
    def __init__(self, codes, fail_at=None):
        self.codes = list(codes)
        self.fail_at = fail_at
        self.n = 0
        self.seen_messages = []

    async def generate(self, messages, task_prompt, entry_point, *seed, on_call=None):
        self.n += 1
        self.seen_messages.append(messages[-1]["content"])
        if self.n == self.fail_at:
            if on_call:
                on_call({"phase": "thinking", "input_tokens": None, "output_tokens": None, "reasoning_tokens": None,
                         "latency_ms": 1.0, "status": "error:ConnectError"})
            raise httpx.ConnectError("vLLM down")
        phases = [{"phase": "thinking", "input_tokens": 10, "output_tokens": 5, "reasoning_tokens": 5,
                   "latency_ms": 1.0, "status": "ok"},
                  {"phase": "answer", "input_tokens": 19, "output_tokens": 2, "reasoning_tokens": 0,
                   "latency_ms": 1.0, "status": "ok"}]
        for ph in phases:
            if on_call:
                on_call(ph)
        code = self.codes.pop(0)
        return Generation("h", 10, "think about it", "ans", code, [], 5, 2, 100, False, True, 1.0, 7,
                          {"thinking": {"n_tokens": 5}, "answer": {"n_tokens": 2}},
                          {"thinking_logprob": np.zeros(5, dtype=np.float16)},
                          no_code_reason=None if code else "no_block", phases=phases)


TASK = TaskSpec("Mbpp/2", "mbpp+", "Write f.", "f", ({"kind": "assert", "source": "assert f(1) == 2"},),
                "prompt_assert", "")


def make_ctx(tmp_path, gen, vis):
    return RunContext("run", "dev", gen, vis, CostLedger(tmp_path / "traj.jsonl"),
                      CostLedger(tmp_path / "ledger.jsonl"), CostLedger(tmp_path / "failures.jsonl"),
                      tmp_path / "logprobs")


# --- runner ----------------------------------------------------------------------

def test_attempt_stops_at_visible_pass_and_has_no_hidden_label(tmp_path):
    ctx = make_ctx(tmp_path, FakeGen(["c1", "c2", "c3"]), FakeVisible([["fail"], ["pass"]]))
    recs = asyncio.run(run_attempt(ctx, TASK, 0))
    assert [r["round"] for r in recs] == [1, 2] and recs[-1]["visible_pass"]
    assert "hidden" not in recs[-1] and recs[-1]["visible_execution"] == OK
    assert recs[1]["prev_code"] == "c1" and "0 of 1" in recs[1]["prev_report"]
    assert len({r["exec_id"] for r in recs}) == 1
    rows, _ = CostLedger(tmp_path / "traj.jsonl").read()
    assert len(rows) == 2 and (tmp_path / rows[0]["logprob_arrays"]).exists()
    led, _ = CostLedger(tmp_path / "ledger.jsonl").read()
    assert [(r["step"], r["arm"], r["http_attempt"], r["status"]) for r in led] == [
        (1, "thinking", 0, "ok"), (1, "answer", 1, "ok"), (2, "thinking", 0, "ok"), (2, "answer", 1, "ok")]


def test_three_rounds_then_stop_and_missing_code(tmp_path):
    ctx = make_ctx(tmp_path, FakeGen([None, "c2", "c3"]), FakeVisible([["fail"], ["fail"]]))
    recs = asyncio.run(run_attempt(ctx, TASK, 1))
    assert len(recs) == 3 and recs[0]["visible_execution"]["status"] == "no_code"
    assert recs[0]["visible_results"][0]["status"] == "not_run" and recs[1]["prev_code"] == ""
    assert recs[0]["visible_report"].startswith("No code to test: the answer contains no")


def test_generation_error_is_recorded_and_stops_the_attempt(tmp_path):
    ctx = make_ctx(tmp_path, FakeGen(["c1"], fail_at=2), FakeVisible([["fail"]]))
    with pytest.raises(AttemptFailed):
        asyncio.run(run_attempt(ctx, TASK, 0))
    fails, _ = CostLedger(tmp_path / "failures.jsonl").read()
    assert fails[0]["stage"] == "generate" and fails[0]["round"] == 2
    led, _ = CostLedger(tmp_path / "ledger.jsonl").read()
    assert [r["status"] for r in led] == ["ok", "ok", "error:ConnectError"]  # earlier calls stay counted


def test_sandbox_error_keeps_the_generation_cost_and_never_reaches_the_model(tmp_path):
    gen = FakeGen(["c1", "c2"])
    ctx = make_ctx(tmp_path, gen, FakeVisible([["fail"]], fail_on_call=1))
    with pytest.raises(AttemptFailed):
        asyncio.run(run_attempt(ctx, TASK, 0))
    rows, _ = CostLedger(tmp_path / "traj.jsonl").read()
    assert rows == [] and gen.n == 1  # no record, no revise prompt with harness text
    fails, _ = CostLedger(tmp_path / "failures.jsonl").read()
    assert fails[0]["stage"] == "sandbox"
    led, _ = CostLedger(tmp_path / "ledger.jsonl").read()
    assert [r["arm"] for r in led] == ["thinking", "answer", None] and led[-1]["status"] == "sandbox:SandboxError"


def row(exec_id, rnd, vp, task="T", attempt=0):
    return {"exec_id": exec_id, "round": rnd, "visible_pass": vp, "task_id": task, "attempt": attempt}


def test_complete_executions_drops_incomplete_and_older_copies():
    rows = [row("old", 1, False), row("old", 2, True),           # complete, then rerun
            row("cut", 1, False),                                 # incomplete
            row("new", 1, False), row("new", 2, False), row("new", 3, False),
            row("other", 1, True, task="U")]
    dropped = []
    kept = complete_executions(rows, dropped=dropped)
    assert {(r["exec_id"], r["round"]) for r in kept} == {("new", 1), ("new", 2), ("new", 3), ("other", 1)}
    assert {(d["exec_id"], d["reason"]) for d in dropped} == {("old", "replaced"), ("cut", "incomplete")}


def test_execution_validation_is_strict():
    assert not execution_is_complete([row("a", 3, False)])  # a lone round 3
    assert not execution_is_complete([row("a", 1, False), row("a", 1, False), row("a", 2, True)])  # duplicate
    assert not execution_is_complete([row("a", 1, True), row("a", 2, True)])  # rounds after a visible pass
    assert not execution_is_complete([row("a", 1, False), row("a", 2, False, task="X")])  # two tasks
    assert not execution_is_complete([row("a", r, False) for r in (1, 2, 3, 4)])  # too many rounds
    assert execution_is_complete([row("a", 1, False), row("a", 2, True)])


def test_scoring_checkpoint_from_record_has_no_label(tmp_path):
    ctx = make_ctx(tmp_path, FakeGen(["c1", "c2"]), FakeVisible([["fail"], ["pass"]]))
    r1, r2 = asyncio.run(run_attempt(ctx, TASK, 0))
    c1, c2 = to_scoring_checkpoint(r1), to_scoring_checkpoint(r2)
    assert c1.prev_code is None and c2.prev_code == "c1" and c2.prev_test_output == r1["visible_report"]
    fields = {f: getattr(c2, f) for f in c2.__dataclass_fields__}
    assert "hidden" not in json.dumps(fields) and c2.telemetry == r2["jev_telemetry"]


# --- visible results: report and telemetry ------------------------------------------

TESTS3 = tuple({"kind": "assert", "source": f"assert f({i}) == {i}"} for i in range(3))


def test_report_shows_a_load_failure_and_tests_not_run():
    ex = {"status": "error", "stage": "load", "error_type": "SyntaxError", "message": "invalid syntax"}
    res = [{"status": "not_run", "error_type": None, "message": None}] * 3
    rep = format_test_report(TESTS3, res, ex)
    assert rep.splitlines()[0] == "The code did not load: SyntaxError: invalid syntax"
    assert rep.count("NOT_RUN") == 3 and rep.endswith("0 of 3 visible tests passed")


def test_not_run_is_not_a_failure_in_the_features():
    ex = {"status": "timeout", "stage": "test", "error_type": "Timeout", "message": "no result within 10 s"}
    res = [{"status": "pass", "error_type": None}, {"status": "timeout", "error_type": "Timeout"},
           {"status": "not_run", "error_type": None}]
    f = cheap_features([{"code": "x", "results": res, "execution": ex, "thinking": "", "thinking_tokens": 0,
                         "cap_hit": False, "think_closed": True, "confidence": {}}])
    assert f["visible_pass_count"] == 1 and f["visible_not_run_count"] == 1 and not f["visible_pass"]
    assert f["error_types"] == ["Timeout"] and f["execution_status"] == "timeout"


# --- driver (scripts/run_loop.py) ----------------------------------------------------

def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class DriverGen(FakeGen):
    """Always code 'c'; any attempt of task 'B' gets a vLLM error."""

    async def generate(self, messages, task_prompt, entry_point, seed_tag, task_id, attempt, rnd, on_call=None):
        if task_id == "B":
            raise httpx.ConnectError("vLLM down")
        self.codes = ["c"]
        return await super().generate(messages, task_prompt, entry_point, seed_tag, task_id, attempt, rnd,
                                      on_call=on_call)


class FakeSampler:
    def __init__(self, path):
        pass

    def start(self):
        return self

    def stop(self):
        return {"power_samples": 0, "energy_wh": None, "mean_power_w": None}


@pytest.fixture
def driver(tmp_path, monkeypatch):
    drv = load_script("run_loop")
    task = lambda tid: TaskSpec(tid, "mbpp+", "Write f.", "f", TASK.visible_tests, "prompt_assert", "")
    monkeypatch.setattr(drv, "RESULTS", tmp_path)
    monkeypatch.setattr(drv, "load_split", lambda: {"benchmarks": {"humaneval+": {"dev": []},
                                                                   "mbpp+": {"dev": ["A", "B", "C"]}}})
    monkeypatch.setattr(drv, "load_tasks", lambda: {t: task(t) for t in "ABC"})
    monkeypatch.setattr(drv, "VisibleRunner", lambda max_concurrent: FakeVisible([]))
    monkeypatch.setattr(drv, "load_tokenizer", lambda: None)
    monkeypatch.setattr(drv, "git_state", lambda: ("abc123", False))
    monkeypatch.setattr(drv.monitor, "vllm_metrics", lambda: {"num_preemptions_total": 0.0})
    monkeypatch.setattr(drv.monitor, "vllm_server_identity",
                        lambda expected: {"vllm_image_id": "sha256:v", "vllm_models": [("m", 16384)]})
    monkeypatch.setattr(drv.monitor, "PowerSampler", FakeSampler)
    monkeypatch.setattr(drv, "Generator", lambda client, tok: DriverGen([]))
    args = argparse.Namespace(run_id="r", split="dev", benchmark="all", limit=0, tasks_file="", attempts=2,
                              first_attempt=0,
                              concurrency=2, visible_workers=2, allow_dirty=False)
    return drv, args


def test_driver_runs_skips_finished_attempts_and_survives_a_failed_one(driver, tmp_path, capsys):
    drv, args = driver
    assert asyncio.run(drv.main_async(args)) == 1  # B's attempts are still incomplete
    out = capsys.readouterr().out
    assert "6 attempts to run (0 already done)" in out and out.count("FAILED AttemptFailed") == 2
    rows, _ = CostLedger(tmp_path / "runs" / "r" / "trajectories.jsonl").read()
    assert {(r["task_id"], r["attempt"]) for r in rows} == {("A", 0), ("A", 1), ("C", 0), ("C", 1)}
    fails, _ = CostLedger(tmp_path / "runs" / "r" / "failures.jsonl").read()
    assert {(f["task_id"], f["attempt"]) for f in fails} == {("B", 0), ("B", 1)}

    # Resume: only the failed attempts run again; every session is kept.
    assert asyncio.run(drv.main_async(args)) == 1
    assert "2 attempts to run (4 already done)" in capsys.readouterr().out
    meta = json.loads((tmp_path / "runs" / "r" / "run_meta.json").read_text(encoding="utf-8"))
    assert meta["protocol"]["max_rounds"] == 3 and meta["protocol"]["git_commit"] == "abc123"
    assert [s["n_jobs"] for s in meta["sessions"]] == [6, 2] and meta["sessions"][0]["elapsed_s"] is not None
    assert meta["sessions"][0]["outcome"] == "finished" and meta["protocol"]["generation_concurrency"] == 2
    assert meta["sessions"][0]["vllm_delta"] == {"num_preemptions_total": 0.0} and not meta["non_protocol"]


def test_driver_refuses_a_resume_with_another_protocol(driver, monkeypatch, capsys):
    drv, args = driver
    asyncio.run(drv.main_async(args))
    monkeypatch.setattr(drv, "THINK_CAP", 12_288)
    assert asyncio.run(drv.main_async(args)) == 2
    assert "differs in: think_cap" in capsys.readouterr().out


def test_driver_refuses_a_dirty_tree_unless_allowed(driver, monkeypatch, tmp_path):
    drv, args = driver
    monkeypatch.setattr(drv, "git_state", lambda: ("abc123", True))
    assert asyncio.run(drv.main_async(args)) == 2
    args.allow_dirty = True
    asyncio.run(drv.main_async(args))
    meta = json.loads((tmp_path / "runs" / "r" / "run_meta.json").read_text(encoding="utf-8"))
    assert meta["non_protocol"] is True and meta["protocol"]["git_dirty"] is True


def test_driver_refuses_the_test_split(monkeypatch):
    drv = load_script("run_loop")
    monkeypatch.setattr("sys.argv", ["run_loop.py", "--run-id", "x", "--split", "test"])
    assert drv.main() == 1


# --- grader rules and labels -------------------------------------------------------

def test_majority_vote_rules():
    decide = load_script("grade_hidden").decide
    p = lambda passed, valid=True: {"valid": valid, "passed": passed, "base": "b", "plus": "p"}
    assert decide([p(True), p(True)])[0] == "pass"
    assert decide([p(False), p(False)])[0] == "fail"
    assert decide([p(True), p(False)])[0] == "undecided"              # needs a third grade
    assert decide([p(True), p(False), p(True)])[0] == "pass"
    assert decide([p(True), p(None, valid=False)])[0] == "undecided"  # an invalid grade is not a vote
    assert decide([p(True), p(None, valid=False), p(None, valid=False)])[0] == "invalid"


def write_jsonl(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def test_labels_join_only_on_matching_complete_checkpoints(tmp_path):
    cps = [{**row("e1", 1, False), "checkpoint_id": "T/a0/r1", "code": "c1"},
           {**row("e1", 2, True), "checkpoint_id": "T/a0/r2", "code": "c2"}]
    write_jsonl(tmp_path / "trajectories.jsonl", cps)
    (tmp_path / "grade_sessions").mkdir()
    (tmp_path / "grade_sessions" / "s1.json").write_text(json.dumps({"protocol": True}), encoding="utf-8")
    (tmp_path / "grade_sessions" / "s2.json").write_text(json.dumps({"protocol": False}), encoding="utf-8")
    lab = lambda cp, code, status="pass", session="s1": {
        "exec_id": "e1", "checkpoint_id": cp, "code_sha256": code_sha(code), "grade_session": session,
        "status": status, "passed": status == "pass", "base": "pass", "plus": "pass", "n_valid_votes": 2}
    write_jsonl(tmp_path / "hidden_labels.jsonl", [lab("T/a0/r1", "c1", "fail"), lab("T/a0/r2", "c2")])
    report = {}
    rows = load_labelled(tmp_path, report=report)
    assert [r["hidden"]["passed"] for r in rows] == [False, True] and report["grade_session"] == "s1"

    def refused(labels, match, **kw):
        write_jsonl(tmp_path / "hidden_labels.jsonl", labels)
        with pytest.raises(LabelError, match=match):
            load_labelled(tmp_path, **kw)

    refused([lab("T/a0/r1", "c1")], "no label")
    refused([lab("T/a0/r1", "c1"), lab("T/a0/r2", "other code")], "other code")
    refused([lab("T/a0/r1", "c1"), lab("T/a0/r1", "c1"), lab("T/a0/r2", "c2")], "duplicate")
    refused([lab("T/a0/r1", "c1"), lab("T/a0/r2", "c2", "invalid")], "invalid label")
    assert len(load_labelled(tmp_path, allow_invalid=True)) == 1
    refused([lab("T/a0/r1", "c1"), lab("T/a0/r2", "c2", session="s2")], "one grading session")
    refused([lab("T/a0/r1", "c1", session="s2"), lab("T/a0/r2", "c2", session="s2")], "not protocol")
    assert len(load_labelled(tmp_path, allow_nonprotocol=True)) == 2
    refused([lab("T/a0/r1", "c1", session="s9"), lab("T/a0/r2", "c2", session="s9")], "no session file")
    write_jsonl(tmp_path / "hidden_labels.jsonl", [lab("T/a0/r1", "c1"), lab("T/a0/r2", "c2")])
    with open(tmp_path / "trajectories.jsonl", "a", encoding="utf-8") as f:
        f.write('{"broken\n')
    with pytest.raises(LabelError, match="damaged"):
        load_labelled(tmp_path)


# --- run telemetry -----------------------------------------------------------------

METRICS = """# HELP vllm:num_preemptions_total x
vllm:num_preemptions_total{engine="0",model_name="m"} 4.0
vllm:num_preemptions_created{engine="0",model_name="m"} 1.7e+09
vllm:generation_tokens_total{engine="0",model_name="m"} 100.0
vllm:e2e_request_latency_seconds_bucket{le="1.0",model_name="m"} 3.0
"""


def test_vllm_metrics_and_delta(monkeypatch):
    monkeypatch.setattr(monitor.httpx, "get", lambda url, timeout: httpx.Response(200, text=METRICS))
    m = monitor.vllm_metrics()
    assert m == {"num_preemptions_total": 4.0, "generation_tokens_total": 100.0}
    end = {"num_preemptions_total": 6.0, "generation_tokens_total": 350.0}
    assert monitor.metrics_delta(m, end) == {"generation_tokens_total": 250.0, "num_preemptions_total": 2.0}
    assert monitor.metrics_delta(None, end) is None
    reset = monitor.metrics_delta(end, {"num_preemptions_total": 1.0, "generation_tokens_total": 400.0})
    assert reset == {"generation_tokens_total": 50.0, "num_preemptions_total": None, "counter_reset": True}


def test_energy_and_sampler(tmp_path):
    samples = [{"t": 0.0, "power_w": 100.0}, {"t": 36.0, "power_w": 200.0}]
    assert monitor.energy_wh(samples) == pytest.approx(1.5)  # 36 s at 150 W
    assert monitor.energy_wh(samples[:1]) is None
    it = iter(range(1000))
    s = monitor.PowerSampler(tmp_path / "p.jsonl", interval_s=0.01,
                             sample=lambda: {"t": float(next(it)), "power_w": 50.0}).start()
    import time
    time.sleep(0.1)
    summary = s.stop()
    assert summary["power_samples"] >= 2 and summary["mean_power_w"] == 50.0
    assert len((tmp_path / "p.jsonl").read_text().splitlines()) == summary["power_samples"]


def test_visible_reply_must_match_the_tests():
    good = json.dumps({"ok": True, "runner": "v", "execution": {"status": "ok"},
                       "results": [{"status": "pass"}, {"status": "not_run"}]}).encode()
    assert VisibleRunner._parse(good, 2)["results"][1]["status"] == "not_run"
    assert VisibleRunner._parse(good, 3) is None                       # wrong number of results
    assert VisibleRunner._parse(good + b"\n" + good, 2) is None        # more than one line
    assert VisibleRunner._parse(good.replace(b"not_run", b"maybe"), 2) is None
    assert VisibleRunner._parse(b'{"ok": false, "error": "x"}', 2) is None


class FakeProc:
    def __init__(self, returncode, stdout=b"", stderr=b""):
        self.returncode, self.stdout, self.stderr = returncode, stdout, stderr


def runner_with(monkeypatch, run_rc, rm_rc):
    import subprocess as sp
    good = json.dumps({"ok": True, "runner": "v", "execution": {"status": "ok"}, "results": [{"status": "pass"}]})

    def fake_run(cmd, **kw):
        if cmd[:2] == ["docker", "run"]:
            return FakeProc(run_rc, good.encode())
        if cmd[:2] == ["docker", "rm"]:
            return sp.CompletedProcess(cmd, rm_rc, "", "" if rm_rc == 0 else "daemon error")
        return sp.CompletedProcess(cmd, 0, "exit=1 oom=false", "")
    monkeypatch.setattr("system1.loop.sandbox.subprocess.run", fake_run)
    monkeypatch.setattr("system1.loop.sandbox.image_id", lambda image: "sha256:x")
    return VisibleRunner(max_concurrent=1)


def test_visible_runner_needs_exit_code_zero(monkeypatch):
    vr = runner_with(monkeypatch, run_rc=1, rm_rc=0)
    with pytest.raises(SandboxError, match="exit 1"):
        vr.run("x", [{"kind": "assert", "source": "assert True"}])


def test_failed_cleanup_discards_the_result_and_stops_later_checks(monkeypatch):
    vr = runner_with(monkeypatch, run_rc=0, rm_rc=1)
    with pytest.raises(SandboxError, match="could not remove"):
        vr.run("x", [{"kind": "assert", "source": "assert True"}])
    with pytest.raises(SandboxError, match="stopped"):
        vr.run("x", [{"kind": "assert", "source": "assert True"}])


def test_driver_runs_only_the_tasks_in_a_tasks_file(driver, tmp_path, monkeypatch, capsys):
    drv, args = driver
    (tmp_path / "subset.json").write_text(json.dumps({"tasks": ["C"]}), encoding="utf-8")
    monkeypatch.setattr(drv, "ROOT", tmp_path)
    args.tasks_file, args.attempts = "subset.json", 3
    assert asyncio.run(drv.main_async(args)) == 0
    assert "3 attempts to run (0 already done)" in capsys.readouterr().out


def test_frozen_pilot_subsample():
    sub = load_script("make_pilot_subsample")
    frozen = json.loads(sub.SUBSAMPLE_PATH.read_text(encoding="utf-8"))
    from system1.eval.split import load_split
    split = load_split()
    assert frozen["benchmarks"] == sub.draw(split)  # the rule reproduces the file
    assert {b: len(v) for b, v in frozen["benchmarks"].items()} == {"humaneval+": 22, "mbpp+": 50}
    for b, ids in frozen["benchmarks"].items():
        assert set(ids) <= set(split["benchmarks"][b]["dev"])  # development tasks only


def test_driver_first_attempt_runs_only_later_attempts(driver, tmp_path, capsys):
    drv, args = driver
    args.first_attempt, args.attempts = 1, 3
    assert asyncio.run(drv.main_async(args)) == 1  # B still fails
    assert "6 attempts to run (0 already done)" in capsys.readouterr().out
    rows, _ = CostLedger(tmp_path / "runs" / "r" / "trajectories.jsonl").read()
    assert {r["attempt"] for r in rows} == {1, 2}
