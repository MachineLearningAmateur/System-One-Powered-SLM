import json

import httpx
import pytest

from system1.eval.ledger import CostLedger
from system1.routers.jev import (
    ByteBudgetExceeded,
    JevClient,
    JevProtocolError,
    JevRequestError,
    encode_body,
)

KEY = "test-key-should-never-be-logged"

QUESTIONS = {
    "on_task": {"type": "noul", "instructions": "On task?"},
    "status": {
        "type": "choice",
        "instructions": "On track?",
        "criteria": {"on_track": "yes", "drifting": "no"},
    },
}


def good_body(**over):
    body = {
        "model": "jev-1.13.0",
        "answers": {
            "on_task": {"type": "noul", "noul": 0.37},
            "status": {"type": "choice", "choice": "drifting", "confidence": 0.9,
                       "probabilities": {"on_track": 0.05, "drifting": 0.95}},
        },
        "usage": {"input_tokens": 500, "output_tokens": 70},
    }
    body.update(over)
    return body


def make_client(handler, tmp_path, **kw):
    sleeps = []
    ledger = CostLedger(tmp_path / "ledger.jsonl")
    client = JevClient(api_key=KEY, ledger=ledger, transport=httpx.MockTransport(handler),
                       sleep=sleeps.append, **kw)
    return client, ledger, sleeps


def sequence(*responses):
    """Handler that returns the given responses in order; an exception is raised."""
    it = iter(responses)
    seen = []

    def handler(request):
        seen.append(request)
        r = next(it)
        if isinstance(r, Exception):
            raise r
        return r

    handler.seen = seen
    return handler


def test_valid_response_and_exact_bytes(tmp_path):
    handler = sequence(httpx.Response(200, json=good_body()))
    client, ledger, _ = make_client(handler, tmp_path)
    r = client.ask("state", QUESTIONS, task_id="t1", attempt=2, step=1, arm="base+history")
    sent = handler.seen[0]
    assert r.request_bytes == len(sent.content)
    assert sent.content == encode_body({"model": "jev-latest", "state": "state", "questions": QUESTIONS})
    assert sent.headers["authorization"] == f"Bearer {KEY}"
    assert r.model_returned == "jev-1.13.0" and r.http_attempts == 1
    assert r.probability("on_task") == 0.37 and r.probability("status", "drifting") == 0.95
    rows, bad = ledger.read()
    assert bad == [] and len(rows) == 1
    row = rows[0]
    assert (row["status"], row["http_attempt"], row["arm"], row["attempt"]) == ("ok", 0, "base+history", 2)
    assert (row["input_tokens"], row["output_tokens"], row["model_returned"]) == (500, 70, "jev-1.13.0")
    assert row["call_id"] == r.call_id


def test_retry_after_then_success_logs_both_attempts(tmp_path):
    handler = sequence(httpx.Response(429, headers={"Retry-After": "2"}), httpx.Response(200, json=good_body()))
    client, ledger, sleeps = make_client(handler, tmp_path)
    r = client.ask("s", QUESTIONS)
    assert r.http_attempts == 2 and sleeps == [2.0]
    rows, _ = ledger.read()
    assert [x["status"] for x in rows] == ["http:429", "ok"]
    assert [x["http_attempt"] for x in rows] == [0, 1]
    assert rows[0]["input_tokens"] is None and rows[0]["usd_computed"] is None
    assert rows[0]["call_id"] == rows[1]["call_id"]


def test_transport_error_is_retried(tmp_path):
    handler = sequence(httpx.ConnectError("down"), httpx.Response(200, json=good_body()))
    client, ledger, sleeps = make_client(handler, tmp_path)
    client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert rows[0]["status"] == "transport:ConnectError" and len(sleeps) == 1


def test_retries_exhausted(tmp_path):
    handler = sequence(*[httpx.Response(503) for _ in range(3)])
    client, ledger, sleeps = make_client(handler, tmp_path, max_retries=2)
    with pytest.raises(JevRequestError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert len(rows) == 3 and len(sleeps) == 2


def test_client_error_not_retried(tmp_path):
    handler = sequence(httpx.Response(400, json={"error": "bad"}))
    client, ledger, sleeps = make_client(handler, tmp_path)
    with pytest.raises(JevRequestError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert len(rows) == 1 and rows[0]["status"] == "http:400" and sleeps == []


NOUL_OK = {"type": "noul", "noul": 0.4}
CHOICE_OK = good_body()["answers"]["status"]


@pytest.mark.parametrize(
    "body",
    [
        {},
        good_body(model=""),
        good_body(usage={"input_tokens": True, "output_tokens": 1}),
        good_body(usage={"input_tokens": 1.5, "output_tokens": 1}),
        good_body(answers={"on_task": NOUL_OK}),
        good_body(answers={"on_task": {"noul": 0.4}, "status": CHOICE_OK}),  # missing type
        good_body(answers={"on_task": {"type": "noul", "noul": 1.2}, "status": CHOICE_OK}),
        good_body(answers={"on_task": {"type": "choice", "noul": 0.4}, "status": CHOICE_OK}),
        good_body(answers={"on_task": NOUL_OK, "status": {
            "type": "choice", "choice": "on_track", "confidence": 0.5,
            "probabilities": {"on_track": 0.5, "other": 0.5}}}),
        good_body(answers={"on_task": NOUL_OK, "status": {
            "type": "choice", "choice": "on_track", "confidence": 0.5,
            "probabilities": {"on_track": 0.5, "drifting": 0.7}}}),
        good_body(answers={"on_task": NOUL_OK, "status": {
            "type": "choice", "choice": "maybe", "confidence": 0.5,
            "probabilities": {"on_track": 0.5, "drifting": 0.5}}}),
        good_body(answers={"on_task": NOUL_OK, "status": {
            "type": "choice", "choice": "on_track",
            "probabilities": {"on_track": 0.5, "drifting": 0.5}}}),  # missing confidence
    ],
)
def test_invalid_responses_are_rejected_not_retried(tmp_path, body):
    handler = sequence(httpx.Response(200, json=body))
    client, ledger, sleeps = make_client(handler, tmp_path)
    with pytest.raises(JevProtocolError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert len(rows) == 1 and rows[0]["status"].startswith("protocol:") and sleeps == []


def test_usage_kept_when_answers_invalid(tmp_path):
    handler = sequence(httpx.Response(200, json=good_body(answers={})))
    client, ledger, _ = make_client(handler, tmp_path)
    with pytest.raises(JevProtocolError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert (rows[0]["input_tokens"], rows[0]["output_tokens"]) == (500, 70)


def test_invalid_json_is_protocol_error(tmp_path):
    handler = sequence(httpx.Response(200, content=b"not json"))
    client, ledger, _ = make_client(handler, tmp_path)
    with pytest.raises(JevProtocolError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert rows[0]["status"] == "protocol:invalid_json"


def test_byte_budget_uses_exact_payload(tmp_path):
    state = "é" * 100
    exact = len(encode_body({"model": "jev-latest", "state": state, "questions": QUESTIONS}))
    handler = sequence(httpx.Response(200, json=good_body()))
    client, _, _ = make_client(handler, tmp_path, byte_budget=exact)
    assert client.ask(state, QUESTIONS).request_bytes == exact
    client2, _, _ = make_client(sequence(), tmp_path, byte_budget=exact - 1)
    with pytest.raises(ByteBudgetExceeded):
        client2.ask(state, QUESTIONS)


def test_nan_rejected_before_sending(tmp_path):
    handler = sequence()
    client, ledger, _ = make_client(handler, tmp_path)
    with pytest.raises(ValueError):
        client.ask({"x": float("nan")}, QUESTIONS)
    assert handler.seen == [] and ledger.read() == ([], [])


def test_key_never_written_to_ledger(tmp_path):
    handler = sequence(httpx.Response(500), httpx.Response(200, json=good_body()))
    client, ledger, _ = make_client(handler, tmp_path)
    client.ask("s", QUESTIONS)
    assert KEY not in ledger.path.read_text(encoding="utf-8")


def test_missing_key_and_bad_retries(monkeypatch):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        JevClient()
    with pytest.raises(ValueError):
        JevClient(api_key="k", max_retries=-1)


def test_probability_needs_option_for_choice(tmp_path):
    handler = sequence(httpx.Response(200, json=good_body()))
    client, _, _ = make_client(handler, tmp_path)
    r = client.ask("s", QUESTIONS)
    with pytest.raises(ValueError):
        r.probability("status")
    assert json.loads(json.dumps(r.raw))["model"] == "jev-1.13.0"


SCORE_Q = {"lvl": {"type": "score", "instructions": "How lost?", "criteria": ["fine", "unsure", "lost"]}}


def score_body(**answer_over):
    answer = {"type": "score", "score": 1.05, "legend": {"0": "fine", "1": "unsure", "2": "lost"},
              "probabilities": {"0": 0.0, "1": 0.95, "2": 0.05}, "confidence": 0.9}
    answer.update(answer_over)
    return {"model": "jev-1.13.0", "answers": {"lvl": answer}, "usage": {"input_tokens": 1, "output_tokens": 1}}


def test_valid_score(tmp_path):
    client, _, _ = make_client(sequence(httpx.Response(200, json=score_body())), tmp_path)
    r = client.ask("s", SCORE_Q)
    assert r.score("lvl") == 1.05 and r.probability("lvl", "2") == 0.05


@pytest.mark.parametrize(
    "over",
    [
        {"probabilities": {"bogus": 1.0}},
        {"legend": {"0": "fine", "1": "unsure"}},
        {"legend": {"0": "lost", "1": "unsure", "2": "fine"}},  # levels in the wrong order
        {"score": 2.5},
        {"score": 0.2},  # inconsistent with the weighted levels (1.05)
        {"score": None},
    ],
)
def test_invalid_score_rejected(tmp_path, over):
    client, _, _ = make_client(sequence(httpx.Response(200, json=score_body(**over))), tmp_path)
    with pytest.raises(JevProtocolError):
        client.ask("s", SCORE_Q)


def test_dispatch_uses_question_type_not_fields(tmp_path):
    q = {"q": {"type": "choice", "instructions": "?", "criteria": {"yes": "a", "no": "b"}}}
    body = {"model": "m", "usage": {"input_tokens": 1, "output_tokens": 1},
            "answers": {"q": {"type": "choice", "choice": "yes", "confidence": 0.6,
                              "probabilities": {"yes": 0.8, "no": 0.2}, "noul": 99}}}
    client, _, _ = make_client(sequence(httpx.Response(200, json=body)), tmp_path)
    assert client.ask("s", q).probability("q", "yes") == 0.8


def test_huge_integer_is_logged_protocol_error(tmp_path):
    raw = (b'{"model":"m","usage":{"input_tokens":3,"output_tokens":4},"answers":{"on_task":'
           b'{"type":"noul","noul":1' + b"0" * 400 + b'},"status":{}}}')
    client, ledger, _ = make_client(sequence(httpx.Response(200, content=raw)), tmp_path)
    with pytest.raises(JevProtocolError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert len(rows) == 1 and rows[0]["status"].startswith("protocol:")
    assert (rows[0]["input_tokens"], rows[0]["output_tokens"]) == (3, 4)


def test_unsupported_question_type_rejected_before_sending(tmp_path):
    handler = sequence()
    client, _, _ = make_client(handler, tmp_path)
    with pytest.raises(ValueError):
        client.ask("s", {"b": {"type": "box", "instructions": "?"}})
    with pytest.raises(ValueError):
        client.ask("s", {"s": {"type": "score", "instructions": "?", "criteria": ["only one"]}})
    assert handler.seen == []


def test_redirect_is_not_success(tmp_path):
    handler = sequence(httpx.Response(302, json=good_body()))
    client, ledger, sleeps = make_client(handler, tmp_path)
    with pytest.raises(JevRequestError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert rows[0]["status"] == "http:302" and sleeps == []


def test_error_response_keeps_usage(tmp_path):
    handler = sequence(httpx.Response(500, json={"usage": {"input_tokens": 9, "output_tokens": 0}}),
                       httpx.Response(200, json=good_body()))
    client, ledger, _ = make_client(handler, tmp_path)
    client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert rows[0]["status"] == "http:500" and rows[0]["input_tokens"] == 9


def test_long_retry_after_stops_instead_of_retrying_early(tmp_path):
    handler = sequence(httpx.Response(429, headers={"Retry-After": "120"}))
    client, ledger, sleeps = make_client(handler, tmp_path)
    with pytest.raises(JevRequestError):
        client.ask("s", QUESTIONS)
    rows, _ = ledger.read()
    assert len(rows) == 1 and sleeps == []
