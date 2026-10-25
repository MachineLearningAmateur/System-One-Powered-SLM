"""Frozen fresh-benchmark test of the Jev-only strong4 mean.

    uv run python scripts/analyze_bcb_jev_only.py --run-id bcb-jev-only-test-v1

Primary, two-sided, alpha .05: AUROC(strong4 mean) minus AUROC(cheap),
19,999 paired whole-task bootstrap draws. The full cheap+code+thinking router,
task-weighted AUROC, and frozen 10/25/50% operating points are descriptive.
No model, feature, weight, or threshold is fitted from these labels.
"""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P
from system1.eval import replay as R

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg, score_final  # noqa: E402

ROUTERS = CONFIGS / "routers_q8b-v1.json"
MANIFEST = CONFIGS / "bcb_jev_only_tasks_v1.json"
N_ATTEMPTS = 5


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    out_path = RESULTS / f"bcb_jev_only_analysis_{args.run_id}.json"
    if out_path.exists():
        print("STOP: analysis output already exists; refusing to overwrite")
        return 2
    cfg = json.loads(ROUTERS.read_text(encoding="utf-8"))
    tasks = set(json.loads(MANIFEST.read_text(encoding="utf-8"))["tasks"])
    data = load_rg().load([args.run_id], split="test", require_ok=True)
    all_attempts = {(d["cp"]["task_id"], d["cp"]["attempt"]) for d in data}
    if all_attempts != {(tid, a) for tid in tasks for a in range(N_ATTEMPTS)}:
        print("STOP: incomplete or unexpected task/attempt set")
        return 2
    meta = json.loads((RESULTS / "runs" / args.run_id / "grade_meta.json").read_text(encoding="utf-8"))
    if meta.get("calibration_failures") or meta["labels"].get("invalid"):
        print("STOP: invalid hidden grades or failed reference calibration")
        return 2
    vp = [d for d in data if d["cp"]["visible_pass"]]
    if not vp:
        print("STOP: no visible-pass checkpoints")
        return 2
    y = np.array([int(not d["cp"]["hidden"]["passed"]) for d in vp])
    groups = np.array([d["cp"]["task_id"] for d in vp])
    if len(set(y)) != 2:
        print("STOP: visible-pass population has only one hidden outcome; AUROC undefined")
        return 2
    score_names = ["cheap", "strong4 mean", "cheap+code+thinking"]
    scores = {k: np.array([score_final(d, cfg["routers"][k]) for d in vp], dtype=float)
              for k in score_names}
    if any(not np.isfinite(v).all() for v in scores.values()):
        print("STOP: missing or nonfinite score")
        return 2
    metrics = {k: {"auroc": float(roc_auc_score(y, s)),
                   "auroc_task_weighted": float(roc_auc_score(y, s, sample_weight=P.task_weights(groups))),
                   "auprc": float(average_precision_score(y, s))} for k, s in scores.items()}
    test = P.bootstrap_test(y, groups, np.array(["bcb"] * len(y)),
                            scores["cheap"], scores["strong4 mean"], n_boot=19_999, seed=20261025)
    ids = [d["cp"]["checkpoint_id"] for d in vp]
    ops = {}
    for name in score_names:
        ops[name] = {}
        for rate, th in cfg["routers"][name]["thresholds"].items():
            esc = np.array([R.escalate(v, th["t"], th["alpha"], cid)
                            for v, cid in zip(scores[name], ids)])
            accepted = ~esc
            ops[name][rate] = {"realized_rate": float(esc.mean()),
                               "hidden_fails_escalated": float(esc[y == 1].mean()),
                               "residual_fail_rate_accepted": float(y[accepted].mean()) if accepted.any() else None}
    out = {"run_id": args.run_id, "hypothesis": "AUROC(strong4 mean) - AUROC(cheap) > 0",
           "test": "two-sided paired task bootstrap, alpha=0.05", "n_boot_planned": 19_999,
           "n_tasks_manifest": len(tasks), "n_attempts": len(all_attempts),
           "n_checkpoints": len(data), "n_visible_pass": len(vp), "n_hidden_fail": int(y.sum()),
           "n_positive_tasks": len(set(groups[y == 1])), "failure_prevalence": float(y.mean()),
           "routers_version": cfg["version"], "primary": {**test, "reject_at_0.05": test["p_two_sided"] < .05},
           "metrics": metrics, "operating_points": ops,
           "descriptive_delta_vs_full": metrics["strong4 mean"]["auroc"] -
                                        metrics["cheap+code+thinking"]["auroc"]}
    out_path.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(f"{len(vp)} visible-pass checkpoints, {int(y.sum())} hidden failures, "
          f"{out['n_positive_tasks']} positive tasks")
    print(f"AUROC cheap={metrics['cheap']['auroc']:.3f}, Jev-only={metrics['strong4 mean']['auroc']:.3f}, "
          f"full={metrics['cheap+code+thinking']['auroc']:.3f}")
    print(f"primary delta={test['delta']:.3f}, p={test['p_two_sided']:.4f}, "
          f"CI=({test['ci95'][0]:.3f}, {test['ci95'][1]:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
