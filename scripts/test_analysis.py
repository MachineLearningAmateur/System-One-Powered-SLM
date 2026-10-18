"""The frozen primary test analysis on the visible-pass test checkpoints (docs/research-plan.md,
Evaluation and statistics; Amendment A2 applies through load_labelled).

    uv run python scripts/test_analysis.py --run-id main-test-v1

Every score comes from the frozen final models in configs/routers_v2.json (refitted on all
development visible-pass rows); nothing is fitted, selected or tuned on test rows.

Holm family (two tests, familywise alpha = 0.05; predict.bootstrap_test, 19,999 replicates,
whole tasks resampled within benchmark):
  primary    cheap                vs cheap+code+thinking
  secondary  cheap+code           vs cheap+code+thinking   (the trace contrast)

Descriptive (outside Holm): Table 1 (AUROC with task-bootstrap intervals, AUPRC with
prevalence, Brier for the LR predictors, FNR at 1/5/10% FPR, task-weighted AUROC) for the
LR predictors, the frozen sensitivities (cheap+strong4, the strong4 mean), Pinocchio input-v1
(input-v2 as a labeled sensitivity) and the logprob comparator; paired deltas against cheap;
results by benchmark and by cap hit; the same-question contrast; the per-answer audit; the
within-task AUROC; the operating points at the frozen thresholds. A missing score is never
filled here: the primary test needs both Jev arms on every row and stops otherwise.
Writes results/test_analysis_<run-id>.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P
from system1.eval import replay as R
from system1.features import pinocchio_input as PI
from system1.loop.tasks import load_tasks

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg, pinocchio_rows, score_final  # noqa: E402

PRIMARY = ("cheap", "cheap+code+thinking")
SECONDARY = ("cheap+code", "cheap+code+thinking")
LR_SETS = ["cheap", "cheap+code", "cheap+code+thinking", "cheap+strong4"]
MEAN = "strong4 mean"
PIN1, PIN2, LOGPROB = "pinocchio (input-v1)", "pinocchio (input-v2, sensitivity)", "logprob tail confidence"
TABLE = LR_SETS + [MEAN, PIN1, PIN2, LOGPROB]
N_BOOT_CI = 2000


def auroc(y, s, w=None):
    return float(roc_auc_score(y, s, sample_weight=w)) if len(set(y)) == 2 else None


def metrics(y, s, groups, probability: bool) -> dict:
    out = {"n": int(len(y)), "positives": int(y.sum()), "prevalence": float(y.mean()),
           "tasks": len(set(groups)), "positive_tasks": len(set(groups[y == 1])),
           "auroc": auroc(y, s), "auroc_task_weighted": auroc(y, s, P.task_weights(groups)),
           "auprc": float(average_precision_score(y, s)),
           "fnr_at_fpr": {str(f): P.fnr_at_fpr(y, s, f) for f in (0.01, 0.05, 0.10)}}
    if probability:
        out["brier"] = float(np.mean((s - y) ** 2))
    return out


def within_task_auroc(y, s, groups) -> dict:
    vals = []
    for t in np.unique(groups):
        m = groups == t
        if len(set(y[m])) == 2:
            vals.append(roc_auc_score(y[m], s[m]))
    return {"tasks_with_both_outcomes": len(vals), "mean": float(np.mean(vals)) if vals else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--routers", default="v2")
    args = ap.parse_args()
    cfg = json.loads((CONFIGS / f"routers_{args.routers}.json").read_text(encoding="utf-8"))
    routers = cfg["routers"]
    rg = load_rg()
    data = rg.load([args.run_id], split="test", require_ok=False)
    cps = [d["cp"] for d in data]
    vp = [d for d in data if d["cp"]["visible_pass"]]
    jev_missing = [d["cp"]["checkpoint_id"] for d in vp if d["history"] is None or d["trace"] is None]
    if jev_missing:
        raise SystemExit(f"STOP: {len(jev_missing)} visible-pass rows lack a Jev arm (e.g. {jev_missing[0]})")

    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in vp])
    groups = np.array([d["cp"]["task_id"] for d in vp])
    strata = np.array([d["cp"]["benchmark"] for d in vp])
    ids = [d["cp"]["checkpoint_id"] for d in vp]

    # Frozen scores
    pin1 = pinocchio_rows([args.run_id], list(routers["pinocchio"]["model"]["setup"]), cps, True)
    tasks = load_tasks()
    recs2, counts2 = PI.select_records(PI.read_records(RESULTS / "runs" / args.run_id, PI.V2), cps, tasks, PI.V2,
                                       require_pinned=True)
    if counts2["rejected"]:
        raise SystemExit(f"STOP: {len(counts2['rejected'])} input-v2 records fail the provenance checks")
    scores: dict[str, np.ndarray] = {}
    for name in LR_SETS + [MEAN]:
        scores[name] = np.array([score_final(d, routers[name]) for d in vp], float)
    scores[PIN1] = np.array([np.nan if c not in pin1 else pin1[c]["score"] for c in ids], float)
    scores[PIN2] = np.array([np.nan if c not in recs2 else recs2[c]["score"] for c in ids], float)
    lp_missing = sum(P._num(d["cp"]["features"].get("thinking_tail_conf")) is None for d in vp)
    scores[LOGPROB] = np.array([P.logprob_comparator(d["cp"]["features"]) for d in vp], float)
    missing = {k: int(np.isnan(v).sum()) for k, v in scores.items()}
    for k in LR_SETS + [MEAN]:
        if missing[k]:
            raise SystemExit(f"STOP: {missing[k]} rows have no {k} score")

    out = {"run": args.run_id, "routers": cfg["version"], "pipeline": P.PIPELINE_VERSION,
           "population": "visible-pass test checkpoints, Amendment A2 exclusions applied",
           "n_checkpoints_all": len(data), "n_visible_pass": len(vp),
           "visible_fail_hidden_pass": int(sum((not d["cp"]["visible_pass"]) and d["cp"]["hidden"]["passed"]
                                               for d in data)),
           "missing_scores": missing, "logprob_missing_rows": int(lp_missing),
           "pinocchio_v2_counts": {k: (len(v) if isinstance(v, list) else v) for k, v in counts2.items()}}

    # Holm family
    tests = {}
    for name, (a, b) in (("primary", PRIMARY), ("secondary", SECONDARY)):
        tests[name] = {"a": a, "b": b, **P.bootstrap_test(y, groups, strata, scores[a], scores[b])}
    adj = P.holm({k: v["p_two_sided"] for k, v in tests.items()})
    for k in tests:
        tests[k]["p_holm"] = adj[k]
        tests[k]["reject_at_0.05"] = adj[k] < 0.05
    out["holm_family"] = tests

    # Table 1 (descriptive intervals: whole-task bootstrap over fixed scores)
    def table(mask, label):
        yy, gg = y[mask], groups[mask]
        res = {"subset": label}
        for k in TABLE:
            s = scores[k][mask]
            ok = ~np.isnan(s)
            if ok.sum() == 0 or len(set(yy[ok])) < 2:
                res[k] = None
                continue
            res[k] = metrics(yy[ok], s[ok], gg[ok], probability=k in LR_SETS)
            res[k]["rows_left_out"] = int((~ok).sum())
        full = {k: scores[k][mask] for k in TABLE if not np.isnan(scores[k][mask]).any()}
        pairs = [("cheap", k) for k in full if k != "cheap"] + [SECONDARY]
        if len(set(yy)) == 2:
            res["bootstrap"] = P.task_bootstrap(yy, gg, full, pairs, n_boot=N_BOOT_CI)
            res["delta_vs_cheap"] = {f"{b} - {a}": res[b]["auroc"] - res[a]["auroc"] for a, b in pairs}
        return res

    out["table1"] = table(np.ones(len(y), bool), "all visible-pass")
    out["by_benchmark"] = {b: table(strata == b, b) for b in sorted(set(strata))}
    cap = np.array([bool(d["cp"]["features"].get("cap_hit")) for d in vp])
    out["by_cap_hit"] = {str(v): table(cap == v, f"cap_hit={v}") for v in (False, True) if (cap == v).any()}
    out["within_task"] = {k: within_task_auroc(y, scores[k], groups) for k in LR_SETS + [MEAN]}

    # Same-question contrast: each code answer with the thinking (trace arm) vs without (history arm)
    same = {}
    for q in ("code_likely_fails", "special_cases_visible_tests"):
        rows = [i for i, d in enumerate(vp) if d["history"]["applicability"][q] == "applicable"
                and d["trace"]["applicability"][q] == "applicable"]
        h = np.array([vp[i]["history"]["features"][q] for i in rows], float)
        t = np.array([vp[i]["trace"]["features"][q] for i in rows], float)
        yy, gg = y[rows], groups[rows]
        b = P.task_bootstrap(yy, gg, {"history": h, "trace": t}, [("history", "trace")], n_boot=N_BOOT_CI)
        same[q] = {"n": len(rows), "history_arm": auroc(yy, h), "trace_arm": auroc(yy, t), "bootstrap": b}
    swapped = np.array([score_final({**d, "history": {**d["history"], "features": {
        **d["history"]["features"], **{q: d["trace"]["features"][q] for q in P.CODE_QS}},
        "applicability": {**d["history"]["applicability"], **{q: d["trace"]["applicability"][q]
                                                              for q in P.CODE_QS}}}},
        routers["cheap+code"]) for d in vp], float)
    b = P.task_bootstrap(y, groups, {"history": scores["cheap+code"], "trace": swapped}, [("history", "trace")],
                         n_boot=N_BOOT_CI)
    same["cheap+code predictor"] = {"history_arm": auroc(y, scores["cheap+code"]), "trace_arm": auroc(y, swapped),
                                    "bootstrap": b}
    out["same_question"] = same

    # Per-answer audit: standalone AUROC of each oriented answer on its applicable rows
    audit = {}
    for q in P.CODE_QS + P.THINKING_QS:
        for arm, key in ((P.HISTORY_ARM, "history"), (P.TRACE_ARM, "trace")):
            if q not in P.CODE_QS and key == "history":
                continue
            rows = [i for i, d in enumerate(vp) if d[key]["applicability"][q] == "applicable"]
            if not rows:
                audit[f"{q} [{arm}]"] = {"applicable_rows": 0}
                continue
            v = np.array([vp[i][key]["features"][q] for i in rows], float)
            v = 1 - v if q in P.TRUE_IS_GOOD else v
            rr = np.array(rows)
            ent = {"applicable_rows": len(rows), "positives": int(y[rr].sum()),
                   "positive_tasks": len(set(groups[rr][y[rr] == 1])), "auroc": auroc(y[rr], v)}
            for b in sorted(set(strata)):
                m = strata[rr] == b
                ent[f"auroc {b}"] = auroc(y[rr][m], v[m])
            for c in (False, True):
                m = cap[rr] == c
                ent[f"auroc cap_hit={c}"] = auroc(y[rr][m], v[m]) if m.any() else None
            audit[f"{q} [{arm}]"] = ent
    out["audit"] = audit

    # Operating points at the frozen thresholds (deployment view; no fallback needed: no score is missing)
    ops = {}
    for k in LR_SETS + [MEAN, "pinocchio"]:
        s = scores[PIN1] if k == "pinocchio" else scores[k]
        ops[k] = {}
        for q, th in routers[k]["thresholds"].items():
            if np.isnan(s).any():
                ops[k][q] = None
                continue
            esc = np.array([R.escalate(v, th["t"], th["alpha"], c) for v, c in zip(s, ids)])
            acc = ~esc
            ops[k][q] = {"realized_rate": float(esc.mean()), "hidden_fails_escalated": float(esc[y == 1].mean()),
                         "residual_fail_rate_accepted": float(y[acc].mean()) if acc.any() else None,
                         "fpr": float(esc[y == 0].mean()), "fnr": float(1 - esc[y == 1].mean())}
    out["operating_points"] = ops

    # Report
    t1 = out["table1"]
    print(f"{args.run_id}: {len(vp)} visible-pass checkpoints, {int(y.sum())} hidden fail "
          f"({y.mean():.1%}) from {len(set(groups[y == 1]))} tasks; {len(set(groups))} tasks; "
          f"benchmarks {dict(Counter(strata))}")
    for name, r in tests.items():
        print(f"  {name:9s} {r['b']} - {r['a']}: d = {r['delta']:+.3f} (95% {r['ci95'][0]:+.3f} to "
              f"{r['ci95'][1]:+.3f}); p = {r['p_two_sided']:.4f}, Holm p = {r['p_holm']:.4f}; B = {r['n_boot']}")
    print("\nTable 1 (descriptive)")
    for k in TABLE:
        m = t1[k]
        if m is None:
            print(f"  {k:36s} n/a")
            continue
        lo, hi = t1["bootstrap"]["auroc"].get(k, (float("nan"), float("nan")))
        print(f"  {k:36s} AUROC {m['auroc']:.3f} ({lo:.3f}-{hi:.3f}) tw {m['auroc_task_weighted']:.3f} "
              f"AUPRC {m['auprc']:.3f} FNR@5% {m['fnr_at_fpr']['0.05']['fnr']:.3f}"
              + (f" Brier {m['brier']:.3f}" if "brier" in m else "") + f" left out {m['rows_left_out']}")
    for k, d in t1["delta_vs_cheap"].items():
        lo, hi = t1["bootstrap"]["delta"][k]
        print(f"  d[{k}] = {d:+.3f} ({lo:+.3f} to {hi:+.3f})")
    for b, r in out["by_benchmark"].items():
        print(f"\n{b}: n {r['cheap']['n']}, positives {r['cheap']['positives']} from {r['cheap']['positive_tasks']} "
              f"tasks; " + ", ".join(f"{k} {r[k]['auroc']:.3f}" for k in TABLE if r[k]))
    for q, r in same.items():
        print(f"  same-question {q}: history {r['history_arm']:.3f} vs trace {r['trace_arm']:.3f}")
    path = RESULTS / f"test_analysis_{args.run_id}.json"
    path.write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    print(f"\nwritten {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
