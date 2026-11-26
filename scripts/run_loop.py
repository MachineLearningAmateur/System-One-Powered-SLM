"""Run the small-model loop on a split.

    docker compose build sandbox && docker compose up -d vllm
    uv run python scripts/run_loop.py --run-id pilot --split dev --attempts 1

Hosted worker (Qwen3.5-9B study): DeepInfra's text-completions endpoint, with
DEEPINFRA_API_KEY in .env. The calls are billed per token; no GPU power or
vLLM counters exist for this backend, so the run records them as missing.

    uv run python scripts/run_loop.py --backend deepinfra --run-id q9b-smoke --split dev \\
        --benchmark humaneval+ --limit 2 --attempts 1 --allow-dirty --max-billed-tokens 200000

--max-billed-tokens (needed for DeepInfra) is a guard on input plus output
tokens of this session: after it is reached, no new attempt starts. Attempts
that already run finish, so the total can go past it. It is not a dollar cap.

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
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

from system1.config import RESULTS, ROOT
from system1.eval.ledger import CostLedger
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
from system1.loop.generate import (CODE_TOKENS, DEEPINFRA_URL, MAX_MODEL_LEN, MODEL, REVISION, SAMPLING, SEED_TAG,
                                   THINK_CAP, TOP_LOGPROBS, Generator, load_tokenizer)
from system1.loop import monitor
from system1.loop.runner import MAX_ROUNDS, VISIBLE_TIMEOUT_S, AttemptFailed, RunContext, complete_executions, run_attempt
from system1.loop.sandbox import VisibleRunner
from system1.loop.tasks import VISIBLE_TESTS_PATH, load_tasks


FREEZE_TAG = "q9b-protocol-freeze-v1"
DEEPINFRA_RETRIES = 4  # transient HTTP errors (429, 5xx) only; every try is a ledger row
DEEPINFRA_TOP_LOGPROBS = 1  # DeepInfra returns only the top-1 alternative (checked 2026-11-26)


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


def protocol(tokenizer, visible: VisibleRunner, dirty: bool, commit: str, concurrency: int,
             think_cap: int = THINK_CAP, remote_manifest: dict | None = None,
             server_url: str = "http://localhost:8000", backend: str = "vllm", api_key: str = "") -> dict:
    template = tokenizer.chat_template if tokenizer is not None else None
    if backend == "deepinfra":
        identity = monitor.deepinfra_server_identity(MODEL, api_key)
    elif remote_manifest is not None:
        identity = monitor.remote_vllm_server_identity(EXPECTED_SERVER, remote_manifest, f"{server_url}/v1/models")
    else:
        identity = monitor.vllm_server_identity(EXPECTED_SERVER)
    return {"model": MODEL, "revision": REVISION, **identity,
            "backend": backend, "server_url": server_url,
            "generation_concurrency": concurrency,
            "chat_template_sha256": hashlib.sha256(template.encode()).hexdigest() if template else None,
            "sampling": SAMPLING, "seed_tag": SEED_TAG, "think_cap": think_cap, "code_tokens": CODE_TOKENS,
            "max_model_len": MAX_MODEL_LEN,
            "top_logprobs": DEEPINFRA_TOP_LOGPROBS if backend == "deepinfra" else TOP_LOGPROBS,
            "confidence_top_k": DEEPINFRA_TOP_LOGPROBS if backend == "deepinfra" else TOP_LOGPROBS,
            "stop_reason_source": "last_token" if backend == "deepinfra" else "server",
            "max_rounds": MAX_ROUNDS,
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
    remote_path = getattr(args, "remote_manifest", "")
    backend = getattr(args, "backend", "vllm")
    api_key = ""
    if backend == "deepinfra":
        if remote_path or getattr(args, "server_url", "http://localhost:8000") != "http://localhost:8000":
            print("--backend deepinfra takes no --remote-manifest or --server-url")
            return 2
        server_url = DEEPINFRA_URL.removesuffix("/completions")
        api_key = os.environ.get("DEEPINFRA_API_KEY", "")
        if not api_key:
            print("DEEPINFRA_API_KEY is not set in .env")
            return 2
        print(f"DEEPINFRA_API_KEY length: {len(api_key)}")
    else:
        server_url = getattr(args, "server_url", "http://localhost:8000").rstrip("/")
        if bool(remote_path) != (server_url != "http://localhost:8000"):
            print("--remote-manifest and a nonlocal --server-url must be provided together")
            return 2
    try:
        remote_manifest = json.loads(Path(remote_path).read_text(encoding="utf-8")) if remote_path else None
    except (OSError, ValueError) as e:
        print(f"cannot read remote deployment manifest: {e}")
        return 2
    tokenizer = load_tokenizer()
    visible = VisibleRunner(max_concurrent=args.visible_workers)
    try:
        # Compared as stored: a JSON round trip turns tuples into lists.
        proto = json.loads(json.dumps(protocol(tokenizer, visible, dirty, commit, args.concurrency,
                                               args.think_cap, remote_manifest, server_url, backend, api_key)))
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
    attempts = range(args.first_attempt, args.attempts)
    jobs = [(tid, a) for tid in ids for a in attempts if (tid, a) not in done]
    session = {"started": datetime.now(timezone.utc).isoformat(), "ended": None, "elapsed_s": None,
               "args": {k: v for k, v in vars(args).items()}, "n_jobs": len(jobs), "n_failed": None}
    meta["sessions"].append(session)
    meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"{len(jobs)} attempts to run ({len(done)} already done)", flush=True)

    hosted = backend == "deepinfra"
    metrics_url = f"{server_url}/metrics"

    def metrics() -> dict | None:
        if hosted:
            return None  # DeepInfra exposes no vLLM counters
        return monitor.vllm_metrics(metrics_url) if remote_manifest else monitor.vllm_metrics()

    metrics_start = metrics()
    sampler = None if (remote_manifest or hosted) else monitor.PowerSampler(out / "power.jsonl").start()
    sem = asyncio.Semaphore(args.concurrency)
    t0 = time.perf_counter()
    n_done, n_failed, n_guard = 0, 0, 0
    max_billed = getattr(args, "max_billed_tokens", 0)
    outcome = "interrupted"
    ctx = None
    try:
        headers = {"Authorization": f"Bearer {api_key}"} if hosted else None
        async with httpx.AsyncClient(headers=headers) as client:
            if hosted:
                generator = Generator(client, tokenizer, url=DEEPINFRA_URL, think_cap=args.think_cap,
                                      max_retries=DEEPINFRA_RETRIES, top_logprobs=DEEPINFRA_TOP_LOGPROBS,
                                      infer_missing_stop_reason=True)
                provider = "deepinfra"
            elif remote_manifest:
                generator = Generator(client, tokenizer, url=f"{server_url}/v1/completions", think_cap=args.think_cap)
                provider = "azure-container-app-vllm"
            else:
                generator = Generator(client, tokenizer, think_cap=args.think_cap)
                provider = "local-vllm"
            ctx = RunContext(run_id=args.run_id, split=args.split, generator=generator,
                             visible=visible, store=store, ledger=ledger, failures=failures,
                             logprob_dir=out / "logprobs", provider=provider)

            async def one(tid: str, attempt: int) -> None:
                nonlocal n_done, n_failed, n_guard
                async with sem:
                    used = getattr(ctx.generator, "tokens_used", None)
                    if max_billed and used and used["input"] + used["output"] >= max_billed:
                        n_guard += 1  # not started; a resume runs it
                        if n_guard == 1:
                            print(f"token guard reached ({used}); no new attempts start", flush=True)
                        return
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
        metrics_end = metrics()
        session.update({"ended": datetime.now(timezone.utc).isoformat(), "outcome": outcome, "elapsed_s": elapsed,
                        "n_failed": n_failed, "n_not_started_guard": n_guard, "max_billed_tokens": max_billed,
                        "tokens_used": getattr(ctx.generator, "tokens_used", None) if ctx else None,
                        **(sampler.stop() if sampler else {"power_samples": 0, "energy_wh": None, "mean_power_w": None}),
                        "vllm_metrics_start": metrics_start,
                        "vllm_metrics_end": metrics_end, "vllm_delta": monitor.metrics_delta(metrics_start, metrics_end)})
        meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    missing = [(t, a) for t in ids for a in attempts if (t, a) not in finished(store)]
    print(f"finished in {session['elapsed_s']:.0f} s; {len(missing)} requested attempts incomplete", flush=True)
    return 1 if missing else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--split", choices=["dev", "test"], default="dev")
    ap.add_argument("--benchmark", choices=["all", "humaneval+", "mbpp+"], default="all")
    ap.add_argument("--limit", type=int, default=0, help="first N tasks of the split (0 = all)")
    ap.add_argument("--tasks-file", default="", help="JSON file with a 'tasks' list (repo-relative); only these run")
    ap.add_argument("--attempts", type=int, default=1, help="attempt indices run up to (not including) this value")
    ap.add_argument("--first-attempt", type=int, default=0,
                    help="first attempt index; seeds depend on the index (not on the run), "
                         "but the same seed does not reproduce the output")
    ap.add_argument("--think-cap", type=int, default=THINK_CAP,
                    help="thinking tokens per round; only for the cap comparison (part of the protocol)")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--max-billed-tokens", type=int, default=0,
                    help="DeepInfra: no new attempt starts after this many input + output tokens (0 = no guard)")
    ap.add_argument("--visible-workers", type=int, default=4, help="visible-check containers at the same time")
    ap.add_argument("--allow-dirty", action="store_true", help="smoke runs only: the run is marked non-protocol")
    ap.add_argument("--backend", choices=["vllm", "deepinfra"], default="vllm",
                    help="vllm: local or Azure vLLM; deepinfra: hosted, billed per token (DEEPINFRA_API_KEY)")
    ap.add_argument("--server-url", default="http://localhost:8000", help="vLLM base URL (HTTPS for Azure)")
    ap.add_argument("--remote-manifest", default="", help="Azure deployment identity JSON for remote vLLM")
    args = ap.parse_args()
    if not 0 < args.think_cap <= MAX_MODEL_LEN - CODE_TOKENS:
        print(f"--think-cap must be in 1..{MAX_MODEL_LEN - CODE_TOKENS}")
        return 2
    if args.backend == "deepinfra" and args.max_billed_tokens <= 0:
        print("--backend deepinfra needs --max-billed-tokens (a guard for the billed calls)")
        return 2
    if args.split == "test":
        # Test tasks get generation only after the protocol freeze (docs/research-plan.md): the freeze
        # tag must exist and be in the history of the commit that runs.
        r = subprocess.run(["git", "merge-base", "--is-ancestor", FREEZE_TAG, "HEAD"], cwd=ROOT,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"Test tasks get no generation before the protocol freeze: tag {FREEZE_TAG} is missing "
                  f"or not in the history of HEAD.")
            return 1
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
