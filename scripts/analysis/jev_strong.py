"""Dev-only, exploratory: keep only the strong Jev answers (standalone AUROC far from 0.5).

    uv run python scripts/analysis/jev_strong.py

The dev heuristic (chosen October 16 after the per-answer dev results, so it is
not validated by the nested check below): keep an answer if its standalone AUROC
is >= 0.5 + MARGIN or <= 0.5 - MARGIN on at least MIN_ROWS applicable rows. It
picked the four answers that are now frozen by name as predict.STRONG_QS.

The nested check applies the rule inside each outer training part only. It
protects against within-fold selection leakage; it does not account for the
choice of the rule itself. The cheap comparator is fitted on exactly the same
outer folds, so the difference isolates the feature change.

The fixed strong4 mean (predict.jev_mean) is reported on all rows; the nested
mean uses the answers each fold picked, so it is a different estimator.
"""
import contextlib
import io
import runpy
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(str(Path(__file__).with_name("jev_select.py")))
data, y, groups, X, idx, P, oof, cols_of = (g[k] for k in ("data", "y", "groups", "X_all", "idx", "P", "oof",
                                                             "cols_of"))
jev_cols = g["jev_cols"]
MARGIN, MIN_ROWS = 0.20, 100
OUTER_SEEDS = range(200, 205)


def arm_of(c):
    return "history" if c[4:] in P.CODE_QS else "trace"


# Recorded applicability (a structural NA is stored as 0 in X, so never infer it from X).
applies = {c: np.array([d[arm_of(c)]["applicability"][c[4:]] == "applicable" for d in data]) for c in jev_cols}


def strong(rows):
    keep = []
    for c in jev_cols:
        m = rows & applies[c]
        if m.sum() >= MIN_ROWS and len(set(y[m])) == 2:
            if abs(roc_auc_score(y[m], X[m, idx[c]]) - 0.5) >= MARGIN:
                keep.append(c)
    return keep


def oriented_mean(cols, rows):
    """Mean of the chosen answers, oriented by the rubric; structural NA = predict.NA_ORIENTED."""
    parts = []
    for c in cols:
        v = X[rows, idx[c]]
        v = 1.0 - v if c[4:] in P.TRUE_IS_GOOD else v
        parts.append(np.where(applies[c][rows], v, P.NA_ORIENTED))
    return np.mean(parts, axis=0)


sel = strong(np.ones(len(y), bool))
print(f"rule on all dev rows keeps: {sel}  (frozen as predict.STRONG_QS: {P.STRONG_QS})")
assert [c[4:] for c in sel] == P.STRONG_QS

fixed_mean = np.array([P.jev_mean(d["history"], d["trace"]) for d in data])
assert np.allclose(fixed_mean, oriented_mean(sel, np.arange(len(y))))

# Nested, with the cheap comparator on the same outer folds
res = {k: [] for k in ("cheap", "cheap + selected", "selected mean")}
picks = []
for seed in OUTER_SEEDS:
    p = {k: np.full(len(y), np.nan) for k in res}
    for fit, score in StratifiedGroupKFold(P.N_FOLDS, shuffle=True, random_state=seed).split(X, y, groups):
        rows = np.zeros(len(y), bool)
        rows[fit] = True
        k = strong(rows)
        picks.append(tuple(c[4:] for c in k))
        for name, extra in (("cheap", []), ("cheap + selected", k)):
            m = P.make_model().fit(X[fit][:, cols_of(extra)], y[fit])
            p[name][score] = m.predict_proba(X[score][:, cols_of(extra)])[:, 1]
        p["selected mean"][score] = oriented_mean(k, score) if k else 0.5
    for name in res:
        res[name].append(p[name])
nested = {f"nested: {k}": np.mean(v, axis=0) for k, v in res.items()}
nested["fixed strong4 mean (all rows)"] = fixed_mean

pairs = [("nested: cheap", k) for k in nested if k != "nested: cheap"]
bs = P.task_bootstrap(y, groups, nested, pairs)
bw = P.task_bootstrap(y, groups, nested, pairs, weighted=True)
w = P.task_weights(groups)
base = roc_auc_score(y, nested["nested: cheap"])
print(f"\n{'predictor':34s} AUROC  d vs matched cheap (task bootstrap)  task-weighted d")
print(f"{'nested: cheap':34s} {base:.3f}")
for k in nested:
    if k == "nested: cheap":
        continue
    a = roc_auc_score(y, nested[k])
    lo, hi = bs["delta"][f"{k} - nested: cheap"]
    wlo, whi = bw["delta"][f"{k} - nested: cheap"]
    dw = roc_auc_score(y, nested[k], sample_weight=w) - roc_auc_score(y, nested["nested: cheap"], sample_weight=w)
    print(f"{k:34s} {a:.3f}  {a - base:+.3f} ({lo:+.3f} to {hi:+.3f})        {dw:+.3f} ({wlo:+.3f} to {whi:+.3f})")
print("\nnested picks:", Counter(picks).most_common())

print("\nby subgroup (fixed strong4 mean vs the 20-split cheap LR):")
for name, m in g["sub"].items():
    if len(set(y[m])) < 2:
        continue
    print(f"  {name:12s} n={m.sum():3d}  cheap {roc_auc_score(y[m], g['preds']['cheap'][m]):.3f}  "
          f"strong4 mean {roc_auc_score(y[m], fixed_mean[m]):.3f}")
