"""Dev-only, descriptive: does the thinking change how well Jev's answers separate hidden fail from pass?

Same code questions answered without the thinking (history arm) and with it (trace arm).
Visible-pass checkpoints, y = 1 for hidden fail. No billed calls.
"""
import argparse
import importlib.util
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts" / "resource_guide.py")
rg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rg)
from system1.eval import predict as P  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--run-id", action="append")
args = ap.parse_args()
run_ids = args.run_id or ["pilot-v1", "pilot-v1b"]
data = [d for d in rg.load(run_ids) if d["cp"]["visible_pass"]]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
groups = np.array([d["cp"]["task_id"] for d in data])
w = P.task_weights(groups)
print(f"{len(y)} visible-pass checkpoints, {y.sum()} hidden fail, {len(set(groups[y == 1]))} positive tasks")


def answers(arm_key, q):
    out = []
    for d in data:
        rec = d[arm_key]
        out.append(rec["features"].get(q) if rec["applicability"][q] == "applicable" else np.nan)
    return np.array(out, dtype=float)


print("\n1. Single answers, standalone AUROC (0.5 = no signal; below 0.5 = inverse direction)")
preds, pairs = {}, []
for q in P.CODE_QS:
    h, t = answers("history", q), answers("trace", q)
    ok = ~np.isnan(h) & ~np.isnan(t)
    if len(set(y[ok])) < 2:
        print(f"  {q:34s} n={ok.sum():3d}  (one class only)")
        continue
    ah, at = roc_auc_score(y[ok], h[ok]), roc_auc_score(y[ok], t[ok])
    wk = P.task_weights(groups[ok])  # weights recomputed on the applicable rows
    print(f"  {q:34s} n={ok.sum():3d}  no thinking {ah:.3f}  with thinking {at:.3f}  diff {at - ah:+.3f}"
          f"  | task-weighted {roc_auc_score(y[ok], h[ok], sample_weight=wk):.3f} -> "
          f"{roc_auc_score(y[ok], t[ok], sample_weight=wk):.3f}")
    if ok.all():
        preds[f"{q}/no"], preds[f"{q}/with"] = h, t
        pairs.append((f"{q}/no", f"{q}/with"))
for q in P.THINKING_QS:
    t = answers("trace", q)
    ok = ~np.isnan(t)
    if ok.sum() and len(set(y[ok])) == 2:
        print(f"  {q:34s} n={ok.sum():3d}  with thinking {roc_auc_score(y[ok], t[ok]):.3f}")

if pairs:
    bs = P.task_bootstrap(y, groups, preds, pairs)
    print("  task bootstrap of the with-minus-without difference:")
    for k, (lo, hi) in bs["delta"].items():
        print(f"    {k}: ({lo:+.3f} to {hi:+.3f}), share > 0 = {bs['delta_share_positive'][k]:.2f}")

print("\n2. In the frozen LR (cheap features + answers), out-of-fold, 20 splits")
variants = {
    "cheap": lambda d: P.row_vector(d["cp"]["features"], d["has_trace"], d["history"], d["trace"], "cheap"),
    "cheap+code (no thinking)": lambda d: P.row_vector(d["cp"]["features"], d["has_trace"], d["history"], d["trace"],
                                                       "cheap+code"),
    "cheap+code (with thinking)": lambda d: P.row_vector(d["cp"]["features"], d["has_trace"], d["trace"], d["trace"],
                                                         "cheap+code"),
    "cheap+code+thinking (frozen)": lambda d: P.row_vector(d["cp"]["features"], d["has_trace"], d["history"],
                                                           d["trace"], "cheap+code+thinking"),
    "cheap+code+thinking (all trace arm)": lambda d: P.row_vector(d["cp"]["features"], d["has_trace"], d["trace"],
                                                                  d["trace"], "cheap+code+thinking"),
}
setcols = {"cheap": "cheap", "cheap+code (no thinking)": "cheap+code", "cheap+code (with thinking)": "cheap+code",
           "cheap+code+thinking (frozen)": "cheap+code+thinking",
           "cheap+code+thinking (all trace arm)": "cheap+code+thinking"}
lr = {}
for name, fn in variants.items():
    X = P.matrix([fn(d) for d in data], P.columns(setcols[name], True))
    lr[name] = np.mean([P.oof_scores(X, y, groups, s) for s in range(rg.REPEATS)], axis=0)
    print(f"  {name:38s} AUROC {roc_auc_score(y, lr[name]):.3f}  task-weighted "
          f"{roc_auc_score(y, lr[name], sample_weight=w):.3f}")
lr_pairs = [("cheap+code (no thinking)", "cheap+code (with thinking)"), ("cheap", "cheap+code (with thinking)"),
            ("cheap", "cheap+code+thinking (all trace arm)")]
bs = P.task_bootstrap(y, groups, lr, lr_pairs)
bw = P.task_bootstrap(y, groups, lr, lr_pairs, weighted=True)
for k, (lo, hi) in bs["delta"].items():
    print(f"  d[{k}]: ({lo:+.3f} to {hi:+.3f}); task-weighted ({bw['delta'][k][0]:+.3f} to {bw['delta'][k][1]:+.3f})")
sys.exit(0)
