"""Dev-only, exploratory: what does each Jev answer add, and what would feature selection honestly buy?

    uv run python scripts/analysis/jev_select.py

Visible-pass dev checkpoints, y = 1 for hidden fail. No Jev calls.

1. Add-one: cheap + one Jev answer against cheap (out-of-fold, task bootstrap of the difference).
2. Where Jev is strong: standalone AUROC of the round-1 answers by benchmark, cap hit and round.
3. Nested selection: inside each outer training part, a forward selection of Jev answers by inner
   grouped CV; the outer part, never seen by the selection, grades it. This is the honest estimate
   of "pick the strong features"; the plain (non-nested) number is printed next to it to show the
   optimism.
"""
import importlib.util
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts" / "resource_guide.py")
rg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rg)
from system1.eval import predict as P  # noqa: E402

MIN_GAIN = 0.005  # inner-CV AUROC gain needed to add one more answer
OUTER_SEEDS = range(5)

data = [d for d in rg.load(["pilot-v1", "pilot-v1b"]) if d["cp"]["visible_pass"]]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
groups = np.array([d["cp"]["task_id"] for d in data])
cheap_cols = P.columns("cheap", True)
jev_cols = [c for c in P.columns("cheap+code+thinking", True) if c.startswith("jev_")]
rows = [P.row_vector(d["cp"]["features"], d["has_trace"], d["history"], d["trace"], "cheap+code+thinking")
        for d in data]
X_all = P.matrix(rows, cheap_cols + jev_cols)
idx = {c: i for i, c in enumerate(cheap_cols + jev_cols)}
print(f"{len(y)} visible-pass checkpoints, {y.sum()} hidden fail, {len(set(groups[y == 1]))} positive tasks")


def cols_of(extra):
    return [idx[c] for c in cheap_cols + list(extra)]


def oof(X, yy, gg, seeds):
    return np.mean([P.oof_scores(X, yy, gg, s) for s in seeds], axis=0)


# 1. Add-one
print("\n1. Add-one: cheap + one Jev answer (out-of-fold, 20 splits)")
preds = {"cheap": oof(X_all[:, cols_of([])], y, groups, range(rg.REPEATS))}
for c in jev_cols:
    preds[c] = oof(X_all[:, cols_of([c])], y, groups, range(rg.REPEATS))
preds["all"] = oof(X_all, y, groups, range(rg.REPEATS))
bs = P.task_bootstrap(y, groups, preds, [("cheap", c) for c in jev_cols + ["all"]])
base = roc_auc_score(y, preds["cheap"])
print(f"  {'cheap':40s} {base:.3f}")
for c in jev_cols + ["all"]:
    a = roc_auc_score(y, preds[c])
    lo, hi = bs["delta"][f"{c} - cheap"]
    print(f"  + {c:38s} {a:.3f}  d {a - base:+.3f} ({lo:+.3f} to {hi:+.3f})")

# 2. Where Jev is strong (round-1 answers, standalone)
print("\n2. Standalone AUROC by subgroup (on_task shown as 1 - AUROC, so higher = better separator)")
sub = {
    "all": np.ones(len(y), bool),
    "HumanEval+": np.array([d["cp"]["benchmark"] == "humaneval+" for d in data]),
    "MBPP+": np.array([d["cp"]["benchmark"] == "mbpp+" for d in data]),
    "cap hit": np.array([bool(d["cp"]["features"]["cap_hit"]) for d in data]),
    "no cap hit": np.array([not d["cp"]["features"]["cap_hit"] for d in data]),
    "round 1": np.array([d["cp"]["round"] == 1 for d in data]),
    "round 2+": np.array([d["cp"]["round"] > 1 for d in data]),
}
show = ["jev_code_likely_fails", "jev_special_cases_visible_tests", "jev_on_task", "jev_unsupported_claim"]
print(f"  {'subgroup':12s} {'n':>4s} {'fail':>5s}  " + "  ".join(f"{c[4:]:>18.18s}" for c in show) + "  cheap(oof)")
for name, m in sub.items():
    if len(set(y[m])) < 2:
        print(f"  {name:12s} {m.sum():4d} {y[m].sum():5d}  (one class only)")
        continue
    vals = []
    for c in show:
        arm = "history" if c[4:] in P.CODE_QS else "trace"
        ok = m & np.array([d[arm]["applicability"][c[4:]] == "applicable" for d in data])  # recorded applicability
        a = roc_auc_score(y[ok], X_all[ok, idx[c]]) if len(set(y[ok])) == 2 else float("nan")
        vals.append(1 - a if c == "jev_on_task" else a)
    print(f"  {name:12s} {m.sum():4d} {y[m].sum():5d}  " + "  ".join(f"{v:18.3f}" for v in vals)
          + f"  {roc_auc_score(y[m], preds['cheap'][m]):.3f}")


# 3. Nested forward selection
def inner_auc(X, yy, gg, extra):
    return roc_auc_score(yy, oof(X[:, cols_of(extra)], yy, gg, [0]))


def select(X, yy, gg):
    chosen, best = [], inner_auc(X, yy, gg, [])
    while True:
        cand = [(inner_auc(X, yy, gg, chosen + [c]), c) for c in jev_cols if c not in chosen]
        if not cand:
            return chosen
        a, c = max(cand)
        if a - best < MIN_GAIN:
            return chosen
        chosen, best = chosen + [c], a


print(f"\n3. Nested forward selection (min inner gain {MIN_GAIN}); outer 5 folds x {len(OUTER_SEEDS)} seeds")
picked, nested, cheap_outer = Counter(), [], []
n_sel = 0
for seed in OUTER_SEEDS:
    p_sel, p_cheap = np.full(len(y), np.nan), np.full(len(y), np.nan)
    for fit, score in StratifiedGroupKFold(P.N_FOLDS, shuffle=True, random_state=100 + seed).split(X_all, y, groups):
        chosen = select(X_all[fit], y[fit], groups[fit])
        picked.update(chosen or ["(none)"])
        n_sel += 1
        for p, extra in ((p_sel, chosen), (p_cheap, [])):
            m = P.make_model().fit(X_all[fit][:, cols_of(extra)], y[fit])
            p[score] = m.predict_proba(X_all[score][:, cols_of(extra)])[:, 1]
    nested.append(p_sel)
    cheap_outer.append(p_cheap)
a_sel, a_cheap = roc_auc_score(y, np.mean(nested, 0)), roc_auc_score(y, np.mean(cheap_outer, 0))
bsn = P.task_bootstrap(y, groups, {"cheap": np.mean(cheap_outer, 0), "selected": np.mean(nested, 0)},
                       [("cheap", "selected")])
lo, hi = bsn["delta"]["selected - cheap"]
print(f"  honest (nested): cheap {a_cheap:.3f}, selected {a_sel:.3f}, d {a_sel - a_cheap:+.3f} ({lo:+.3f} to {hi:+.3f})")
print(f"  how often each answer was picked ({n_sel} selections):")
for c, k in picked.most_common():
    print(f"    {c:40s} {k}/{n_sel}")

# 4. Without logprobs (a model or API that does not return them)
print("\n4. Without the logprob columns (black-box setting)")
no_lp = [c for c in cheap_cols if not any(c.startswith(k) for k in P.LOGPROB)]
code_cols = [f"jev_{q}" for q in P.CODE_QS]
bb = {"cheap": preds["cheap"],
      "cheap - logprobs": oof(X_all[:, [idx[c] for c in no_lp]], y, groups, range(rg.REPEATS)),
      "cheap - logprobs + code": oof(X_all[:, [idx[c] for c in no_lp + code_cols]], y, groups, range(rg.REPEATS)),
      "cheap - logprobs + all Jev": oof(X_all[:, [idx[c] for c in no_lp + jev_cols]], y, groups, range(rg.REPEATS)),
      "Jev answers only": oof(X_all[:, [idx[c] for c in jev_cols + ["first_round", "trace_missing"]]], y, groups,
                              range(rg.REPEATS))}
bsb = P.task_bootstrap(y, groups, bb, [("cheap - logprobs", "cheap - logprobs + code"),
                                       ("cheap - logprobs", "cheap - logprobs + all Jev"),
                                       ("cheap", "Jev answers only")])
for k, p in bb.items():
    print(f"  {k:30s} {roc_auc_score(y, p):.3f}")
for k, (lo, hi) in bsb["delta"].items():
    print(f"  d[{k}]: ({lo:+.3f} to {hi:+.3f})")

full_choice = select(X_all, y, groups)
a_plain = roc_auc_score(y, oof(X_all[:, cols_of(full_choice)], y, groups, range(rg.REPEATS)))
print(f"  optimistic (select and grade on the same data): {full_choice} -> {a_plain:.3f}")
