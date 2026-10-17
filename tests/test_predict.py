import importlib.util
from pathlib import Path

import numpy as np
import pytest
from sklearn.model_selection import StratifiedGroupKFold

from system1.eval import predict as P
from system1.features.telemetry import JEV_TELEMETRY_KEYS


def feats(round_=1, **over):
    f = {"round": round_, "visible_pass_fraction": 1.0, "visible_not_run_count": 0, "code_lines": 5,
         "marker_count": 2, "thinking_tokens": 99, "thinking_mean_logprob": -0.1, "thinking_tail_conf": 11.0,
         "thinking_bottom10_group_conf": 10.0, "answer_mean_logprob": -0.01, "visible_pass": True,
         "cap_hit": False, "think_closed": True, "loop_flag": False, "code_missing": False, "error_types": [],
         "execution_stage": None, "pass_count_delta": None, "similarity_to_previous": None,
         "same_error_as_previous": None, "same_failing_tests_as_previous": None, "returns_to_earlier_code": None}
    if round_ > 1:
        f.update(pass_count_delta=1, similarity_to_previous=0.8, same_error_as_previous=False,
                 same_failing_tests_as_previous=False, returns_to_earlier_code=False)
    f.update(over)
    return f


def jev(arm, round_=1, **values):
    qs = P.CODE_QS if arm == P.HISTORY_ARM else P.CODE_QS + P.THINKING_QS
    app, out = {}, {}
    for q in qs:
        na = (round_ == 1 and q in ("repeats_previous_code", "repeating_failed_fix",
                                    "approach_change_without_evidence", "stated_fix_matches_change"))
        na_vp = q == "clear_next_step"
        app[q] = "na:first_round" if na else "na:visible_pass" if na_vp else "applicable"
        out[q] = None if app[q] != "applicable" else values.get(q, 0.5)
    return {"checkpoint_id": "T/a0/r1", "arm": arm, "applicability": app, "features": out}


def test_columns_are_fixed_by_the_schema_not_the_data():
    cheap = P.columns("cheap", True)
    full = P.columns("cheap+code+thinking", True)
    assert full[:len(cheap)] == cheap  # every set starts with the same cheap block
    assert "jev_clear_next_step" not in full and "jev_clear_next_step" in P.columns("cheap+code+thinking", False)
    assert {"first_round", "trace_missing"} <= set(cheap)
    assert not any(c.startswith("jev_") and c.endswith("__missing") for c in full)  # no per-question indicators
    with pytest.raises(ValueError):
        P.columns("cheap+thinking", True)


def test_round_one_history_is_structural_one_shared_indicator():
    v = P.cheap_vector(feats(1), has_trace=True)
    assert v["first_round"] == 1.0 and all(v[f"{k}__missing"] == 0.0 for k in P.CHEAP_HISTORY)
    assert all(v[k] == 0.0 for k in P.CHEAP_HISTORY)
    # After round 1 a missing similarity (a round without code) is not structural: own indicator.
    v = P.cheap_vector(feats(2, similarity_to_previous=None), has_trace=True)
    assert v["similarity_to_previous__missing"] == 1.0 and v["first_round"] == 0.0


def test_cheap_baseline_has_the_telemetry_jev_gets():
    cols = set(P.columns("cheap", True))
    assert set(JEV_TELEMETRY_KEYS) <= cols  # includes same_failing_tests_as_previous


def test_timeout_and_load_errors_are_encoded():
    v = P.cheap_vector(feats(1, error_types=["Timeout"]), has_trace=True)
    assert v["err_Timeout"] == 1.0 and v["err_other"] == 0.0
    v = P.cheap_vector(feats(1, error_types=["NameError"], execution_stage="load"), has_trace=False)
    assert v["err_load"] == 1.0 and v["err_other"] == 0.0 and v["trace_missing"] == 1.0
    v = P.cheap_vector(feats(1, thinking_tail_conf=None), has_trace=True)
    assert v["thinking_tail_conf"] == 0.0 and v["thinking_tail_conf__missing"] == 1.0


def test_jev_block_structural_na_is_zero_and_an_applicable_gap_is_an_error():
    h, t = jev(P.HISTORY_ARM, code_likely_fails=0.7), jev(P.TRACE_ARM, on_task=0.9)
    full = P.jev_vector(h, t, "cheap+code+thinking")
    assert full["jev_code_likely_fails"] == 0.7  # code answers come from the history arm
    assert full["jev_on_task"] == 0.9 and full["jev_repeating_failed_fix"] == 0.0
    code = P.jev_vector(h, t, "cheap+code")
    assert set(full) - set(code) == {f"jev_{q}" for q in P.THINKING_QS}
    assert P.jev_vector(h, t, "cheap") == {}
    h["features"]["code_likely_fails"] = None  # applicable but missing
    with pytest.raises(ValueError):
        P.jev_vector(h, t, "cheap+code")
    h = jev(P.HISTORY_ARM)
    h["applicability"]["code_likely_fails"] = "na:arm_lacks_trace"  # not a structural reason
    h["features"]["code_likely_fails"] = None
    with pytest.raises(ValueError):
        P.jev_vector(h, t, "cheap+code")


def test_matrix_uses_the_frozen_order_and_refuses_a_missing_column():
    cols = P.columns("cheap", True)
    rows = [P.row_vector(feats(1), True, jev(P.HISTORY_ARM), jev(P.TRACE_ARM), "cheap")]
    X = P.matrix(rows, cols)
    assert X.shape == (1, len(cols)) and X[0, cols.index("first_round")] == 1.0
    with pytest.raises(KeyError):
        P.matrix(rows, P.columns("cheap+code", True))


def test_final_model_predicts_like_the_pipeline():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(80, 4))
    X[:, 3] = 1.0  # a constant column stays and does no harm
    y = (X[:, 0] + rng.normal(0, 0.5, 80) > 0).astype(int)
    m = P.fit_final(X, y, ["a", "b", "c", "d"])
    ref = P.make_model().fit(X, y).predict_proba(X)[:, 1]
    assert np.allclose(P.predict_final(m, X), ref)


def test_out_of_fold_scores_never_fit_on_the_scored_task():
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(40), 3)
    y = rng.integers(0, 2, len(groups))
    X = rng.normal(size=(len(groups), 3))
    for fit, score in StratifiedGroupKFold(P.N_FOLDS, shuffle=True, random_state=1).split(X, y, groups):
        assert not set(groups[fit]) & set(groups[score])
    p = P.oof_scores(X, y, groups, seed=1)
    assert p.shape == y.shape and ((p > 0) & (p < 1)).all()


def test_task_weights_give_each_task_total_weight_one():
    g = np.array(["a", "a", "a", "b", "c", "c"])
    w = P.task_weights(g)
    assert np.allclose([w[g == t].sum() for t in "abc"], 1.0)


def test_task_bootstrap_gives_ordered_intervals_pooled_and_weighted():
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(30), 4)
    y = rng.integers(0, 2, len(groups))
    good = y + rng.normal(0, 0.5, len(y))
    noise = rng.normal(size=len(y))
    for weighted in (False, True):
        out = P.task_bootstrap(y, groups, {"noise": noise, "good": good}, [("noise", "good")], n_boot=200,
                               weighted=weighted)
        lo, hi = out["delta"]["good - noise"]
        assert lo <= hi and lo > 0


def load_script(name):
    path = Path(__file__).resolve().parents[1] / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_resource_guide_rebuilds_the_request_hash_like_the_scorer(tmp_path):
    import hashlib

    import httpx

    from system1.eval.ledger import CostLedger
    from system1.features.evidence import Checkpoint
    from system1.features.jev_scoring import JevScorer, ScoreStore, load_rubric
    from system1.routers.jev import JevClient

    rg = load_script("resource_guide")
    cp = Checkpoint(task_id="T", benchmark="mbpp+", attempt=0, round=2, task_prompt="Write f.", code="def f(): pass",
                    visible_test_output="ok", visible_pass=True, thinking="I fixed it.",
                    telemetry={"visible_pass_fraction": 1.0}, prev_code="def f(): 0", prev_test_output="fail")

    def handler(request):
        import json
        body = json.loads(request.content)
        return httpx.Response(200, json={"model": "jev-1.13.0", "usage": {"input_tokens": 1, "output_tokens": 1},
                                         "answers": {q: {"type": "noul", "noul": 0.5} for q in body["questions"]}})

    client = JevClient(api_key="k", transport=httpx.MockTransport(handler), ledger=CostLedger(tmp_path / "l.jsonl"))
    recs = JevScorer(client, load_rubric(), ScoreStore(tmp_path / "s.jsonl"), run_id="r").score_arms(cp)
    hashes = rg.request_hashes(cp, load_rubric(), client.model, client.byte_budget)
    assert {r.arm: r.request_sha256 for r in recs} == hashes
    changed = Checkpoint(**{**cp.__dict__, "code": "def f(): return 1"})
    assert rg.request_hashes(changed, load_rubric(), client.model, client.byte_budget) != hashes
    assert hashlib.sha256(b"").hexdigest() not in hashes.values()


def test_strong4_set_takes_code_answers_from_history_and_thinking_from_trace():
    h = jev(P.HISTORY_ARM, code_likely_fails=0.7, special_cases_visible_tests=0.1)
    t = jev(P.TRACE_ARM, code_likely_fails=0.2, on_task=0.9, unsupported_claim=0.3)
    v = P.jev_vector(h, t, "cheap+strong4")
    assert v == {"jev_code_likely_fails": 0.7, "jev_special_cases_visible_tests": 0.1, "jev_on_task": 0.9,
                 "jev_unsupported_claim": 0.3}
    cols = P.columns("cheap+strong4", True)
    assert cols[:len(P.columns("cheap", True))] == P.columns("cheap", True)
    assert "cheap+strong4" not in P.FEATURE_SETS  # a sensitivity, never a primary set


def test_jev_mean_orients_by_rubric_and_handles_na_and_failures():
    h = jev(P.HISTORY_ARM, code_likely_fails=0.8, special_cases_visible_tests=0.0)
    t = jev(P.TRACE_ARM, on_task=0.9, unsupported_claim=0.5)
    assert P.jev_mean(h, t) == pytest.approx((0.8 + 0.0 + (1 - 0.9) + 0.5) / 4)
    # A structural NA counts as 0.5 and the denominator stays 4.
    t2 = jev(P.TRACE_ARM, on_task=0.9, unsupported_claim=0.5)
    t2["applicability"]["on_task"] = "na:trace_missing"
    t2["features"]["on_task"] = None
    assert P.jev_mean(h, t2) == pytest.approx((0.8 + 0.0 + 0.5 + 0.5) / 4)
    # A failed scoring call makes the score unavailable.
    assert P.jev_mean(h, {**t, "status": "failed"}) is None
    assert "stated_fix_matches_change" in P.TRUE_IS_GOOD and "on_task" in P.TRUE_IS_GOOD


def test_bootstrap_test_finds_a_real_difference_and_not_a_null():
    rng = np.random.default_rng(1)
    groups = np.repeat(np.arange(60), 4)
    strata = np.where(groups < 30, "a", "b")
    y = rng.integers(0, 2, len(groups))
    noise = rng.normal(size=len(y))
    good = y + rng.normal(0, 0.6, len(y))
    r = P.bootstrap_test(y, groups, strata, noise, good, n_boot=999)
    assert r["delta"] > 0 and r["p_two_sided"] < 0.01 and r["ci95"][0] > 0
    r0 = P.bootstrap_test(y, groups, strata, good, good + 1e-9 * rng.normal(size=len(y)), n_boot=999)
    assert r0["p_two_sided"] > 0.5


def test_holm():
    adj = P.holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert adj == pytest.approx({"a": 0.03, "b": 0.06, "c": 0.06})
