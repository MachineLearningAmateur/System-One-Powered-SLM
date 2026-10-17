import hashlib
import json

import httpx
import pytest

from system1.config import CONFIGS
from system1.eval.ledger import CostLedger
from system1.features.evidence import (
    ARMS,
    CODE_MAX_CHARS_TRIMMED,
    TEST_OUTPUT_MAX_CHARS,
    TRACE_HEAD_SHARE,
    Checkpoint,
    EvidenceTooLarge,
    build_arms,
    build_evidence,
    head_tail,
)
from system1.features.jev_scoring import (
    APPLICABLE,
    JevScorer,
    ModelVersionChanged,
    ScoreStore,
    applicability,
    load_rubric,
)
from system1.routers.jev import BYTE_BUDGET, JevClient, request_body

RUBRIC = load_rubric()
TRACE_QS = {"on_task", "repeating_failed_fix", "approach_change_without_evidence",
            "unsupported_claim", "stated_fix_matches_change", "clear_next_step"}
CODE_QS = {"code_likely_fails", "special_cases_visible_tests", "repeats_previous_code"}


def checkpoint(round_=2, visible_pass=False, thinking="I think the bug is the loop bound.", **over):
    base = dict(
        task_id="HumanEval/0", benchmark="humaneval+", attempt=1, round=round_,
        task_prompt="def has_close_elements(numbers, threshold): ...",
        code="def has_close_elements(numbers, threshold):\n    return False\n",
        visible_test_output="AssertionError: expected True",
        visible_pass=visible_pass, thinking=thinking,
        telemetry={"pass_count_delta": 0, "similarity_to_previous": 0.97, "same_error": True},
        prev_code=None if round_ == 1 else "def has_close_elements(n, t):\n    return None\n",
        prev_test_output=None if round_ == 1 else "AssertionError: expected True",
    )
    base.update(over)
    return Checkpoint(**base)


# --- checkpoint validation (H1, H2) ------------------------------------------

@pytest.mark.parametrize("over", [
    dict(round_=1, prev_code="x", prev_test_output="y"),  # round 1 with history
    dict(round_=3, prev_code=None, prev_test_output=None),  # later round without history
    dict(round_=2, prev_test_output=None),  # code without its test output
    dict(round_=0, prev_code=None, prev_test_output=None),
])
def test_inconsistent_history_is_an_error(over):
    with pytest.raises(ValueError):
        checkpoint(**over)


# --- rubric and applicability ------------------------------------------------

def test_rubric_loads_with_string_criteria_keys():
    assert RUBRIC.version == "rubric-v2" and len(RUBRIC.sha256) == 64
    for qid in RUBRIC.questions:
        q = RUBRIC.api_question(qid)
        assert q["type"] == "noul" and set(q["criteria"]) == {"true", "false"}


def test_rubric_hash_ignores_status_but_not_text(tmp_path):
    src = (CONFIGS / "rubric_v2.yaml").read_text(encoding="utf-8")
    p1, p2 = tmp_path / "a.yaml", tmp_path / "b.yaml"
    p1.write_text(src.replace("status: frozen", "status: proposed"), encoding="utf-8")
    p2.write_text(src.replace("Is the model working on", "Is the model busy with"), encoding="utf-8")
    assert load_rubric(p1).sha256 == RUBRIC.sha256
    assert load_rubric(p2).sha256 != RUBRIC.sha256


def test_unquoted_yaml_booleans_rejected(tmp_path):
    p = tmp_path / "r.yaml"
    p.write_text("version: x\nquestions:\n  q:\n    instructions: i\n    criteria:\n      true: a\n      false: b\n",
                 encoding="utf-8")
    with pytest.raises(ValueError):
        load_rubric(p)


def test_history_arm_asks_only_code_questions():
    app = applicability(RUBRIC, checkpoint(), "base+history")
    assert all(app[q] == "na:arm_lacks_trace" for q in TRACE_QS)
    assert all(app[q] == APPLICABLE for q in CODE_QS)


def test_first_round_and_visible_pass_rules_with_all_reasons():
    app = applicability(RUBRIC, checkpoint(round_=1), "base+history+trace")
    assert app["repeating_failed_fix"] == "na:first_round" and app["on_task"] == APPLICABLE
    app = applicability(RUBRIC, checkpoint(round_=1), "base+history")
    assert app["repeating_failed_fix"] == "na:first_round,arm_lacks_trace"  # every reason, checkpoint first
    app = applicability(RUBRIC, checkpoint(visible_pass=True), "base+history+trace")
    assert app["clear_next_step"] == "na:visible_pass"


def test_empty_thinking_is_trace_missing_not_a_trace():
    cp = checkpoint(thinking="   ")
    app = applicability(RUBRIC, cp, "base+history+trace")
    assert all(app[q].startswith("na:trace_missing") for q in TRACE_QS)
    assert all(app[q] == APPLICABLE for q in CODE_QS)
    ev = build_evidence(cp, "base+history+trace", {}, model="m", budget=28_000)
    assert "thinking" not in ev.state and ev.trace_retained_chars == 0


# --- evidence ----------------------------------------------------------------

def test_arms_share_the_same_base_and_history():
    cp = checkpoint()
    a = build_evidence(cp, "base+history", {}, model="m", budget=28_000).state
    b = build_evidence(cp, "base+history+trace", {}, model="m", budget=28_000).state
    assert "thinking" not in a and b["thinking"] == cp.thinking
    assert {k: v for k, v in b.items() if k != "thinking"} == a
    assert a["previous_code"] == cp.prev_code


def test_first_round_has_no_history_block():
    state = build_evidence(checkpoint(round_=1), "base+history+trace", {}, model="m", budget=28_000).state
    assert "previous_code" not in state


def test_nan_telemetry_is_sanitized_and_recorded():
    cp = checkpoint(telemetry={"similarity_to_previous": float("nan"), "deep": {"x": float("inf")}, "ok": 1.0})
    ev = build_evidence(cp, "base+history", {}, model="m", budget=28_000)
    assert ev.state["loop_telemetry"] == {"similarity_to_previous": None, "deep": {"x": None}, "ok": 1.0}
    assert ev.telemetry_sanitized == ["similarity_to_previous", "deep.x"]


def test_test_output_bounded():
    cp = checkpoint(visible_test_output="x" * 10_000)
    out = build_evidence(cp, "base+history", {}, model="m", budget=None).state["visible_test_output"]
    assert out.startswith("x" * (TEST_OUTPUT_MAX_CHARS // 2)) and "omitted by the harness" in out


@pytest.mark.parametrize("unit", ["é\"\n", "a"])
def test_trace_fitted_to_exact_budget(unit):
    trace = "START " + unit * 30_000 + " END"
    cp = checkpoint(thinking=trace)
    qs = {"on_task": RUBRIC.api_question("on_task")}
    budget = 12_000
    ev = build_evidence(cp, "base+history+trace", qs, model="jev-latest", budget=budget)
    exact = len(request_body("jev-latest", ev.state, qs))
    assert ev.payload_bytes == exact <= budget
    assert budget - exact < (50 if unit != "a" else 5)  # little thinking is wasted
    t = ev.state["thinking"]
    assert t.startswith("START") and t.endswith("END") and "omitted by the harness" in t
    assert ev.trace_truncated and ev.trace_original_chars == len(trace)


def test_head_tail_split_and_short_text():
    assert head_tail("abc", 10) == "abc"
    text = "".join(chr(65 + i % 26) for i in range(1000))
    out = head_tail(text, 400, TRACE_HEAD_SHARE)
    head, tail = out.split("\n[...")[0], out.split("...]\n")[1]
    assert len(head) == 100 and len(tail) == 300 and head == text[:100] and tail == text[-300:]


def test_trace_size_never_decreases_as_more_is_kept():
    cp = checkpoint(thinking="é" * 1_500)
    qs = {"on_task": RUBRIC.api_question("on_task")}
    from system1.features.evidence import base_state
    state, _ = base_state(cp, ARMS["base+history+trace"])
    sizes = [len(request_body("m", {**state, "thinking": head_tail(cp.thinking, k, TRACE_HEAD_SHARE)}, qs))
             for k in range(len(cp.thinking))]
    assert all(b >= a for a, b in zip(sizes, sizes[1:]))


def test_fallback_trims_task_and_code_for_every_arm():
    big = "x = 1\n" * 10_000
    cp = checkpoint(code=big, prev_code=big)
    with pytest.raises(EvidenceTooLarge):
        build_evidence(cp, "base+history", {}, model="m", budget=28_000)
    evs = build_arms(cp, {arm: {} for arm in ARMS}, model="m", budget=28_000)
    assert all(ev.base_trimmed for ev in evs.values())
    a, b = (evs[arm].state for arm in ARMS)
    assert {k: v for k, v in b.items() if k != "thinking"} == a  # one shared base
    assert "omitted by the harness" in a["current_code"] and len(a["current_code"]) < CODE_MAX_CHARS_TRIMMED + 100
    assert all(ev.unfitted_bytes > 28_000 for ev in evs.values())


def test_too_large_even_after_fallback():
    with pytest.raises(EvidenceTooLarge) as e:
        build_arms(checkpoint(), {arm: {} for arm in ARMS}, model="m", budget=200)
    assert e.value.unfitted_bytes and e.value.unfitted_bytes > 200


# --- scorer --------------------------------------------------------------------

def jev_api(model="jev-1.13.0", seen=None):
    """Mock Jev: answers every question that the request asks."""
    calls = []

    def handler(request):
        body = json.loads(request.content)
        calls.append(request)
        if seen is not None:
            seen.append(request)
        answers = {q: {"type": "noul", "noul": 0.42} for q in body["questions"]}
        version = model(len(calls)) if callable(model) else model
        return httpx.Response(200, json={"model": version, "answers": answers,
                                         "usage": {"input_tokens": 100, "output_tokens": 10}})
    return handler


def make_scorer(tmp_path, handler, store_name="scores.jsonl", **client_kw):
    client = JevClient(api_key="k", transport=httpx.MockTransport(handler), sleep=lambda s: None,
                       ledger=CostLedger(tmp_path / "ledger.jsonl"), **client_kw)
    store = ScoreStore(tmp_path / store_name)
    return JevScorer(client, RUBRIC, store, run_id="run-test"), store


def test_scores_both_arms_with_durable_records(tmp_path):
    seen = []
    scorer, store = make_scorer(tmp_path, jev_api(seen=seen))
    hist, full = scorer.score_arms(checkpoint())
    assert (hist.arm, full.arm) == tuple(ARMS)
    assert set(json.loads(seen[0].content)["questions"]) == CODE_QS
    assert "thinking" not in json.loads(seen[0].content)["state"]
    assert "thinking" in json.loads(seen[1].content)["state"]
    assert hist.features["on_task"] is None and full.features["on_task"] == 0.42
    for rec, req in ((hist, seen[0]), (full, seen[1])):
        assert rec.request_sha256 == hashlib.sha256(req.content).hexdigest()
        assert rec.request_bytes == len(req.content)
        assert rec.evidence_version and rec.byte_budget == 56_000 and rec.visible_pass is False
    rows, bad = store.read()
    assert bad == [] and len(rows) == 2 and rows[1]["call_id"] == full.call_id
    assert rows[1]["rubric_sha256"] == RUBRIC.sha256 and rows[1]["raw_answers"]["on_task"]["noul"] == 0.42
    ledger_rows, _ = CostLedger(tmp_path / "ledger.jsonl").read()
    assert {r["call_id"] for r in ledger_rows} == {hist.call_id, full.call_id}


def test_no_applicable_questions_means_no_call(tmp_path):
    seen = []
    scorer, store = make_scorer(tmp_path, jev_api(seen=seen))
    scorer.rubric = type(RUBRIC)(RUBRIC.version, RUBRIC.sha256, {"on_task": RUBRIC.questions["on_task"]})
    rec = scorer.score(checkpoint(), "base+history")
    assert rec.status == "no_questions" and seen == [] and rec.call_id is None


def test_protocol_error_recorded_without_features(tmp_path):
    def handler(request):
        return httpx.Response(200, json={"model": "m", "answers": {}, "usage": {"input_tokens": 1, "output_tokens": 1}})
    scorer, store = make_scorer(tmp_path, handler)
    rec = scorer.score(checkpoint(), "base+history+trace")
    assert rec.status == "protocol_error" and all(v is None for v in rec.features.values())


def test_request_error_recorded(tmp_path):
    scorer, store = make_scorer(tmp_path, lambda r: httpx.Response(400, json={}))
    rec = scorer.score(checkpoint(), "base+history+trace")
    assert rec.status == "request_error" and rec.request_sha256 and rec.call_id is None


def test_too_large_marks_every_arm_so_pairs_stay_paired(tmp_path):
    seen = []
    scorer, store = make_scorer(tmp_path, jev_api(seen=seen), byte_budget=600)
    recs = scorer.score_arms(checkpoint())
    assert [r.status for r in recs] == ["evidence_too_large", "evidence_too_large"] and seen == []
    assert all(r.unfitted_bytes > 600 for r in recs)


def test_fallback_trim_recorded(tmp_path):
    big = "x = 1\n" * 10_000
    scorer, store = make_scorer(tmp_path, jev_api())
    recs = scorer.score_arms(checkpoint(code=big, prev_code=big))
    assert all(r.status == "ok" and r.base_trimmed for r in recs)


def test_model_version_change_stops_and_skips_remaining_arms(tmp_path):
    seen = []
    scorer, store = make_scorer(tmp_path, jev_api(model=lambda n: "jev-1.13.0" if n <= 2 else "jev-1.14.0",
                                                  seen=seen))
    scorer.score_arms(checkpoint())  # calls 1-2: old version
    with pytest.raises(ModelVersionChanged):
        scorer.score_arms(checkpoint(attempt=2))  # call 3 changes; the trace arm is not called
    assert len(seen) == 3
    rows, _ = store.read()
    assert [r["status"] for r in rows] == ["ok", "ok", "model_changed", "skipped"]


def test_resumed_run_still_detects_a_version_change(tmp_path):
    scorer, store = make_scorer(tmp_path, jev_api(model="jev-1.13.0"))
    scorer.score_arms(checkpoint())
    resumed, _ = make_scorer(tmp_path, jev_api(model="jev-1.14.0"))  # same store file, new process
    assert resumed.model_version == "jev-1.13.0"
    with pytest.raises(ModelVersionChanged):
        resumed.score_arms(checkpoint(attempt=2))


def test_default_budget_keeps_a_full_8k_trace():
    # The largest 8K-cap thinking in the pilot was 37,543 characters; with the
    # rest of the evidence the request stays under the default budget, uncut.
    cp = checkpoint(thinking="step " * 8_000)  # 40,000 characters
    qs = {q: RUBRIC.api_question(q) for q, s in applicability(RUBRIC, cp, "base+history+trace").items() if s == APPLICABLE}
    ev = build_evidence(cp, "base+history+trace", qs, model="jev-latest", budget=BYTE_BUDGET)
    assert ev.trace_truncated is False and ev.payload_bytes <= BYTE_BUDGET
