"""Run the small-model loop on a split.

    docker compose build sandbox && docker compose up -d vllm
    uv run python scripts/run_loop.py --run-id pilot --split dev --attempts 1

Outputs go to results/runs/<run-id>/: trajectories.jsonl (one record per
checkpoint), ledger.jsonl (one row per vLLM call), failures.jsonl,
logprobs/*.npz, power.jsonl (GPU power samples) and run_meta.json (with each
session's run time, energy and vLLM counter changes such as KV-cache
preemptions). Hidden labels come later from scripts/grade_hidden.py.

run_meta.json holds the protocol fingerprint (model, template, sampling, caps,
seeds, frozen files, sandbox image and limits, git commit). A rerun with the
same run id skips (task, attempt) pairs that already finished, and it stops if
the fingerprint differs: a run never mixes two protocols. Adding tasks or
attempts is allowed, because they are not part of the protocol. The git tree
must be clean; --allow-dirty is for smoke runs only and marks the run as not
protocol. The exit code is 1 if any requested attempt is still incomplete.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone

import httpx

from system1.config import RESULTS, ROOT
from system1.eval.ledger import CostLedger
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
from system1.loop.generate import (CODE_TOKENS, MAX_MODEL_LEN, MODEL, REVISION, SAMPLING, SEED_TAG, THINK_CAP,
                                   TOP_LOGPROBS, Generator, load_tokenizer)
from system1.loop import monitor
from system1.loop.runner import MAX_ROUNDS, VISIBLE_TIMEOUT_S, AttemptFailed, RunContext, complete_executions, run_attempt
from system1.loop.sandbox import VisibleRunner
from system1.loop.tasks import VISIBLE_TESTS_PATH, load_tasks


def finished(store: CostLedger) -> set[tuple[str, int]]:
    """(task, attempt) pairs with a complete execution. Incomplete executions are rerun;
    their rows stay, marked by exec_id, and complete_executions() drops them."""
    rows, _ = store.read()
    return {(r["task_id"], r["attempt"]) for r in complete_executions(rows)}


def git_state() -> tuple[str, bool]:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    return commit, bool(status.strip())  # untracked files count as dirty


EXPECTED_SERVER = {"--model": MODEL, "--revision": REVISION, "--max-model-len": str(MAX_MODEL_LEN),
                   "--dtype": "bfloat16", "--seed": "0"}


def protocol(tokenizer, visible: VisibleRunner, dirty: bool, commit: str, concurrency: int) -> dict:
    template = tokenizer.chat_template if tokenizer is not None else None
    return {"model": MODEL, "revision": REVISION, **monitor.vllm_server_identity(EXPECTED_SERVER),
            "generation_concurrency": concurrency,
            "chat_template_sha256": hashlib.sha256(template.encode()).hexdigest() if template else None,
            "sampling": SAMPLING, "seed_tag": SEED_TAG, "think_cap": THINK_CAP, "code_tokens": CODE_TOKENS,
            "max_model_len": MAX_MODEL_LEN, "top_logprobs": TOP_LOGPROBS, "max_rounds": MAX_ROUNDS,
            "visible_timeout_s": VISIBLE_TIMEOUT_S, **visible.protocol(),
            "split_sha256": file_sha256(SPLIT_PATH), "visible_tests_sha256": file_sha256(VISIBLE_TESTS_PATH),
            "git_commit": commit, "git_dirty": dirty}


async def main_async(args) -> int:
    split = load_split()
    tasks = load_tasks()
    ids = [t for b in ("humaneval+", "mbpp+") if args.benchmark in ("all", b)
           for t in split["benchmarks"][b][args.split]]
    if args.tasks_file:  # a frozen task list, e.g. configs/pilot_subsample_v1.json
        keep = set(json.loads((ROOT / args.tasks_file).read_text(encoding="utf-8"))["tasks"])
        ids = [t for t in ids if t in keep]
    if args.limit:
        ids = ids[: args.limit]

    commit, dirty = git_state()
    if dirty and not args.allow_dirty:
        print("The git tree has changes. Commit them first (protocol runs need a clean commit), "
              "or use --allow-dirty for a smoke run.")
        return 2
    out = RESULTS / "runs" / args.run_id
    out.mkdir(parents=True, exist_ok=True)
    tokenizer = load_tokenizer()
    visible = VisibleRunner(max_concurrent=args.visible_workers)
    try:
        proto = protocol(tokenizer, visible, dirty, commit, args.concurrency)
    except monitor.ServerMismatch as e:
        print(f"STOP: {e}")
        return 2
    meta_path = out / "run_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        old = meta.get("protocol")
        if old != proto:
            diff = sorted(k for k in set(old or {}) | set(proto) if (old or {}).get(k) != proto.get(k))
            print(f"run {args.run_id} was started with another protocol (differs in: {', '.join(diff)}); "
                  "use a new run id")
            return 2
    else:
        meta = {"run_id": args.run_id, "split": args.split, "protocol": proto, "non_protocol": dirty, "sessions": []}

    store, ledger = CostLedger(out / "trajectories.jsonl"), CostLedger(out / "ledger.jsonl")
    failures = CostLedger(out / "failures.jsonl")
    done = finished(store)
    jobs = [(tid, a) for tid in ids for a in range(args.attempts) if (tid, a) not in done]
    session = {"started": datetime.now(timezone.utc).isoformat(), "ended": None, "elapsed_s": None,
               "args": {k: v for k, v in vars(args).items()}, "n_jobs": len(jobs), "n_failed": None}
    meta["sessions"].append(session)
    meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{len(jobs)} attempts to run ({len(done)} already done)", flush=True)

    metrics_start = monitor.vllm_metrics()
    sampler = monitor.PowerSampler(out / "power.jsonl").start()
    sem = asyncio.Semaphore(args.concurrency)
    t0 = time.perf_counter()
    n_done, n_failed = 0, 0
    outcome = "interrupted"
    try:
        async with httpx.AsyncClient() as client:
            ctx = RunContext(run_id=args.run_id, split=args.split, generator=Generator(client, tokenizer),
                             visible=visible, store=store, ledger=ledger, failures=failures,
                             logprob_dir=out / "logprobs")

            async def one(tid: str, attempt: int) -> None:
                nonlocal n_done, n_failed
                async with sem:
                    try:
                        recs = await run_attempt(ctx, tasks[tid], attempt)
                    except Exception as e:  # one failed attempt must not stop the run
                        n_done += 1
                        n_failed += 1
                        if not isinstance(e, AttemptFailed):  # AttemptFailed is already in failures.jsonl
                            failures.append_obj({"run_id": args.run_id, "exec_id": None, "task_id": tid,
                                                 "attempt": attempt, "round": None, "stage": "driver",
                                                 "error": f"{type(e).__name__}: {e}"[:500]})
                        print(f"[{n_done}/{len(jobs)}] {tid} a{attempt}: FAILED {type(e).__name__}: {e}", flush=True)
                        return
                n_done += 1
                last = recs[-1]
                print(f"[{n_done}/{len(jobs)}] {tid} a{attempt}: rounds {len(recs)}, "
                      f"visible_pass {last['visible_pass']}, "
                      f"thinking tokens {[r['generation']['thinking_tokens'] for r in recs]}", flush=True)

            await asyncio.gather(*(one(t, a) for t, a in jobs))
        outcome = "finished"
    finally:  # also on Ctrl+C: the session keeps its time, energy and counters
        elapsed = round(time.perf_counter() - t0, 1)
        metrics_end = monitor.vllm_metrics()
        session.update({"ended": datetime.now(timezone.utc).isoformat(), "outcome": outcome, "elapsed_s": elapsed,
                        "n_failed": n_failed, **sampler.stop(), "vllm_metrics_start": metrics_start,
                        "vllm_metrics_end": metrics_end, "vllm_delta": monitor.metrics_delta(metrics_start, metrics_end)})
        meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    missing = [(t, a) for t in ids for a in range(args.attempts) if (t, a) not in finished(store)]
    print(f"finished in {session['elapsed_s']:.0f} s; {len(missing)} requested attempts incomplete", flush=True)
    return 1 if missing else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    ap.add_argument("--benchmark", choices=["all", "humaneval+", "mbpp+"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="first N tasks of the split (0 = all)")
    ap.add_argument("--tasks-file", default="", help="JSON file with a 'tasks' list (repo-relative); only these run")
    ap.add_argument("--attempts", type=int, default=1)
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--visible-workers", type=int, default=4, help="visible-check containers at the same time")
    ap.add_argument("--allow-dirty", action="store_true", help="smoke runs only: the run is marked non-protocol")
    args = ap.parse_args()
    if args.split == "test":
        print("Test tasks get no generation until the protocol is frozen (docs/research-plan.md). "
              "Remove this guard only after the freeze.")
        return 1
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
