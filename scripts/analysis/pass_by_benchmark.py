"""Descriptive (October 18, after the planned test analysis): final hidden pass of the three
router-free replay policies and the oracle, by benchmark, on main-test-v1 (Amendment A2 applies).

    uv run python scripts/analysis/pass_by_benchmark.py

Same outcome model as scripts/replay.py: always-small never calls the frontier; forced-only
sends only attempts that never pass the visible tests; always-frontier answers every attempt;
the oracle escalates exactly when the frontier answer passes and the small code fails.
Frontier outcomes are the mean over the 3 graded answers of each task.
"""
import sys
import numpy as np
from system1.config import RESULTS, ROOT
from system1.eval import replay as R
from system1.eval.labels import load_labelled
sys.path.insert(0, str(ROOT / "scripts"))
from replay import frontier_outcomes

attempts = R.build_attempts(load_labelled(RESULTS / "runs" / "main-test-v1", report={}))
z, _, _ = frontier_outcomes("frontier-test-v1")
none = np.zeros(len(attempts), bool)
pols = {"always-small": R.outcome(attempts, z, none, "always-small", forced_to_frontier=False),
        "forced-only": R.outcome(attempts, z, none, "forced-only"),
        "always-frontier": R.always_frontier(attempts, z), "oracle": R.oracle(attempts, z)}
for b in sorted({a.benchmark for a in attempts}) + ["all"]:
    m = np.array([b in ("all", a.benchmark) for a in attempts])
    tasks = len({a.task_id for a, k in zip(attempts, m) if k})
    print(f"{b}: {int(m.sum())} attempts, {tasks} tasks")
    for k, r in pols.items():
        print(f"  {k:16s} {r.final[m].mean():.3f}")
