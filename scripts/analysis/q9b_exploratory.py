"""Exploratory analyses of the Qwen3.5-9B results for the paper revision, version 1. Not prespecified.

    uv run python scripts/analysis/q9b_exploratory.py

Descriptive and exploratory; nothing here changes a frozen router, threshold or test result, and no
model is fitted on test rows (every fit below uses development rows only and is then scored on test).
All rows are visible-pass checkpoints with the Amendment A2 exclusions applied (load_labelled).

1. Workers side by side: the frozen test analyses of Qwen3-1.7B (docs/results/test_analysis_main-test-v1.json),
   Qwen3-8B (docs/results/test_analysis_q8b-test-v1.json) and Qwen3.5-9B (results/test_analysis_q9b-test-v1.json):
   H1/H2, Table 1 AUROCs and the history-arm code_likely_fails AUROC (the 9B "direct jev" router).
2. Single-feature AUROC of every telemetry-only (cheap) column, dev and test, for 1.7B and 9B (the 8B run
   data is not in this repository). Hidden fail = positive class; 0.5 = no signal either way.
3. Top-1 emulation. DeepInfra returns only the top-1 logprob, so the 9B confidence features use k = 1
   (docs/q9b-plan.md part A); the vLLM studies used k = 5. The 1.7B logprob files hold the k = 5 token
   confidence and the sampled token's logprob, not the five alternatives. Minus the sampled logprob is the
   k = 1 confidence whenever the sampled token is the top-1 token, and an upper bound otherwise; the share of
   tokens where the two agree is measured on the 9B files, which hold both. The script first rebuilds the
   stored k = 5 features from the files (a check of the rebuild), then replaces thinking_tail_conf and
   thinking_bottom10_group_conf with the k = 1 values. Fits on 1.7B dev (pilot-v1, pilot-v1b), scores
   1.7B test (main-test-v1): telemetry-only with k = 5 features, with k = 1 features, and without the
   eight logprob columns; the last also for 9B (dev q9b-pilot-v1/-v1b, test q9b-test-v1). Paired whole-task
   bootstrap (predict.bootstrap_test, 19,999 draws), exploratory, no multiplicity adjustment.
4. Dev out-of-fold AUROC (the freeze's own scores) against test AUROC of the frozen telemetry-only router,
   per benchmark, for 1.7B and 9B.
Writes results/q9b_exploratory_v1.json.
"""

from __future__ import annotations

import json
import math
import sys

import numpy as np
from sklearn.metrics import roc_auc_score

from system1.config import RESULTS, ROOT
from system1.eval import predict as P
from system1.loop.generate import CONF_WINDOW

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg  # noqa: E402

VERSION = "q9b-exploratory-v1"
OUT = RESULTS / "q9b_exploratory_v1.json"
WORKERS = {"Qwen3-1.7B": ROOT / "docs/results/test_analysis_main-test-v1.json",
           "Qwen3-8B": ROOT / "docs/results/test_analysis_q8b-test-v1.json",
           "Qwen3.5-9B": RESULTS / "test_analysis_q9b-test-v1.json"}
RUNS = {"Qwen3-1.7B": {"dev": ["pilot-v1", "pilot-v1b"], "test": ["main-test-v1"],
                       "dev_scores": RESULTS / "dev_router_scores.json"},
        "Qwen3.5-9B": {"dev": ["q9b-pilot-v1", "q9b-pilot-v1b"], "test": ["q9b-test-v1"],
                       "dev_scores": RESULTS / "dev_router_scores_q9b-v1.json"}}
TABLE1 = ["cheap", "cheap+code", "cheap+code+thinking", "cheap+strong4", "strong4 mean",
          "pinocchio (input-v1)", "logprob tail confidence"]
LOGPROB_COLS = P.LOGPROB + [f"{k}__missing" for k in P.LOGPROB]
REBUILT = ("thinking_tail_conf", "thinking_bottom10_group_conf")


def summary(conf: np.ndarray, window: int = CONF_WINDOW) -> dict[str, float]:
    """tail_conf and bottom10_group_conf as in generate.confidence_summary, from token confidences."""
    w = min(window, len(conf))
    groups = np.convolve(conf, np.ones(w) / w, mode="valid")
    k = max(1, math.ceil(0.1 * len(groups)))
    return {"thinking_tail_conf": round(float(conf[-w:].mean()), 4),
            "thinking_bottom10_group_conf": round(float(np.sort(groups)[:k].mean()), 4)}


def arrays(run: str, cp: dict) -> dict:
    path = RESULTS / "runs" / run / "logprobs" / f"{cp['checkpoint_id'].replace('/', '_')}_{cp['exec_id'][:8]}.npz"
    with np.load(path) as z:
        return {k: z[k].astype(np.float64) for k in z.files}


def vp_rows(rg, runs: list[str], split: str) -> list[dict]:
    return [d for d in rg.load(runs, split=split, require_ok=False) if d["cp"]["visible_pass"]]


def labels(rows: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in rows])
    return (y, np.array([d["cp"]["task_id"] for d in rows]), np.array([d["cp"]["benchmark"] for d in rows]))


def with_k1(rows: list[dict]) -> tuple[list[dict], dict]:
    """Copies of the rows with the two rebuilt features at k = 1, and the check of the k = 5 rebuild."""
    out, err, n_thinking = [], [], 0
    for d in rows:
        f = dict(d["cp"]["features"])
        a = arrays(d["run"], d["cp"])
        conf5, lp = a.get("thinking_conf"), a.get("thinking_logprob")
        if conf5 is not None and len(conf5) and f.get("thinking_tail_conf") is not None:
            n_thinking += 1
            rebuilt = summary(conf5)
            err += [abs(rebuilt[k] - f[k]) for k in REBUILT]
            f.update(summary(-lp))
        out.append({**d, "cp": {**d["cp"], "features": f}})
    return out, {"rows_with_thinking_logprobs": n_thinking, "k5_rebuild_abs_error_max": max(err) if err else None,
                 "k5_rebuild_abs_error_mean": float(np.mean(err)) if err else None}


def k1_agreement(rows: list[dict]) -> dict:
    """9B files: the stored k = 1 confidence against minus the sampled logprob."""
    n = same = 0
    gap = []
    for d in rows:
        a = arrays(d["run"], d["cp"])
        c, lp = a.get("thinking_conf"), a.get("thinking_logprob")
        if c is None or not len(c):
            continue
        diff = (-lp) - c  # >= 0 up to float16 rounding: the sampled token is at most as likely as the top-1
        n += len(c)
        same += int(np.sum(np.abs(diff) < 2e-3))
        gap.append(diff)
    gap = np.concatenate(gap)
    return {"tokens": n, "share_sampled_equals_top1": same / n, "mean_gap": float(gap.mean()),
            "p99_gap": float(np.percentile(gap, 99))}


def fit_score(dev: list[dict], test: list[dict], rg, drop: list[str] = ()) -> np.ndarray:
    Xd, cols = rg.design(dev, "cheap", True)
    Xt, _ = rg.design(test, "cheap", True)
    keep = [i for i, c in enumerate(cols) if c not in drop]
    yd = labels(dev)[0]
    model = P.fit_final(Xd[:, keep], yd, [cols[i] for i in keep])
    return P.predict_final(model, Xt[:, keep])


def feature_aurocs(rows: list[dict]) -> dict:
    y = labels(rows)[0]
    out = {}
    for c in P.columns("cheap", True):
        vec = [P.cheap_vector(d["cp"]["features"], d["has_trace"]) for d in rows]
        x = np.array([v[c] for v in vec])
        out[c] = None if np.ptp(x) == 0 else float(roc_auc_score(y, x))
    return out


def main() -> int:
    rg = load_rg()
    out: dict = {"version": VERSION, "prespecified": False}

    # 1. Workers side by side.
    side = {}
    for w, path in WORKERS.items():
        t = json.loads(path.read_text(encoding="utf-8"))
        tb, sq = t["table1"], t["same_question"]
        side[w] = {"file": str(path.relative_to(ROOT)), "n_visible_pass": t["n_visible_pass"],
                   "hidden_fail": tb["cheap"]["positives"], "fail_tasks": tb["cheap"]["positive_tasks"],
                   "tasks": tb["cheap"]["tasks"],
                   "H1": {k: t["holm_family"]["primary"][k] for k in ("delta", "ci95", "p_holm")},
                   "H2": {k: t["holm_family"]["secondary"][k] for k in ("delta", "ci95", "p_holm")},
                   "auroc": {r: tb[r]["auroc"] for r in TABLE1},
                   "direct_jev_history_code_likely_fails": sq["code_likely_fails"]["history_arm"],
                   "same_question_trace_minus_history": {q: v["trace_arm"] - v["history_arm"]
                                                         for q, v in sq.items() if "trace_arm" in v}}
    out["workers"] = side
    print("worker        H1 delta  Holm p  cheap  full   strong4  directJev")
    for w, s in side.items():
        print(f"{w:12s} {s['H1']['delta']:+.3f}   {s['H1']['p_holm']:.4f}  {s['auroc']['cheap']:.3f}  "
              f"{s['auroc']['cheap+code+thinking']:.3f}  {s['auroc']['strong4 mean']:.3f}    "
              f"{s['direct_jev_history_code_likely_fails']:.3f}")

    data = {w: {sp: vp_rows(rg, r[sp], sp) for sp in ("dev", "test")} for w, r in RUNS.items()}

    # 2. Single-feature AUROC.
    out["feature_auroc"] = {w: {sp: feature_aurocs(rows) for sp, rows in d.items()} for w, d in data.items()}
    print("\nfeature                         1.7B dev  1.7B test  9B dev  9B test")
    fa = out["feature_auroc"]
    for c in P.columns("cheap", True):
        vals = [fa[w][sp][c] for w in RUNS for sp in ("dev", "test")]
        if all(v is None for v in vals):
            continue
        print(f"{c:30s} " + "  ".join("  -   " if v is None else f"{v:.3f} " for v in vals))

    # 3. Top-1 emulation and the router without logprob features.
    agree = k1_agreement(data["Qwen3.5-9B"]["test"])
    small_dev, chk_dev = with_k1(data["Qwen3-1.7B"]["dev"])
    small_test, chk_test = with_k1(data["Qwen3-1.7B"]["test"])
    y, g, st = labels(data["Qwen3-1.7B"]["test"])
    s5 = fit_score(data["Qwen3-1.7B"]["dev"], data["Qwen3-1.7B"]["test"], rg)
    s1 = fit_score(small_dev, small_test, rg)
    s0 = fit_score(data["Qwen3-1.7B"]["dev"], data["Qwen3-1.7B"]["test"], rg, LOGPROB_COLS)
    k1_feats = feature_aurocs(small_test)
    y9, g9, st9 = labels(data["Qwen3.5-9B"]["test"])
    n9 = fit_score(data["Qwen3.5-9B"]["dev"], data["Qwen3.5-9B"]["test"], rg)
    n0 = fit_score(data["Qwen3.5-9B"]["dev"], data["Qwen3.5-9B"]["test"], rg, LOGPROB_COLS)
    out["top1"] = {
        "k1_agreement_9b_test": agree, "rebuild_check_1.7b_dev": chk_dev, "rebuild_check_1.7b_test": chk_test,
        "feature_auroc_1.7b_test_k5": {c: fa["Qwen3-1.7B"]["test"][c] for c in REBUILT},
        "feature_auroc_1.7b_test_k1": {c: k1_feats[c] for c in REBUILT},
        "1.7b_cheap_refit": {"auroc_k5": float(roc_auc_score(y, s5)), "auroc_k1": float(roc_auc_score(y, s1)),
                             "auroc_no_logprob": float(roc_auc_score(y, s0)),
                             "k1_minus_k5": P.bootstrap_test(y, g, st, s5, s1),
                             "no_logprob_minus_k5": P.bootstrap_test(y, g, st, s5, s0)},
        "9b_cheap_refit": {"auroc_with_logprob": float(roc_auc_score(y9, n9)),
                           "auroc_no_logprob": float(roc_auc_score(y9, n0)),
                           "no_logprob_minus_with": P.bootstrap_test(y9, g9, st9, n9, n0)}}
    t1 = out["top1"]
    print(f"\n9B tokens with sampled = top-1: {agree['share_sampled_equals_top1']:.1%} of {agree['tokens']}")
    print(f"1.7B k=5 rebuild error: max {chk_test['k5_rebuild_abs_error_max']}, mean {chk_test['k5_rebuild_abs_error_mean']}")
    r = t1["1.7b_cheap_refit"]
    print(f"1.7B cheap refit on dev, test AUROC: k5 {r['auroc_k5']:.3f}, k1 {r['auroc_k1']:.3f}, no logprob "
          f"{r['auroc_no_logprob']:.3f}; k1-k5 {r['k1_minus_k5']['delta']:+.3f} {r['k1_minus_k5']['ci95']}, "
          f"p {r['k1_minus_k5']['p_two_sided']:.3f}")
    r = t1["9b_cheap_refit"]
    print(f"9B cheap refit: with logprob {r['auroc_with_logprob']:.3f}, without {r['auroc_no_logprob']:.3f}; "
          f"d {r['no_logprob_minus_with']['delta']:+.3f} {r['no_logprob_minus_with']['ci95']}")

    # 4. Dev out-of-fold against test, per benchmark.
    shift = {}
    for w, r in RUNS.items():
        dev_s = json.loads(r["dev_scores"].read_text(encoding="utf-8"))["scores"]["cheap"]
        t = json.loads(WORKERS[w].read_text(encoding="utf-8"))
        rows = data[w]["dev"]
        yd = labels(rows)[0]
        sd = np.array([dev_s[d["cp"]["checkpoint_id"]] for d in rows])
        bench = np.array([d["cp"]["benchmark"] for d in rows])
        shift[w] = {"all": {"dev_oof": float(roc_auc_score(yd, sd)), "test": t["table1"]["cheap"]["auroc"],
                            "dev_n": len(rows), "dev_fail": int(yd.sum())}}
        for b in sorted(set(bench)):
            m = bench == b
            shift[w][b] = {"dev_oof": float(roc_auc_score(yd[m], sd[m])), "dev_n": int(m.sum()),
                           "dev_fail": int(yd[m].sum()), "test": t["by_benchmark"][b]["cheap"]["auroc"],
                           "test_n": t["by_benchmark"][b]["cheap"]["n"],
                           "test_fail": t["by_benchmark"][b]["cheap"]["positives"]}
    out["dev_vs_test_cheap"] = shift
    print("\ntelemetry-only, dev out-of-fold vs test")
    for w, s in shift.items():
        for b, v in s.items():
            print(f"  {w:11s} {b:11s} dev {v['dev_oof']:.3f}  test {v['test']:.3f}")

    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
