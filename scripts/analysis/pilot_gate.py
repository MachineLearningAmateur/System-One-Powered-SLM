"""Pilot headroom gate: cap hits, hidden pass rate, projected positive test tasks."""
import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

from system1.eval.labels import load_labelled

ROOT = Path(".")
RUNS = ROOT / "results" / "runs"
split = json.loads((ROOT / "configs/split_v1.json").read_text())
sub = json.loads((ROOT / "configs/pilot_subsample_v1.json").read_text())
SUB = set(sub["tasks"])

cps = []
for rid in ("pilot-v1", "pilot-v1b"):
    rep = {}
    rows = load_labelled(RUNS / rid, report=rep)
    print(rid, len(rows), "checkpoints; report:", {k: (v if not isinstance(v, list) else len(v)) for k, v in rep.items()})
    cps += rows
keys = [(c["task_id"], c["attempt"], c["round"]) for c in cps]
assert len(keys) == len(set(keys)), "duplicate checkpoints across runs"


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"),) * 2
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


for bench in ("humaneval+", "mbpp+", "all"):
    B = [c for c in cps if bench == "all" or c["benchmark"] == bench]
    print(f"\n=== {bench} ===")
    cap = sum(c["generation"]["cap_hit"] for c in B)
    print(f"checkpoints {len(B)}; cap hits {cap} ({cap / len(B):.1%})")
    for a_set, name in ((lambda c: c["attempt"] == 0, "attempt 0, all dev"), (lambda c: True, "all attempts")):
        att = defaultdict(list)
        for c in B:
            if a_set(c):
                att[(c["task_id"], c["attempt"])].append(c)
        finals = [sorted(v, key=lambda c: c["round"])[-1] for v in att.values()]
        hp = sum(f["hidden"]["passed"] for f in finals)
        vp = sum(f["visible_pass"] for f in finals)
        lo, hi = wilson(hp, len(finals))
        print(f"{name}: attempts {len(finals)}; final visible pass {vp} ({vp / len(finals):.1%}); "
              f"final hidden pass {hp} ({hp / len(finals):.1%}, Wilson {lo:.1%}-{hi:.1%})")
    vpc = [c for c in B if c["visible_pass"]]
    vphf = [c for c in vpc if not c["hidden"]["passed"]]
    vfhp = [c for c in B if not c["visible_pass"] and c["hidden"]["passed"]]
    print(f"visible-pass checkpoints {len(vpc)}; of these hidden-fail {len(vphf)} ({len(vphf) / max(1, len(vpc)):.1%}); "
          f"visible-fail/hidden-pass {len(vfhp)}")
    print("thinking median", statistics.median(c["generation"]["thinking_tokens"] for c in B))
    if bench == "all":
        continue
    # five-attempt subsample: tasks with >=1 VP/HF checkpoint over attempts 0-4
    S = [c for c in B if c["task_id"] in SUB]
    per = defaultdict(set)
    for c in S:
        per[c["task_id"]].add(c["attempt"])
    full = [t for t, a in per.items() if a == set(range(5))]
    pos = {c["task_id"] for c in S if c["visible_pass"] and not c["hidden"]["passed"]}
    k, n = len(pos & set(full)), len(full)
    lo, hi = wilson(k, n)
    n_test = len(split["benchmarks"][bench]["test"])
    print(f"subsample tasks with 5 attempts {n}/{len(sub['benchmarks'][bench])}; with >=1 VP/HF checkpoint {k} "
          f"({k / n:.1%}, Wilson {lo:.1%}-{hi:.1%})")
    print(f"projected positive test tasks: {k / n * n_test:.1f} of {n_test} (interval {lo * n_test:.1f}-{hi * n_test:.1f})")
    one = {c["task_id"] for c in B if c["attempt"] == 0 and c["visible_pass"] and not c["hidden"]["passed"]}
    print(f"attempt-0 tasks with VP/HF: {len(one)} of {len({c['task_id'] for c in B if c['attempt'] == 0})}")
    print("positive tasks:", sorted(pos))
