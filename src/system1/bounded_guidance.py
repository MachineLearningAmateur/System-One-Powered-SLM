"""One shared Qwen draft, then isolated control and bounded-advice continuations.

This module has no network or grading side effects. The driver injects model and
visible-test clients. Hidden labels are deliberately absent from every prompt.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import uuid
from dataclasses import dataclass
from typing import Any, Callable, Protocol

from system1.loop.generate import SEED_TAG
from system1.loop.runner import VISIBLE_TIMEOUT_S
from system1.loop.tasks import TaskSpec, first_round_messages, format_test_report

PLAN_MAX_WORDS = 120
PLAN_MAX_CHARS = 900
PLAN_MAX_OUTPUT_TOKENS = 512  # total completion, including provider reasoning
ARMS = ("control", "guidance")
DEV30_PLANNER_INSTRUCTIONS = (
    "Give the Qwen coding assistant one short repair plan for the task below. "
    "Use at most 100 whitespace-separated words and 900 characters after trimming "
    "leading and trailing whitespace. Use plain text only: no backticks, code "
    "fences, numbered lists, or advice about final-answer formatting. "
    "State a concrete defect and repair only if one is evident. If no clear "
    "defect is evident, say so and give only useful checks; do not invent a "
    "defect or change. Do not write code, a patch, hidden tests, or a final answer.\n\n"
)


class Worker(Protocol):
    async def generate(self, messages: list[dict], task_prompt: str, entry_point: str | None,
                       *seed_parts: Any, on_call=None) -> Any: ...


class Visible(Protocol):
    def run(self, code: str, tests: list[dict], timeout: float) -> dict: ...


class Adviser(Protocol):
    def ask(self, messages: list[dict], *, task_id: str, sample: int) -> Any: ...


class InvalidPlan(ValueError):
    pass


def _plan_messages_with_header(task: TaskSpec, code: str | None, report: str,
                               header: str) -> list[dict]:
    shown = first_round_messages(task)[0]["content"]
    return [{"role": "user", "content": (
        header +
        f"Task and visible examples:\n{shown}\n"
        f"First draft:\n```python\n{(code or '').rstrip()}\n```\n"
        f"Visible-test result:\n{report.rstrip()}\n"
    )}]


def plan_messages(task: TaskSpec, code: str | None, report: str) -> list[dict]:
    """The original planner prompt, retained for earlier protocol versions."""
    header = (
        "Give the Qwen coding assistant one short repair plan for the task below. "
        f"Use at most {PLAN_MAX_WORDS} whitespace-separated words and {PLAN_MAX_CHARS} characters "
        "after trimming leading and trailing whitespace. "
        "State the likely defect and concrete steps to fix it. "
        "Do not write code, a patch, hidden tests, or a final answer. "
        "If the visible result gives insufficient evidence, say what to check.\n\n"
    )
    return _plan_messages_with_header(task, code, report, header)


def dev30_plan_messages(task: TaskSpec, code: str | None, report: str) -> list[dict]:
    """The successful preflight's instruction header with fresh task evidence."""
    return _plan_messages_with_header(task, code, report, DEV30_PLANNER_INSTRUCTIONS)


def validate_plan(reply: str | None) -> str:
    if not isinstance(reply, str) or not reply.strip():
        raise InvalidPlan("empty adviser response")
    plan = reply.strip()
    if len(plan) > PLAN_MAX_CHARS or len(plan.split()) > PLAN_MAX_WORDS:
        raise InvalidPlan("adviser response exceeded the fixed bound")
    if "```" in plan:
        raise InvalidPlan("adviser response contains a code fence")
    return plan


def continuation_messages(task: TaskSpec, code: str, report: str, plan: str | None = None) -> list[dict]:
    """Same continuation task in each arm; only guidance receives a plan."""
    base = first_round_messages(task)[0]["content"]
    base += (f"\nYour first draft:\n```python\n{code.rstrip()}\n```\n"
             f"\nVisible-test result:\n{report.rstrip()}\n"
             "\nReview the draft against the full task and visible result. "
             "Correct any defect you find; keep correct behavior. "
             "Reply with the complete final code in one ```python code block.\n")
    if plan is not None:
        base += "\nAdvice from a separate assistant (check it; it may be wrong):\n" + plan + "\n"
    return [{"role": "user", "content": base}]


@dataclass
class PairResult:
    pair_id: str
    rows: list[dict]
    plan: dict | None
    final: dict[str, dict]


async def run_pair(task: TaskSpec, attempt: int, worker: Worker, visible: Visible,
                   adviser: Adviser, *, on_worker_call=None, on_advice=None,
                   on_checkpoint=None,
                   planner_messages: Callable[[TaskSpec, str | None, str], list[dict]] = plan_messages,
                   require_equal_continuation_caps: bool = False) -> PairResult:
    """Run one paired unit: one shared draft and one continuation per arm.

    Invalid advice is a charged, recorded treatment delivery failure. Provider,
    configuration, accounting, and integrity errors still stop the pair.
    """
    pair_id = uuid.uuid4().hex
    rows: list[dict] = []

    async def checkpoint(arm: str, rnd: int, messages: list[dict]) -> dict:
        calls: list[dict] = []

        def hook(call: dict) -> None:
            item = {"pair_id": pair_id, "task_id": task.task_id, "attempt": attempt,
                    "arm": arm, "round": rnd, **call}
            calls.append(item)
            if on_worker_call is not None:
                on_worker_call(item)

        # The same round seed is used in both branches. Different prompts can
        # still produce different stochastic streams; pairing is by task/draft.
        g = await worker.generate(messages, task.prompt, task.entry_point,
                                  SEED_TAG, task.task_id, attempt, rnd, on_call=hook)
        if g.code is None:
            execution = {"status": "no_code", "stage": "extract", "error_type": "NoCode",
                         "message": "the answer contains no usable Python code block"}
            results = [{"status": "not_run", "error_type": None, "message": None} for _ in task.visible_tests]
            runner = None
            visible_elapsed_s = None
        else:
            v = await asyncio.to_thread(visible.run, g.code, list(task.visible_tests), VISIBLE_TIMEOUT_S)
            execution, results, runner = v["execution"], v["results"], v.get("runner")
            visible_elapsed_s = v.get("elapsed_s")
        passed = bool(g.code is not None and execution.get("status") == "ok"
                      and all(r["status"] == "pass" for r in results))
        report = format_test_report(task.visible_tests, results, execution)
        row = {"pair_id": pair_id, "task_id": task.task_id, "benchmark": task.benchmark,
               "attempt": attempt, "arm": arm, "round": rnd,
               "checkpoint_id": f"{task.task_id}/a{attempt}/{arm}/r{rnd}",
               "prompt_messages": messages,
               "prompt_sha256": hashlib.sha256(json.dumps(messages, sort_keys=True).encode()).hexdigest(),
               "code_sha256": hashlib.sha256((g.code or "").encode()).hexdigest(),
               "code": g.code, "answer": g.answer, "thinking": g.thinking,
               "visible_execution": execution, "visible_results": results, "visible_report": report,
               "visible_pass": passed, "visible_runner": runner,
               "visible_elapsed_s": visible_elapsed_s,
               "generation": {"prompt_tokens": g.prompt_tokens, "thinking_tokens": g.thinking_tokens,
                              "answer_tokens": g.answer_tokens, "latency_ms": g.latency_ms,
                              "cap_hit": g.cap_hit, "effective_cap": g.effective_cap},
               "worker_calls": calls}
        rows.append(row)
        if on_checkpoint is not None:
            on_checkpoint(row)
        return row

    first = await checkpoint("shared", 1, first_round_messages(task))
    req = planner_messages(task, first["code"], first["visible_report"])
    reply = adviser.ask(req, task_id=task.task_id, sample=attempt)
    if reply.status != "ok":
        raise RuntimeError(f"adviser returned {reply.status}")
    finish_reason = getattr(reply, "finish_reason", None)
    if finish_reason not in ("stop", "length", "content_filter"):
        raise RuntimeError(f"unresolved adviser finish reason: {finish_reason}")
    visible_text = reply.content.strip() if isinstance(reply.content, str) else ""
    char_count, word_count = len(visible_text), len(visible_text.split())
    plan = None
    invalid_reason = None
    if finish_reason == "length":
        invalid_reason = "truncated_completion"
    elif finish_reason == "content_filter":
        invalid_reason = "filtered_completion"
    else:
        try:
            plan = validate_plan(reply.content)
        except InvalidPlan as exc:
            invalid_reason = str(exc)
    plan_record = {"pair_id": pair_id, "task_id": task.task_id, "attempt": attempt,
                   "request_messages": req,
                   "request_sha256": hashlib.sha256(json.dumps(req, sort_keys=True).encode()).hexdigest(),
                   "plan": plan, "visible_content": reply.content,
                   "visible_chars": char_count, "visible_words": word_count,
                   "delivery_status": "delivered" if plan is not None else "invalid",
                   "invalid_reason": invalid_reason, "finish_reason": finish_reason,
                   "call_id": reply.call_id, "status": reply.status,
                   "model_returned": reply.model_returned,
                   "provider_returned": getattr(reply, "provider_returned", None),
                   "input_tokens": reply.input_tokens,
                   "output_tokens": reply.output_tokens, "usd_reported": reply.usd_reported,
                   "usd_computed": reply.usd_computed, "latency_ms": reply.latency_ms}
    if on_advice is not None:
        on_advice(plan_record)
    final: dict[str, dict] = {}
    continuation_by_arm = {
        arm: continuation_messages(task, first["code"] or "(no code was produced)",
                                   first["visible_report"], plan if arm == "guidance" else None)
        for arm in ARMS
    }
    if require_equal_continuation_caps:
        from system1.loop.generate import render_prompt
        caps = {}
        for arm, messages in continuation_by_arm.items():
            prompt = render_prompt(worker.tokenizer, messages)
            n_prompt = len(worker.tokenizer(prompt)["input_ids"])
            caps[arm] = min(worker.think_cap, worker.max_model_len - n_prompt - worker.code_tokens - 16)
        if caps["control"] != caps["guidance"] or min(caps.values()) <= 0:
            raise RuntimeError(f"unequal or exhausted Qwen continuation thinking caps: {caps}")
    # Balance temporal ordering without consulting any outcome or hidden label.
    order = ARMS if int(hashlib.sha256(f"{task.task_id}:{attempt}".encode()).hexdigest(), 16) % 2 == 0 else ARMS[::-1]
    for arm in order:
        messages = continuation_by_arm[arm]
        final[arm] = await checkpoint(arm, 2, messages)
    return PairResult(pair_id, rows, plan_record, final)
