"""Exploratory (October 18, after the planned test analysis): why does the trace call judge the
code worse than the history call? Splits the same-question contrast by thinking length and by
the loop flag, and reports ties and mean probabilities of each call.

    uv run python scripts/analysis/trace_diagnostics.py

Descriptive only; run after the test results were seen.
"""
import sys
from collections import Counter
import numpy as np
from sklearn.metrics import roc_auc_score
from system1.config import ROOT
sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg
data = [d for d in load_rg().load(["main-test-v1"], split="test", require_ok=False) if d["cp"]["visible_pass"]]
y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in data])
tt = np.array([d["cp"]["features"]["thinking_tokens"] for d in data])
loop = np.array([bool(d["cp"]["features"].get("loop_flag")) for d in data])
print("rows", len(y), "loop_flag", loop.sum(), "empty thinking", (tt == 0).sum())
for q in ("code_likely_fails", "special_cases_visible_tests"):
    h = np.array([d["history"]["features"][q] for d in data]); t = np.array([d["trace"]["features"][q] for d in data])
    print(f"\n{q}: distinct values history {len(set(h))}, trace {len(set(t))}; share at mode history "
          f"{Counter(h).most_common(1)[0][1]/len(h):.2f}, trace {Counter(t).most_common(1)[0][1]/len(t):.2f}")
    print(f"  mean P(true) history {h.mean():.3f} trace {t.mean():.3f}; on hidden fails {h[y==1].mean():.3f} vs {t[y==1].mean():.3f}; "
          f"on hidden passes {h[y==0].mean():.3f} vs {t[y==0].mean():.3f}")
    print(f"  correlation history-trace {np.corrcoef(h, t)[0,1]:.3f}")
    edges = np.quantile(tt, [0, 1/3, 2/3, 1])
    for i in range(3):
        m = (tt >= edges[i]) & (tt <= edges[i+1]) if i == 2 else (tt >= edges[i]) & (tt < edges[i+1])
        if len(set(y[m])) == 2:
            print(f"  thinking tokens {int(edges[i])}-{int(edges[i+1])}: n {m.sum()}, fails {y[m].sum()}, "
                  f"history {roc_auc_score(y[m], h[m]):.3f}, trace {roc_auc_score(y[m], t[m]):.3f}")
print()
for q in ("code_likely_fails", "special_cases_visible_tests"):
    h = np.array([d["history"]["features"][q] for d in data]); t = np.array([d["trace"]["features"][q] for d in data])
    for v in (False, True):
        m = loop == v
        print(f"{q} loop_flag={v}: n {m.sum()}, fails {y[m].sum()}, history {roc_auc_score(y[m], h[m]):.3f}, trace {roc_auc_score(y[m], t[m]):.3f}")
