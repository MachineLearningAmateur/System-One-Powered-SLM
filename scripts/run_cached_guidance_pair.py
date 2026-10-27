"""Prepare or run one engineering pair from a saved draft and accepted plan.

Offline, with no network calls:
    uv run python scripts/run_cached_guidance_pair.py --prepare \
      --output results/bg-cached-plan-pair-prepared-20261027.json

The real mode requires a separate GPU approval, an active deletion watchdog,
a clean commit, a fresh run ID, and the exact offline packet. It makes zero
frontier calls and at most four Qwen HTTP calls for two continuations. It never
regenerates the shared draft or repeats a stopped pair.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import hashlib
import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

import httpx

from system1.bounded_guidance import continuation_messages, validate_plan
from system1.config import RESULTS, ROOT
from system1.eval.ledger import CostLedger, read_jsonl
from system1.loop.generate import (CODE_TOKENS, MAX_MODEL_LEN, MODEL, REVISION, SAMPLING, SEED_TAG,
                                   THINK_CAP, TOP_LOGPROBS, Generator, load_tokenizer,
                                   render_prompt, request_seed)
from system1.loop.monitor import remote_vllm_server_identity
from system1.loop.runner import VISIBLE_TIMEOUT_S
from system1.loop.sandbox import VisibleRunner
from system1.loop.tasks import first_round_messages, load_tasks

try:
    from scripts.preflight_bounded_guidance_planner import SOURCE_RUN_ID, source_request
    from scripts.run_loop import EXPECTED_SERVER
except ModuleNotFoundError:  # direct script execution
    from preflight_bounded_guidance_planner import SOURCE_RUN_ID, source_request
    from run_loop import EXPECTED_SERVER

PREFLIGHT_RUN_ID = "bg-v1b-planner-preflight-20261027"
PREFLIGHT_CALL_ID = "5b76a3eef8ad495b9806d402b6a31ee0"
PLAN_SHA256 = "8dada55126c03965446ce27d754dad6f237e83c22300ceee5d54b83d258c7fe2"
TASK_ID = "HumanEval/59"
ATTEMPT = 0
ROUND = 2
MAX_WORKER_HTTP = 4
MAX_WALL_SECONDS = 900
MAX_WATCHDOG_SECONDS = 40 * 60
PROPOSED_GPU_LIMIT_USD = 3.0
GPU_RATE_USD_PER_HOUR_ASSUMPTION = 3.2004
ENGINEERING_LABEL = "engineering integration check using a cached accepted plan"
CONFIG_PATH = ROOT / "configs" / "cached_guidance_integration_v1.json"


def _one(path: Path) -> dict:
    rows, damaged = read_jsonl(path)
    if damaged or len(rows) != 1:
        raise ValueError(f"expected exactly one intact record in {path}")
    return rows[0]


def _sha_json(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def _config_sha256() -> str:
    raw = CONFIG_PATH.read_bytes()
    config = json.loads(raw)
    expected = {"version": "cached-accepted-plan-integration-v1",
                "purpose": ENGINEERING_LABEL, "primary_research_estimate": False,
                "task_id": TASK_ID, "attempt": ATTEMPT,
                "source_run_id": SOURCE_RUN_ID,
                "source_checkpoint_id": "HumanEval/59/a0/shared/r1",
                "preflight_run_id": PREFLIGHT_RUN_ID,
                "preflight_call_id": PREFLIGHT_CALL_ID,
                "accepted_plan_sha256": PLAN_SHA256,
                "continuation_arms": ["control", "guidance"],
                "max_worker_http_requests": MAX_WORKER_HTTP,
                "max_frontier_requests": 0,
                "max_wall_seconds": MAX_WALL_SECONDS,
                "max_watchdog_seconds": MAX_WATCHDOG_SECONDS,
                "proposed_gpu_spend_limit_usd": PROPOSED_GPU_LIMIT_USD}
    if config != expected:
        raise ValueError("cached-plan integration configuration changed")
    return hashlib.sha256(raw).hexdigest()


def verified_sources() -> tuple[object, dict, str, dict]:
    """Read only saved generation and planner artifacts, never hidden grades."""
    original_request = source_request()  # verifies the original draft/adviser join
    source_pair = _one(RESULTS / "runs" / SOURCE_RUN_ID / "pairs.jsonl")
    if source_pair["task_id"] != TASK_ID or source_pair["attempt"] != ATTEMPT:
        raise ValueError("source pair identity changed")
    first = next((r for r in source_pair["rows"] if r["arm"] == "shared" and r["round"] == 1), None)
    if first is None or first["checkpoint_id"] != "HumanEval/59/a0/shared/r1":
        raise ValueError("saved shared checkpoint changed")
    tasks = load_tasks()
    task = tasks[TASK_ID]
    if first["prompt_messages"] != first_round_messages(task):
        raise ValueError("saved draft prompt does not match the frozen task")
    if _sha_json(first["prompt_messages"]) != first["prompt_sha256"]:
        raise ValueError("saved draft prompt hash mismatch")
    if hashlib.sha256((first["code"] or "").encode()).hexdigest() != first["code_sha256"]:
        raise ValueError("saved draft code hash mismatch")
    if not first["code"] or first["visible_report"] not in original_request["messages"][0]["content"]:
        raise ValueError("source planner request does not match the saved checkpoint")

    preflight = RESULTS / "runs" / PREFLIGHT_RUN_ID
    result = json.loads((preflight / "preflight_result.json").read_text())
    request = json.loads((preflight / "preflight_request.json").read_text())
    exchange = _one(preflight / "frontier_exchanges.jsonl")
    ledger = _one(preflight / "ledger.jsonl")
    if not (result["call_id"] == exchange["call_id"] == ledger["call_id"] == PREFLIGHT_CALL_ID):
        raise ValueError("accepted plan call provenance changed")
    if request != exchange["request_body"]:
        raise ValueError("saved preflight request/response join mismatch")
    if request["messages"][0]["content"].split("Task and visible examples:\n", 1)[1] != (
            original_request["messages"][0]["content"].split("Task and visible examples:\n", 1)[1]):
        raise ValueError("preflight used another draft or visible result")
    raw_plan = exchange["response_body"]["choices"][0]["message"]["content"]
    if raw_plan != result["visible_content"] or raw_plan != validate_plan(raw_plan):
        raise ValueError("preflight accepted plan differs from saved visible text")
    if hashlib.sha256(raw_plan.encode()).hexdigest() != PLAN_SHA256:
        raise ValueError("accepted plan hash changed")
    if (result["delivery_status"] != "delivered" or result["validation_reasons"]
            or not all(result["validation_rules"].values()) or result["finish_reason"] != "stop"
            or exchange["response_body"]["choices"][0]["finish_reason"] != "stop"):
        raise ValueError("saved plan did not pass every frozen delivery rule")
    provenance = {"source_run_id": SOURCE_RUN_ID, "source_pair_id": source_pair["pair_id"],
                  "source_checkpoint_id": first["checkpoint_id"],
                  "source_checkpoint_code_sha256": first["code_sha256"],
                  "source_visible_report_sha256": hashlib.sha256(first["visible_report"].encode()).hexdigest(),
                  "preflight_run_id": PREFLIGHT_RUN_ID, "preflight_call_id": PREFLIGHT_CALL_ID,
                  "plan_sha256": PLAN_SHA256, "previously_incurred_planner_usd": ledger["usd_reported"]}
    return task, first, raw_plan, provenance


def prepare_packet(tokenizer=None) -> dict:
    config_sha256 = _config_sha256()
    task, first, plan, provenance = verified_sources()
    tokenizer = tokenizer or load_tokenizer()
    control = continuation_messages(task, first["code"], first["visible_report"])
    guidance = continuation_messages(task, first["code"], first["visible_report"], plan)
    base = control[0]["content"]
    advice_suffix = "\nAdvice from a separate assistant (check it; it may be wrong):\n" + plan + "\n"
    if guidance[0]["content"] != base + advice_suffix or advice_suffix in base:
        raise ValueError("continuation base instructions or advice isolation changed")
    seed = request_seed(SEED_TAG, TASK_ID, ATTEMPT, ROUND)
    first_phase = {}
    prompt_tokens = {}
    effective_caps = {}
    for arm, messages in (("control", control), ("guidance", guidance)):
        prompt = render_prompt(tokenizer, messages)
        n_prompt = len(tokenizer(prompt)["input_ids"])
        cap = min(THINK_CAP, MAX_MODEL_LEN - n_prompt - CODE_TOKENS - 16)
        if cap <= 0:
            raise ValueError("continuation prompt leaves no room for thinking")
        first_phase[arm] = {"model": MODEL, "prompt": prompt, "max_tokens": cap,
                            "seed": seed, "logprobs": TOP_LOGPROBS, **SAMPLING,
                            "stop": ["</think>"]}
        prompt_tokens[arm] = n_prompt
        effective_caps[arm] = cap
    if effective_caps["control"] != effective_caps["guidance"]:
        raise ValueError("the branches have different effective Qwen thinking caps")
    return {"version": "cached-accepted-plan-integration-v1", "label": ENGINEERING_LABEL,
            "config_sha256": config_sha256,
            "task_id": TASK_ID, "attempt": ATTEMPT, "source": provenance,
            "worker": {"model": MODEL, "revision": REVISION, "sampling": SAMPLING,
                       "seed": seed, "seed_tag": SEED_TAG, "round": ROUND,
                       "think_cap": THINK_CAP, "answer_cap": CODE_TOKENS,
                       "max_model_len": MAX_MODEL_LEN, "top_logprobs": TOP_LOGPROBS,
                       "effective_think_caps": effective_caps, "prompt_tokens": prompt_tokens},
            "base_content_sha256": hashlib.sha256(base.encode()).hexdigest(),
            "messages": {"control": control, "guidance": guidance},
            "first_phase_http_requests": first_phase,
            "cached_shared_checkpoint": first,
            "incremental_frontier_requests": 0,
            "max_worker_http_requests": MAX_WORKER_HTTP}


class CallBudget:
    def __init__(self, maximum: int):
        self.maximum = maximum
        self.used = 0


class RecordingClient:
    """Record every Qwen HTTP request and raw response before Generator parses it."""

    def __init__(self, client: httpx.AsyncClient, arm: str, exchange_log: CostLedger,
                 budget: CallBudget):
        self.client, self.arm, self.exchange_log, self.budget = client, arm, exchange_log, budget
        self.arm_calls = 0

    async def post(self, url, *, json, timeout):
        if self.budget.used >= self.budget.maximum:
            raise RuntimeError("four-call Qwen HTTP ceiling reached")
        self.budget.used += 1
        self.arm_calls += 1
        call_id = uuid.uuid4().hex
        started = time.perf_counter()
        row = {"call_id": call_id, "arm": self.arm,
               "phase": "thinking" if self.arm_calls == 1 else "answer",
               "http_ordinal": self.budget.used, "request_body": json,
               "response_body": None, "http_status": None}
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
            self.exchange_log.append_obj(row)


def _checkpoint(task, pair_id: str, arm: str, messages: list[dict], generation, visible_result) -> dict:
    code = generation.code
    if code is None:
        execution = {"status": "no_code", "stage": "extract", "error_type": "NoCode",
                     "message": "the answer contains no usable Python code block"}
        results = [{"status": "not_run", "error_type": None, "message": None} for _ in task.visible_tests]
        runner, elapsed = None, None
    else:
        execution, results = visible_result["execution"], visible_result["results"]
        runner, elapsed = visible_result.get("runner"), visible_result.get("elapsed_s")
    from system1.loop.tasks import format_test_report
    report = format_test_report(task.visible_tests, results, execution)
    return {"pair_id": pair_id, "task_id": TASK_ID, "benchmark": task.benchmark,
            "attempt": ATTEMPT, "arm": arm, "round": ROUND,
            "checkpoint_id": f"{TASK_ID}/a{ATTEMPT}/{arm}/r{ROUND}",
            "prompt_messages": messages, "prompt_sha256": _sha_json(messages),
            "code": code, "code_sha256": hashlib.sha256((code or "").encode()).hexdigest(),
            "answer": generation.answer, "thinking": generation.thinking,
            "visible_execution": execution, "visible_results": results,
            "visible_report": report,
            "visible_pass": bool(code is not None and execution.get("status") == "ok"
                                 and all(x["status"] == "pass" for x in results)),
            "visible_runner": runner, "visible_elapsed_s": elapsed,
            "generation": {"prompt_tokens": generation.prompt_tokens,
                           "thinking_tokens": generation.thinking_tokens,
                           "answer_tokens": generation.answer_tokens,
                           "latency_ms": generation.latency_ms,
                           "cap_hit": generation.cap_hit,
                           "effective_cap": generation.effective_cap,
                           "seed": generation.seed,
                           "phase1_finish": generation.phase1_finish,
                           "answer_finish": generation.answer_finish}}


async def _run_real(args, packet: dict) -> Path:
    if not args.operator_approved or args.max_worker_http_requests != MAX_WORKER_HTTP:
        raise SystemExit("a separately approved real pair requires exactly four Qwen HTTP slots")
    if args.max_frontier_requests != 0 or args.max_wall_seconds is None or not 0 < args.max_wall_seconds <= MAX_WALL_SECONDS:
        raise SystemExit("real cached pair needs zero frontier calls and at most 900 seconds")
    if args.approved_gpu_usd is None or not 0 < args.approved_gpu_usd <= PROPOSED_GPU_LIMIT_USD:
        raise SystemExit("a new positive GPU approval of at most $3 is required")
    if not args.run_id or not args.server_url or not args.remote_manifest or not args.watchdog_manifest:
        raise SystemExit("real cached pair needs a fresh run ID, server identity, and watchdog")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip():
        raise SystemExit("real cached pair needs a clean committed tree")
    watcher = json.loads(Path(args.watchdog_manifest).read_text())
    started = datetime.fromisoformat(watcher["started_utc"])
    deadline = datetime.fromisoformat(watcher["deadline_utc"])
    if ((deadline - started).total_seconds() > MAX_WATCHDOG_SECONDS
            or deadline <= datetime.now(timezone.utc) or not watcher.get("resource_group")):
        raise SystemExit("independent GPU deletion watchdog is outside the 40-minute guard")
    modeled_watchdog_gpu_usd = ((deadline - started).total_seconds() / 3600
                                * GPU_RATE_USD_PER_HOUR_ASSUMPTION)
    if modeled_watchdog_gpu_usd > args.approved_gpu_usd:
        raise SystemExit("modeled GPU spend to watchdog deadline exceeds the new approval")
    try:
        os.kill(int(watcher["pid"]), 0)
    except (OSError, ValueError) as exc:
        raise SystemExit("independent GPU deletion watchdog is not running") from exc
    manifest = json.loads(Path(args.remote_manifest).read_text())
    identity = remote_vllm_server_identity(EXPECTED_SERVER, manifest,
                                           args.server_url.rstrip("/") + "/v1/models")
    out = RESULTS / "runs" / args.run_id
    out.mkdir(parents=True, exist_ok=False)
    (out / "prepared_packet.json").write_text(json.dumps(packet, indent=2))
    task, source_first, _, _ = verified_sources()
    pair_id = uuid.uuid4().hex
    first = copy.deepcopy(source_first)
    first["pair_id"] = pair_id
    first["source_pair_id"] = packet["source"]["source_pair_id"]
    session = {"started": datetime.now(timezone.utc).isoformat(),
               "max_worker_http_requests": MAX_WORKER_HTTP, "max_frontier_requests": 0,
               "max_wall_seconds": args.max_wall_seconds, "status": "running"}
    meta = {"run_id": args.run_id,
            "protocol": {"experiment": "cached-plan-engineering-integration-v1", "backend": "real",
                         "engineering_only": True, "label": ENGINEERING_LABEL,
                         "task_ids": [TASK_ID], "attempts": 1,
                         "source": packet["source"], "worker": packet["worker"],
                         "server_url": args.server_url.rstrip("/"), "server": identity,
                         "visible": VisibleRunner(max_concurrent=1).protocol(),
                         "git_commit": commit, "git_dirty": False,
                         "prepared_packet_sha256": _sha_json(packet),
                         "watchdog_group": watcher["resource_group"],
                         "watchdog_deadline_utc": watcher["deadline_utc"],
                         "approved_gpu_usd": args.approved_gpu_usd,
                         "modeled_watchdog_gpu_usd": modeled_watchdog_gpu_usd},
            "sessions": [session]}
    meta_path = out / "run_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2))
    calls = CostLedger(out / "worker_calls.jsonl")
    exchanges = CostLedger(out / "worker_exchanges.jsonl")
    checkpoints = CostLedger(out / "checkpoints.jsonl")
    pairs = CostLedger(out / "pairs.jsonl")
    failures = CostLedger(out / "failures.jsonl")
    visible = VisibleRunner(max_concurrent=1)
    budget = CallBudget(MAX_WORKER_HTTP)
    started_monotonic = time.monotonic()
    try:
        async with httpx.AsyncClient() as http:
            final = {}
            tokenizer = load_tokenizer()
            for arm in ("control", "guidance"):
                remaining = args.max_wall_seconds - (time.monotonic() - started_monotonic)
                if remaining <= 0:
                    raise RuntimeError("wall-time ceiling reached before the next continuation")
                client = RecordingClient(http, arm, exchanges, budget)
                generator = Generator(client, tokenizer,
                                      url=args.server_url.rstrip("/") + "/v1/completions")
                messages = packet["messages"][arm]

                def on_call(call, arm=arm):
                    calls.append_obj({"pair_id": pair_id, "task_id": TASK_ID, "attempt": ATTEMPT,
                                      "arm": arm, "round": ROUND, **call})

                generation = await asyncio.wait_for(generator.generate(
                    messages, task.prompt, task.entry_point, SEED_TAG, TASK_ID, ATTEMPT, ROUND,
                    on_call=on_call), timeout=remaining)
                visible_result = (await asyncio.to_thread(visible.run, generation.code,
                    list(task.visible_tests), VISIBLE_TIMEOUT_S) if generation.code is not None else None)
                row = _checkpoint(task, pair_id, arm, messages, generation, visible_result)
                checkpoints.append_obj(row)
                final[arm] = row
        recorded, damaged = exchanges.read()
        if damaged or len(recorded) != budget.used:
            raise RuntimeError("Qwen HTTP exchange log is incomplete")
        for arm in ("control", "guidance"):
            first_call = next((x for x in recorded if x["arm"] == arm and x["phase"] == "thinking"), None)
            if first_call is None or first_call["request_body"] != packet["first_phase_http_requests"][arm]:
                raise RuntimeError(f"{arm} Qwen request differs from the reviewed offline packet")
        pairs.append_obj({"pair_id": pair_id, "task_id": TASK_ID, "benchmark": task.benchmark,
                          "attempt": ATTEMPT, "first_visible_pass": first["visible_pass"],
                          "advice_delivery": "cached_delivered_to_guidance",
                          "plan_call_id": PREFLIGHT_CALL_ID,
                          "engineering_only": True, "label": ENGINEERING_LABEL,
                          "rows": [first, final["control"], final["guidance"]],
                          "final_checkpoint_ids": {a: r["checkpoint_id"] for a, r in final.items()}})
        session["status"] = "finished"
    except BaseException as exc:
        failures.append_obj({"task_id": TASK_ID, "error_type": type(exc).__name__,
                             "error": str(exc)[:300]})
        session["status"] = "stopped"
        raise
    finally:
        session["ended"] = datetime.now(timezone.utc).isoformat()
        session["elapsed_s"] = round(time.monotonic() - started_monotonic, 1)
        session["worker_http_requests"] = budget.used
        meta_path.write_text(json.dumps(meta, indent=2))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--real", action="store_true")
    parser.add_argument("--output", help="new ignored offline packet")
    parser.add_argument("--prepared-file", help="exact offline packet approved for the real pair")
    parser.add_argument("--run-id")
    parser.add_argument("--operator-approved", action="store_true")
    parser.add_argument("--max-worker-http-requests", type=int)
    parser.add_argument("--max-frontier-requests", type=int)
    parser.add_argument("--max-wall-seconds", type=float)
    parser.add_argument("--approved-gpu-usd", type=float)
    parser.add_argument("--server-url")
    parser.add_argument("--remote-manifest")
    parser.add_argument("--watchdog-manifest")
    args = parser.parse_args()
    packet = prepare_packet()
    if args.prepare:
        if not args.output or args.run_id or args.operator_approved:
            parser.error("offline preparation needs only a new --output path")
        target = ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as stream:
            json.dump(packet, stream, indent=2)
        print(json.dumps({"prepared": str(target), "source": packet["source"],
                          "worker": packet["worker"], "max_worker_http_requests": MAX_WORKER_HTTP,
                          "incremental_frontier_requests": 0,
                          "control_and_guidance_share_base": True}))
        return
    if not args.prepared_file or json.loads(Path(args.prepared_file).read_text()) != packet:
        parser.error("real pair requires the exact reviewed offline packet")
    out = asyncio.run(_run_real(args, packet))
    print(f"saved {out}")


if __name__ == "__main__":
    sys.exit(main())
