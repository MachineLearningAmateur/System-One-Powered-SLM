"""Checkpoint-failure predictors: feature sets, the pipeline, grouped out-of-fold AUROC.

The feature sets follow docs/research-plan.md (primary and secondary claims):

    cheap                cheap features only
    cheap+code           + Jev's three code answers from the history arm
    cheap+code+thinking  + Jev's six thinking answers from the trace arm
                         (the primary Jev feature set; also the secondary
                         contrast's second side)

The pipeline is fixed: missing values -> 0 plus a missing indicator for each
feature that can be missing, standard scaling, L2 logistic regression with
C = 1. Folds are grouped by task, so no task is in both the fitting and the
scored part. Nothing here reads test-split data; the caller decides the rows.
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

PIPELINE_VERSION = "predict-v1"
C = 1.0
N_FOLDS = 5

# Cheap features (plan: visible tests passed, round, error type, code length,
# trace statistics, structural repeats, a small prespecified logprob summary).
CHEAP_NUMERIC = [
    "round", "visible_pass_fraction", "visible_not_run_count", "code_lines", "marker_count",
    "thinking_mean_logprob", "thinking_tail_conf", "thinking_bottom10_group_conf", "answer_mean_logprob",
]
CHEAP_LOG = ["thinking_tokens"]  # log1p, because the length is heavy tailed
CHEAP_BOOL = ["cap_hit", "think_closed", "loop_flag", "code_missing"]
CHEAP_HISTORY = ["pass_count_delta", "similarity_to_previous", "same_error_as_previous", "returns_to_earlier_code"]
ERROR_TYPES = ["AssertionError", "timeout", "load", "other_error"]

CODE_QS = ["code_likely_fails", "special_cases_visible_tests", "repeats_previous_code"]
THINKING_QS = ["on_task", "repeating_failed_fix", "approach_change_without_evidence", "unsupported_claim",
               "stated_fix_matches_change", "clear_next_step"]
FEATURE_SETS = ("cheap", "cheap+code", "cheap+code+thinking")
HISTORY_ARM, TRACE_ARM = "base+history", "base+history+trace"


def _num(x) -> float | None:
    if x is None or isinstance(x, bool):
        return None if x is None else float(x)
    v = float(x)
    return v if math.isfinite(v) else None


def cheap_vector(f: dict) -> dict[str, float | None]:
    out: dict[str, float | None] = {k: _num(f.get(k)) for k in CHEAP_NUMERIC}
    t = _num(f.get("thinking_tokens"))
    out["log_thinking_tokens"] = None if t is None else math.log1p(t)
    out.update({k: float(bool(f.get(k))) for k in CHEAP_BOOL})
    out.update({k: _num(f.get(k)) for k in CHEAP_HISTORY})
    errs = set(f.get("error_types") or [])
    stage = f.get("execution_stage")
    out["err_AssertionError"] = float("AssertionError" in errs)
    out["err_timeout"] = float("timeout" in errs)
    out["err_load"] = float(stage == "load")
    out["err_other_error"] = float(bool(errs - {"AssertionError", "timeout"}) and stage != "load")
    return out


def jev_vector(history: dict, trace: dict, sets: str) -> dict[str, float | None]:
    """Jev answers for a feature set; a question that does not apply is None."""
    out: dict[str, float | None] = {}
    if sets in ("cheap+code", "cheap+code+thinking"):
        out.update({f"jev_{q}": _num(history["features"].get(q)) for q in CODE_QS})
    if sets == "cheap+code+thinking":
        out.update({f"jev_{q}": _num(trace["features"].get(q)) for q in THINKING_QS})
    return out


@dataclass
class Design:
    X: np.ndarray
    columns: list[str]


def design(rows: list[dict[str, float | None]]) -> Design:
    """Missing -> 0 plus an indicator; constant columns are dropped (they carry nothing)."""
    keys = sorted({k for r in rows for k in r})
    cols, data = [], []
    for k in keys:
        v = [r.get(k) for r in rows]
        miss = [x is None for x in v]
        filled = [0.0 if x is None else x for x in v]
        for name, col in ((k, filled), (f"{k}__missing", [float(m) for m in miss])):
            if name.endswith("__missing") and not any(miss):
                continue
            if len(set(col)) > 1:
                cols.append(name)
                data.append(col)
    return Design(np.array(data, dtype=float).T if data else np.zeros((len(rows), 0)), cols)


def make_model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=5000))


def oof_scores(X: np.ndarray, y: np.ndarray, groups: np.ndarray, seed: int) -> np.ndarray:
    """Out-of-fold predicted failure probabilities, folds grouped by task."""
    pred = np.full(len(y), np.nan)
    for fit, score in StratifiedGroupKFold(N_FOLDS, shuffle=True, random_state=seed).split(X, y, groups):
        m = make_model().fit(X[fit], y[fit])
        pred[score] = m.predict_proba(X[score])[:, 1]
    assert not np.isnan(pred).any()
    return pred


def task_bootstrap(y: np.ndarray, groups: np.ndarray, preds: dict[str, np.ndarray], pairs: list[tuple[str, str]],
                   n_boot: int = 2000, seed: int = 0) -> dict:
    """Percentile intervals for AUROC and paired dAUROC, resampling whole tasks."""
    rng = np.random.default_rng(seed)
    tasks = np.unique(groups)
    idx = {t: np.flatnonzero(groups == t) for t in tasks}
    auc = {k: [] for k in preds}
    delta = {p: [] for p in pairs}
    for _ in range(n_boot):
        rows = np.concatenate([idx[t] for t in rng.choice(tasks, len(tasks), replace=True)])
        if len(set(y[rows])) < 2:
            continue
        a = {k: roc_auc_score(y[rows], p[rows]) for k, p in preds.items()}
        for k in preds:
            auc[k].append(a[k])
        for lo, hi in pairs:
            delta[(lo, hi)].append(a[hi] - a[lo])
    ci = lambda v: (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)))
    return {"auroc": {k: ci(v) for k, v in auc.items()}, "delta": {f"{hi} - {lo}": ci(v) for (lo, hi), v in delta.items()},
            "delta_share_positive": {f"{hi} - {lo}": float(np.mean(np.array(v) > 0)) for (lo, hi), v in delta.items()}}
