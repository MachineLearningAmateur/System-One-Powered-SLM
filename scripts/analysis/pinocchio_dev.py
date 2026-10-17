"""Dev-only, descriptive: Pinocchio-0.8B against the other predictors (Table 1 view).

    uv run python scripts/analysis/pinocchio_dev.py

Visible-pass dev checkpoints (y = 1 hidden fail). Scores: the frozen dev scores in
results/dev_router_scores_v2.json (OOF for the LRs; no fitting for the mean and
Pinocchio), plus the logprob comparator (minus the thinking tail confidence) and a
descriptive cheap+Pinocchio LR. Pairs bootstrapped over tasks.
"""
import contextlib
import importlib.util
import io
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("rg", ROOT / "scripts" / "resource_guide.py")
rg = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(rg)
from system1.eval import predict as P  # noqa: E402

data = [d for d in rg.load(["pilot-v1", "pilot-v1b"]) if d["cp"]["visible_pass"]]
ids = [d["cp"]["checkpoint_id"] for d in data]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
groups = np.array([d["cp"]["task_id"] for d in data])
bench = np.array([d["cp"]["benchmark"] for d in data])
cap = np.array([bool(d["cp"]["features"]["cap_hit"]) for d in data])
dev = json.loads((ROOT / "results" / "dev_router_scores_v2.json").read_text())["scores"]
S = {k: np.array([dev[k][c] for c in ids]) for k in dev}
tail = np.array([d["cp"]["features"]["thinking_tail_conf"] or 0.0 for d in data])
S["logprob (-tail conf)"] = -tail
# descriptive: cheap + Pinocchio in the frozen pipeline (not a frozen router)
Xc, _ = rg.design(data, "cheap", True)
X = np.column_stack([Xc, S["pinocchio"]])
S["cheap + pinocchio (descr.)"] = np.mean([P.oof_scores(X, y, groups, s) for s in range(rg.REPEATS)], axis=0)
X2, _ = rg.design(data, "cheap+code+thinking", True)
X2 = np.column_stack([X2, S["pinocchio"]])
S["full + pinocchio (descr.)"] = np.mean([P.oof_scores(X2, y, groups, s) for s in range(rg.REPEATS)], axis=0)

print(f"{len(y)} visible-pass dev checkpoints, {y.sum()} hidden fail, {len(set(groups[y == 1]))} positive tasks")
w = P.task_weights(groups)
order = ["cheap", "cheap+code", "cheap+code+thinking", "cheap+strong4", "strong4 mean", "pinocchio",
         "logprob (-tail conf)", "cheap + pinocchio (descr.)", "full + pinocchio (descr.)"]
pairs = [("pinocchio", "cheap"), ("pinocchio", "strong4 mean"), ("pinocchio", "cheap+code+thinking"),
         ("cheap", "cheap + pinocchio (descr.)"), ("cheap+code+thinking", "full + pinocchio (descr.)")]
bs = P.task_bootstrap(y, groups, {k: S[k] for k in order}, pairs)
print(f"\n{'predictor':30s} AUROC (95%)            task-wtd  HE+    MBPP+  cap-hit(30)")
for k in order:
    lo, hi = bs["auroc"][k]
    sub = [roc_auc_score(y[m], S[k][m]) for m in (bench == "humaneval+", bench == "mbpp+", cap)]
    print(f"{k:30s} {roc_auc_score(y, S[k]):.3f} ({lo:.3f}-{hi:.3f})   {roc_auc_score(y, S[k], sample_weight=w):.3f}"
          f"    {sub[0]:.3f}  {sub[1]:.3f}  {sub[2]:.3f}")
print()
for a, b in pairs:
    lo, hi = bs["delta"][f"{b} - {a}"]
    print(f"d[{b} - {a}] = {roc_auc_score(y, S[b]) - roc_auc_score(y, S[a]):+.3f} ({lo:+.3f} to {hi:+.3f})")
print("\nSpearman with Pinocchio:", {k: round(spearmanr(S["pinocchio"], S[k])[0], 2)
                                     for k in ("cheap", "strong4 mean", "cheap+code+thinking", "logprob (-tail conf)")})
recs = [json.loads(l) for r in ("pilot-v1", "pilot-v1b") for l in open(ROOT / "results" / "runs" / r / "pinocchio_scores.jsonl")]
print(f"CPU seconds per checkpoint: mean {np.mean([r['cpu_seconds'] for r in recs]):.2f}, "
      f"p_correct mean {np.mean([r['p_correct'] for r in recs]):.3f}")
