"""Freeze the routers for the replay: final models and escalation thresholds (dev only).

    uv run python scripts/freeze_routers.py --run-id pilot-v1 --run-id pilot-v1b --version v2

For each router (the predict-v2 feature sets, the sensitivity cheap+strong4, the
strong4 mean, and from v2 on Pinocchio-0.8B) on the visible-pass development
checkpoints:
  - the final model: one LR refitted on all rows (portable; the mean needs none);
  - the out-of-fold scores (REPEATS split averages, as in the resource guide);
  - the weighted dev score distribution (for percentiles in the ranking view);
  - for q_VP in replay.RATES, (t, alpha) = the weighted quantile of those scores,
    each row weighted 1 / (the number of sampled attempts of its task), plus the
    pooled and attempt-0-only thresholds as sensitivities.
Writes configs/routers_<version>.json (frozen; refuses to overwrite) and
results/dev_router_scores_<version>.json (the dev scores, for the dev replay).

v1: the five routers above. v2 (October 17, before any test run): v1 plus
Pinocchio, whose router score is 1 - p_correct from scripts/score_pinocchio.py
(no fitting, like the strong4 mean). v2 refuses to write if any v1 router's
model or thresholds would differ from the frozen v1 file.
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

ROUTERS_V1 = list(P.FEATURE_SETS) + list(P.SENSITIVITY_SETS) + ["strong4 mean"]
ROUTERS = {"v1": ROUTERS_V1, "v2": ROUTERS_V1 + ["pinocchio"]}
FALLBACK = "cheap"  # decides when a Jev (or Pinocchio) score is missing
PINOCCHIO_FILE = "pinocchio_scores.jsonl"


def pinocchio_scores(run_ids: list[str]) -> tuple[dict[str, float], str]:
    """Router score (1 - p_correct) per checkpoint id, and the frozen input version."""
    from system1.eval.ledger import read_jsonl
    out, versions = {}, set()
    for rid in run_ids:
        rows, bad = read_jsonl(RESULTS / "runs" / rid / PINOCCHIO_FILE)
        if bad:
            raise SystemExit(f"STOP: damaged lines in {rid}/{PINOCCHIO_FILE}")
        for r in rows:
            if r["checkpoint_id"] in out:
                raise SystemExit(f"STOP: two Pinocchio scores for {r['checkpoint_id']}")
            out[r["checkpoint_id"]] = r["score"]
            versions.add((r["input_version"], r["adapter"], r["base_model"], r["package"]))
    if len(versions) != 1:
        raise SystemExit(f"STOP: Pinocchio scores were made with different setups {versions}")
    return out, json.dumps(sorted(versions)[0])


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
    ap.add_argument("--version", choices=sorted(ROUTERS), required=True)
    args = ap.parse_args()
    OUT = CONFIGS / f"routers_{args.version}.json"
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
    pin_setup = None
    for name in ROUTERS[args.version]:
        if name == "pinocchio":
            pin, pin_setup = pinocchio_scores(args.run_id)
            missing = [d["cp"]["checkpoint_id"] for d in vp if d["cp"]["checkpoint_id"] not in pin]
            if missing:
                raise SystemExit(f"STOP: {len(missing)} dev decision checkpoints have no Pinocchio score")
            s = np.array([pin[d["cp"]["checkpoint_id"]] for d in vp])
            model = {"kind": "external", "name": "pinocchio-0.8b", "file": PINOCCHIO_FILE,
                     "score": "1 - p_correct", "setup": json.loads(pin_setup)}
        elif name == "strong4 mean":
            s = np.array([P.jev_mean(d["history"], d["trace"]) for d in vp])
            model = {"kind": "mean", "questions": P.STRONG_QS, "na_oriented": P.NA_ORIENTED,
                     "true_is_good": sorted(P.TRUE_IS_GOOD)}
        else:
            X, cols = rg.design(vp, name, True)
            s = np.mean([P.oof_scores(X, y, groups, seed) for seed in range(rg.REPEATS)], axis=0)
            model = {"kind": "lr", "feature_set": name, **P.fit_final(X, y, cols)}
        routers[name] = {"model": model, "thresholds": thresholds(s, w, ids),
                         # The weighted dev distribution: the ranking view maps scores to percentiles in it,
                         # so a cheap-LR fallback score and a router score share one scale.
                         "dev_distribution": {"scores": [float(v) for v in s], "weights": [float(v) for v in w]},
                         "sensitivity_thresholds": {"pooled": thresholds(s, np.ones(len(s)), ids),
                                                    "attempt0": thresholds(s[a0], np.ones(a0.sum()),
                                                                           [i for i, k in zip(ids, a0) if k])}}
        scores_out[name] = dict(zip(ids, map(float, s)))
        print(f"{name:22s} " + "  ".join(f"q={q}: t={v['t']:.4f} a={v['alpha']:.2f} dev {v['dev_rate_weighted']:.3f}"
                                          for q, v in routers[name]["thresholds"].items()))

    if args.version != "v1":
        v1 = json.loads((CONFIGS / "routers_v1.json").read_text(encoding="utf-8"))["routers"]
        for name in ROUTERS_V1:
            if json.loads(json.dumps(routers[name])) != v1[name]:
                raise SystemExit(f"STOP: router {name} differs from the frozen v1 file")
    cfg = {"version": f"routers-{args.version}", "created": datetime.now(timezone.utc).isoformat(), "git_commit": commit,
           "runs": args.run_id, "pipeline": P.PIPELINE_VERSION, "rates": list(R.RATES), "tie_tag": R.TIE_TAG,
           "weighting": "each dev VP row weighted 1 / sampled attempts of its task",
           "scores": f"OOF mean over {rg.REPEATS} task-grouped splits (strong4 mean, pinocchio: no fitting)",
           "dev_scores_file": f"dev_router_scores_{args.version}.json",
           "fallback_when_jev_missing": FALLBACK, "n_rows": len(vp), "routers": routers}
    OUT.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    dev_file = RESULTS / cfg["dev_scores_file"]
    dev_file.write_text(json.dumps({"runs": args.run_id, "scores": scores_out}), encoding="utf-8")
    print(f"written {OUT} and {dev_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
