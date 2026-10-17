"""Dev-only, descriptive: Pinocchio-0.8B against the other predictors (Table 1 view).

    uv run python scripts/analysis/pinocchio_dev.py

Visible-pass dev checkpoints (y = 1 hidden fail): 470 checkpoints from 205 tasks, 116
hidden fails from 49 tasks. Scores: the frozen dev scores in
results/dev_router_scores_v2.json (OOF for the LRs; no fitting for the strong4 mean
and Pinocchio input-v1), Pinocchio input-v2 (the executed code as the answer; a
dev-informed sensitivity frozen before it was scored), the frozen logprob comparator
(predict.logprob_comparator), and a descriptive cheap+Pinocchio LR. Intervals
bootstrap tasks over fixed scores, without refitting. Pinocchio records are used only
if they match the current execution and rebuilt input (pinocchio_input.select_records).
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import average_precision_score, roc_auc_score

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts" / "resource_guide.py")
rg = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(rg)
from system1.eval import predict as P  # noqa: E402
from system1.features import pinocchio_input as PI  # noqa: E402
from system1.loop.tasks import load_tasks  # noqa: E402

RUNS = ["pilot-v1", "pilot-v1b"]
data = [d for d in rg.load(RUNS) if d["cp"]["visible_pass"]]
ids = [d["cp"]["checkpoint_id"] for d in data]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
groups = np.array([d["cp"]["task_id"] for d in data])
bench = np.array([d["cp"]["benchmark"] for d in data])
cap = np.array([bool(d["cp"]["features"]["cap_hit"]) for d in data])
dev = json.loads((ROOT / "results" / "dev_router_scores_v2.json").read_text())["scores"]
S = {k: np.array([dev[k][c] for c in ids]) for k in dev}

tasks = load_tasks()
pin_rec = {}
for v in PI.INPUT_VERSIONS:
    pin_rec[v] = {}
    for rid in RUNS:
        cps = [d["cp"] for d in data if d["run"] == rid]
        recs, counts = PI.select_records(PI.read_records(ROOT / "results" / "runs" / rid, v), cps, tasks, v,
                                         require_pinned=(v == PI.V2))
        pin_rec[v].update(recs)
        print(f"{v} {rid}: {counts}")
assert np.allclose([pin_rec[PI.V1][c]["score"] for c in ids], S["pinocchio"])  # the frozen router's scores
have_v2 = len(pin_rec[PI.V2]) == len(ids)
if have_v2:
    S["pinocchio input-v2 (code)"] = np.array([pin_rec[PI.V2][c]["score"] for c in ids])
missing_lp = sum(d["cp"]["features"].get("thinking_tail_conf") is None for d in data)
S["logprob comparator"] = np.array([P.logprob_comparator(d["cp"]["features"]) for d in data])
Xc, _ = rg.design(data, "cheap", True)
S["cheap + pinocchio (descr.)"] = np.mean([P.oof_scores(np.column_stack([Xc, S["pinocchio"]]), y, groups, s)
                                           for s in range(rg.REPEATS)], axis=0)

print(f"\n{len(y)} visible-pass dev checkpoints, {len(set(groups))} tasks, {y.sum()} hidden fail from "
      f"{len(set(groups[y == 1]))} tasks; logprob comparator missing: {missing_lp}")
w = P.task_weights(groups)
order = ["cheap", "cheap+code", "cheap+code+thinking", "cheap+strong4", "strong4 mean", "pinocchio"] + \
        (["pinocchio input-v2 (code)"] if have_v2 else []) + ["logprob comparator", "cheap + pinocchio (descr.)"]
pairs = [("pinocchio", "cheap"), ("pinocchio", "strong4 mean"), ("cheap", "logprob comparator"),
         ("cheap", "cheap + pinocchio (descr.)")] + ([("pinocchio", "pinocchio input-v2 (code)")] if have_v2 else [])
bs = P.task_bootstrap(y, groups, {k: S[k] for k in order}, pairs)
bw = P.task_bootstrap(y, groups, {k: S[k] for k in order}, pairs, weighted=True)
print(f"\n{'predictor':28s} AUROC (95%)          task-wtd  AUPRC  FNR@5%FPR  HE+    MBPP+  cap-hit(30)")
for k in order:
    lo, hi = bs["auroc"][k]
    sub = [roc_auc_score(y[m], S[k][m]) for m in (bench == "humaneval+", bench == "mbpp+", cap)]
    f = P.fnr_at_fpr(y, S[k])
    print(f"{k:28s} {roc_auc_score(y, S[k]):.3f} ({lo:.3f}-{hi:.3f})  {roc_auc_score(y, S[k], sample_weight=w):.3f}"
          f"    {average_precision_score(y, S[k]):.3f}  {f['fnr']:.3f}      {sub[0]:.3f}  {sub[1]:.3f}  {sub[2]:.3f}")
print(f"(prevalence {y.mean():.3f}: the AUPRC of a random score)")
for a, b in pairs:
    lo, hi = bs["delta"][f"{b} - {a}"]
    wlo, whi = bw["delta"][f"{b} - {a}"]
    d = roc_auc_score(y, S[b]) - roc_auc_score(y, S[a])
    dw = roc_auc_score(y, S[b], sample_weight=w) - roc_auc_score(y, S[a], sample_weight=w)
    print(f"d[{b} - {a}] = {d:+.3f} ({lo:+.3f} to {hi:+.3f}); task-weighted {dw:+.3f} ({wlo:+.3f} to {whi:+.3f})")

p1 = np.array([pin_rec[PI.V1][c]["p_correct"] for c in ids])
print(f"\ncalibration on these rows: mean p_correct input-v1 {p1.mean():.3f}"
      + (f", input-v2 {np.mean([pin_rec[PI.V2][c]['p_correct'] for c in ids]):.3f}" if have_v2 else "")
      + f"; observed pass {1 - y.mean():.3f}")
print("Spearman with Pinocchio input-v1:", {k: round(float(spearmanr(S["pinocchio"], S[k])[0]), 2)
                                           for k in order if k != "pinocchio"})
secs = [pin_rec[PI.V1][c]["cpu_seconds"] for c in ids]
print(f"elapsed CPU inference seconds per decision checkpoint (input-v1): {np.mean(secs):.2f}")
