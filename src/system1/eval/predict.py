"""Checkpoint-failure predictors: a fixed feature schema, the pipeline, grouped out-of-fold AUROC.

The feature sets follow docs/research-plan.md (primary and secondary claims):

    cheap                cheap features only
    cheap+code           + Jev's three code answers from the history arm
    cheap+code+thinking  + Jev's thinking answers from the trace arm
                         (the primary Jev feature set; also the secondary
                         contrast's second side)

The columns come from this schema, never from the data, so development and
test rows always get the same columns in the same order. Missing values:

  * structural (the value cannot exist by design): history features and
    history questions in round 1, thinking questions without a trace,
    clear_next_step at a visible pass. Zero-filled with no own indicator;
    the shared indicators first_round and trace_missing, present in every
    feature set, carry the condition once.
  * anything else (e.g. similarity_to_previous when a round had no code, a
    logprob summary that could not be computed): zero-filled plus a
    per-feature indicator.
  * a Jev question that applied but has no value is an error, never filled.

clear_next_step is not applicable at a visible pass, so it is not in the
visible-pass predictor. The pipeline is fixed: standard scaling, then an L2
logistic regression with C = 1. Folds are grouped by task.

Sensitivity analyses (descriptive, never the primary result). On October 16,
after the predict-v2 freeze and after inspecting development outcomes (no test
trajectory existed), the four answers in STRONG_QS were selected on
development data and frozen as named:

    cheap+strong4   cheap features + the four answers (code answers from the
                    history arm, thinking answers from the trace arm)
    strong4 mean    an equal-weight mean of the four answers, oriented so that
                    higher = more likely to fail (directions from the rubric
                    text); not a calibrated probability (jev_mean)
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

PIPELINE_VERSION = "predict-v2"
C = 1.0
N_FOLDS = 5

# Cheap features (plan: visible tests passed, round, error type, code length,
# trace statistics, structural repeats, a small prespecified logprob summary).
CHEAP_NUMERIC = ["round", "visible_pass_fraction", "visible_not_run_count", "code_lines", "marker_count"]
LOGPROB = ["thinking_mean_logprob", "thinking_tail_conf", "thinking_bottom10_group_conf", "answer_mean_logprob"]
CHEAP_BOOL = ["visible_pass", "cap_hit", "think_closed", "loop_flag", "code_missing"]
# The six telemetry numbers that Jev also gets (telemetry.JEV_TELEMETRY_KEYS), minus
# visible_pass_fraction, which is above: missing by design in round 1.
CHEAP_HISTORY = ["pass_count_delta", "similarity_to_previous", "same_error_as_previous",
                 "same_failing_tests_as_previous", "returns_to_earlier_code"]
ERRORS = ["err_AssertionError", "err_Timeout", "err_load", "err_other"]
SHARED = ["first_round", "trace_missing"]

CODE_QS = ["code_likely_fails", "special_cases_visible_tests", "repeats_previous_code"]
THINKING_QS = ["on_task", "repeating_failed_fix", "approach_change_without_evidence", "unsupported_claim",
               "stated_fix_matches_change", "clear_next_step"]
FEATURE_SETS = ("cheap", "cheap+code", "cheap+code+thinking")
STRONG_QS = ["code_likely_fails", "special_cases_visible_tests", "on_task", "unsupported_claim"]
SENSITIVITY_SETS = ("cheap+strong4",)
# rubric_v2.yaml: "true" means trouble for every question except these two.
TRUE_IS_GOOD = {"on_task", "stated_fix_matches_change"}
NA_ORIENTED = 0.5  # a structurally unavailable component of the mean counts as neutral
HISTORY_ARM, TRACE_ARM = "base+history", "base+history+trace"
# Reasons for a structural NA (jev_scoring.applicability); "arm_lacks_*" never
# happens for the arm each question is read from.
STRUCTURAL_NA = {"first_round", "trace_missing", "visible_pass"}


def _num(x) -> float | None:
    if x is None:
        return None
    v = float(x)
    return v if math.isfinite(v) else None


def columns(feature_set: str, visible_pass_only: bool) -> list[str]:
    """The frozen column order of a feature set."""
    cols = (CHEAP_NUMERIC + ["log_thinking_tokens"] + LOGPROB + [f"{k}__missing" for k in LOGPROB]
            + CHEAP_BOOL + CHEAP_HISTORY + [f"{k}__missing" for k in CHEAP_HISTORY] + ERRORS + SHARED)
    if feature_set in ("cheap+code", "cheap+code+thinking"):
        cols += [f"jev_{q}" for q in CODE_QS]
    if feature_set == "cheap+code+thinking":
        cols += [f"jev_{q}" for q in THINKING_QS if not (visible_pass_only and q == "clear_next_step")]
    if feature_set == "cheap+strong4":
        cols += [f"jev_{q}" for q in STRONG_QS]
    if feature_set not in FEATURE_SETS + SENSITIVITY_SETS:
        raise ValueError(f"unknown feature set {feature_set!r}")
    return cols


def cheap_vector(f: dict, has_trace: bool) -> dict[str, float]:
    out: dict[str, float] = {k: _num(f.get(k)) for k in CHEAP_NUMERIC}
    if any(v is None for v in out.values()):
        raise ValueError(f"cheap feature missing: {[k for k, v in out.items() if v is None]}")
    out["log_thinking_tokens"] = math.log1p(float(f["thinking_tokens"]))
    for k in LOGPROB:
        v = _num(f.get(k))
        out[k], out[f"{k}__missing"] = (0.0, 1.0) if v is None else (v, 0.0)
    out.update({k: float(bool(f.get(k))) for k in CHEAP_BOOL})
    first = int(f["round"]) == 1
    for k in CHEAP_HISTORY:
        v = _num(f.get(k))
        out[k] = 0.0 if v is None else v
        out[f"{k}__missing"] = float(v is None and not first)  # structural in round 1: no own indicator
    errs = set(f.get("error_types") or [])
    load = f.get("execution_stage") == "load"
    out["err_AssertionError"] = float("AssertionError" in errs)
    out["err_Timeout"] = float("Timeout" in errs)  # visible_runner.py: execution error_type "Timeout"
    out["err_load"] = float(load)
    out["err_other"] = float(bool(errs - {"AssertionError", "Timeout"}) and not load)
    out["first_round"] = float(first)
    out["trace_missing"] = float(not has_trace)
    return out


def jev_vector(history: dict, trace: dict, feature_set: str) -> dict[str, float]:
    """Jev answers of a feature set. A structural NA becomes 0 (the shared indicators carry it);
    an applicable question without a value is an error."""
    out: dict[str, float] = {}
    qs = []
    if feature_set in ("cheap+code", "cheap+code+thinking"):
        qs += [(q, history) for q in CODE_QS]
    if feature_set == "cheap+code+thinking":
        qs += [(q, trace) for q in THINKING_QS]
    if feature_set == "cheap+strong4":
        qs += [(q, history if q in CODE_QS else trace) for q in STRONG_QS]
    for q, rec in qs:
        app = rec["applicability"][q]
        v = _num(rec["features"].get(q))
        if app == "applicable":
            if v is None:
                raise ValueError(f"{rec['checkpoint_id']} {rec['arm']}: {q} applies but has no value")
            out[f"jev_{q}"] = v
        else:
            reasons = set(app.removeprefix("na:").split(","))
            if not reasons <= STRUCTURAL_NA:
                raise ValueError(f"{rec['checkpoint_id']} {rec['arm']}: {q} not applicable for {app}")
            out[f"jev_{q}"] = 0.0
    return out


def jev_mean(history: dict, trace: dict, qs: list[str] = STRONG_QS) -> float | None:
    """The frozen equal-weight Jev score: the mean of the oriented answers (higher = more
    likely to fail). A structurally unavailable answer counts as NA_ORIENTED and the
    denominator stays len(qs). A record that is not "ok" (a failed scoring call) makes the
    score unavailable (None); such rows are counted and left out, never filled."""
    vals = []
    for q in qs:
        rec = history if q in CODE_QS else trace
        if rec.get("status", "ok") != "ok":
            return None
        if rec["applicability"][q] != "applicable":
            reasons = set(rec["applicability"][q].removeprefix("na:").split(","))
            if not reasons <= STRUCTURAL_NA:
                raise ValueError(f"{rec['checkpoint_id']} {rec['arm']}: {q} not applicable for {reasons}")
            vals.append(NA_ORIENTED)
            continue
        v = _num(rec["features"].get(q))
        if v is None:
            raise ValueError(f"{rec['checkpoint_id']} {rec['arm']}: {q} applies but has no value")
        vals.append(1.0 - v if q in TRUE_IS_GOOD else v)
    return float(np.mean(vals))


def row_vector(cp_features: dict, has_trace: bool, history: dict, trace: dict, feature_set: str) -> dict[str, float]:
    return {**cheap_vector(cp_features, has_trace), **jev_vector(history, trace, feature_set)}


def matrix(rows: list[dict[str, float]], cols: list[str]) -> np.ndarray:
    """Rows in the frozen column order; a missing key is an error, extra keys are ignored."""
    return np.array([[r[c] for c in cols] for r in rows], dtype=float)


def make_model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=5000))


def fit_final(X: np.ndarray, y: np.ndarray, cols: list[str]) -> dict:
    """The test predictor: one LR refitted on all eligible development rows, in a portable form."""
    m = make_model().fit(X, y)
    sc, lr = m[0], m[-1]
    return {"pipeline": PIPELINE_VERSION, "C": C, "columns": cols, "mean": sc.mean_.tolist(),
            "scale": sc.scale_.tolist(), "coef": lr.coef_[0].tolist(), "intercept": float(lr.intercept_[0]),
            "n": int(len(y)), "positives": int(y.sum())}


def predict_final(model: dict, X: np.ndarray) -> np.ndarray:
    z = (X - np.array(model["mean"])) / np.array(model["scale"])
    return 1 / (1 + np.exp(-(z @ np.array(model["coef"]) + model["intercept"])))


def oof_scores(X: np.ndarray, y: np.ndarray, groups: np.ndarray, seed: int) -> np.ndarray:
    """Out-of-fold predicted failure probabilities, folds grouped by task."""
    pred = np.full(len(y), np.nan)
    for fit, score in StratifiedGroupKFold(N_FOLDS, shuffle=True, random_state=seed).split(X, y, groups):
        if set(groups[fit]) & set(groups[score]):
            raise AssertionError("a task is in both the fitted and the scored part")
        m = make_model().fit(X[fit], y[fit])
        pred[score] = m.predict_proba(X[score])[:, 1]
    assert not np.isnan(pred).any()
    return pred


def task_weights(groups: np.ndarray) -> np.ndarray:
    """Weights that give each task the same total weight (for the task-weighted sensitivity)."""
    _, inv, counts = np.unique(groups, return_inverse=True, return_counts=True)
    return 1.0 / counts[inv]


def task_bootstrap(y: np.ndarray, groups: np.ndarray, preds: dict[str, np.ndarray], pairs: list[tuple[str, str]],
                   n_boot: int = 2000, seed: int = 0, weighted: bool = False) -> dict:
    """Percentile intervals for AUROC and paired dAUROC, resampling whole tasks over fixed
    out-of-fold predictions (the model fitting is not redone, so this is descriptive)."""
    rng = np.random.default_rng(seed)
    tasks = np.unique(groups)
    idx = {t: np.flatnonzero(groups == t) for t in tasks}
    auc = {k: [] for k in preds}
    delta = {p: [] for p in pairs}
    for _ in range(n_boot):
        rows = np.concatenate([idx[t] for t in rng.choice(tasks, len(tasks), replace=True)])
        if len(set(y[rows])) < 2:
            continue
        # A task drawn twice keeps both copies; each copy has total weight 1.
        w = 1.0 / np.array([len(idx[g]) for g in groups[rows]]) if weighted else None
        a = {k: roc_auc_score(y[rows], p[rows], sample_weight=w) for k, p in preds.items()}
        for k in preds:
            auc[k].append(a[k])
        for lo, hi in pairs:
            delta[(lo, hi)].append(a[hi] - a[lo])
    ci = lambda v: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))
    return {"auroc": {k: ci(v) for k, v in auc.items()},
            "delta": {f"{hi} - {lo}": ci(v) for (lo, hi), v in delta.items()},
            # Share of resamples with a positive difference: descriptive, not a probability that it helps.
            "delta_share_positive": {f"{hi} - {lo}": float(np.mean(np.array(v) > 0)) for (lo, hi), v in delta.items()}}


def bootstrap_test(y: np.ndarray, groups: np.ndarray, strata: np.ndarray, score_a: np.ndarray,
                   score_b: np.ndarray, n_boot: int = 19_999, seed: int = 0) -> dict:
    """Two-sided paired task bootstrap test of dAUROC = AUROC(b) - AUROC(a), centered on
    the null (Hall and Wilson): whole tasks are resampled within each stratum (benchmark)
    with all their rows and both scores; p = (1 + #{|d* - d| >= |d|}) / (B + 1). Also
    returns the unadjusted percentile interval of d. Asymptotic, not exact."""
    rng = np.random.default_rng(seed)
    d_hat = roc_auc_score(y, score_b) - roc_auc_score(y, score_a)
    by_stratum = {s: np.unique(groups[strata == s]) for s in np.unique(strata)}
    idx = {t: np.flatnonzero(groups == t) for t in np.unique(groups)}
    ds = []
    for _ in range(n_boot):
        rows = np.concatenate([idx[t] for ts in by_stratum.values() for t in rng.choice(ts, len(ts), replace=True)])
        if len(set(y[rows])) < 2:
            continue
        ds.append(roc_auc_score(y[rows], score_b[rows]) - roc_auc_score(y[rows], score_a[rows]))
    ds = np.array(ds)
    p = (1 + np.sum(np.abs(ds - d_hat) >= abs(d_hat))) / (len(ds) + 1)
    return {"delta": float(d_hat), "p_two_sided": float(p), "n_boot": int(len(ds)),
            "ci95": (float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5)))}


def holm(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm-adjusted p-values (familywise), in the input order."""
    order = sorted(pvalues, key=pvalues.get)
    m, out, running = len(order), {}, 0.0
    for i, k in enumerate(order):
        running = max(running, min(1.0, (m - i) * pvalues[k]))
        out[k] = running
    return {k: out[k] for k in pvalues}


# Table 1 standalone comparator (frozen October 17): the DeepConf-style tail confidence of the
# thinking (minus the mean top-5 logprob over the last <= 1,024 thinking tokens; generate.py).
# Lower confidence = more likely to fail, so the score is its negative. Valid scores are <= 0;
# a missing value (no thinking tokens) gets the finite score 1.0, the highest failure rank, and all
# missing values tie. Its count is reported.
LOGPROB_MISSING_SCORE = 1.0


def logprob_comparator(features: dict) -> float:
    v = _num(features.get("thinking_tail_conf"))
    return LOGPROB_MISSING_SCORE if v is None else -v


def fnr_at_fpr(y: np.ndarray, scores: np.ndarray, max_fpr: float = 0.05) -> dict:
    """Miss rate at the most permissive threshold whose false-positive rate is <= max_fpr
    (frozen convention: thresholds at the observed score values, rule "escalate if s >= t",
    no interpolation between ROC points; ties stay together). y = 1 for a hidden fail."""
    y, s = np.asarray(y), np.asarray(scores, float)
    neg, pos = (y == 0), (y == 1)
    best = {"threshold": float("inf"), "fpr": 0.0, "fnr": 1.0}
    for t in np.unique(s)[::-1]:
        esc = s >= t
        fpr = float(esc[neg].mean())
        if fpr > max_fpr:
            break
        best = {"threshold": float(t), "fpr": fpr, "fnr": float(1 - esc[pos].mean())}
    return best
