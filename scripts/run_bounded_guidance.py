"""Run bounded-guidance-v1 pairs. Defaults to a zero-cost mocked demonstration.

    uv run python scripts/run_bounded_guidance.py --run-id bg-mock-demo --mock

Real inference is gated by --real, --operator-approved, --limit-usd, a clean
commit, local pinned vLLM identity, and a separate test freeze tag. Never use
--real without the operator's specific dollar-limit approval. A stopped job
is not restarted automatically; --resume is an explicit operator action.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import time
import uuid
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from system1.bounded_guidance import (PLAN_MAX_OUTPUT_TOKENS, PLAN_MAX_WORDS, PLAN_MAX_CHARS,
                                      dev30_plan_messages, plan_messages, run_pair)
from system1.bounded_guidance_dev30 import (FRONTIER_LIMIT_USD as DEV30_FRONTIER_LIMIT_USD,
    GPU_RATE_USD_PER_HOUR as DEV30_GPU_RATE,
    MAX_FRONTIER_REQUESTS as DEV30_MAX_FRONTIER, MAX_PAIRS as DEV30_MAX_PAIRS,
    MAX_WALL_SECONDS as DEV30_MAX_WALL, MAX_WORKER_HTTP as DEV30_MAX_WORKER,
    TOTAL_CEILING_USD as DEV30_TOTAL_CEILING, WATCHDOG_SECONDS as DEV30_WATCHDOG_SECONDS,
    load_manifest as load_dev30_manifest)
from system1.config import RESULTS, ROOT, load_prices
from system1.eval.ledger import CostLedger, LedgerRow
from system1.eval.split import load_split
from system1.eval.exclusions import load_exclusions
from system1.frontier.client import API_URL, MODEL as FRONTIER_MODEL, PROVIDER, REASONING, parse_reply
from system1.loop.generate import Generator, MODEL as WORKER_MODEL, REVISION, load_tokenizer
from system1.loop.monitor import remote_vllm_server_identity, vllm_server_identity
from system1.loop.sandbox import VisibleRunner
from system1.loop.tasks import TaskSpec, load_tasks

PILOT_TASKS_FILE = "configs/bounded_guidance_pilot_v1.json"
DEV30_TASKS_FILE = "configs/bounded_guidance_dev30_v1.json"
PILOT_MAX_PAIRS = 120
PILOT_MAX_FRONTIER_USD = 1.50
PILOT_MAX_FRONTIER_REQUESTS = 120
PILOT_MAX_WORKER_HTTP_REQUESTS = 720
PILOT_MAX_RUN_SECONDS = 9000  # 2.5 h; external GPU deletion deadline is 3 h
PILOT_GPU_RATE_ASSUMPTION = 3.2004
PILOT_GPU_LIFETIME_HOURS = 3.0
PILOT_TOTAL_BUDGET_USD = 20.0
MAX_CONSECUTIVE_INVALID_ADVICE = 3


def validate_pilot_limits(args):
    """Fail before any paid call if pilot selection or operational caps expand."""
    if args.tasks_file == DEV30_TASKS_FILE:
        if args.split != "dev" or args.attempts != 1 or args.limit:
            raise SystemExit("dev30 requires the complete frozen development manifest and one attempt")
        if (args.limit_usd != DEV30_FRONTIER_LIMIT_USD
                or args.max_frontier_requests != DEV30_MAX_FRONTIER
                or args.max_worker_http_requests != DEV30_MAX_WORKER
                or args.max_wall_seconds != DEV30_MAX_WALL):
            raise SystemExit("dev30 requires exact frozen request, spend, and wall-time limits")
        if DEV30_GPU_RATE * DEV30_WATCHDOG_SECONDS / 3600 + args.limit_usd >= DEV30_TOTAL_CEILING:
            raise SystemExit("dev30 watchdog model reaches the proposed total ceiling")
        load_dev30_manifest()
        return
    if args.split != "dev" or args.attempts != 1 or args.tasks_file != PILOT_TASKS_FILE:
        raise SystemExit("real pilot requires the frozen 120-task dev file and one attempt")
    if any(x <= 0 for x in (args.limit_usd, args.max_frontier_requests,
                             args.max_worker_http_requests, args.max_wall_seconds)):
        raise SystemExit("pilot limits must be positive")
    if args.limit_usd > PILOT_MAX_FRONTIER_USD or args.max_frontier_requests > PILOT_MAX_FRONTIER_REQUESTS:
        raise SystemExit("frontier pilot cap exceeded")
    if args.max_worker_http_requests > PILOT_MAX_WORKER_HTTP_REQUESTS:
        raise SystemExit("Qwen pilot request cap exceeded")
    if args.max_wall_seconds > PILOT_MAX_RUN_SECONDS:
        raise SystemExit("pilot run-time cap exceeded")
    if PILOT_GPU_RATE_ASSUMPTION * PILOT_GPU_LIFETIME_HOURS + args.limit_usd >= PILOT_TOTAL_BUDGET_USD:
        raise SystemExit("modeled GPU lifetime plus frontier limit reaches the $20 ceiling")


@dataclass
class AdviceReply:
    content: str | None
    status: str
    call_id: str
    model_returned: str | None
    provider_returned: str | None
    input_tokens: int | None
    output_tokens: int | None
    usd_reported: float | None
    usd_computed: float | None
    latency_ms: float
    finish_reason: str = "stop"


class MockWorker:
    def __init__(self):
        self.calls = 0

    async def generate(self, messages, task_prompt, entry_point, *seed_parts, on_call=None):
        from system1.loop.generate import Generation
        self.calls += 1
        prompt = messages[0]["content"]
        if "Your first draft" not in prompt:
            code = ("def add_one(x):\n    return x + 1\n" if "AlreadyCorrect" in task_prompt
                    else "def add_one(x):\n    return x\n")
        elif "Advice from a separate assistant" in prompt:
            code = "def add_one(x):\n    return x + 1\n"
        elif "return x + 1" in prompt:
            code = "def add_one(x):\n    return x + 1\n"
        else:
            code = "def add_one(x):\n    return x\n"
        if on_call:
            on_call({"phase": "thinking", "input_tokens": len(prompt.split()), "output_tokens": 7,
                     "reasoning_tokens": 7, "latency_ms": 1.0, "status": "ok"})
            on_call({"phase": "answer", "input_tokens": len(prompt.split()) + 7, "output_tokens": 12,
                     "reasoning_tokens": 0, "latency_ms": 1.0, "status": "ok"})
        return Generation("mock", len(prompt.split()), "mock thought", f"```python\n{code}```", code,
                          [], 7, 12, 8192, False, True, 2.0, 1)


class MockVisible:
    def protocol(self):
        return {"visible_image_id": "mock-no-execution"}

    def run(self, code, tests, timeout):
        # No generated code is executed in mock mode.
        passed = "return x + 1" in code
        return {"execution": {"status": "ok", "stage": None}, "results": [
            {"status": "pass" if passed else "fail", "error_type": None, "message": None} for _ in tests],
            "runner": "mock-no-execution"}


class MockAdviser:
    def __init__(self, case="valid"):
        self.calls = 0
        self.case = case

    def ask(self, messages, *, task_id, sample):
        self.calls += 1
        content = {"valid": "The draft returns the input unchanged. Add one to x in the returned value.",
                   "overlength": "word " * 121, "empty": "", "truncated": "Check the edge case.",
                   "reasoning-only": None}[self.case]
        return AdviceReply(content,
                           "ok", f"mock-{self.calls}", "mock-adviser", "mock-provider",
                           len(messages[0]["content"].split()),
                           15, 0.0, 0.0, 1.0, "length" if self.case == "truncated" else "stop")


class BoundedAdviser:
    """One pinned OpenRouter request per eligible pair, with a ledger guard."""

    def __init__(self, ledger: CostLedger, limit_usd: float, exchanges: CostLedger):
        from system1.eval.ledger import usd_for
        prices = load_prices()
        entry = prices["models"][FRONTIER_MODEL]
        if entry["usd_per_m_input"] is None or entry["usd_per_m_output"] is None:
            raise RuntimeError("a pinned input and output price is required")
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is missing")
        self.client = httpx.Client(timeout=300, headers={"Authorization": f"Bearer {key}"})
        self.ledger, self.exchanges, self.limit_usd, self.prices = ledger, exchanges, limit_usd, prices
        self.p_in, self.p_out = entry["usd_per_m_input"], entry["usd_per_m_output"]
        self.usd_for = usd_for

    def close(self):
        self.client.close()

    def ask(self, messages, *, task_id, sample):
        import time
        import uuid
        # A conservative reservation uses UTF-8 bytes rather than a typical
        # characters-per-token ratio. The provider's actual usage is recorded.
        estimate = sum(len(m["content"].encode("utf-8")) for m in messages) + 500
        reserve = (estimate * self.p_in + PLAN_MAX_OUTPUT_TOKENS * self.p_out) / 1_000_000
        old_rows, damaged = self.ledger.read()
        if damaged:
            raise RuntimeError("damaged frontier ledger; stopping")
        spent = sum(float(r.get("usd_reported") if r.get("usd_reported") is not None else
                          r.get("usd_computed") if r.get("usd_computed") is not None else reserve)
                    for r in old_rows if r.get("component") == "frontier")
        if spent + reserve > self.limit_usd:
            raise RuntimeError(f"frontier spend guard stopped at ${spent:.4f}; next reserve ${reserve:.4f}; "
                               f"limit ${self.limit_usd:.2f}")
        call_id = uuid.uuid4().hex
        t0 = time.perf_counter()
        status = "ok"
        parsed = parse_reply(None)
        response_body = None
        status_code = None
        request_body = {"model": FRONTIER_MODEL, "messages": messages,
            "max_tokens": PLAN_MAX_OUTPUT_TOKENS, "reasoning": REASONING,
            "provider": PROVIDER, "usage": {"include": True}}
        try:
            response = self.client.post(API_URL, json=request_body)
            status_code = response.status_code
            try:
                response_body = response.json()
                parsed = parse_reply(response_body)
            except ValueError:
                parsed = parse_reply(None)
            status = parsed["status"] if response.is_success else f"http:{response.status_code}"
            if response.is_success and isinstance(response_body, dict):
                choices = response_body.get("choices")
                if isinstance(choices, list) and choices and isinstance(choices[0], dict):
                    message = choices[0].get("message")
                    content = message.get("content") if isinstance(message, dict) else None
                    if content is not None and not isinstance(content, str):
                        status = "protocol:non-string content"
                if parsed["input_tokens"] is None or parsed["output_tokens"] is None:
                    status = "protocol:missing usage"
                if parsed["finish_reason"] not in ("stop", "length", "content_filter"):
                    status = "protocol:unresolved finish reason"
                if parsed["output_tokens"] is not None and parsed["output_tokens"] > PLAN_MAX_OUTPUT_TOKENS:
                    status = "protocol:completion exceeds request cap"
                if parsed["model_returned"] not in (FRONTIER_MODEL, "anthropic/claude-sonnet-5.5"):
                    status = "protocol:unexpected returned model"
                if parsed["provider_returned"] is not None and parsed["provider_returned"].lower() != "anthropic":
                    status = "protocol:unexpected returned provider"
                if status == "protocol:empty content" and parsed["input_tokens"] is not None and parsed["output_tokens"] is not None:
                    status = "ok"  # ordinary failed delivery; the pair records and retains it
        except httpx.TransportError as e:
            status = f"transport:{type(e).__name__}"
        cost = self.usd_for(self.prices, FRONTIER_MODEL, parsed["input_tokens"], parsed["output_tokens"])
        elapsed = round((time.perf_counter() - t0) * 1000, 1)
        self.ledger.append(LedgerRow(component="frontier", model=FRONTIER_MODEL, provider="openrouter",
            task_id=task_id, step=sample, arm="bounded_plan", call_id=call_id, http_attempt=0, status=status,
            input_tokens=parsed["input_tokens"], output_tokens=parsed["output_tokens"],
            reasoning_tokens=parsed["reasoning_tokens"], usd_reported=parsed["usd_reported"],
            usd_computed=cost, latency_ms=elapsed, model_returned=parsed["model_returned"]))
        # Append the credential-free request body and full provider response even
        # when parsing fails, so a billed rejection can be reproduced offline.
        self.exchanges.append_obj({"call_id": call_id, "task_id": task_id, "sample": sample,
            "request_body": request_body, "http_status": status_code,
            "response_body": response_body, "status": status})
        if status != "ok":
            raise RuntimeError(f"frontier call {call_id} stopped with {status}")
        actual_spend = sum(float(r.get("usd_reported") if r.get("usd_reported") is not None else
                                 r.get("usd_computed") if r.get("usd_computed") is not None else reserve)
                           for r in self.ledger.read()[0] if r.get("component") == "frontier")
        if actual_spend > self.limit_usd:
            raise RuntimeError(f"frontier spending violation: ${actual_spend:.4f} > ${self.limit_usd:.4f}")
        return AdviceReply(parsed["content"], status, call_id, parsed["model_returned"],
                           parsed["provider_returned"],
                           parsed["input_tokens"], parsed["output_tokens"], parsed["usd_reported"], cost, elapsed,
                           parsed["finish_reason"])


class RecordingWorkerClient:
    """One record per Qwen HTTP attempt, including failures and raw bodies."""

    def __init__(self, client: httpx.AsyncClient, exchanges: CostLedger, maximum: int):
        self.client, self.exchanges, self.maximum = client, exchanges, maximum
        self.used = 0
        self.task_id = None

    async def post(self, url, *, json, timeout):
        if self.used >= self.maximum:
            raise RuntimeError("Qwen HTTP request ceiling reached")
        self.used += 1
        row = {"call_id": uuid.uuid4().hex, "task_id": self.task_id,
               "http_ordinal": self.used, "request_body": json,
               "response_body": None, "http_status": None}
        started = time.perf_counter()
        try:
            response = await self.client.post(url, json=json, timeout=timeout)
            row["http_status"] = response.status_code
            try:
                row["response_body"] = response.json()
            except ValueError:
                row["response_text"] = response.text
            return response
        except BaseException as exc:
            row["error_type"] = type(exc).__name__
            raise
        finally:
            row["latency_ms"] = round((time.perf_counter() - started) * 1000, 1)
            self.exchanges.append_obj(row)


def git_state():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip())
    return commit, dirty


def mock_tasks():
    return {f"Mock/{i}": TaskSpec(f"Mock/{i}", "mock",
        "Implement add_one(x)." + (" AlreadyCorrect" if i == 2 else ""),
        "add_one", ({"kind": "assert", "source": "assert add_one(1) == 2"},), "mock", "") for i in range(3)}


async def run(args):
    if args.mock == args.real:
        raise SystemExit("choose exactly one of --mock or --real")
    if args.real and getattr(args, "mock_advice_case", "valid") != "valid":
        raise SystemExit("--mock-advice-case is only for mock runs")
    if args.real and (not args.operator_approved or args.limit_usd is None or args.limit_usd <= 0):
        raise SystemExit("real inference needs --operator-approved and a positive --limit-usd")
    if args.real and (not args.max_wall_seconds or not args.max_worker_http_requests
                      or not args.max_frontier_requests):
        raise SystemExit("real inference also needs wall-time and request-count ceilings")
    if args.real:
        validate_pilot_limits(args)
    is_dev30 = args.real and args.tasks_file == DEV30_TASKS_FILE
    if is_dev30 and args.resume:
        raise SystemExit("dev30 does not allow resuming, retrying, or replacing a stopped task")
    if bool(args.remote_manifest) != (args.server_url.rstrip("/") != "http://localhost:8000"):
        raise SystemExit("a remote server URL and --remote-manifest must be provided together")
    if args.real and args.split == "test":
        tag = subprocess.run(["git", "merge-base", "--is-ancestor", "bounded-guidance-v1-freeze", "HEAD"],
                             cwd=ROOT)
        if tag.returncode != 0:
            raise SystemExit("test generation needs the new bounded-guidance-v1-freeze tag")
    commit, dirty = git_state()
    if args.real and dirty:
        raise SystemExit("real protocol run needs a clean committed tree")
    if args.mock:
        tasks, ids = mock_tasks(), list(mock_tasks())
        worker, visible, adviser = MockWorker(), MockVisible(), MockAdviser(getattr(args, "mock_advice_case", "valid"))
        server_identity = {"mock": True}
    else:
        try:
            from scripts.run_loop import EXPECTED_SERVER
        except ModuleNotFoundError:  # direct `python scripts/run_bounded_guidance.py`
            from run_loop import EXPECTED_SERVER
        if args.remote_manifest:
            manifest = json.loads(open(args.remote_manifest, encoding="utf-8").read())
            server_identity = remote_vllm_server_identity(
                EXPECTED_SERVER, manifest, args.server_url.rstrip("/") + "/v1/models")
        else:
            server_identity = vllm_server_identity(EXPECTED_SERVER)
        tasks, split = load_tasks(), load_split()
        ids = [t for b in ("humaneval+", "mbpp+") for t in split["benchmarks"][b][args.split]]
        excluded = load_exclusions()
        ids = [tid for tid in ids if tid not in excluded["tasks"]]
        visible = VisibleRunner(max_concurrent=1)
        worker = None  # constructed inside the HTTP client context
        adviser = None
    task_file_sha256 = None
    if args.tasks_file:
        if args.mock:
            raise SystemExit("--tasks-file is only for the real development pilot")
        task_file = ROOT / args.tasks_file
        raw = task_file.read_bytes()
        spec = json.loads(raw)
        selected = spec.get("tasks")
        expected_version = "bounded-guidance-dev30-v1" if is_dev30 else "bounded-guidance-pilot-v1"
        if (spec.get("version") != expected_version or spec.get("split") != args.split
                or not isinstance(selected, list) or len(selected) != len(set(selected))):
            raise SystemExit("invalid pilot task manifest")
        expected_count = DEV30_MAX_PAIRS if is_dev30 else PILOT_MAX_PAIRS
        expected_benchmarks = {"humaneval+": 9, "mbpp+": 21} if is_dev30 else {"humaneval+": 36, "mbpp+": 84}
        if len(selected) != expected_count or any(tid not in ids for tid in selected):
            raise SystemExit("pilot tasks are missing, excluded, or outside the split")
        if Counter(tasks[tid].benchmark for tid in selected) != expected_benchmarks:
            raise SystemExit("pilot benchmark counts changed")
        if is_dev30:
            load_dev30_manifest(task_file)
        ids = selected
        import hashlib
        task_file_sha256 = hashlib.sha256(raw).hexdigest()
    ids = ids[:args.limit] if args.limit else ids
    if args.real and len(ids) * args.attempts > (DEV30_MAX_PAIRS if is_dev30 else PILOT_MAX_PAIRS):
        raise SystemExit("pilot exceeds its paired-unit ceiling")
    out = RESULTS / "runs" / args.run_id
    if out.exists() and not args.resume:
        raise SystemExit(f"{out} exists; use a fresh run id, or explicit --resume after a stopped job")
    out.mkdir(parents=True, exist_ok=True)
    proto = {"experiment": "bounded-guidance-v1", "amendment": "invalid-advice-v1a-20261027",
             "backend": "mock" if args.mock else "real",
             "mock_advice_case": getattr(args, "mock_advice_case", "valid") if args.mock else None,
             "split": args.split, "task_ids": ids, "attempts": args.attempts,
             "shared_drafts": 1, "continuations_per_arm": 1, "advice_for_first_pass": True,
             "plan_max_words": PLAN_MAX_WORDS, "plan_max_chars": PLAN_MAX_CHARS,
             "plan_max_output_tokens": PLAN_MAX_OUTPUT_TOKENS, "worker_model": WORKER_MODEL,
             "max_consecutive_invalid_advice": MAX_CONSECUTIVE_INVALID_ADVICE,
             "worker_revision": REVISION, "frontier_model": FRONTIER_MODEL,
             "excluded_tasks_sha256": excluded["sha256"] if args.real else None,
             "task_file_sha256": task_file_sha256,
             "pilot_profile": "dev30-v1" if is_dev30 else None,
             "planner_prompt": "successful-planner-preflight-v1b-20261027" if is_dev30 else "original-v1a",
             "server": server_identity, "server_url": args.server_url.rstrip("/"),
             "visible": visible.protocol(), "git_commit": commit,
             "git_dirty": dirty}
    meta_file = out / "run_meta.json"
    if meta_file.exists():
        old = json.loads(meta_file.read_text())
        if old["protocol"] != proto:
            raise SystemExit("resume protocol mismatch; use a new run id")
        meta = old
    else:
        meta = {"run_id": args.run_id, "protocol": proto, "sessions": []}
    pairs = CostLedger(out / "pairs.jsonl")
    plans = CostLedger(out / "plans.jsonl")
    exchanges = CostLedger(out / "frontier_exchanges.jsonl")
    checkpoints = CostLedger(out / "checkpoints.jsonl")
    calls = CostLedger(out / "worker_calls.jsonl")
    worker_exchanges = CostLedger(out / "worker_exchanges.jsonl") if is_dev30 else None
    failures = CostLedger(out / "failures.jsonl")
    ledger = CostLedger(out / "ledger.jsonl")
    done, bad = pairs.read()
    if bad:
        raise SystemExit("damaged pair data; stopping before any inference")
    completed = {(r["task_id"], r["attempt"]) for r in done}
    invalid_streak = 0
    for old_pair in reversed(done):
        if old_pair.get("advice_delivery") != "invalid":
            break
        invalid_streak += 1
    session = {"started": datetime.now(timezone.utc).isoformat(), "limit_usd": args.limit_usd,
               "max_wall_seconds": args.max_wall_seconds,
               "max_worker_http_requests": args.max_worker_http_requests,
               "max_frontier_requests": args.max_frontier_requests,
               "n_pending": len(ids) * args.attempts - len(completed), "status": "running"}
    meta["sessions"].append(session)
    meta_file.write_text(json.dumps(meta, indent=2))

    start_time = time.monotonic()

    async def body(worker, adviser):
        nonlocal invalid_streak
        for task_id in ids:
            for attempt in range(args.attempts):
                if (task_id, attempt) in completed:
                    continue
                if invalid_streak >= MAX_CONSECUTIVE_INVALID_ADVICE:
                    raise RuntimeError("three consecutive invalid advice deliveries; stop before another paid pair")
                if args.real:
                    # Reserve the maximum for a whole pair before it starts:
                    # three two-phase Qwen generations and one plan request.
                    n_worker = len(calls.read()[0])
                    n_plan = sum(r.get("component") == "frontier" for r in ledger.read()[0])
                    if is_dev30 and len(worker_exchanges.read()[0]) != n_worker:
                        raise RuntimeError("Qwen exchange and usage logs disagree; stop before another task")
                    if n_worker + 6 > args.max_worker_http_requests:
                        raise RuntimeError("Qwen HTTP request ceiling reached before next pair")
                    if n_plan + 1 > args.max_frontier_requests:
                        raise RuntimeError("frontier request ceiling reached before next pair")
                    if time.monotonic() - start_time >= args.max_wall_seconds:
                        raise RuntimeError("wall-time ceiling reached before next pair")
                try:
                    if is_dev30:
                        worker_client.task_id = task_id
                    result = await run_pair(tasks[task_id], attempt, worker, visible, adviser,
                                            on_worker_call=calls.append_obj, on_advice=plans.append_obj,
                                            on_checkpoint=checkpoints.append_obj,
                                            planner_messages=dev30_plan_messages if is_dev30 else plan_messages,
                                            require_equal_continuation_caps=is_dev30)
                    # The unit is committed only when both branches finish.
                    pairs.append_obj({"pair_id": result.pair_id, "task_id": task_id,
                        "benchmark": tasks[task_id].benchmark, "attempt": attempt,
                        "first_visible_pass": result.rows[0]["visible_pass"],
                        "advice_delivery": result.plan["delivery_status"],
                        "plan_call_id": result.plan["call_id"] if result.plan else None,
                        "rows": result.rows, "final_checkpoint_ids": {
                            arm: rec["checkpoint_id"] for arm, rec in result.final.items()}})
                    invalid_streak = invalid_streak + 1 if result.plan["delivery_status"] == "invalid" else 0
                    print(f"{task_id} a{attempt}: first pass={result.rows[0]['visible_pass']}, "
                          f"final={[result.final[a]['visible_pass'] for a in ('control', 'guidance')]}", flush=True)
                except Exception as e:
                    failures.append_obj({"task_id": task_id, "attempt": attempt,
                                         "error_type": type(e).__name__, "error": str(e)[:300]})
                    raise

    try:
        if args.mock:
            await body(worker, adviser)
            session["mock_counts"] = {"worker_generations": worker.calls, "frontier_plans": adviser.calls}
        else:
            async with httpx.AsyncClient() as client:
                worker_client = (RecordingWorkerClient(client, worker_exchanges, args.max_worker_http_requests)
                                 if is_dev30 else client)
                worker = Generator(worker_client, load_tokenizer(),
                                   url=args.server_url.rstrip("/") + "/v1/completions")
                adviser = BoundedAdviser(ledger, args.limit_usd, exchanges)
                try:
                    await body(worker, adviser)
                finally:
                    adviser.close()
        session["status"] = "finished"
    except BaseException:
        session["status"] = "stopped"
        raise
    finally:
        session["ended"] = datetime.now(timezone.utc).isoformat()
        session["elapsed_s"] = round(time.monotonic() - start_time, 1)
        meta_file.write_text(json.dumps(meta, indent=2))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--mock-advice-case", choices=("valid", "overlength", "empty", "truncated", "reasoning-only"),
                    default="valid", help="mock-only response shape for integration checks")
    ap.add_argument("--real", action="store_true")
    ap.add_argument("--operator-approved", action="store_true")
    ap.add_argument("--limit-usd", type=float)
    ap.add_argument("--max-wall-seconds", type=float)
    ap.add_argument("--max-worker-http-requests", type=int)
    ap.add_argument("--max-frontier-requests", type=int)
    ap.add_argument("--server-url", default="http://localhost:8000")
    ap.add_argument("--remote-manifest", default="")
    ap.add_argument("--split", choices=("dev", "test"), default="dev")
    ap.add_argument("--attempts", type=int, default=1)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tasks-file", default="")
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()
    if args.attempts < 1 or args.limit < 0:
        ap.error("attempts must be positive and limit nonnegative")
    out = asyncio.run(run(args))
    print(f"saved {out}")


if __name__ == "__main__":
    sys.exit(main())
