"""Direct client for Jev (TypeSafe System One API).

Every question in one request sees the same state, so each evidence arm is a
separate call. The body is serialized once; the byte budget is checked on the
exact bytes that are sent. Each HTTP attempt gets its own ledger row, and a
response is used only after it passes validation.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable

import httpx

from system1 import config  # noqa: F401  (loads .env)
from system1.eval.ledger import CostLedger, LedgerRow, usd_for

API_URL = "https://api.typesafe.ai/v1/systemone"
DEFAULT_MODEL = "jev-latest"
# The earlier 28,000-byte budget came from a "~32,000 bytes long-context mode"
# note that no source confirms; third-party sources give 32K *tokens* for the
# state. Measured on 2026-10-16 (jev-1.13.0): requests up to 55,776 bytes
# (14,320 input tokens) were valid with unchanged latency. At the 8K thinking
# cap the largest of 621 dev trace requests was 41,855 bytes, so 56,000 keeps
# every 8K trace whole and stays within the size tested live.
BYTE_BUDGET = 56_000
RETRY_STATUS = {429, 500, 502, 503, 529}
MAX_BACKOFF_S = 60.0
PROB_SUM_TOLERANCE = 0.02
SUPPORTED_TYPES = {"noul", "choice", "score"}
_NO_JSON = object()


class ByteBudgetExceeded(ValueError):
    pass


class JevProtocolError(RuntimeError):
    """The API answered, but the response is not a valid answer to the request."""


class JevRequestError(RuntimeError):
    """The call failed after retries (HTTP error or transport error)."""


@dataclass
class JevResult:
    answers: dict[str, Any]
    question_types: dict[str, str]
    model_returned: str
    input_tokens: int
    output_tokens: int
    latency_ms: float  # whole logical call, including retries and backoff
    request_bytes: int
    request_sha256: str  # hash of the exact bytes sent
    call_id: str
    http_attempts: int
    raw: dict

    def probability(self, qid: str, option: str | None = None) -> float:
        """P(true) for a noul question, or P(option) for a choice/score question.

        Dispatch is on the type of the question that was sent, never on which
        fields happen to be present in the answer.
        """
        answer, qtype = self.answers[qid], self.question_types[qid]
        if qtype == "noul":
            return float(answer["noul"])
        if option is None:
            raise ValueError(f"question {qid!r} is {qtype}; it needs an option name")
        return float(answer["probabilities"][option])

    def score(self, qid: str) -> float:
        """The probability-weighted level of a score question (0 .. levels - 1)."""
        if self.question_types[qid] != "score":
            raise ValueError(f"question {qid!r} is not a score question")
        return float(self.answers[qid]["score"])


def encode_body(body: dict) -> bytes:
    """Compact UTF-8 JSON; NaN and Infinity are rejected before anything is sent."""
    return json.dumps(body, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")


def request_body(model: str, state: Any, questions: dict) -> bytes:
    """The exact bytes of a Jev request. The budget check, the hash and the send all use this."""
    return encode_body({"model": model, "state": state, "questions": questions})


def _is_count(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def _is_num(x: Any, lo: float, hi: float) -> bool:
    # Bounds first: math.isfinite() overflows on very large JSON integers.
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not lo <= x <= hi:
        return False
    return isinstance(x, int) or math.isfinite(x)


def _is_prob(x: Any) -> bool:
    return _is_num(x, 0.0, 1.0)


def check_questions(questions: dict) -> None:
    """Reject question types and score rubrics that the validator cannot check."""
    for qid, q in questions.items():
        qtype = q.get("type") if isinstance(q, dict) else None
        if qtype not in SUPPORTED_TYPES:
            raise ValueError(f"{qid}: unsupported question type {qtype!r}")
        if qtype == "choice" and not (isinstance(q.get("criteria"), dict) and q["criteria"]):
            raise ValueError(f"{qid}: choice criteria must be a non-empty map")
        if qtype == "score" and not (isinstance(q.get("criteria"), list) and 2 <= len(q["criteria"]) <= 10):
            raise ValueError(f"{qid}: score criteria must be a list of 2-10 levels")


def parse_usage(data: Any) -> tuple[int | None, int | None]:
    """Token usage if present and well formed; (None, None) otherwise."""
    usage = data.get("usage") if isinstance(data, dict) else None
    if not isinstance(usage, dict):
        return None, None
    i, o = usage.get("input_tokens"), usage.get("output_tokens")
    return (i if _is_count(i) else None), (o if _is_count(o) else None)


def validate_response(data: Any, questions: dict) -> tuple[dict, str, int, int]:
    """Check a response against the questions that were sent. Raises JevProtocolError."""
    if not isinstance(data, dict):
        raise JevProtocolError("body is not an object")
    model = data.get("model")
    if not isinstance(model, str) or not model:
        raise JevProtocolError("missing model version")
    in_tok, out_tok = parse_usage(data)
    if in_tok is None or out_tok is None:
        raise JevProtocolError("missing or invalid usage")
    answers = data.get("answers")
    if not isinstance(answers, dict) or set(answers) != set(questions):
        raise JevProtocolError("answer ids do not match question ids")

    for qid, q in questions.items():
        a, qtype = answers[qid], q["type"]
        if not isinstance(a, dict):
            raise JevProtocolError(f"{qid}: answer is not an object")
        if a.get("type") != qtype:
            raise JevProtocolError(f"{qid}: answer type {a.get('type')!r} != {qtype!r}")
        if qtype == "noul":
            if not _is_prob(a.get("noul")):
                raise JevProtocolError(f"{qid}: noul is not a probability")
            continue

        probs = a.get("probabilities")
        if not isinstance(probs, dict) or not probs or not all(_is_prob(p) for p in probs.values()):
            raise JevProtocolError(f"{qid}: invalid probabilities")
        total = sum(probs.values())
        if abs(total - 1.0) > PROB_SUM_TOLERANCE:
            raise JevProtocolError(f"{qid}: probabilities sum to {total:.3f}")
        if not _is_prob(a.get("confidence")):
            raise JevProtocolError(f"{qid}: confidence is not a probability")

        if qtype == "choice":
            if set(probs) != set(q["criteria"]):
                raise JevProtocolError(f"{qid}: options do not match the criteria")
            if a.get("choice") not in probs:
                raise JevProtocolError(f"{qid}: choice is not one of the options")
        else:  # score
            levels = [str(i) for i in range(len(q["criteria"]))]
            if set(probs) != set(levels):
                raise JevProtocolError(f"{qid}: score levels do not match the criteria")
            legend = a.get("legend")
            if not isinstance(legend, dict) or set(legend) != set(levels):
                raise JevProtocolError(f"{qid}: legend does not match the levels")
            for i, desc in enumerate(q["criteria"]):
                if isinstance(desc, str) and legend[str(i)] != desc:
                    raise JevProtocolError(f"{qid}: legend level {i} is not the submitted description")
            top = len(levels) - 1
            if not _is_num(a.get("score"), 0.0, float(top)):
                raise JevProtocolError(f"{qid}: score is outside 0..{top}")
            expected = sum(int(k) * p for k, p in probs.items())
            # Rounded probabilities move the weighted level by up to ~0.01 per level.
            if abs(a["score"] - expected) > PROB_SUM_TOLERANCE * top + 0.01:
                raise JevProtocolError(f"{qid}: score {a['score']} != weighted levels {expected:.3f}")
    return answers, model, in_tok, out_tok


def _retry_after_s(resp: httpx.Response | None) -> float | None:
    value = resp.headers.get("retry-after") if resp is not None else None
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = parsedate_to_datetime(value)
        return max(0.0, (when - datetime.now(timezone.utc)).total_seconds())
    except (TypeError, ValueError):
        return None


class JevClient:
    def __init__(
        self,
        api_key: str | None = None,
        model: str = DEFAULT_MODEL,
        ledger: CostLedger | None = None,
        prices: dict | None = None,
        byte_budget: int | None = BYTE_BUDGET,
        timeout: float = 60.0,
        max_retries: int = 5,
        transport: httpx.BaseTransport | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ):
        key = api_key or os.environ.get("TYPESAFE_API_KEY")
        if not key:
            raise RuntimeError("TYPESAFE_API_KEY is not set; see .env.example")
        if max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        self.model = model
        self.ledger = ledger
        self.prices = prices
        self.byte_budget = byte_budget
        self.max_retries = max_retries
        self._sleep = sleep
        self._http = httpx.Client(
            timeout=timeout,
            transport=transport,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> JevClient:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def ask(
        self,
        state: Any,
        questions: dict,
        *,
        task_id: str | None = None,
        attempt: int | None = None,
        step: int | None = None,
        arm: str | None = None,
    ) -> JevResult:
        check_questions(questions)
        payload = request_body(self.model, state, questions)
        n_bytes = len(payload)
        if self.byte_budget is not None and n_bytes > self.byte_budget:
            raise ByteBudgetExceeded(f"request is {n_bytes} bytes; budget is {self.byte_budget}")

        call_id = uuid.uuid4().hex
        t_call = time.perf_counter()
        for i in range(self.max_retries + 1):
            t0 = time.perf_counter()
            resp: httpx.Response | None = None
            data: Any = None
            status = "ok"
            try:
                resp = self._http.post(API_URL, content=payload)
            except httpx.TransportError as e:
                status = f"transport:{type(e).__name__}"
            if resp is not None:
                # Parse every body, so an error response still gives its usage.
                try:
                    data = resp.json()
                except ValueError:
                    data = _NO_JSON
                if not 200 <= resp.status_code < 300:
                    status = f"http:{resp.status_code}"
                elif data is _NO_JSON:
                    status = "protocol:invalid_json"

            validated = None
            if status == "ok":
                try:
                    validated = validate_response(data, questions)
                except JevProtocolError as e:
                    status = f"protocol:{e}"
                except (TypeError, ValueError, OverflowError, KeyError) as e:
                    status = f"protocol:{type(e).__name__}"

            in_tok, out_tok = parse_usage(data)  # as reported, also on error responses
            model_returned = data.get("model") if isinstance(data, dict) else None
            self._log(task_id, attempt, step, arm, call_id, i, status, in_tok, out_tok,
                      (time.perf_counter() - t0) * 1000, n_bytes, model_returned)

            if validated is not None:
                answers, model_ret, in_tok, out_tok = validated
                return JevResult(
                    answers=answers,
                    question_types={qid: q["type"] for qid, q in questions.items()},
                    model_returned=model_ret,
                    input_tokens=in_tok,
                    output_tokens=out_tok,
                    latency_ms=(time.perf_counter() - t_call) * 1000,
                    request_bytes=n_bytes,
                    request_sha256=hashlib.sha256(payload).hexdigest(),
                    call_id=call_id,
                    http_attempts=i + 1,
                    raw=data,
                )

            # A malformed answer may already be billed, so it is not retried.
            if status.startswith("protocol:"):
                raise JevProtocolError(f"call {call_id}: {status}")
            retryable = status.startswith("transport:") or (
                resp is not None and resp.status_code in RETRY_STATUS
            )
            if not retryable or i == self.max_retries:
                raise JevRequestError(f"call {call_id}: {status} after {i + 1} attempt(s)")
            wait = _retry_after_s(resp)
            if wait is not None and wait > MAX_BACKOFF_S:
                # Do not retry earlier than the server asked; stop and report instead.
                raise JevRequestError(
                    f"call {call_id}: {status}; server asked to wait {wait:.0f} s (limit {MAX_BACKOFF_S:.0f} s)"
                )
            if wait is None:
                wait = min(MAX_BACKOFF_S, (2.0**i) * (0.5 + random.random() / 2))
            self._sleep(wait)
        raise AssertionError("unreachable")

    def _log(self, task_id, attempt, step, arm, call_id, http_attempt, status,
             in_tok, out_tok, latency_ms, n_bytes, model_returned) -> None:
        if self.ledger is None:
            return
        self.ledger.append(
            LedgerRow(
                component="router",
                model=self.model,
                provider="typesafe",
                task_id=task_id,
                attempt=attempt,
                step=step,
                arm=arm,
                call_id=call_id,
                http_attempt=http_attempt,
                status=status,
                input_tokens=in_tok,
                output_tokens=out_tok,
                usd_computed=usd_for(self.prices, self.model, in_tok, out_tok),
                latency_ms=latency_ms,
                request_bytes=n_bytes,
                model_returned=model_returned if isinstance(model_returned, str) else None,
            )
        )
