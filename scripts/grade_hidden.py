"""Grade every complete checkpoint of a run on the hidden EvalPlus tests.

    docker compose stop vllm
    docker compose up -d sandbox
    uv run python scripts/grade_hidden.py --run-id <run-id>

Prespecified rules (docs/research-plan.md, Harness rules):
  - Grading runs after generation, with vLLM stopped, in one grader worker,
    one dataset at a time (the worker loads it once, so its state is fixed).
  - Calibration first: the reference solution of every graded task must get a
    valid pass, and so must one reference solution that also maps 1 GiB (the
    memory canary). If not, grading stops.
  - Each distinct code of a task is graded twice (pass 1 over all codes, then
    pass 2), and a third time only when the two valid grades disagree or one
    is invalid. A vote is "base and plus both pass" in that grade. An invalid
    grade (worker failure, container out-of-memory kill) is retried once and
    is never a vote. The label is the majority of valid votes; without a
    majority the label is "invalid" and analyses must report it.
  - A checkpoint without code is a failure without grading.
Outputs in results/runs/<run-id>/:
  hidden_grades.jsonl          every physical grading call (all sessions), written as it ends
  grade_sessions/<session>.json  the grader fingerprint and counts of each session
  grade_meta.json              a copy of the session that wrote the current labels
  hidden_labels.jsonl          one label per complete checkpoint, tagged with its session
The session file is written before the labels are replaced, and
system1.eval.labels.load_labelled() checks that labels and session match.
A session with vLLM running or a changed git tree is marked non-protocol.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from system1.config import RESULTS, ROOT
from system1.eval.labels import LABELS_FILE, META_FILE, SESSIONS_DIR, code_sha
from system1.eval.ledger import CostLedger
from system1.loop.runner import complete_executions
from system1.loop.sandbox import DEFAULT_CONTAINER, Sandbox, SandboxError

CACHE_DIR = ROOT / "data" / "evalplus_cache" / "evalplus"
GRADING_CODE = ("scripts/grade_hidden.py", "src/system1/loop/sandbox.py", "src/system1/eval/labels.py",
                "docker/sandbox/worker.py", "docker/sandbox/Dockerfile", "docker-compose.yml")
CANARY = "\n_s1_memory_canary = bytearray(1024 ** 3)\n"
DATASET = {"humaneval+": "humaneval", "mbpp+": "mbpp"}


def sha256_files(paths: list[Path], root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(paths):
        h.update(p.relative_to(root).as_posix().encode() + b"\0")
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()


def container_facts(container: str = DEFAULT_CONTAINER) -> dict:
    fmt = ('{"image": "{{.Image}}", "memory": {{.HostConfig.Memory}}, "memory_swap": {{.HostConfig.MemorySwap}}, '
           '"nano_cpus": {{.HostConfig.NanoCpus}}, "pids_limit": {{.HostConfig.PidsLimit}}, '
           '"cgroupns": "{{.HostConfig.CgroupnsMode}}", "network": "{{.HostConfig.NetworkMode}}"}')
    r = subprocess.run(["docker", "inspect", "-f", fmt, container], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise SystemExit(f"grader container {container} not found; run: docker compose up -d sandbox")
    return json.loads(r.stdout)


def vllm_running() -> bool:
    r = subprocess.run(["docker", "ps", "--filter", "name=system1-vllm-1", "--format", "{{.Names}}"],
                       capture_output=True, text=True, timeout=60)
    return bool(r.stdout.strip())


def git_state() -> tuple[str, bool]:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    return commit, bool(status.strip())


def grade_once(sb: Sandbox, dataset: str, task_id: str, code: str, log: Callable[[dict], None],
               canonical: bool = False) -> dict:
    """One grade, retried once when invalid. Every physical call is logged; the last one is returned."""
    g: dict = {}
    for retry in range(2):
        t0 = time.perf_counter()
        try:
            g = sb.canonical(dataset, task_id, code) if canonical else sb.hidden(dataset, task_id, code)
        except SandboxError as e:
            g = {"valid": False, "error": str(e)[:300]}
        g = {**g, "retry": retry, "elapsed_s": round(time.perf_counter() - t0, 2)}
        log(g)
        if g.get("valid"):
            break
    return g


def decide(grades: list[dict]) -> tuple[str, dict | None]:
    """("pass"|"fail"|"undecided"|"invalid", the grade that carries the label)."""
    valid = [g for g in grades if g.get("valid")]
    for want in (True, False):
        agree = [g for g in valid if g["passed"] is want]
        if len(agree) >= 2:
            return ("pass" if want else "fail"), agree[0]
    return ("undecided" if len(grades) < 3 else "invalid"), None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--force", action="store_true", help="grade again although hidden_labels.jsonl exists")
    ap.add_argument("--allow-vllm", action="store_true", help="grade while vLLM runs (marks the labels non-protocol)")
    args = ap.parse_args()
    out = RESULTS / "runs" / args.run_id
    labels_path = out / LABELS_FILE
    if labels_path.exists() and not args.force:
        print(f"{labels_path} exists; use --force to grade again")
        return 1
    vllm = vllm_running()
    if vllm and not args.allow_vllm:
        print("vLLM is running; stop it first (docker compose stop vllm)")
        return 1

    rows, bad = CostLedger(out / "trajectories.jsonl").read()
    if bad:
        print(f"STOP: {len(bad)} damaged lines in trajectories.jsonl; repair them before grading")
        return 2
    dropped: list[dict] = []
    cps = complete_executions(rows, dropped=dropped)
    session = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    commit, dirty = git_state()
    meta: dict = {"run_id": args.run_id, "session": session, "started": datetime.now(timezone.utc).isoformat(),
                  "protocol": not (vllm or dirty), "vllm_running": vllm, "git_commit": commit, "git_dirty": dirty,
                  "grading_code_sha256": sha256_files([ROOT / p for p in GRADING_CODE], ROOT),
                  "evalplus_cache_sha256": sha256_files([p for p in CACHE_DIR.rglob("*") if p.is_file()], CACHE_DIR),
                  "container": container_facts(), "n_checkpoints": len(cps), "dropped_executions": dropped}

    # Distinct (dataset, task, code) units; checkpoints without code need no grade.
    units: dict[tuple[str, str, str], str] = {}
    for r in cps:
        if r["code"] is not None:
            units[(DATASET[r["benchmark"]], r["task_id"], code_sha(r["code"]))] = r["code"]
    grades_log = CostLedger(out / "hidden_grades.jsonl")
    votes: dict[tuple[str, str, str], list[dict]] = {k: [] for k in units}

    def logger(**ctx) -> Callable[[dict], None]:
        return lambda g: grades_log.append_obj({"session": session, **ctx, **g})

    sb = Sandbox(stderr_log=out / "grader_stderr.log")
    hello = sb.ping()
    meta["grader_version"], meta["grader_settings"] = hello["version"], hello["settings"]
    meta["datasets"] = {}
    t_start = time.perf_counter()
    try:
        for ds in ("humaneval", "mbpp"):
            keys = [k for k in units if k[0] == ds]
            if not keys:
                continue
            sb.close()  # a fresh worker holds only this dataset
            loaded = sb.load([ds])
            tasks = sorted({k[1] for k in keys})
            print(f"{ds}: worker {loaded['vm_size'] / 2**30:.2f} GiB mapped; calibrating {len(tasks)} tasks", flush=True)
            cal = {t: grade_once(sb, ds, t, "", logger(dataset=ds, task_id=t, purpose="calibration"), canonical=True)
                   for t in tasks}
            cal_fail = [t for t, g in cal.items() if not (g.get("valid") and g.get("passed"))]
            canary = grade_once(sb, ds, tasks[0], CANARY, logger(dataset=ds, task_id=tasks[0], purpose="canary"),
                                canonical=True)
            canary_ok = bool(canary.get("valid") and canary.get("passed"))
            meta["datasets"][ds] = {"vm_size": loaded["vm_size"], "n_tasks": len(tasks), "n_codes": len(keys),
                                    "calibration_failures": cal_fail, "canary_passed": canary_ok,
                                    "memory_limit": canary.get("memory_limit")}
            if cal_fail or not canary_ok:
                print(f"{ds}: calibration failed (reference failures {cal_fail}, canary {canary})")
                return 2
            for rep in (1, 2, 3):
                todo = keys if rep < 3 else [k for k in keys if decide(votes[k])[0] == "undecided"]
                for k in todo:
                    votes[k].append(grade_once(sb, ds, k[1], units[k], logger(
                        dataset=ds, task_id=k[1], code_sha256=k[2], purpose="candidate", replicate=rep)))
                print(f"{ds}: replicate {rep} graded {len(todo)} codes", flush=True)
    finally:
        sb.close()

    labels: list[dict] = []
    counts = {"pass": 0, "fail": 0, "invalid": 0, "no_code": 0}
    first_vs_final = 0
    for r in cps:
        if r["code"] is None:
            lab = {"status": "no_code", "passed": False, "base": "no_code", "plus": "no_code",
                   "n_replicates": 0, "n_valid_votes": 0}
        else:
            k = (DATASET[r["benchmark"]], r["task_id"], code_sha(r["code"]))
            status, g = decide(votes[k])
            status = "invalid" if status == "undecided" else status
            lab = {"status": status, "passed": status == "pass", "base": g["base"] if g else None,
                   "plus": g["plus"] if g else None, "n_replicates": len(votes[k]),
                   "n_valid_votes": sum(bool(v.get("valid")) for v in votes[k])}
            first = votes[k][0]
            first_vs_final += bool(g) and bool(first.get("valid")) and first["passed"] != lab["passed"]
        counts[lab["status"]] += 1
        labels.append({"exec_id": r["exec_id"], "checkpoint_id": r["checkpoint_id"], "code_sha256": code_sha(r["code"]),
                       "grade_session": session, **lab})

    pairs = [v for v in votes.values() if len(v) >= 2 and v[0].get("valid") and v[1].get("valid")]
    meta.update({"ended": datetime.now(timezone.utc).isoformat(), "elapsed_s": round(time.perf_counter() - t_start, 1),
                 "n_codes": len(units), "labels": counts,
                 "first_two_disagree": sum(v[0]["passed"] != v[1]["passed"] for v in pairs),
                 "first_two_valid_pairs": len(pairs), "checkpoints_first_grade_differs": first_vs_final})
    # Publish: the session file first, then the labels, then the pointer copy.
    (out / SESSIONS_DIR).mkdir(exist_ok=True)
    (out / SESSIONS_DIR / f"{session}.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    tmp = labels_path.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(x) + "\n" for x in labels), encoding="utf-8")
    tmp.replace(labels_path)
    (out / META_FILE).write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"labels: {counts}; first two grades disagree on {meta['first_two_disagree']} of {len(pairs)} codes"
          + ("" if meta["protocol"] else "; NON-PROTOCOL session (vLLM running or git tree changed)"))
    return 0 if counts["invalid"] == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
