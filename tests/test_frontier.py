import json

import httpx
import pytest

from system1.eval.ledger import CostLedger, LedgerRow
from system1.frontier import client as F

PRICES = {"models": {F.MODEL: {"usd_per_m_input": 2.0, "usd_per_m_output": 10.0}}}
MSG = [{"role": "user", "content": "Write f."}]


def reply(content="```python\ndef f():\n    return 1\n```", prompt=100, completion=200, cost=0.0022):
    return {"model": "anthropic/claude-sonnet-5.5", "provider": "Anthropic",
            "choices": [{"message": {"role": "assistant", "content": content}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": prompt, "completion_tokens": completion, "cost": cost,
                      "completion_tokens_details": {"reasoning_tokens": 50}}}


def make(tmp_path, handler, limit=5.0, **kw):
    ledger = CostLedger(tmp_path / "ledger.jsonl")
    sleeps = []
    c = F.FrontierClient(ledger, PRICES, limit, api_key="k", transport=httpx.MockTransport(handler),
                         sleep=sleeps.append, **kw)
    return c, ledger, sleeps


def test_request_is_pinned_and_the_reply_is_logged(tmp_path):
    seen = []

    def handler(request):
        seen.append(json.loads(request.content))
        return httpx.Response(200, json=reply())

    c, ledger, _ = make(tmp_path, handler)
    r = c.ask(MSG, task_id="T", sample=2)
    body = seen[0]
    assert body["model"] == F.MODEL and body["provider"] == {"order": ["anthropic"], "allow_fallbacks": False}
    assert body["reasoning"] == {"effort": "low"} and body["usage"] == {"include": True}
    assert body["messages"] == MSG and body["max_tokens"] == F.MAX_TOKENS
    assert r.status == "ok" and "def f" in r.content and r.reasoning_tokens == 50
    assert r.usd_reported == 0.0022 and r.usd_computed == pytest.approx((100 * 2 + 200 * 10) / 1e6)
    rows, _ = ledger.read()
    assert len(rows) == 1 and rows[0]["component"] == "frontier" and rows[0]["step"] == 2
    assert rows[0]["call_id"] == r.call_id and rows[0]["usd_reported"] == 0.0022


def test_spend_guard_stops_before_any_request(tmp_path):
    calls = []

    def handler(request):
        calls.append(1)
        return httpx.Response(200, json=reply())

    c, ledger, _ = make(tmp_path, handler, limit=0.10)
    ledger.append(LedgerRow(component="frontier", model=F.MODEL, provider="openrouter", usd_reported=0.05))
    # worst case of the next call: 8,000 output tokens x $10/M = $0.08 > the $0.05 left
    with pytest.raises(F.SpendLimitReached):
        c.ask(MSG, task_id="T", sample=0)
    assert calls == []


def test_unknown_cost_counts_at_the_worst_case_and_unsent_requests_are_free(tmp_path):
    path = tmp_path / "l.jsonl"
    led = CostLedger(path)
    led.append(LedgerRow(component="frontier", model="m", provider="p", usd_reported=0.01))
    led.append(LedgerRow(component="frontier", model="m", provider="p", usd_computed=0.02))
    led.append(LedgerRow(component="frontier", model="m", provider="p", status="protocol:empty content"))
    led.append(LedgerRow(component="frontier", model="m", provider="p", status="transport:ConnectError"))
    led.append(LedgerRow(component="router", model="jev", provider="typesafe", usd_computed=9.0))
    spent, unknown = F.ledger_spend(path, worst_case_usd=0.5)
    assert spent == pytest.approx(0.01 + 0.02 + 0.5) and unknown == 1


def test_server_errors_are_retried_and_each_attempt_is_logged(tmp_path):
    n = []

    def handler(request):
        n.append(1)
        return httpx.Response(503, json={"error": "busy"}) if len(n) == 1 else httpx.Response(200, json=reply())

    c, ledger, sleeps = make(tmp_path, handler)
    r = c.ask(MSG, task_id="T", sample=0)
    rows, _ = ledger.read()
    assert r.status == "ok" and r.http_attempts == 2 and len(sleeps) == 1
    assert [x["status"] for x in rows] == ["http:503", "ok"] and [x["http_attempt"] for x in rows] == [0, 1]
    assert len({x["call_id"] for x in rows}) == 1


def test_an_unusable_reply_is_returned_not_retried(tmp_path):
    n = []

    def handler(request):
        n.append(1)
        return httpx.Response(200, json=reply(content=""))

    c, ledger, _ = make(tmp_path, handler)
    r = c.ask(MSG, task_id="T", sample=0)
    assert r.content is None and r.status == "protocol:empty content" and len(n) == 1
    assert ledger.read()[0][0]["usd_reported"] == 0.0022  # it may be billed, so its cost is kept


def test_a_client_error_is_not_retried(tmp_path):
    def handler(request):
        return httpx.Response(400, json={"error": "bad"})

    c, ledger, sleeps = make(tmp_path, handler)
    with pytest.raises(F.FrontierRequestError):
        c.ask(MSG, task_id="T", sample=0)
    assert sleeps == [] and len(ledger.read()[0]) == 1


def test_a_missing_price_is_refused(tmp_path):
    with pytest.raises(RuntimeError):
        F.FrontierClient(CostLedger(tmp_path / "l.jsonl"), {"models": {}}, 5.0, api_key="k")


def test_grader_makes_one_unit_per_answer_and_refuses_duplicates():
    import importlib.util
    from pathlib import Path
    path = Path(__file__).resolve().parents[1] / "scripts" / "grade_hidden.py"
    spec = importlib.util.spec_from_file_location("grade_hidden", path)
    gh = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gh)
    rows = [{"task_id": "Mbpp/2", "benchmark": "mbpp+", "sample": 0, "code": "def f(): pass\n"},
            {"task_id": "Mbpp/2", "benchmark": "mbpp+", "sample": 1, "code": None}]
    units = gh.frontier_units(rows)
    assert [u["checkpoint_id"] for u in units] == ["Mbpp/2/frontier/s0", "Mbpp/2/frontier/s1"]
    assert units[1]["code"] is None
    with pytest.raises(SystemExit):
        gh.frontier_units(rows + rows[:1])
