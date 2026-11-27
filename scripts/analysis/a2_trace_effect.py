"""Why do the reasoning judgments not help (and at 1.7B hurt) the full router? Exploratory, version 1.

    uv run python scripts/analysis/a2_trace_effect.py

For the paper revision (Reviewer A, second comment). Not prespecified; descriptive and exploratory. No model
is fitted on test rows: every refit uses development rows only and is then scored on test. Rows are
visible-pass checkpoints with the Amendment A2 exclusions (load_labelled). Workers: Qwen3-1.7B (dev pilot-v1,
pilot-v1b; test main-test-v1; frozen routers routers-v2) and Qwen3.5-9B (dev q9b-pilot-v1, q9b-pilot-v1b;
test q9b-test-v1; routers-q9b-v1). The 8B run data is not in this repository.

The full router takes its three code judgments from the history request and its five reasoning judgments
from the trace request (predict.jev_vector), so full minus code (H2) measures the five reasoning judgments.

1. Signal of each reasoning judgment: single-feature AUROC on dev and on test, oriented toward failure
   (on_task and stated_fix_matches_change reversed, as in Strong4), and the frozen full router's standardized
   weight for it. A weight whose sign disagrees with the dev direction of its own feature reflects overlap
   with the other features; a test AUROC near 0.5 means the feature adds noise on test.
2. Dev out-of-fold AUROC of the code and full routers (the freeze's own scores) against their test AUROC.
3. Drop-one refits: the full router refitted on dev without one reasoning judgment, scored on test.
4. Same question, two requests: code_likely_fails and special_cases_visible_tests from the history request
   and from the trace request. (a) AUROC of each by thinking-length tertile (cut points from all rows,
   label-free). (b) The mean trace-minus-history score for hidden-fail and hidden-pass rows: the trace hurts
   ranking when it lowers the score of failing answers or raises the score of passing answers.
Writes results/a2_trace_effect_v1.json.
"""

from __future__ import annotations

import json
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg  # noqa: E402

VERSION = "a2-trace-effect-v1"
OUT = RESULTS / "a2_trace_effect_v1.json"
WORKERS = {
    "Qwen3-1.7B": {"dev": ["pilot-v1", "pilot-v1b"], "test": ["main-test-v1"], "routers": "routers_v2.json",
                   "dev_scores": RESULTS / "dev_router_scores.json"},
    "Qwen3.5-9B": {"dev": ["q9b-pilot-v1", "q9b-pilot-v1b"], "test": ["q9b-test-v1"], "routers": "routers_q9b-v1.json",
                   "dev_scores": RESULTS / "dev_router_scores_q9b-v1.json"}}
REASONING = [q for q in P.THINKING_QS if q != "clear_next_step"]  # not applicable at a terminal visible pass
SAME = ["code_likely_fails", "special_cases_visible_tests"]


def auc(y, x) -> float | None:
    x = np.asarray(x, float)
    return None if len(set(y)) < 2 or np.ptp(x) == 0 else float(roc_auc_score(y, x))


def oriented(q: str, v: float) -> float:
    return 1.0 - v if q in P.TRUE_IS_GOOD else v


def judgment(d: dict, q: str, arm: str) -> float | None:
    rec = d[arm]
    if rec is None or rec["applicability"].get(q) != "applicable":
        return None
    return P._num(rec["features"].get(q))


def single(rows: list[dict], q: str, arm: str) -> dict:
    pairs = [(0 if d["cp"]["hidden"]["passed"] else 1, judgment(d, q, arm)) for d in rows]
    pairs = [(y, oriented(q, v)) for y, v in pairs if v is not None]
    y = np.array([p[0] for p in pairs])
    return {"n": len(pairs), "fail": int(y.sum()), "auroc": auc(y, [p[1] for p in pairs])}


def main() -> int:
    rg = load_rg()
    out: dict = {"version": VERSION, "prespecified": False, "workers": {}}
    for w, cfg in WORKERS.items():
        dev = [d for d in rg.load(cfg["dev"], split="dev", require_ok=False) if d["cp"]["visible_pass"]]
        test = [d for d in rg.load(cfg["test"], split="test", require_ok=False) if d["cp"]["visible_pass"]]
        routers = json.loads((CONFIGS / cfg["routers"]).read_text(encoding="utf-8"))["routers"]
        full = routers["cheap+code+thinking"]["model"]
        weight = dict(zip(full["columns"], full["coef"]))
        res: dict = {"routers": cfg["routers"], "n_dev": len(dev), "n_test": len(test)}

        # 1. Signal of each reasoning judgment.
        res["reasoning_judgments"] = {
            q: {"dev": single(dev, q, "trace"), "test": single(test, q, "trace"),
                "frozen_weight": weight.get(f"jev_{q}"),
                "weight_toward_failure": None if weight.get(f"jev_{q}") is None else
                (weight[f"jev_{q}"] * (-1 if q in P.TRUE_IS_GOOD else 1))} for q in REASONING}

        # 2. Dev out-of-fold against test.
        dev_s = json.loads(cfg["dev_scores"].read_text(encoding="utf-8"))["scores"]
        yd = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in dev])
        yt = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in test])
        g, st = np.array([d["cp"]["task_id"] for d in test]), np.array([d["cp"]["benchmark"] for d in test])
        Xd, cols = rg.design(dev, "cheap+code+thinking", True)
        Xt, _ = rg.design(test, "cheap+code+thinking", True)
        Xcd, ccols = rg.design(dev, "cheap+code", True)
        Xct, _ = rg.design(test, "cheap+code", True)
        s_full = P.predict_final(P.fit_final(Xd, yd, cols), Xt)
        s_code = P.predict_final(P.fit_final(Xcd, yd, ccols), Xct)
        res["dev_oof_vs_test"] = {
            name: {"dev_oof": auc(yd, [dev_s[name][d["cp"]["checkpoint_id"]] for d in dev]),
                   "test_refit": auc(yt, s)} for name, s in (("cheap+code", s_code), ("cheap+code+thinking", s_full))}

        # 3. Drop-one refits (dev fit, test score).
        drop = {}
        for q in REASONING:
            keep = [i for i, c in enumerate(cols) if c != f"jev_{q}"]
            m = P.fit_final(Xd[:, keep], yd, [cols[i] for i in keep])
            s = P.predict_final(m, Xt[:, keep])
            drop[q] = {"test_auroc": auc(yt, s), "minus_full": auc(yt, s) - auc(yt, s_full)}
        keep = [i for i, c in enumerate(cols) if not any(c == f"jev_{q}" for q in REASONING)]
        drop["all five"] = {"test_auroc": auc(yt, P.predict_final(P.fit_final(Xd[:, keep], yd, [cols[i] for i in keep]), Xt[:, keep]))}
        res["drop_one"] = drop
        res["full_minus_code_refit"] = P.bootstrap_test(yt, g, st, s_code, s_full)

        # 4. Same question, history request against trace request.
        tok = np.array([float(d["cp"]["features"]["thinking_tokens"]) for d in test])
        cuts = np.quantile(tok, [1 / 3, 2 / 3])
        tert = np.digitize(tok, cuts)
        same = {}
        for q in SAME:
            h = np.array([judgment(d, q, "history") for d in test], dtype=object)
            t = np.array([judgment(d, q, "trace") for d in test], dtype=object)
            ok = np.array([a is not None and b is not None for a, b in zip(h, t)])
            hh, tt, yy, te = h[ok].astype(float), t[ok].astype(float), yt[ok], tert[ok]
            diff = tt - hh
            same[q] = {
                "rows": int(ok.sum()), "auroc_history": auc(yy, hh), "auroc_trace": auc(yy, tt),
                "mean_shift_fail": float(diff[yy == 1].mean()), "mean_shift_pass": float(diff[yy == 0].mean()),
                "share_fail_lowered": float((diff[yy == 1] < 0).mean()), "share_pass_raised": float((diff[yy == 0] > 0).mean()),
                "by_thinking_tertile": [{"tokens_from": float(([tok.min()] + list(cuts))[k]),
                                         "rows": int((te == k).sum()), "fail": int(yy[te == k].sum()),
                                         "auroc_history": auc(yy[te == k], hh[te == k]),
                                         "auroc_trace": auc(yy[te == k], tt[te == k])} for k in range(3)]}
        res["same_question"] = same
        out["workers"][w] = res

        print(f"\n== {w}: dev {len(dev)}, test {len(test)} visible-pass rows")
        print("reasoning judgment                 dev AUROC  test AUROC  frozen weight toward failure")
        for q, v in res["reasoning_judgments"].items():
            print(f"  {q:34s} {v['dev']['auroc']:.3f}      {v['test']['auroc']:.3f}       {v['weight_toward_failure']:+.3f}")
        for k, v in res["dev_oof_vs_test"].items():
            print(f"  {k:22s} dev OOF {v['dev_oof']:.3f}  test (refit) {v['test_refit']:.3f}")
        r = res["full_minus_code_refit"]
        print(f"  full - code on test {r['delta']:+.4f} {r['ci95']}")
        for q, v in drop.items():
            extra = f" ({v['minus_full']:+.4f} vs full)" if "minus_full" in v else ""
            print(f"  without {q:34s} test {v['test_auroc']:.3f}{extra}")
        for q, v in same.items():
            print(f"  same question {q}: history {v['auroc_history']:.3f}, trace {v['auroc_trace']:.3f}; "
                  f"shift fail {v['mean_shift_fail']:+.3f}, pass {v['mean_shift_pass']:+.3f}")
            for b in v["by_thinking_tertile"]:
                print(f"     tokens >= {b['tokens_from']:6.0f}: n {b['rows']:4d} fail {b['fail']:3d}  "
                      f"history {b['auroc_history']:.3f}  trace {b['auroc_trace']:.3f}")
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
