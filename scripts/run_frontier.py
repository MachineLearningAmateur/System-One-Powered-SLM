"""Collect frontier takeover answers (takeover from scratch, the main help mode).

    uv run python scripts/run_frontier.py --run-id frontier-dev-v1 --split dev --samples 1 --limit 20 --limit-usd 5

For each task and sample index, one call to the pinned frontier model with
exactly the small model's round-1 message (the task and its visible tests).
Each sample is an independent replicate; the replay reuses each answer at
every checkpoint of its task. No repair, retry on content, or fallback.

Outputs in results/runs/<run-id>/:
  frontier_answers.jsonl  one record per (task, sample) call that returned
  ledger.jsonl            one row per HTTP attempt (cost ledger)
  run_meta.json           split, model, provider, parameters, prompt hash rule, git commit
A rerun with the same run id skips (task, sample) pairs that already have an
answer and stops if the protocol differs. The spend guard (--limit-usd, a
required, user-approved limit) counts every frontier row in this run's ledger.
--split test needs --confirm-test (test generation only after the protocol freeze).
Tasks in configs/grading_exclusions_v1.json (Amendment A2) get no call; each
session records the exclusion file it applied.
Hidden grades come later: scripts/grade_hidden.py --run-id <run-id> --frontier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from system1.config import RESULTS, ROOT, load_prices
from system1.eval.exclusions import load_exclusions
from system1.eval.ledger import CostLedger, read_jsonl
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
from system1.frontier.client import (MAX_TOKENS, MODEL, PROVIDER, REASONING, FrontierClient, FrontierRequestError,
                                     SpendLimitReached)
from system1.loop.generate import add_missing_imports, extract_code, prompt_imports
from system1.loop.tasks import VISIBLE_TESTS_PATH, first_round_messages, load_tasks

ANSWERS = "frontier_answers.jsonl"
SELECT_SEED = 20261017  # --limit takes a seeded shuffle of the split, so a small check covers both benchmarks


def git_state() -> tuple[str, bool]:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    return commit, bool(status.strip())


def protocol(dirty: bool, manifest_sha256: str | None = None, strict_spend: bool = False) -> dict:
    p = {"mode": "takeover_from_scratch", "model": MODEL, "provider": PROVIDER, "reasoning": REASONING,
            "max_tokens": MAX_TOKENS, "temperature": "provider default", "messages": "loop.tasks.first_round_messages",
            "visible_tests_sha256": file_sha256(VISIBLE_TESTS_PATH), "split_sha256": file_sha256(SPLIT_PATH),
            "client_sha256": file_sha256(ROOT / "src" / "system1" / "frontier" / "client.py"),
            "git_dirty": dirty}
    if manifest_sha256 is not None:
        p.update({"frozen_manifest_sha256": manifest_sha256, "strict_spend": strict_spend})
    return p


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--split", choices=("dev", "test"), required=True)
    ap.add_argument("--samples", type=int, default=3, help="sample indices 0..N-1 per task")
    ap.add_argument("--limit", type=int, help="only the first N tasks of a seeded shuffle of the split")
    ap.add_argument("--limit-usd", type=float, required=True, help="approved spend limit for this run's ledger")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--confirm-test", action="store_true")
    ap.add_argument("--allow-dirty", action="store_true", help="smoke runs only; marks the run as not protocol")
    ap.add_argument("--frozen-manifest", help="extension manifest: verify source hashes, tasks and prompts before calls")
    ap.add_argument("--strict-spend", action="store_true", help="reserve all allowed HTTP retries at a conservative token bound")
    args = ap.parse_args()
    if args.split == "test" and not args.confirm_test:
        print("--split test needs --confirm-test (only after the protocol freeze)")
        return 2
    commit, dirty = git_state()
    if dirty and not args.allow_dirty:
        print("The git tree has changes. Commit them first, or use --allow-dirty for a smoke run.")
        return 2

    split, tasks = load_split(), load_tasks()
    excl = load_exclusions()
    ids = [t for b in ("humaneval+", "mbpp+") for t in split["benchmarks"][b][args.split] if t not in excl["tasks"]]
    if args.limit:
        ids = random.Random(SELECT_SEED).sample(ids, len(ids))[: args.limit]

    manifest_sha = None
    if args.frozen_manifest:
        mp = ROOT / args.frozen_manifest
        manifest = json.loads(mp.read_text(encoding="utf-8"))
        if not args.strict_spend or args.limit or args.split != "test" or args.run_id != manifest["frontier_run"]:
            print("STOP: frozen extension requires strict spend, all test tasks, and the frozen run id")
            return 2
        if args.samples != manifest["frontier"]["samples_per_task"] or sorted(ids) != manifest["task_ids"]:
            print("STOP: frontier sample/task grid differs from the frozen manifest")
            return 2
        for rel, old_sha in manifest["source_hashes"].items():
            if file_sha256(ROOT / rel) != old_sha:
                print(f"STOP: frozen source changed: {rel}")
                return 2
        for tid in ids:
            messages = first_round_messages(tasks[tid])
            canonical = hashlib.sha256(json.dumps(messages, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            if canonical != manifest["task_prompt_sha256"][tid]:
                print(f"STOP: frozen frontier prompt changed: {tid}")
                return 2
        manifest_sha = file_sha256(mp)

    out = RESULTS / "runs" / args.run_id
    out.mkdir(parents=True, exist_ok=True)
    proto = protocol(dirty, manifest_sha, args.strict_spend)
    meta_path = out / "run_meta.json"
    if meta_path.exists():
        old = json.loads(meta_path.read_text(encoding="utf-8"))
        if old["protocol"] != proto or old["split"] != args.split:
            print(f"STOP: {meta_path} has another protocol or split; use a new run id")
            return 2
        meta = old
    else:
        meta = {"run_id": args.run_id, "split": args.split, "protocol": proto, "git_commit": commit, "sessions": []}
    meta["sessions"].append({"started": datetime.now(timezone.utc).isoformat(), "git_commit": commit,
                             "limit_usd": args.limit_usd, "samples": args.samples, "n_tasks": len(ids),
                             "exclusions": {"version": excl["version"], "sha256": excl["sha256"],
                                            "tasks": sorted(excl["tasks"])}})
    meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")

    done = {(r["task_id"], r["sample"]) for r in read_jsonl(out / ANSWERS)[0]}
    todo = [(t, s) for t in ids for s in range(args.samples) if (t, s) not in done]
    print(f"{len(ids)} tasks x {args.samples} samples; {len(todo)} calls to make, {len(done)} already done")
    prices = load_prices()
    answers, ledger = CostLedger(out / ANSWERS), CostLedger(out / "ledger.jsonl")

    def one(task_id: str, sample: int) -> dict:
        task = tasks[task_id]
        messages = first_round_messages(task)
        reply = client.ask(messages, task_id=task_id, sample=sample)
        code, rule, n_blocks, added = None, "none", 0, []
        if reply.content is not None:
            code, rule, n_blocks = extract_code(reply.content, task.entry_point)
            if code is not None:
                code, added = add_missing_imports(code, prompt_imports(task.prompt))
        rec = {"task_id": task_id, "benchmark": task.benchmark, "sample": sample, "call_id": reply.call_id,
               "status": reply.status, "prompt_sha256": hashlib.sha256(json.dumps(messages).encode()).hexdigest(),
               "answer": reply.content, "code": code, "code_rule": rule, "n_code_blocks": n_blocks,
               "imports_added": added, "finish_reason": reply.finish_reason, "model_returned": reply.model_returned,
               "provider_returned": reply.provider_returned, "input_tokens": reply.input_tokens,
               "output_tokens": reply.output_tokens, "reasoning_tokens": reply.reasoning_tokens,
               "usd_reported": reply.usd_reported, "usd_computed": reply.usd_computed,
               "latency_ms": round(reply.latency_ms, 1), "http_attempts": reply.http_attempts,
               "ts": datetime.now(timezone.utc).isoformat()}
        answers.append_obj(rec)
        return rec

    n_ok = n_fail = 0
    stopped = None
    with FrontierClient(ledger, prices, args.limit_usd, strict_cap=args.strict_spend) as client, ThreadPoolExecutor(args.concurrency) as pool:
        futs = {pool.submit(one, t, s): (t, s) for t, s in todo}
        for f in as_completed(futs):
            try:
                rec = f.result()
                n_ok += 1
                if rec["status"] != "ok" or rec["code"] is None:
                    print(f"  {futs[f]}: status {rec['status']}, code {rec['code_rule']}", flush=True)
            except SpendLimitReached as e:
                stopped = str(e)
                n_fail += 1
            except FrontierRequestError as e:
                print(f"  {futs[f]}: {e}", flush=True)
                n_fail += 1
            if stopped:
                for g in futs:
                    g.cancel()
    rows, _ = read_jsonl(out / ANSWERS)
    spent = sum((r["usd_reported"] if r["usd_reported"] is not None else (r["usd_computed"] or 0.0)) for r in rows)
    print(f"answers {len(rows)} ({n_ok} new, {n_fail} not made); answer cost ${spent:.4f}"
          + (f"\nSTOPPED by the spend guard: {stopped}" if stopped else ""))
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
