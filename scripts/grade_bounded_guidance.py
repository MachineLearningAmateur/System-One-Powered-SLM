"""Grade final paired answers after generation; never expose labels to either model.

    uv run python scripts/grade_bounded_guidance.py --run-id bg-mock-demo --mock
    docker compose stop vllm
    uv run python scripts/grade_bounded_guidance.py --run-id <approved-run> --real

The mock path executes no candidate code. The real path uses the existing
networkless EvalPlus grader and its two-vote/conditional-third rule. It refuses
to overwrite labels and refuses grading while vLLM is running.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime, timezone

import httpx

from system1.config import RESULTS, ROOT
from system1.eval.ledger import CostLedger, read_jsonl
from system1.loop.sandbox import Sandbox
from system1.loop.tasks import DATASET
try:
    from scripts.grade_hidden import (CACHE_DIR, CANARY, GRADING_CODE, container_facts,
                                      decide, grade_once, sha256_files, vllm_running)
except ModuleNotFoundError:  # direct `python scripts/grade_bounded_guidance.py`
    from grade_hidden import (CACHE_DIR, CANARY, GRADING_CODE, container_facts,
                              decide, grade_once, sha256_files, vllm_running)


def final_units(pairs):
    units = {}
    for pair in pairs:
        by_id = {r["checkpoint_id"]: r for r in pair["rows"]}
        for arm, cid in pair["final_checkpoint_ids"].items():
            if cid not in by_id:
                raise ValueError(f"missing final checkpoint {cid}")
            row = by_id[cid]
            code = row["code"]
            code_sha = hashlib.sha256((code or "").encode()).hexdigest()
            if code_sha != row["code_sha256"]:
                raise ValueError(f"code hash mismatch at {cid}")
            key = (pair["task_id"], pair["attempt"], arm)
            if key in units:
                raise ValueError(f"duplicate final unit {key}")
            units[key] = {"pair_id": pair["pair_id"], "checkpoint_id": cid, "benchmark": pair["benchmark"],
                          "task_id": pair["task_id"], "attempt": pair["attempt"], "arm": arm,
                          "code": code, "code_sha256": code_sha}
    return units


def generation_is_gradable(meta: dict, *, real: bool) -> bool:
    latest_status = meta["sessions"][-1]["status"] if meta["sessions"] else None
    return latest_status == "finished" or (
        real and meta["protocol"].get("pilot_profile") == "dev30-v1"
        and latest_status == "stopped")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--mock", action="store_true")
    mode.add_argument("--real", action="store_true")
    args = ap.parse_args()
    out = RESULTS / "runs" / args.run_id
    meta = json.loads((out / "run_meta.json").read_text())
    if meta["protocol"]["backend"] != ("mock" if args.mock else "real"):
        ap.error("grade mode does not match generation backend")
    # A stopped fixed development batch is never resumed or replenished. Its
    # already completed pairs can be graded after vLLM is gone, while the task
    # accounting report marks every other manifest task as incomplete.
    if not generation_is_gradable(meta, real=args.real):
        ap.error("generation did not finish; no partial grading")
    label_path = out / "bounded_hidden_labels.jsonl"
    if label_path.exists():
        ap.error("labels already exist; use a new run id")
    pairs, bad = read_jsonl(out / "pairs.jsonl")
    if bad or not pairs:
        ap.error("pair data missing or damaged")
    units = final_units(pairs)
    if len(units) != len(pairs) * 2:
        ap.error("both arms must have a final answer for every pair")
    grades = {}
    grade_log = CostLedger(out / "bounded_hidden_grades.jsonl")
    grade_session = f"{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:6]}"
    provenance = {}
    if args.mock:
        for key, unit in units.items():
            grades[key] = {"status": "pass" if "return x + 1" in (unit["code"] or "") else "fail",
                           "passed": "return x + 1" in (unit["code"] or ""), "n_replicates": 0}
    else:
        if vllm_running():
            ap.error("stop vLLM before hidden grading")
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT,
                                             text=True).strip())
        if dirty or commit != meta["protocol"]["git_commit"]:
            ap.error("real grading needs the clean generation commit")
        server_url = meta["protocol"].get("server_url", "http://localhost:8000")
        if server_url != "http://localhost:8000":
            try:
                response = httpx.get(server_url + "/v1/models", timeout=5.0)
                if response.is_success:
                    ap.error("remote vLLM is still reachable; stop it before hidden grading")
            except httpx.HTTPError:
                pass
        sb = Sandbox(stderr_log=out / "bounded_grader_stderr.log")
        try:
            hello = sb.ping()
            provenance = {"git_commit": commit, "git_dirty": dirty,
                "grader_version": hello.get("version"), "grader_settings": hello.get("settings"),
                "container": container_facts(),
                "grading_code_sha256": sha256_files([ROOT / p for p in (*GRADING_CODE,
                    "scripts/grade_bounded_guidance.py")], ROOT),
                "evalplus_cache_sha256": sha256_files([p for p in CACHE_DIR.rglob("*") if p.is_file()], CACHE_DIR)}
            for ds in ("humaneval", "mbpp"):
                keys = [k for k, u in units.items() if DATASET[u["benchmark"]] == ds]
                if not keys:
                    continue
                sb.close()
                sb.load([ds])
                task_ids = sorted({units[k]["task_id"] for k in keys})
                for tid in task_ids:
                    check = grade_once(sb, ds, tid, "", lambda g: grade_log.append_obj(
                        {"purpose": "calibration", "dataset": ds, "task_id": tid, **g}), canonical=True)
                    if not (check.get("valid") and check.get("passed")):
                        raise RuntimeError(f"reference calibration failed for {tid}")
                canary = grade_once(sb, ds, task_ids[0], CANARY, lambda g: grade_log.append_obj(
                    {"purpose": "canary", "dataset": ds, "task_id": task_ids[0], **g}), canonical=True)
                if not (canary.get("valid") and canary.get("passed")):
                    raise RuntimeError(f"memory canary failed for {ds}")
                distinct = {}
                for k in keys:
                    u = units[k]
                    if u["code"] is not None:
                        distinct[(u["task_id"], u["code_sha256"])] = u["code"]
                votes = {key: [] for key in distinct}
                for rep in (1, 2, 3):
                    todo = list(distinct) if rep < 3 else [k for k in distinct if decide(votes[k])[0] == "undecided"]
                    for tid, sha in todo:
                        votes[(tid, sha)].append(grade_once(sb, ds, tid, distinct[(tid, sha)],
                            lambda g, tid=tid, sha=sha: grade_log.append_obj({"purpose": "candidate",
                            "dataset": ds, "task_id": tid, "code_sha256": sha, "replicate": rep, **g})))
                for k in keys:
                    u = units[k]
                    if u["code"] is None:
                        grades[k] = {"status": "no_code", "passed": False, "n_replicates": 0}
                    else:
                        v = votes[(u["task_id"], u["code_sha256"])]
                        status, _ = decide(v)
                        grades[k] = {"status": "invalid" if status == "undecided" else status,
                                     "passed": status == "pass", "n_replicates": len(v)}
        finally:
            sb.close()
    rows = [{k: v for k, v in unit.items() if k != "code"} | grades[key] | {"grade_session": grade_session}
            for key, unit in units.items()]
    if any(r["status"] == "invalid" for r in rows):
        raise RuntimeError("invalid hidden grade; preserving raw grade log without publishing labels")
    label_path.write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out / "bounded_grade_meta.json").write_text(json.dumps({
        "run_id": args.run_id, "backend": "mock" if args.mock else "real",
        "created": datetime.now(timezone.utc).isoformat(), "grade_session": grade_session,
        "provenance": provenance, "n_pairs": len(pairs),
        "n_labels": len(rows), "status_counts": {s: sum(r["status"] == s for r in rows)
                                                   for s in ("pass", "fail", "no_code")}}, indent=2))
    print(f"graded {len(pairs)} paired units; wrote {len(rows)} final labels")


if __name__ == "__main__":
    sys.exit(main())
