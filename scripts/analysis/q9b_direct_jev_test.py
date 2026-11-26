"""The prespecified direct Jev test of the Qwen3.5-9B study (docs/q9b-plan.md, part B), version 1.

    uv run python scripts/analysis/q9b_direct_jev_test.py --run-id q9b-test-v1

On the visible-pass test checkpoints (Amendment A2 exclusions applied through load_labelled):
dAUROC = AUROC(direct Jev) - AUROC(telemetry-only router), where direct Jev is the frozen
"direct jev" router of configs/routers_q9b-v1.json (the history-request code_likely_fails
probability, no fitting) and the telemetry-only router is its frozen "cheap" final model.
Two-sided paired whole-task bootstrap, tasks resampled within benchmark, 19,999 draws, seed 0
(predict.bootstrap_test, the same test as the Holm family). This test is separate from the Holm
family of H1 and H2: alpha 0.05 on its own, no multiplicity adjustment. Nothing is fitted,
selected or tuned on test rows. A visible-pass row without a history-arm answer stops the test.
Writes results/q9b_direct_jev_test_<run-id>.json.
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

VERSION = "q9b-direct-jev-test-v1"
ROUTERS = "q9b-v1"
A, B = "cheap", "direct jev"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--split", default="test", choices=("dev", "test"),
                    help="test is the prespecified test; dev only checks the code (in-sample for cheap)")
    args = ap.parse_args()
    cfg = json.loads((CONFIGS / f"routers_{ROUTERS}.json").read_text(encoding="utf-8"))
    routers = cfg["routers"]
    if routers[B]["model"] != {"kind": "jev_question", "arm": P.HISTORY_ARM, "question": "code_likely_fails"}:
        raise SystemExit("STOP: the frozen direct Jev router is not the prespecified one")
    data = load_rg().load([args.run_id], split=args.split, require_ok=False)
    vp = [d for d in data if d["cp"]["visible_pass"]]
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in vp])
    groups = np.array([d["cp"]["task_id"] for d in vp])
    strata = np.array([d["cp"]["benchmark"] for d in vp])
    s = {}
    for name in (A, B):
        v = [score_final(d, routers[name]) for d in vp]
        missing = [d["cp"]["checkpoint_id"] for d, x in zip(vp, v) if x is None]
        if missing:
            raise SystemExit(f"STOP: {len(missing)} visible-pass rows have no {name} score (e.g. {missing[0]})")
        s[name] = np.array(v, float)
    res = P.bootstrap_test(y, groups, strata, s[A], s[B])
    out = {"version": VERSION, "run": args.run_id, "split": args.split, "routers": cfg["version"],
           "population": "visible-pass checkpoints, Amendment A2 exclusions applied",
           "n_visible_pass": len(vp), "n_hidden_fail": int(y.sum()), "n_tasks": int(len(set(groups))),
           "n_fail_tasks": int(len(set(groups[y == 1]))),
           "auroc": {A: float(roc_auc_score(y, s[A])), B: float(roc_auc_score(y, s[B]))},
           "test": {"a": A, "b": B, **res, "alpha": 0.05, "reject_at_0.05": res["p_two_sided"] < 0.05,
                    "family": "separate from the H1/H2 Holm family"}}
    print(f"{args.run_id}: {len(vp)} visible-pass rows, {int(y.sum())} hidden fail on {out['n_fail_tasks']} tasks")
    print(f"AUROC {A} {out['auroc'][A]:.3f}, {B} {out['auroc'][B]:.3f}; d = {res['delta']:+.4f} "
          f"(95% CI {res['ci95'][0]:+.4f} to {res['ci95'][1]:+.4f}); p = {res['p_two_sided']:.4f}; B = {res['n_boot']}")
    path = RESULTS / f"q9b_direct_jev_test_{args.run_id}.json"
    if args.split == "test" and path.exists():
        raise SystemExit(f"{path} exists; the prespecified test is written once")
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
