"""Evidence states for Jev, one per arm.

Every arm starts from the same canonical base state (task, current code,
bounded visible test output, loop telemetry). An arm adds blocks:

    base+history          the previous code and its test output
    base+history+trace    the same, plus the current round's thinking

The thinking gets only the bytes that remain under the budget after the base
and history are in place. It keeps its start and its end, and the omitted
middle is marked. Base and history are never trimmed to make room for it.

Fallback: when the base and history alone do not fit, the task and the code
(current and previous) are cut to fixed sizes, the same way for every arm of
the checkpoint, and the evidence is marked base_trimmed. build_arms() makes
that decision once per checkpoint, so the arms always share one base.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from system1.routers.jev import request_body

# Bump when any rule below changes; it is stored with every scoring record.
EVIDENCE_VERSION = "evidence-v2"

ARMS: dict[str, frozenset[str]] = {
    "base+history": frozenset({"history"}),
    "base+history+trace": frozenset({"history", "trace"}),
}

# Fixed bounds in characters (the byte budget still applies to the whole request).
TEST_OUTPUT_MAX_CHARS = 3_000  # every test output, always
TASK_MAX_CHARS_TRIMMED = 4_000  # fallback only
CODE_MAX_CHARS_TRIMMED = 6_000  # fallback only, current and previous code
# Share of the retained thinking taken from its start; the rest is its end.
TRACE_HEAD_SHARE = 0.25


class EvidenceTooLarge(ValueError):
    """The base state (and history) does not fit the byte budget, even after the fallback."""

    def __init__(self, message: str, unfitted_bytes: int | None = None):
        super().__init__(message)
        self.unfitted_bytes = unfitted_bytes


@dataclass(frozen=True)
class Checkpoint:
    task_id: str
    benchmark: str  # humaneval+ | mbpp+
    attempt: int  # generation attempt (0-4)
    round: int  # 1-based write -> test round
    task_prompt: str
    code: str
    visible_test_output: str
    visible_pass: bool
    thinking: str
    telemetry: dict[str, Any] = field(default_factory=dict)
    prev_code: str | None = None
    prev_test_output: str | None = None

    def __post_init__(self) -> None:
        # Inconsistent history wiring would silently turn history questions
        # into "not applicable", so it is an error here.
        if self.round < 1:
            raise ValueError(f"{self.task_id}: round must be >= 1, got {self.round}")
        if (self.round == 1) != (self.prev_code is None):
            raise ValueError(f"{self.task_id}: round {self.round} but prev_code is "
                             f"{'missing' if self.prev_code is None else 'present'}")
        if (self.prev_code is None) != (self.prev_test_output is None):
            raise ValueError(f"{self.task_id}: prev_code and prev_test_output must both be present or both absent")

    @property
    def checkpoint_id(self) -> str:
        return f"{self.task_id}/a{self.attempt}/r{self.round}"

    @property
    def first_round(self) -> bool:
        return self.round == 1

    @property
    def has_trace(self) -> bool:
        return bool(self.thinking.strip())


@dataclass
class Evidence:
    state: dict[str, Any]
    payload_bytes: int
    unfitted_bytes: int  # untrimmed base and history, plus the whole thinking if the arm has it
    base_trimmed: bool = False
    telemetry_sanitized: list[str] = field(default_factory=list)
    trace_original_chars: int | None = None
    trace_retained_chars: int | None = None

    @property
    def trace_truncated(self) -> bool | None:
        if self.trace_original_chars is None:
            return None
        return self.trace_retained_chars < self.trace_original_chars


def head_tail(text: str, keep_chars: int, head_share: float = 0.5) -> str:
    """Keep keep_chars characters from the start and end of text; mark the gap."""
    if keep_chars >= len(text):
        return text
    head = int(keep_chars * head_share)
    tail = keep_chars - head
    omitted = len(text) - keep_chars
    return text[:head] + f"\n[... {omitted} characters omitted by the harness ...]\n" + (text[-tail:] if tail else "")


def sanitize(value: Any, path: str = "", changed: list[str] | None = None) -> Any:
    """Replace NaN and Infinity (not valid JSON) with None, and record where."""
    if changed is None:
        changed = []
    if isinstance(value, float) and not math.isfinite(value):
        changed.append(path or "<root>")
        return None
    if isinstance(value, dict):
        return {k: sanitize(v, f"{path}.{k}" if path else str(k), changed) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [sanitize(v, f"{path}[{i}]", changed) for i, v in enumerate(value)]
    return value


def base_state(cp: Checkpoint, blocks: frozenset[str], *, trimmed: bool = False) -> tuple[dict[str, Any], list[str]]:
    sanitized: list[str] = []
    telemetry = sanitize(cp.telemetry, "", sanitized)
    task = head_tail(cp.task_prompt, TASK_MAX_CHARS_TRIMMED) if trimmed else cp.task_prompt
    code = head_tail(cp.code, CODE_MAX_CHARS_TRIMMED) if trimmed else cp.code
    state: dict[str, Any] = {
        "task": task,
        "round": cp.round,
        "current_code": code,
        "visible_test_output": head_tail(cp.visible_test_output, TEST_OUTPUT_MAX_CHARS),
        "visible_tests_passed": cp.visible_pass,
        "loop_telemetry": telemetry,
    }
    if "history" in blocks and not cp.first_round:
        prev = head_tail(cp.prev_code, CODE_MAX_CHARS_TRIMMED) if trimmed else cp.prev_code
        state["previous_code"] = prev
        state["previous_test_output"] = head_tail(cp.prev_test_output, TEST_OUTPUT_MAX_CHARS)
    return state, sanitized


def build_evidence(cp: Checkpoint, arm: str, questions: dict, *, model: str, budget: int | None,
                   trimmed: bool = False) -> Evidence:
    """The state for one arm, sized against the exact request payload."""
    blocks = ARMS[arm]
    state, sanitized = base_state(cp, blocks, trimmed=trimmed)
    with_trace = "trace" in blocks and cp.has_trace

    def size(s: dict) -> int:
        return len(request_body(model, s, questions))

    untrimmed, _ = base_state(cp, blocks, trimmed=False)
    unfitted = size({**untrimmed, "thinking": cp.thinking} if with_trace else untrimmed)

    if not with_trace:
        n = size(state)
        if budget is not None and n > budget:
            raise EvidenceTooLarge(f"{cp.checkpoint_id} {arm}: {n} bytes; budget {budget}", unfitted)
        ev = Evidence(state=state, payload_bytes=n, unfitted_bytes=unfitted, base_trimmed=trimmed,
                      telemetry_sanitized=sanitized)
        if "trace" in blocks:  # the arm has a trace block, but the thinking is empty
            ev.trace_original_chars, ev.trace_retained_chars = len(cp.thinking), 0
        return ev

    trace = cp.thinking

    def fitted(keep: int) -> dict:
        return {**state, "thinking": head_tail(trace, keep, TRACE_HEAD_SHARE)}

    # The smallest trace block is the gap marker alone (keep = 0).
    if budget is not None and size(fitted(0)) > budget:
        raise EvidenceTooLarge(f"{cp.checkpoint_id} {arm}: base and history leave no room for the thinking "
                               f"within {budget} bytes", unfitted)

    keep = len(trace)
    if budget is not None and size(fitted(keep)) > budget:
        # Largest number of kept characters that still fits; the size does not
        # decrease as keep grows below len(trace) (checked by a brute-force test).
        lo, hi = 0, len(trace) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if size(fitted(mid)) <= budget:
                lo = mid
            else:
                hi = mid - 1
        keep = lo
    final = fitted(keep)
    return Evidence(state=final, payload_bytes=size(final), unfitted_bytes=unfitted, base_trimmed=trimmed,
                    telemetry_sanitized=sanitized, trace_original_chars=len(trace),
                    trace_retained_chars=min(keep, len(trace)))


def build_arms(cp: Checkpoint, arm_questions: dict[str, dict], *, model: str, budget: int | None) -> dict[str, Evidence]:
    """Evidence for several arms with one shared base: untrimmed if every arm fits,
    else trimmed for every arm. Raises EvidenceTooLarge if even that does not fit."""
    for trimmed in (False, True):
        try:
            return {arm: build_evidence(cp, arm, qs, model=model, budget=budget, trimmed=trimmed)
                    for arm, qs in arm_questions.items()}
        except EvidenceTooLarge as e:
            last = e
    raise last
