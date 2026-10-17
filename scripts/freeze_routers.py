"""Freeze the routers for the replay: final models and escalation thresholds (dev only).

    uv run python scripts/freeze_routers.py --run-id pilot-v1 --run-id pilot-v1b

For each router (the predict-v2 feature sets, the sensitivity cheap+strong4, and
the strong4 mean) on the visible-pass development checkpoints:
  - the final model: one LR refitted on all rows (portable; the mean needs none);
  - the out-of-fold scores (REPEATS split averages, as in the resource guide);
  - for q_VP in replay.RATES, (t, alpha) = the weighted quantile of those scores,
    each row weighted 1 / (the number of sampled attempts of its task), plus the
    pooled and attempt-0-only thresholds as sensitivities.
Writes configs/routers_v1.json (frozen; refuses to overwrite) and
results/dev_router_scores.json (the OOF scores, for the dev replay).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

import numpy as np

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P
from system1.eval import replay as R

OUT = CONFIGS / "routers_v1.json"
ROUTERS = list(P.FEATURE_SETS) + list(P.SENSITIVITY_SETS) + ["strong4 mean"]
FALLBACK = "cheap"  # decides when a Jev score is missing


def load_rg():
    spec = importlib.util.spec_from_file_location("resource_guide", ROOT / "scripts" / "resource_guide.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def thresholds(scores, weights, ids):
    out = {}
    for q in R.RATES:
        t, a = R.weighted_threshold(scores, weights, q)
        esc = np.array([R.escalate(s, t, a, c) for s, c in zip(scores, ids)])
        out[f"{q:.2f}"] = {"t": t, "alpha": a, "dev_rate_weighted": float((weights * esc).sum() / weights.sum()),
                           "dev_rate_pooled": float(esc.mean()), "ties_at_t": int((scores == t).sum())}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    args = ap.parse_args()
    if OUT.exists():
        print(f"{OUT} exists and is frozen; write a new version instead")
        return 2
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout.strip())
    if dirty:
        print("The git tree has changes; commit them first (the frozen file records the commit).")
        return 2
    rg = load_rg()
    data = rg.load(args.run_id)
    attempts_per_task = Counter(t for t, _ in {(d["cp"]["task_id"], (d["run"], d["cp"]["attempt"])) for d in data})
    vp = [d for d in data if d["cp"]["visible_pass"]]
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in vp])
    groups = np.array([d["cp"]["task_id"] for d in vp])
    ids = [d["cp"]["checkpoint_id"] for d in vp]
    w = np.array([1.0 / attempts_per_task[d["cp"]["task_id"]] for d in vp])
    a0 = np.array([d["cp"]["attempt"] == 0 for d in vp])

    routers, scores_out = {}, {}
    for name in ROUTERS:
        if name == "strong4 mean":
            s = np.array([P.jev_mean(d["history"], d["trace"]) for d in vp])
            model = {"kind": "mean", "questions": P.STRONG_QS, "na_oriented": P.NA_ORIENTED,
                     "true_is_good": sorted(P.TRUE_IS_GOOD)}
        else:
            X, cols = rg.design(vp, name, True)
            s = np.mean([P.oof_scores(X, y, groups, seed) for seed in range(rg.REPEATS)], axis=0)
            model = {"kind": "lr", "feature_set": name, **P.fit_final(X, y, cols)}
        routers[name] = {"model": model, "thresholds": thresholds(s, w, ids),
                         "sensitivity_thresholds": {"pooled": thresholds(s, np.ones(len(s)), ids),
                                                    "attempt0": thresholds(s[a0], np.ones(a0.sum()),
                                                                           [i for i, k in zip(ids, a0) if k])}}
        scores_out[name] = dict(zip(ids, map(float, s)))
        print(f"{name:22s} " + "  ".join(f"q={q}: t={v['t']:.4f} a={v['alpha']:.2f} dev {v['dev_rate_weighted']:.3f}"
                                          for q, v in routers[name]["thresholds"].items()))

    cfg = {"version": "routers-v1", "created": datetime.now(timezone.utc).isoformat(), "git_commit": commit,
           "runs": args.run_id, "pipeline": P.PIPELINE_VERSION, "rates": list(R.RATES), "tie_tag": R.TIE_TAG,
           "weighting": "each dev VP row weighted 1 / sampled attempts of its task",
           "scores": f"OOF mean over {rg.REPEATS} task-grouped splits (strong4 mean: no fitting)",
           "fallback_when_jev_missing": FALLBACK, "n_rows": len(vp), "routers": routers}
    OUT.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    (RESULTS / "dev_router_scores.json").write_text(json.dumps({"runs": args.run_id, "scores": scores_out}),
                                                     encoding="utf-8")
    print(f"written {OUT} and {RESULTS / 'dev_router_scores.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
