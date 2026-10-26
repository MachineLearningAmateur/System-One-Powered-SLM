"""Grade a BigCodeBench validation run after generation, with vLLM stopped.

    uv run python scripts/prepare_bcb_validation_v2.py hidden
    docker compose -f docker-compose.yml -f docker-compose.bcb.yml \
      -f docker-compose.bcb-v2.yml -f docker-compose.bcb-grader-v2.yml up -d bcb-sandbox
    uv run python scripts/grade_bcb_hidden.py --run-id bcb-jev-only-test-v2 \
      --task-manifest configs/bcb_jev_only_tasks_v2.json \
      --hidden-data results/datasets/bcb_jev_only_hidden_v2.json \
      --grader-image system1-bcb-sandbox:v2 \
      --grading-amendment-tag bcb-jev-only-grader-amendment-v1

All candidate and reference code runs in the networkless bcb-sandbox service.
The existing EvalPlus grader and its data are untouched. This script refuses
to replace an existing label file. It writes the same label/session format as
scripts/grade_hidden.py so the existing provenance checks apply.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone

from system1.config import RESULTS, ROOT
from system1.eval.labels import LABELS_FILE, META_FILE, SESSIONS_DIR, code_sha
from system1.eval.ledger import CostLedger, read_jsonl
from system1.loop.runner import complete_executions
from system1.loop.sandbox import Sandbox

from grade_hidden import decide, git_state, grade_once, vllm_running

CONTAINER = "system1-bcb-sandbox-1"
WORKER = ["python", "/opt/sandbox/bcb_worker.py"]
MANIFEST = ROOT / "configs/bcb_jev_only_tasks_v1.json"
HIDDEN = ROOT / "results/datasets/bcb_jev_only_hidden_v1.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--task-manifest", default="configs/bcb_jev_only_tasks_v1.json")
    ap.add_argument("--hidden-data", default="results/datasets/bcb_jev_only_hidden_v1.json")
    ap.add_argument("--grader-image", default="system1-bcb-sandbox:v1")
    ap.add_argument("--grading-amendment-tag", default="")
    args = ap.parse_args()
    manifest = ROOT / args.task_manifest
    hidden = ROOT / args.hidden_data
    out = RESULTS / "runs" / args.run_id
    labels_path = out / LABELS_FILE
    if labels_path.exists():
        print("STOP: labels already exist; refusing to overwrite")
        return 2
    if vllm_running():
        print("STOP: vLLM is running")
        return 2
    commit, dirty = git_state()
    if dirty:
        print("STOP: clean git tree required")
        return 2
    meta_path = out / "run_meta.json"
    if not meta_path.exists() or not hidden.exists():
        print("STOP: run metadata or local hidden data missing")
        return 2
    run_meta = json.loads(meta_path.read_text(encoding="utf-8"))
    generation_commit = run_meta["protocol"].get("git_commit")
    if run_meta.get("split") != "test" or run_meta.get("non_protocol") or not generation_commit:
        print("STOP: generation is not a clean test run")
        return 2
    if args.grading_amendment_tag:
        tag_commit = subprocess.run(["git", "rev-parse", f"{args.grading_amendment_tag}^{{commit}}"],
                                    cwd=ROOT, capture_output=True, text=True)
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", generation_commit, commit],
                                  cwd=ROOT, capture_output=True)
        if tag_commit.returncode or tag_commit.stdout.strip() != commit or ancestor.returncode:
            print("STOP: grader is not on the frozen grading amendment descendant")
            return 2
    elif generation_commit != commit:
        print("STOP: generation and grading commits differ without a frozen amendment")
        return 2
    if run_meta["protocol"].get("task_manifest_sha256") != sha(manifest):
        print("STOP: generation used another task manifest")
        return 2
    rows, bad = read_jsonl(out / "trajectories.jsonl")
    if bad:
        print(f"STOP: {len(bad)} damaged trajectory rows")
        return 2
    dropped = []
    cps = complete_executions(rows, dropped=dropped)
    ids = set(json.loads(manifest.read_text(encoding="utf-8"))["tasks"])
    if {r["task_id"] for r in cps} != ids or any(r["benchmark"] != "bigcodebench" for r in cps):
        print("STOP: task set differs from the frozen BigCodeBench manifest")
        return 2
    if {(r["task_id"], r["attempt"]) for r in cps} != {(tid, a) for tid in ids for a in range(5)}:
        print("STOP: the planned attempts are not all complete")
        return 2
    image = subprocess.run(["docker", "image", "inspect", "-f", "{{.Id}}", args.grader_image],
                           capture_output=True, text=True, check=True).stdout.strip()
    container_image = subprocess.run(["docker", "inspect", "-f", "{{.Image}}", CONTAINER],
                                     capture_output=True, text=True, check=True).stdout.strip()
    if container_image != image:
        print("STOP: running grader container uses another image")
        return 2
    session = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    log = CostLedger(out / "hidden_grades.jsonl")
    meta = {"run_id": args.run_id, "session": session, "protocol": True, "git_commit": commit,
            "generation_git_commit": generation_commit,
            "grading_amendment_tag": args.grading_amendment_tag or None,
            "git_dirty": False, "started": datetime.now(timezone.utc).isoformat(),
            "dataset": "bigcodebench-v0.1.4", "task_manifest_sha256": sha(manifest),
            "hidden_data_sha256": sha(hidden), "grader_image_id": image,
            "grader_worker_sha256": sha(ROOT / "docker/bcb_sandbox/worker.py"),
            "dropped_executions": dropped, "n_checkpoints": len(cps)}
    sb = Sandbox(container=CONTAINER, cmd=["docker", "exec", "-i", CONTAINER, *WORKER],
                 stderr_log=out / "bcb_grader_stderr.log")

    def logger(task_id, purpose, replicate=None):
        return lambda g: log.append_obj({"session": session, "task_id": task_id,
                                         "purpose": purpose, "replicate": replicate, **g})

    try:
        hello = sb.ping()
        if hello.get("n_tasks") != len(ids):
            print("STOP: grader has another task set")
            return 2
        if args.grading_amendment_tag and hello.get("version") != "bcb-grader-v2-assertEquals":
            print("STOP: grader worker is not the amended version")
            return 2
        meta["grader_version"] = hello["version"]
        cal = {tid: grade_once(sb, "bigcodebench", tid, "", logger(tid, "calibration"), canonical=True)
               for tid in sorted(ids)}
        failed = [tid for tid, g in cal.items() if not (g.get("valid") and g.get("passed"))]
        meta["calibration_failures"] = failed
        if failed:
            print(f"STOP: reference calibration failed for {len(failed)} tasks; no candidate graded")
            return 2
        units = {(r["task_id"], code_sha(r["code"])): r["code"] for r in cps if r["code"] is not None}
        keys = sorted(units)
        votes = {k: [] for k in keys}
        for rep in (1, 2, 3):
            todo = keys if rep < 3 else [k for k in keys if decide(votes[k])[0] == "undecided"]
            for tid, chash in todo:
                votes[(tid, chash)].append(grade_once(sb, "bigcodebench", tid, units[(tid, chash)],
                                                     logger(tid, "candidate", rep)))
            print(f"replicate {rep}: {len(todo)} codes", flush=True)
    finally:
        sb.close()
        # Even a calibration stop leaves a durable session report, without labels.
        (out / SESSIONS_DIR).mkdir(exist_ok=True)
        (out / SESSIONS_DIR / f"{session}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    labels = []
    counts = {"pass": 0, "fail": 0, "invalid": 0, "no_code": 0}
    for r in cps:
        if r["code"] is None:
            status, g, n_votes = "no_code", None, 0
        else:
            vv = votes[(r["task_id"], code_sha(r["code"]))]
            status, g = decide(vv)
            status = "invalid" if status == "undecided" else status
            n_votes = len(vv)
        counts[status] += 1
        labels.append({"exec_id": r["exec_id"], "checkpoint_id": r["checkpoint_id"],
                       "code_sha256": code_sha(r["code"]), "grade_session": session,
                       "status": status, "passed": status == "pass",
                       "base": status, "plus": status, "n_replicates": n_votes,
                       "n_valid_votes": sum(v.get("valid", False) for v in vv) if r["code"] is not None else 0})
    meta["ended"] = datetime.now(timezone.utc).isoformat()
    meta["labels"] = counts
    (out / SESSIONS_DIR / f"{session}.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    with labels_path.open("x", encoding="utf-8") as f:
        for row in labels:
            f.write(json.dumps(row) + "\n")
    (out / META_FILE).write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"labels: {counts}")
    return 0 if counts["invalid"] == 0 else 3


if __name__ == "__main__":
    sys.exit(main())
