"""Paired 8K vs 12K comparison on attempt 0 of the cap-hit dev tasks."""
import json
import statistics
from collections import defaultdict
from pathlib import Path

from system1.eval.labels import load_labelled

tasks = json.loads(Path("configs/cap12k_tasks_v1.json").read_text())["tasks"]
T = set(tasks)


def attempts(run):
    by = defaultdict(list)
    for c in load_labelled(Path("results/runs") / run):
        if c["task_id"] in T and c["attempt"] == 0:
            by[c["task_id"]].append(c)
    return {t: sorted(v, key=lambda c: c["round"]) for t, v in by.items()}


A, B = attempts("pilot-v1"), attempts("pilot-cap12k")
assert set(A) == set(B) == T, (len(A), len(B))
rows = []
for name, R in (("8K", A), ("12K", B)):
    cps = [c for v in R.values() for c in v]
    fin = [v[-1] for v in R.values()]
    cap = sum(c["generation"]["cap_hit"] for c in cps)
    print(f"{name}: checkpoints {len(cps)}, cap hits {cap} ({cap / len(cps):.1%}); "
          f"final visible pass {sum(f['visible_pass'] for f in fin)}/{len(fin)}; "
          f"final hidden pass {sum(f['hidden']['passed'] for f in fin)}/{len(fin)}; "
          f"thinking tokens total {sum(c['generation']['thinking_tokens'] for c in cps)}, "
          f"median {statistics.median(c['generation']['thinking_tokens'] for c in cps)}; "
          f"VP/HF checkpoints {sum(c['visible_pass'] and not c['hidden']['passed'] for c in cps)}")
for b in ("humaneval+", "mbpp+"):
    for name, R in (("8K", A), ("12K", B)):
        fin = [v[-1] for t, v in R.items() if v[0]["benchmark"] == b]
        cps = [c for v in R.values() for c in v if c["benchmark"] == b]
        print(f"  {b} {name}: hidden pass {sum(f['hidden']['passed'] for f in fin)}/{len(fin)}, "
              f"cap hits {sum(c['generation']['cap_hit'] for c in cps)}/{len(cps)}")
gain = sorted(t for t in T if B[t][-1]["hidden"]["passed"] and not A[t][-1]["hidden"]["passed"])
loss = sorted(t for t in T if A[t][-1]["hidden"]["passed"] and not B[t][-1]["hidden"]["passed"])
print("hidden pass 8K fail -> 12K pass:", len(gain), gain)
print("hidden pass 8K pass -> 12K fail:", len(loss), loss)
# Does 12K reproduce the 8K tokens (same seed)? compare first round thinking prefix
same = sum(A[t][0]["thinking"][:2000] == B[t][0]["thinking"][:2000] for t in T)
print(f"first-round thinking: first 2000 chars equal in {same}/{len(T)} tasks")
meta = json.loads(Path("results/runs/pilot-cap12k/run_meta.json").read_text())
s = meta["sessions"][-1]
print("12K session:", {k: s.get(k) for k in ("elapsed_s", "energy_wh", "n_failed")}, s.get("vllm_delta"))
