"""Pilot cap hits by subset (attempt 0 vs subsample attempts), cap-hit vs hidden outcome."""
import json
from collections import defaultdict
from pathlib import Path
from system1.eval.labels import load_labelled
sub = set(json.loads(Path("configs/pilot_subsample_v1.json").read_text())["tasks"])
cps = load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))
def rate(xs): return f"{sum(c['generation']['cap_hit'] for c in xs)}/{len(xs)} = {sum(c['generation']['cap_hit'] for c in xs)/max(1,len(xs)):.1%}"
for b in ("humaneval+", "mbpp+"):
    B = [c for c in cps if c["benchmark"] == b]
    print(b, "a0 all dev", rate([c for c in B if c["attempt"] == 0]),
          "| a0 subsample", rate([c for c in B if c["attempt"] == 0 and c["task_id"] in sub]),
          "| a1-4 subsample", rate([c for c in B if c["attempt"] > 0]))
    # task-weighted: per-task cap-hit share, averaged, attempt 0 only (all dev)
# cap hit vs hidden outcome
for cap in (True, False):
    X = [c for c in cps if c["generation"]["cap_hit"] == cap]
    print("cap_hit", cap, "n", len(X), "hidden pass", f"{sum(c['hidden']['passed'] for c in X)/len(X):.1%}",
          "visible pass", f"{sum(c['visible_pass'] for c in X)/len(X):.1%}")
per = defaultdict(int)
for c in cps: per[c["task_id"]] += c["generation"]["cap_hit"]
print("tasks with any cap hit", sum(1 for v in per.values() if v), "of", len(per))
print("effective caps", sorted({c["generation"]["effective_cap"] for c in cps})[:5], "...", max(c["generation"]["effective_cap"] for c in cps))
print("max prompt tokens", max(c["generation"]["prompt_tokens"] for c in cps))
