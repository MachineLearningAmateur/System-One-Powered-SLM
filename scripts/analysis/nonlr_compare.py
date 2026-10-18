"""Exploratory (October 18, after the planned test analysis): Jev's raw answers without any LR
against the other judges that use no LR, on the visible-pass test checkpoints of main-test-v1.

    uv run python scripts/analysis/nonlr_compare.py

Selected after the test results were seen (code_likely_fails is one of eleven answers), so the
numbers are descriptive, not tests. Same paired task bootstrap as the Holm family
(predict.bootstrap_test, 19,999 replicates, within benchmark).
"""
import json, sys
import numpy as np
from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P
sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg, pinocchio_rows, score_final
routers = json.loads((CONFIGS / "routers_v2.json").read_text(encoding="utf-8"))["routers"]
data = load_rg().load(["main-test-v1"], split="test", require_ok=False)
vp = [d for d in data if d["cp"]["visible_pass"]]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in vp])
g = np.array([d["cp"]["task_id"] for d in vp]); st = np.array([d["cp"]["benchmark"] for d in vp])
pin = pinocchio_rows(["main-test-v1"], list(routers["pinocchio"]["model"]["setup"]), [d["cp"] for d in data], True)
S = {"Jev code_likely_fails (raw)": np.array([d["history"]["features"]["code_likely_fails"] for d in vp]),
     "Jev strong4 mean": np.array([score_final(d, routers["strong4 mean"]) for d in vp]),
     "Pinocchio": np.array([pin[d["cp"]["checkpoint_id"]]["score"] for d in vp]),
     "logprob tail confidence": np.array([P.logprob_comparator(d["cp"]["features"]) for d in vp]),
     "cheap LR": np.array([score_final(d, routers["cheap"]) for d in vp])}
pairs = [(b, a) for a in ("Jev code_likely_fails (raw)", "Jev strong4 mean") for b in ("Pinocchio", "logprob tail confidence", "cheap LR")]
for b, a in pairs:
    t = P.bootstrap_test(y, g, st, S[b], S[a])
    print(f"{a:28s} - {b:24s} {t['delta']:+.3f} (95% {t['ci95'][0]:+.3f} to {t['ci95'][1]:+.3f}) B={t['n_boot']}")
