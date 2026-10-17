"""Frontier helper: Claude Sonnet 5.5 through OpenRouter (docs/research-plan.md, Frontier helper).

Pinned model and provider (no fallbacks), low reasoning effort, usage
included on every call. Each HTTP attempt gets its own cost-ledger row with
the reported cost and the cost computed from the pinned prices. A spend guard
refuses a call whose worst-case cost could take the ledger total over the
approved limit; spend is read back from the ledger file, so the guard holds
across restarts.

Takeover from scratch (the main help mode): the helper gets exactly the
small model's round-1 message (the task and its visible tests) and returns
one answer. No repair, retry on content, or fallback: a reply that cannot be
used is recorded as it is (it may already be billed).
"""

from __future__ import annotations

import os
import random
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable

import httpx

from system1 import config  # noqa: F401  (loads .env)
from system1.eval.ledger import CostLedger, LedgerRow, read_jsonl, usd_for

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "anthropic/claude-sonnet-5.5-20260928"
PROVIDER = {"order": ["anthropic"], "allow_fallbacks": False}
REASONING = {"effort": "low"}
MAX_TOKENS = 8_000
RETRY_STATUS = {408, 429, 500, 502, 503, 529}
MAX_BACKOFF_S = 60.0


class SpendLimitReached(RuntimeError):
    """The next call could take the spend over the approved limit."""


class FrontierRequestError(RuntimeError):
    """The call failed after retries (HTTP or transport error)."""


@dataclass
class FrontierReply:
    content: str | None  # None when the reply has no usable text
    finish_reason: str | None
    model_returned: str | None
    provider_returned: str | None
    input_tokens: int | None
    output_tokens: int | None
    reasoning_tokens: int | None
    usd_reported: float | None
    usd_computed: float | None
    latency_ms: float
    call_id: str
    http_attempts: int
    status: str  # ok | protocol:<reason>


def _count(x: Any) -> int | None:
    return x if isinstance(x, int) and not isinstance(x, bool) and x >= 0 else None


def parse_reply(data: Any) -> dict:
    """Fields of an OpenRouter chat completion; missing parts stay None."""
    out = {"content": None, "finish_reason": None, "model_returned": None, "provider_returned": None,
           "input_tokens": None, "output_tokens": None, "reasoning_tokens": None, "usd_reported": None,
           "status": "ok"}
    if not isinstance(data, dict):
        out["status"] = "protocol:body is not an object"
        return out
    out["model_returned"] = data.get("model") if isinstance(data.get("model"), str) else None
    out["provider_returned"] = data.get("provider") if isinstance(data.get("provider"), str) else None
    usage = data.get("usage") if isinstance(data.get("usage"), dict) else {}
    out["input_tokens"], out["output_tokens"] = _count(usage.get("prompt_tokens")), _count(usage.get("completion_tokens"))
    details = usage.get("completion_tokens_details") if isinstance(usage.get("completion_tokens_details"), dict) else {}
    out["reasoning_tokens"] = _count(details.get("reasoning_tokens"))
    cost = usage.get("cost")
    out["usd_reported"] = float(cost) if isinstance(cost, (int, float)) and not isinstance(cost, bool) else None
    choices = data.get("choices")
    if not (isinstance(choices, list) and choices and isinstance(choices[0], dict)):
        out["status"] = "protocol:no choices"
        return out
    c = choices[0]
    out["finish_reason"] = c.get("finish_reason") if isinstance(c.get("finish_reason"), str) else None
    msg = c.get("message") if isinstance(c.get("message"), dict) else {}
    content = msg.get("content")
    if isinstance(content, str) and content.strip():
        out["content"] = content
    else:
        out["status"] = "protocol:empty content"
    if out["input_tokens"] is None or out["output_tokens"] is None:
        out["status"] = "protocol:missing usage" if out["status"] == "ok" else out["status"]
    return out


def ledger_spend(path, worst_case_usd: float) -> tuple[float, int]:
    """(dollars spent, rows without any cost). A row with no reported or computed cost
    counts at the worst case, so unknown cost never lowers the total."""
    rows, _ = read_jsonl(path)
    total, unknown = 0.0, 0
    for r in rows:
        if r.get("component") != "frontier":
            continue
        usd = r.get("usd_reported")
        usd = r.get("usd_computed") if usd is None else usd
        if usd is None:
            if (r.get("status") or "").startswith(("transport:", "http:")) and r.get("output_tokens") is None:
                continue  # a request that never reached the model is not billed
            unknown += 1
            usd = worst_case_usd
        total += float(usd)
    return total, unknown


class FrontierClient:
    def __init__(self, ledger: CostLedger, prices: dict, limit_usd: float, api_key: str | None = None,
                 model: str = MODEL, max_tokens: int = MAX_TOKENS, timeout: float = 300.0, max_retries: int = 4,
                 transport: httpx.BaseTransport | None = None, sleep: Callable[[float], None] = time.sleep):
        key = api_key or os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is not set; see .env.example")
        entry = (prices or {}).get("models", {}).get(model) or {}
        if entry.get("usd_per_m_input") is None or entry.get("usd_per_m_output") is None:
            raise RuntimeError(f"no pinned price for {model} in configs/prices.yaml; the spend guard needs one")
        if limit_usd <= 0:
            raise ValueError("limit_usd must be > 0")
        self.ledger, self.prices, self.limit_usd = ledger, prices, limit_usd
        self.model, self.max_tokens, self.max_retries = model, max_tokens, max_retries
        self._sleep = sleep
        self._lock = threading.Lock()
        self._inflight = 0.0  # worst-case cost of calls that have not ended
        self._p_in, self._p_out = entry["usd_per_m_input"], entry["usd_per_m_output"]
        self._http = httpx.Client(timeout=timeout, transport=transport,
                                  headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> FrontierClient:
        return self

    def __exit__(self, *exc) -> None:
        self.close()

    def worst_case_usd(self, input_tokens_estimate: int) -> float:
        return (input_tokens_estimate * self._p_in + self.max_tokens * self._p_out) / 1_000_000

    def body(self, messages: list[dict]) -> dict:
        return {"model": self.model, "messages": messages, "max_tokens": self.max_tokens, "reasoning": REASONING,
                "provider": PROVIDER, "usage": {"include": True}}

    def ask(self, messages: list[dict], *, task_id: str, sample: int) -> FrontierReply:
        # A generous input estimate: 1 token per 3 characters, plus the chat overhead.
        reserve = self.worst_case_usd(sum(len(m["content"]) for m in messages) // 3 + 50)
        with self._lock:  # concurrent calls reserve their worst case before they start
            spent, _ = ledger_spend(self.ledger.path, reserve)
            if spent + self._inflight + reserve > self.limit_usd:
                raise SpendLimitReached(f"spent ${spent:.4f} (+${self._inflight:.4f} in flight); the next call "
                                        f"could cost up to ${reserve:.4f}; limit ${self.limit_usd:.2f}")
            self._inflight += reserve
        try:
            return self._ask(messages, task_id, sample)
        finally:
            with self._lock:
                self._inflight -= reserve

    def _ask(self, messages: list[dict], task_id: str, sample: int) -> FrontierReply:
        call_id = uuid.uuid4().hex
        t_call = time.perf_counter()
        for i in range(self.max_retries + 1):
            t0 = time.perf_counter()
            resp, status, parsed = None, "ok", parse_reply(None)
            try:
                resp = self._http.post(API_URL, json=self.body(messages))
            except httpx.TransportError as e:
                status = f"transport:{type(e).__name__}"
            if resp is not None:
                try:
                    data = resp.json()
                except ValueError:
                    data = None
                parsed = parse_reply(data)
                if not 200 <= resp.status_code < 300:
                    status = f"http:{resp.status_code}"
                else:
                    status = parsed["status"]
            usd_c = usd_for(self.prices, self.model, parsed["input_tokens"], parsed["output_tokens"])
            self.ledger.append(LedgerRow(
                component="frontier", model=self.model, provider="openrouter", task_id=task_id, step=sample,
                arm="takeover_from_scratch", call_id=call_id, http_attempt=i, status=status,
                input_tokens=parsed["input_tokens"], output_tokens=parsed["output_tokens"],
                reasoning_tokens=parsed["reasoning_tokens"], usd_reported=parsed["usd_reported"],
                usd_computed=usd_c, latency_ms=round((time.perf_counter() - t0) * 1000, 1),
                model_returned=parsed["model_returned"]))
            if status == "ok" or status.startswith("protocol:"):
                # A protocol problem may already be billed: it is returned as it is, never retried.
                return FrontierReply(
                    content=parsed["content"], finish_reason=parsed["finish_reason"],
                    model_returned=parsed["model_returned"], provider_returned=parsed["provider_returned"],
                    input_tokens=parsed["input_tokens"], output_tokens=parsed["output_tokens"],
                    reasoning_tokens=parsed["reasoning_tokens"], usd_reported=parsed["usd_reported"],
                    usd_computed=usd_c, latency_ms=(time.perf_counter() - t_call) * 1000, call_id=call_id,
                    http_attempts=i + 1, status=status)
            retryable = status.startswith("transport:") or (resp is not None and resp.status_code in RETRY_STATUS)
            if not retryable or i == self.max_retries:
                raise FrontierRequestError(f"call {call_id}: {status} after {i + 1} attempt(s)")
            self._sleep(min(MAX_BACKOFF_S, (2.0 ** i) * (0.5 + random.random() / 2)))
        raise AssertionError("unreachable")
