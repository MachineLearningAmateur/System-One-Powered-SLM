import numpy as np
from sklearn.model_selection import StratifiedGroupKFold

from system1.eval import predict as P


def test_design_fills_missing_with_zero_plus_indicator_and_drops_constants():
    d = P.design([{"a": 1.0, "b": None, "c": 5.0}, {"a": 2.0, "b": 3.0, "c": 5.0}])
    assert d.columns == ["a", "b", "b__missing"]  # c is constant
    assert d.X.tolist() == [[1.0, 0.0, 1.0], [2.0, 3.0, 0.0]]


def test_feature_sets_differ_only_by_their_jev_block():
    hist = {"features": {"code_likely_fails": 0.7, "special_cases_visible_tests": 0.1, "repeats_previous_code": None,
                         "on_task": None}}
    trace = {"features": {q: 0.5 for q in P.THINKING_QS + P.CODE_QS}}
    code = P.jev_vector(hist, trace, "cheap+code")
    full = P.jev_vector(hist, trace, "cheap+code+thinking")
    assert P.jev_vector(hist, trace, "cheap") == {}
    assert code["jev_code_likely_fails"] == 0.7  # code answers come from the history arm
    assert set(full) - set(code) == {f"jev_{q}" for q in P.THINKING_QS}
    assert all(full[k] == v for k, v in code.items())


def test_cheap_vector_handles_first_round_and_errors():
    f = {"round": 1, "visible_pass_fraction": 0.0, "thinking_tokens": 99, "cap_hit": True, "error_types": ["NameError"],
         "execution_stage": "load", "pass_count_delta": None}
    v = P.cheap_vector(f)
    assert v["cap_hit"] == 1.0 and v["err_load"] == 1.0 and v["err_other_error"] == 0.0
    assert v["pass_count_delta"] is None and abs(v["log_thinking_tokens"] - np.log(100)) < 1e-9


def test_out_of_fold_scores_never_fit_on_the_scored_task():
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(40), 3)
    y = rng.integers(0, 2, len(groups))
    X = rng.normal(size=(len(groups), 3))
    for fit, score in StratifiedGroupKFold(P.N_FOLDS, shuffle=True, random_state=1).split(X, y, groups):
        assert not set(groups[fit]) & set(groups[score])
    p = P.oof_scores(X, y, groups, seed=1)
    assert p.shape == y.shape and ((p > 0) & (p < 1)).all()


def test_task_bootstrap_gives_ordered_intervals():
    rng = np.random.default_rng(0)
    groups = np.repeat(np.arange(30), 4)
    y = rng.integers(0, 2, len(groups))
    good = y + rng.normal(0, 0.5, len(y))
    noise = rng.normal(size=len(y))
    out = P.task_bootstrap(y, groups, {"noise": noise, "good": good}, [("noise", "good")], n_boot=200)
    lo, hi = out["delta"]["good - noise"]
    assert lo <= hi and lo > 0
