"""Resource guide on development checkpoints (docs/research-plan.md, Go/no-go 3).

    uv run python scripts/resource_guide.py --run-id pilot-v1 --run-id pilot-v1b

On the visible-pass development checkpoints, compares the cheap-feature
logistic regression with and without Jev's features, with task-grouped
out-of-fold predictions (averaged over REPEATS fold splits) and a task
bootstrap. Rule: if cheap+code+thinking beats cheap by at least 0.03 AUROC
(pooled over checkpoints), spend the time on the full typed questions and the
drift labels; if not, keep Jev in the primary comparison but cut those extras
first. The task-weighted AUROC is a reported sensitivity, never the rule.
This is a guide for effort, not a result: development data only.

It also refits the frozen test predictor of each feature set (one LR on all
visible-pass development rows) and stores it in a portable form, for the
primary sets and for the sensitivity set cheap+strong4. The strong4 mean
needs no fitting; its development AUROC is reported next to them.

load() refuses: a run that is not a development run, Jev scores made with
another rubric, evidence version or byte budget, and a score whose request
hash does not match the request rebuilt from the current trajectory (a score
that belongs to another execution or evidence).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

from system1.config import RESULTS
from system1.eval import predict as P
from system1.eval.labels import load_labelled
from system1.eval.ledger import read_jsonl
from system1.features.evidence import EVIDENCE_VERSION, build_arms
from system1.features.jev_scoring import APPLICABLE, applicability, load_rubric
from system1.loop.runner import to_scoring_checkpoint
from system1.routers.jev import BYTE_BUDGET, request_body

GUIDE_GAIN = 0.03
REPEATS = 20
PAIRS = [("cheap", "cheap+code+thinking"), ("cheap+code", "cheap+code+thinking"), ("cheap", "cheap+code")]
# Sensitivities selected on development data after the freeze (predict.py docstring); descriptive.
MEAN = "strong4 mean"
SENS_PAIRS = [("cheap", "cheap+strong4"), ("cheap", MEAN)]


class LoadError(RuntimeError):
    pass


def request_hashes(cp, rubric, model: str, budget: int) -> dict[str, str]:
    """The hash of each arm's request, rebuilt from the checkpoint the way the scorer builds it."""
    qs = {}
    for arm in (P.HISTORY_ARM, P.TRACE_ARM):
        app = applicability(rubric, cp, arm)
        qs[arm] = {q: rubric.api_question(q) for q, s in app.items() if s == APPLICABLE}
    ev = build_arms(cp, qs, model=model, budget=budget)
    return {arm: hashlib.sha256(request_body(model, ev[arm].state, qs[arm])).hexdigest() for arm in ev}


def load(run_ids: list[str], split: str = "dev", require_ok: bool = True) -> list[dict]:
    """Labelled checkpoints with their two Jev records. The resource guide uses the defaults
    (development runs, both arms ok). The replay can load a test run with require_ok=False:
    a missing or failed arm is then kept as None (the router's fallback decides)."""
    rubric = load_rubric()
    out = []
    for rid in run_ids:
        d = RESULTS / "runs" / rid
        run_split = json.loads((d / "run_meta.json").read_text(encoding="utf-8"))["split"]
        if run_split != split:
            raise LoadError(f"{rid} is a {run_split} run; expected {split}")
        proto = json.loads((d / "jev_meta.json").read_text(encoding="utf-8"))["protocol"]
        want = {"rubric_sha256": rubric.sha256, "evidence_version": EVIDENCE_VERSION, "byte_budget": BYTE_BUDGET}
        bad = {k: (proto.get(k), v) for k, v in want.items() if proto.get(k) != v}
        if bad:
            raise LoadError(f"{rid}: Jev scores were made with another protocol {bad}")
        rows, damaged = read_jsonl(d / "jev_scores.jsonl")
        if damaged:
            raise LoadError(f"{rid}: {len(damaged)} damaged lines in jev_scores.jsonl")
        scores = {(r["checkpoint_id"], r["arm"]): r for r in rows}  # last record wins
        for c in load_labelled(d):
            h, t = scores.get((c["checkpoint_id"], P.HISTORY_ARM)), scores.get((c["checkpoint_id"], P.TRACE_ARM))
            ok = bool(h and t and h["status"] == "ok" and t["status"] == "ok")
            if require_ok and not ok:
                raise LoadError(f"{rid} {c['checkpoint_id']}: Jev scores missing or not ok")
            cp = to_scoring_checkpoint(c)
            present = [r for r in (h, t) if r and r["status"] == "ok"]
            hashes = request_hashes(cp, rubric, present[0]["model_requested"], present[0]["byte_budget"]) if present else {}
            for rec in present:
                if rec["request_sha256"] != hashes[rec["arm"]]:
                    raise LoadError(f"{rid} {c['checkpoint_id']} {rec['arm']}: score is for another request")
            h = h if h and h["status"] == "ok" else None
            t = t if t and t["status"] == "ok" else None
            out.append({"run": rid, "cp": c, "has_trace": cp.has_trace, "history": h, "trace": t})
    return out


def design(data: list[dict], feature_set: str, visible_pass_only: bool) -> tuple[np.ndarray, list[str]]:
    cols = P.columns(feature_set, visible_pass_only)
    rows = [P.row_vector(d["cp"]["features"], d["has_trace"], d["history"], d["trace"], feature_set) for d in data]
    return P.matrix(rows, cols), cols


def evaluate(data: list[dict], label: str, visible_pass_only: bool) -> dict:
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
    groups = np.array([d["cp"]["task_id"] for d in data])
    w = P.task_weights(groups)
    preds, per_split, cols, final = {}, {}, {}, {}
    for fs in P.FEATURE_SETS + P.SENSITIVITY_SETS:
        X, cols[fs] = design(data, fs, visible_pass_only)
        runs = [P.oof_scores(X, y, groups, seed) for seed in range(REPEATS)]
        per_split[fs] = [roc_auc_score(y, p) for p in runs]
        preds[fs] = np.mean(runs, axis=0)
        final[fs] = P.fit_final(X, y, cols[fs])
    means = [P.jev_mean(d["history"], d["trace"]) for d in data]
    assert all(m is not None for m in means)  # load() keeps only rows with both arms ok
    preds[MEAN] = np.array(means)
    res = {"subset": label, "n": len(y), "positives": int(y.sum()), "positive_tasks": len(set(groups[y == 1])),
           "tasks": len(set(groups)), "first_round_rows": int(sum(d["cp"]["round"] == 1 for d in data)),
           "auroc": {fs: roc_auc_score(y, p) for fs, p in preds.items()},
           "auroc_task_weighted": {fs: roc_auc_score(y, p, sample_weight=w) for fs, p in preds.items()},
           "auroc_single_split_mean": {fs: float(np.mean(v)) for fs, v in per_split.items()},
           "auroc_single_split_range": {fs: (min(v), max(v)) for fs, v in per_split.items()},
           "bootstrap": P.task_bootstrap(y, groups, preds, PAIRS + SENS_PAIRS),
           "bootstrap_task_weighted": P.task_bootstrap(y, groups, preds, PAIRS + SENS_PAIRS, weighted=True),
           "columns": cols, "final_models": final}
    print(f"\n== {label}: {res['n']} checkpoints, {res['positives']} hidden fail from {res['positive_tasks']} tasks, "
          f"{res['tasks']} tasks, {res['first_round_rows']} round-1 rows")
    for fs in P.FEATURE_SETS + P.SENSITIVITY_SETS:
        lo, hi = res["bootstrap"]["auroc"][fs]
        a, b = res["auroc_single_split_range"][fs]
        print(f"  {fs:22s} AUROC {res['auroc'][fs]:.3f} ({lo:.3f}-{hi:.3f}); task-weighted "
              f"{res['auroc_task_weighted'][fs]:.3f}; single splits {a:.3f}-{b:.3f}; {len(cols[fs])} columns")
    a, lohi = res["auroc"][MEAN], res["bootstrap"]["auroc"][MEAN]
    print(f"  {MEAN:22s} AUROC {a:.3f} ({lohi[0]:.3f}-{lohi[1]:.3f}); task-weighted "
          f"{res['auroc_task_weighted'][MEAN]:.3f}; no fitting (sensitivity)")
    for lo_, hi_ in PAIRS + SENS_PAIRS:
        k = f"{hi_} - {lo_}"
        lo, hi = res["bootstrap"]["delta"][k]
        wlo, whi = res["bootstrap_task_weighted"]["delta"][k]
        d = res["auroc"][hi_] - res["auroc"][lo_]
        dw = res["auroc_task_weighted"][hi_] - res["auroc_task_weighted"][lo_]
        print(f"  d[{k}] = {d:+.3f} ({lo:+.3f} to {hi:+.3f}); task-weighted {dw:+.3f} ({wlo:+.3f} to {whi:+.3f})")
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    args = ap.parse_args()
    data = load(args.run_id)
    vp = [d for d in data if d["cp"]["visible_pass"]]
    out = {"runs": args.run_id, "pipeline": P.PIPELINE_VERSION, "C": P.C, "folds": P.N_FOLDS, "repeats": REPEATS,
           "fold_seeds": list(range(REPEATS)), "guide_gain": GUIDE_GAIN, "training_population": "visible-pass dev rows"}
    out["visible_pass"] = evaluate(vp, "visible-pass checkpoints (the primary subset)", visible_pass_only=True)
    out["all"] = evaluate(data, "all checkpoints (descriptive)", visible_pass_only=False)
    gain = out["visible_pass"]["auroc"]["cheap+code+thinking"] - out["visible_pass"]["auroc"]["cheap"]
    out["gain"] = gain
    out["decision"] = ("spend time on the extras" if gain >= GUIDE_GAIN
                       else "keep Jev in the primary test; cut the extras first")
    print(f"\nresource guide (pooled): gain {gain:+.3f} vs rule {GUIDE_GAIN:+.2f} -> {out['decision']}")
    fm = out["visible_pass"]["final_models"]["cheap+code+thinking"]
    top = sorted(zip(fm["columns"], fm["coef"]), key=lambda kv: -abs(kv[1]))[:12]
    print("\nlargest standardized coefficients of the refitted full model (descriptive; correlated features share weight):")
    for k, v in top:
        print(f"  {k:40s} {v:+.3f}")
    path = RESULTS / f"resource_guide_{'+'.join(args.run_id)}_{P.PIPELINE_VERSION}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
