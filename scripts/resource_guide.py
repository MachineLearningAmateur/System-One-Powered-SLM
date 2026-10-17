"""Resource guide on development checkpoints (docs/research-plan.md, Go/no-go 3).

    uv run python scripts/resource_guide.py --run-id pilot-v1 --run-id pilot-v1b

On the visible-pass development checkpoints, compares the cheap-feature
logistic regression with and without Jev's features, with task-grouped
out-of-fold predictions (averaged over REPEATS fold splits) and a task
bootstrap. Rule: if cheap+code+thinking beats cheap by at least 0.03 AUROC,
spend the time on the full typed questions and the drift labels; if not, keep
Jev in the primary comparison but cut those extras first. This is a guide for
effort, not a result: development data only.
"""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

from system1.config import RESULTS
from system1.eval import predict as P
from system1.eval.labels import load_labelled
from system1.eval.ledger import CostLedger

GUIDE_GAIN = 0.03
REPEATS = 20


def load(run_ids: list[str]) -> list[dict]:
    out = []
    for rid in run_ids:
        d = RESULTS / "runs" / rid
        rows, bad = CostLedger(d / "jev_scores.jsonl").read()
        if bad:
            raise RuntimeError(f"{rid}: {len(bad)} damaged lines in jev_scores.jsonl")
        scores = {(r["checkpoint_id"], r["arm"]): r for r in rows}  # last record wins
        for c in load_labelled(d):
            h, t = scores.get((c["checkpoint_id"], P.HISTORY_ARM)), scores.get((c["checkpoint_id"], P.TRACE_ARM))
            if not (h and t and h["status"] == "ok" and t["status"] == "ok"):
                raise RuntimeError(f"{rid} {c['checkpoint_id']}: Jev scores missing or not ok")
            out.append({"run": rid, "cp": c, "history": h, "trace": t})
    return out


def evaluate(data: list[dict], label: str) -> dict:
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
    groups = np.array([d["cp"]["task_id"] for d in data])
    preds, per_seed, cols = {}, {}, {}
    for fs in P.FEATURE_SETS:
        rows = [{**P.cheap_vector(d["cp"]["features"]), **P.jev_vector(d["history"], d["trace"], fs)} for d in data]
        des = P.design(rows)
        runs = [P.oof_scores(des.X, y, groups, seed) for seed in range(REPEATS)]
        per_seed[fs] = [roc_auc_score(y, p) for p in runs]
        preds[fs] = np.mean(runs, axis=0)
        cols[fs] = des.columns
    pairs = [("cheap", "cheap+code+thinking"), ("cheap+code", "cheap+code+thinking"), ("cheap", "cheap+code")]
    boot = P.task_bootstrap(y, groups, preds, pairs)
    res = {"subset": label, "n": len(y), "positives": int(y.sum()), "tasks": len(set(groups)),
           "auroc": {fs: roc_auc_score(y, p) for fs, p in preds.items()},
           "auroc_per_split_range": {fs: (min(v), max(v)) for fs, v in per_seed.items()},
           "bootstrap": boot, "columns": cols}
    print(f"\n== {label}: {res['n']} checkpoints, {res['positives']} hidden fail, {res['tasks']} tasks")
    for fs in P.FEATURE_SETS:
        lo, hi = boot["auroc"][fs]
        a, b = res["auroc_per_split_range"][fs]
        print(f"  {fs:22s} AUROC {res['auroc'][fs]:.3f}  (task bootstrap {lo:.3f}-{hi:.3f}; "
              f"single splits {a:.3f}-{b:.3f}; {len(cols[fs])} columns)")
    for lo_, hi_ in pairs:
        k = f"{hi_} - {lo_}"
        lo, hi = boot["delta"][k]
        d = res["auroc"][hi_] - res["auroc"][lo_]
        print(f"  d[{k}] = {d:+.3f}  (task bootstrap {lo:+.3f} to {hi:+.3f}; share > 0: {boot['delta_share_positive'][k]:.0%})")
    return res


def coefficients(data: list[dict]) -> list[tuple[str, float]]:
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
    rows = [{**P.cheap_vector(d["cp"]["features"]), **P.jev_vector(d["history"], d["trace"], "cheap+code+thinking")}
            for d in data]
    des = P.design(rows)
    m = P.make_model().fit(des.X, y)
    return sorted(zip(des.columns, m[-1].coef_[0].tolist()), key=lambda kv: -abs(kv[1]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    args = ap.parse_args()
    data = load(args.run_id)
    vp = [d for d in data if d["cp"]["visible_pass"]]
    out = {"runs": args.run_id, "pipeline": P.PIPELINE_VERSION, "C": P.C, "folds": P.N_FOLDS, "repeats": REPEATS,
           "guide_gain": GUIDE_GAIN}
    out["visible_pass"] = evaluate(vp, "visible-pass checkpoints (the primary subset)")
    out["all"] = evaluate(data, "all checkpoints (descriptive)")
    gain = out["visible_pass"]["auroc"]["cheap+code+thinking"] - out["visible_pass"]["auroc"]["cheap"]
    out["decision"] = "spend time on the extras" if gain >= GUIDE_GAIN else "keep Jev in the primary test; cut the extras first"
    print(f"\nresource guide: gain {gain:+.3f} vs rule {GUIDE_GAIN:+.2f} -> {out['decision']}")
    coef = coefficients(vp)
    out["coefficients_visible_pass_full_fit"] = coef
    print("\nlargest standardized coefficients (cheap+code+thinking, visible-pass, fitted on all dev; descriptive):")
    for k, v in coef[:12]:
        print(f"  {k:40s} {v:+.3f}")
    path = RESULTS / f"resource_guide_{'+'.join(args.run_id)}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
