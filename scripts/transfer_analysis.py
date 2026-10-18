"""Amendment A1.1: cross-benchmark transfer on the main test run (descriptive; outside Holm).

    uv run python scripts/transfer_analysis.py --run-id main-test-v1

For each direction (source -> target), on the target benchmark's test visible-pass rows:
  * AUROC of each frozen LR feature set fit on the source benchmark's development rows and
    of the same set fit on the target benchmark's development rows (configs/routers_transfer_v1.json);
  * transfer gap = AUROC(source fit) - AUROC(target fit), same rows, with predict.bootstrap_test
    (19,999 replicates, whole tasks resampled, conditional on the fitted models);
  * the Jev increment (cheap+code+thinking - cheap, and cheap+code - cheap) within each regime;
  * the strong4 mean as one fixed reference per target (no weights, no fitting).
Directions are never pooled. The A1 reporting rule: a discrimination claim needs at least 30
distinct tasks with a visible-pass hidden fail and 30 with a visible-pass hidden pass; below
that the result is labeled sparse descriptive evidence. Replicates dropped for having one class
are reported (19,999 - n_boot). The p-values are descriptive. Amendment A2 applies through
load_labelled. Writes results/transfer_<run-id>.json.
"""

from __future__ import annotations

import argparse
import json
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg, score_final  # noqa: E402

N_BOOT = 19_999
RULE_TASKS = 30
MEAN = "strong4 mean"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args()
    a1 = json.loads((CONFIGS / "amendment_a1.json").read_text(encoding="utf-8"))["transfer"]
    cfg = json.loads((CONFIGS / "routers_transfer_v1.json").read_text(encoding="utf-8"))
    v2 = json.loads((CONFIGS / "routers_v2.json").read_text(encoding="utf-8"))["routers"]
    # The frozen artifact must be the A1.1 one: pipeline, C, training runs, feature sets
    want = {"amendment": "A1.1", "pipeline": a1["pipeline"], "C": P.C, "runs": ["pilot-v1", "pilot-v1b"],
            "test_rows_read": False}
    bad = {k: (cfg.get(k), v) for k, v in want.items() if cfg.get(k) != v}
    if bad:
        raise SystemExit(f"STOP: routers_transfer_v1.json does not match A1.1: {bad}")
    for bench, part in cfg["by_source"].items():
        for fs in a1["feature_sets"]:
            m = part["models"][fs]
            if m["feature_set"] != fs or m["pipeline"] != a1["pipeline"] or m["columns"] != P.columns(fs, True):
                raise SystemExit(f"STOP: {bench} {fs} is not the frozen predict-v2 model")
    rg = load_rg()
    data =[d for d in rg.load([args.run_id], split="test", require_ok=False) if d["cp"]["visible_pass"]]
    if any(d["history"] is None or d["trace"] is None for d in data):
        raise SystemExit("STOP: a visible-pass row lacks a Jev arm")

    out = {"run": args.run_id, "routers": cfg["version"], "rule_tasks": RULE_TASKS, "directions": []}
    for direction in a1["directions"]:
        src, tgt = direction["source"], direction["target"]
        rows = [d for d in data if d["cp"]["benchmark"] == tgt]
        y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in rows])
        groups = np.array([d["cp"]["task_id"] for d in rows])
        strata = np.array([tgt] * len(rows))
        fail_tasks, pass_tasks = len(set(groups[y == 1])), len(set(groups[y == 0]))
        claim = fail_tasks >= RULE_TASKS and pass_tasks >= RULE_TASKS
        if len(set(y)) < 2:  # AUROC undefined: report the counts only
            out["directions"].append({"source": src, "target": tgt, "n": len(rows), "positives": int(y.sum()),
                                      "tasks_with_vp_hidden_fail": fail_tasks, "tasks_with_vp_hidden_pass": pass_tasks,
                                      "label": "one class: AUROC undefined"})
            print(f"\n{src} -> {tgt}: one class in {len(rows)} rows; AUROC undefined")
            continue
        scores = {}
        for regime, bench in (("source fit", src), ("target fit", tgt)):
            for fs in a1["feature_sets"]:
                m = cfg["by_source"][bench]["models"][fs]
                scores[(regime, fs)] = np.array([score_final(d, {"model": m}) for d in rows], float)
        mean = np.array([score_final(d, v2[MEAN]) for d in rows], float)
        res = {"source": src, "target": tgt, "n": len(rows), "positives": int(y.sum()),
               "tasks_with_vp_hidden_fail": fail_tasks, "tasks_with_vp_hidden_pass": pass_tasks,
               "meets_reporting_rule": claim,
               # The rule is necessary support for a discrimination statement, not evidence of transfer.
               "label": ("meets the 30/30 support rule (descriptive)" if claim
                         else "sparse descriptive evidence (below the 30/30 rule)"),
               "estimand": "fixed fitted models compared on the same rows; training sizes differ; "
                           "no training-set uncertainty; not a pure domain-shift estimate",
               "auroc": {f"{r} | {fs}": float(roc_auc_score(y, s)) for (r, fs), s in scores.items()},
               "strong4_mean_auroc": float(roc_auc_score(y, mean)), "gap": {}, "jev_increment": {}}
        for fs in a1["feature_sets"]:
            t = P.bootstrap_test(y, groups, strata, scores[("target fit", fs)], scores[("source fit", fs)], N_BOOT)
            res["gap"][fs] = {**t, "dropped_replicates": N_BOOT - t["n_boot"]}
        for regime in ("source fit", "target fit"):
            for hi in ("cheap+code", "cheap+code+thinking"):
                t = P.bootstrap_test(y, groups, strata, scores[(regime, "cheap")], scores[(regime, hi)], N_BOOT)
                res["jev_increment"][f"{regime} | {hi} - cheap"] = {**t, "dropped_replicates": N_BOOT - t["n_boot"]}
        out["directions"].append(res)

        print(f"\n{src} -> {tgt}: {len(rows)} VP rows, {int(y.sum())} hidden fail; tasks with a VP fail "
              f"{fail_tasks}, with a VP pass {pass_tasks} -> {res['label']}")
        for fs in a1["feature_sets"]:
            g = res["gap"][fs]
            print(f"  {fs:22s} source fit {res['auroc'][f'source fit | {fs}']:.3f}  target fit "
                  f"{res['auroc'][f'target fit | {fs}']:.3f}  gap {g['delta']:+.3f} ({g['ci95'][0]:+.3f} to "
                  f"{g['ci95'][1]:+.3f}) p {g['p_two_sided']:.3f}; dropped {g['dropped_replicates']}")
        for k, g in res["jev_increment"].items():
            print(f"  increment {k:40s} {g['delta']:+.3f} ({g['ci95'][0]:+.3f} to {g['ci95'][1]:+.3f})")
        print(f"  {MEAN} (fixed reference) {res['strong4_mean_auroc']:.3f}")
    path = RESULTS / f"transfer_{args.run_id}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
