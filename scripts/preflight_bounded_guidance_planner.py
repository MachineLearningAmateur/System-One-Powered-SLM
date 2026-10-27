"""Prepare or run one planner-only preflight from the saved v1a checkpoint.

Offline preparation (no network, GPU, Qwen, or API request):
    uv run python scripts/preflight_bounded_guidance_planner.py --prepare \
      --output results/bg-v1b-planner-preflight-request-approved-20261027.json

A billed call requires separate operator approval, a clean commit, a new run ID,
--real, --operator-approved, --max-requests 1, and --limit-usd <= 0.03.
This script never launches Qwen, Azure, or hidden grading. It sends one planner
request with no retry and preserves the raw credential-free exchange and cost.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from system1.bounded_guidance import InvalidPlan, PLAN_MAX_CHARS, PLAN_MAX_WORDS, validate_plan
from system1.config import RESULTS, ROOT, load_prices
from system1.eval.ledger import CostLedger, read_jsonl
from system1.frontier.client import MODEL as FRONTIER_MODEL, PROVIDER, REASONING

try:
    from scripts.run_bounded_guidance import BoundedAdviser
except ModuleNotFoundError:  # direct script execution
    from run_bounded_guidance import BoundedAdviser

SOURCE_RUN_ID = "bg-v1a-integration-dev-20261027"
SOURCE_TASK_ID = "HumanEval/59"
SOURCE_CALL_ID = "ca2743bdcc1c4ade89b8ca65dc464992"
SOURCE_REQUEST_SHA256 = "821d1bdb3f7360f80cd71ad33feb09f9a686fbd280e641022080accf9fb63e78"
ANCHOR = "Task and visible examples:\n"
PREFLIGHT_MAX_USD = 0.03

# Drafting target only. The frozen delivery validator remains 120 words / 900
# Unicode characters and rejects any backticks used as a code fence.
PREFLIGHT_INSTRUCTIONS = (
    "Give the Qwen coding assistant one short repair plan for the task below. "
    "Use at most 100 whitespace-separated words and 900 characters after trimming "
    "leading and trailing whitespace. Use plain text only: no backticks, code "
    "fences, numbered lists, or advice about final-answer formatting. "
    "State a concrete defect and repair only if one is evident. If no clear "
    "defect is evident, say so and give only useful checks; do not invent a "
    "defect or change. Do not write code, a patch, hidden tests, or a final answer.\n\n"
)


def _one(path: Path) -> dict:
    rows, damaged = read_jsonl(path)
    if damaged or len(rows) != 1:
        raise ValueError(f"expected exactly one intact record in {path}")
    return rows[0]


def source_request() -> dict:
    """Use the saved draft and visible result; read no hidden grading files."""
    run_dir = RESULTS / "runs" / SOURCE_RUN_ID
    pair = _one(run_dir / "pairs.jsonl")
    plan = _one(run_dir / "plans.jsonl")
    exchange = _one(run_dir / "frontier_exchanges.jsonl")
    if pair["task_id"] != SOURCE_TASK_ID or len(pair["rows"]) != 3:
        raise ValueError("saved pair does not match the pinned checkpoint")
    first = next((r for r in pair["rows"] if r["arm"] == "shared" and r["round"] == 1), None)
    if first is None or hashlib.sha256((first["code"] or "").encode()).hexdigest() != first["code_sha256"]:
        raise ValueError("shared draft is missing or its code hash changed")
    if not (plan["call_id"] == pair["plan_call_id"] == exchange["call_id"] == SOURCE_CALL_ID):
        raise ValueError("saved planner call join mismatch")
    request = exchange["request_body"]
    digest = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()
    if digest != SOURCE_REQUEST_SHA256 or request["messages"] != plan["request_messages"]:
        raise ValueError("saved frontier request changed")
    if request["model"] != FRONTIER_MODEL or request["provider"] != PROVIDER or request["reasoning"] != REASONING:
        raise ValueError("saved model or provider route changed")
    if len(request["messages"]) != 1 or request["messages"][0]["role"] != "user":
        raise ValueError("unexpected source message structure")
    old_text = request["messages"][0]["content"]
    if first["code"] not in old_text or first["visible_report"] not in old_text:
        raise ValueError("saved request does not contain the shared checkpoint")
    if ANCHOR not in old_text or "120 whitespace-separated words and 900 characters" not in old_text.split(ANCHOR, 1)[0]:
        raise ValueError("saved planner instructions changed")
    return request


def replace_instructions(source: dict) -> dict:
    request = copy.deepcopy(source)
    original = request["messages"][0]["content"]
    _, marker, remainder = original.partition(ANCHOR)
    if not marker:
        raise ValueError("source request has no task anchor")
    request["messages"][0]["content"] = PREFLIGHT_INSTRUCTIONS + marker + remainder
    return request


def preflight_request() -> dict:
    return replace_instructions(source_request())


def reservation_usd(request: dict) -> float:
    from system1.bounded_guidance import PLAN_MAX_OUTPUT_TOKENS
    prices = load_prices()["models"][FRONTIER_MODEL]
    byte_count = sum(len(m["content"].encode("utf-8")) for m in request["messages"]) + 500
    return (byte_count * prices["usd_per_m_input"]
            + PLAN_MAX_OUTPUT_TOKENS * prices["usd_per_m_output"]) / 1_000_000


def assess_reply(reply, ledger_row: dict) -> dict:
    """Apply every unchanged delivery rule; keep the returned text untouched."""
    text = reply.content.strip() if isinstance(reply.content, str) else ""
    rules = {"nonempty_visible_text": bool(text),
             "at_most_120_words": len(text.split()) <= PLAN_MAX_WORDS,
             "at_most_900_characters": len(text) <= PLAN_MAX_CHARS,
             "no_code_fence": "```" not in text,
             "finish_reason_stop": reply.finish_reason == "stop"}
    validation_reasons = [name for name, passed in rules.items() if not passed]
    validator_reason = None
    try:
        validate_plan(reply.content)
    except InvalidPlan as exc:
        validator_reason = str(exc)
    content_rules = ("nonempty_visible_text", "at_most_120_words", "at_most_900_characters", "no_code_fence")
    if (validator_reason is None) != all(rules[name] for name in content_rules):
        raise RuntimeError("diagnostic rules disagree with the unchanged plan validator")
    return {"delivery_status": "delivered" if not validation_reasons else "invalid",
            "validation_rules": rules, "validation_reasons": validation_reasons,
            "validator_reason": validator_reason, "visible_content": reply.content,
            "visible_words": len(text.split()), "visible_chars": len(text),
            "finish_reason": reply.finish_reason, "call_id": reply.call_id,
            "model_returned": reply.model_returned, "provider_returned": reply.provider_returned,
            "input_tokens": reply.input_tokens, "output_tokens": reply.output_tokens,
            "reasoning_tokens": ledger_row.get("reasoning_tokens"),
            "usd_reported": reply.usd_reported, "usd_computed": reply.usd_computed}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--real", action="store_true")
    parser.add_argument("--output", help="new ignored JSON file for offline preparation")
    parser.add_argument("--run-id", help="fresh ignored run ID for a separately approved call")
    parser.add_argument("--operator-approved", action="store_true")
    parser.add_argument("--max-requests", type=int)
    parser.add_argument("--limit-usd", type=float)
    args = parser.parse_args()
    request = preflight_request()
    reserve = reservation_usd(request)
    if args.prepare:
        if not args.output or args.run_id or args.operator_approved:
            parser.error("--prepare needs only a new --output path")
        target = ROOT / args.output
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as stream:
            json.dump({"source_run_id": SOURCE_RUN_ID, "source_call_id": SOURCE_CALL_ID,
                       "source_request_sha256": SOURCE_REQUEST_SHA256,
                       "request_body": request, "reserved_usd_at_current_pinned_prices": reserve,
                       "delivery_max_words": PLAN_MAX_WORDS, "delivery_max_chars": PLAN_MAX_CHARS}, stream, indent=2)
        print(json.dumps({"prepared": str(target), "planned_requests": 1,
                          "reserved_usd": round(reserve, 6), "paid_calls": 0}))
        return
    if (not args.operator_approved or not args.run_id or args.max_requests != 1
            or args.limit_usd is None or not 0 < args.limit_usd <= PREFLIGHT_MAX_USD):
        parser.error("one real call needs separate approval, --max-requests 1, and 0 < --limit-usd <= 0.03")
    if reserve > args.limit_usd:
        parser.error("the pinned request reservation exceeds the approved frontier limit")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip():
        parser.error("real preflight requires a clean committed tree")
    out = RESULTS / "runs" / args.run_id
    out.mkdir(parents=True, exist_ok=False)
    (out / "preflight_request.json").write_text(json.dumps(request, indent=2))
    (out / "preflight_meta.json").write_text(json.dumps({
        "source_run_id": SOURCE_RUN_ID, "source_call_id": SOURCE_CALL_ID,
        "source_request_sha256": SOURCE_REQUEST_SHA256,
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "max_requests": 1, "limit_usd": args.limit_usd, "reserved_usd": reserve,
        "started_utc": datetime.now(timezone.utc).isoformat()}, indent=2))
    ledger = CostLedger(out / "ledger.jsonl")
    adviser = BoundedAdviser(ledger, args.limit_usd, CostLedger(out / "frontier_exchanges.jsonl"))
    try:
        reply = adviser.ask(request["messages"], task_id=SOURCE_TASK_ID, sample=0)
    finally:
        adviser.close()
    ledger_rows, damaged = ledger.read()
    if damaged or len(ledger_rows) != 1 or ledger_rows[0]["call_id"] != reply.call_id:
        raise RuntimeError("planner cost ledger does not match the one preflight request")
    result = assess_reply(reply, ledger_rows[0])
    (out / "preflight_result.json").write_text(json.dumps(result, indent=2))
    print(json.dumps({k: v for k, v in result.items() if k != "visible_content"}))


if __name__ == "__main__":
    sys.exit(main())
