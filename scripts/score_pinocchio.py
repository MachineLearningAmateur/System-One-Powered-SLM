"""Score every complete checkpoint of a run with Pinocchio-0.8B (local, CPU).

    uv run --group pinocchio python scripts/score_pinocchio.py --run-id pilot-v1

Frozen input format (pinocchio-input-v1, fixed on October 17 before any dev score):
  question  the small model's round-1 message (the task and its visible tests),
            the same for every round of the attempt;
  answer    the checkpoint's answer text after the thinking (the thinking is not given);
  source_model and benchmark are not given (optional; Qwen3-1.7B is not in Pinocchio's
  training mix).
The router score is 1 - p_correct (higher = more likely to fail). Labels are never read.
Output: results/runs/<run-id>/pinocchio_scores.jsonl, one record per checkpoint, with the
CPU seconds of each score. A rerun skips checkpoints that already have a score.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version

from system1.config import RESULTS
from system1.eval.ledger import CostLedger, read_jsonl
from system1.loop.runner import complete_executions
from system1.loop.tasks import first_round_messages, load_tasks

INPUT_VERSION = "pinocchio-input-v1"
ADAPTER = "KevinDavidHayes/pinocchio-0.8b"
BASE = "Qwen/Qwen3.5-0.8B"
OUT = "pinocchio_scores.jsonl"


def inputs(rec: dict, tasks) -> tuple[str, str]:
    question = first_round_messages(tasks[rec["task_id"]])[0]["content"]
    return question, rec["answer"] or ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    d = RESULTS / "runs" / args.run_id
    rows, bad = read_jsonl(d / "trajectories.jsonl")
    if bad:
        print(f"STOP: {len(bad)} damaged lines in trajectories.jsonl")
        return 2
    cps = complete_executions(rows)
    done = {r["checkpoint_id"] for r in read_jsonl(d / OUT)[0]}
    todo = [c for c in cps if c["checkpoint_id"] not in done]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(cps)} checkpoints, {len(done)} already scored, {len(todo)} to score", flush=True)

    import torch
    from pinocchio import Pinocchio

    torch.manual_seed(0)
    t0 = time.perf_counter()
    judge = Pinocchio(adapter=ADAPTER, base_model=BASE, device_map="cpu")
    print(f"model loaded in {time.perf_counter() - t0:.1f} s", flush=True)
    store = CostLedger(d / OUT)
    tasks = load_tasks()
    meta = {"input_version": INPUT_VERSION, "adapter": ADAPTER, "base_model": BASE,
            "package": f"pinocchio-uq=={version('pinocchio-uq')}", "torch": torch.__version__, "device": "cpu"}
    for i, c in enumerate(todo, 1):
        q, a = inputs(c, tasks)
        t = time.perf_counter()
        p = float(judge.score(question=q, answer=a))
        store.append_obj({"checkpoint_id": c["checkpoint_id"], "exec_id": c["exec_id"], "task_id": c["task_id"],
                          "attempt": c["attempt"], "round": c["round"], "p_correct": p, "score": 1.0 - p,
                          "cpu_seconds": round(time.perf_counter() - t, 3),
                          "input_sha256": hashlib.sha256(json.dumps([q, a]).encode()).hexdigest(), **meta,
                          "ts": datetime.now(timezone.utc).isoformat()})
        if i % 50 == 0:
            print(f"  {i}/{len(todo)}", flush=True)
    print(f"done: {len(todo)} scored in {time.perf_counter() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
