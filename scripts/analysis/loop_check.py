"""Stricter: does the trace END in a near-periodic loop? Find where the loop starts."""
import statistics
from collections import Counter
from pathlib import Path
from system1.eval.labels import load_labelled

cps = load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))
cap12 = [c for c in load_labelled(Path("results/runs/pilot-cap12k")) if c["generation"]["cap_hit"]]


def end_loop(t, max_p=1500, match=0.95):
    """Smallest period p such that the last 3 periods (>= 600 chars) are near-identical.
    Then extend backwards while the period holds. Returns (p, loop_chars) or None."""
    for p in range(8, max_p + 1):
        span = max(3 * p, 600)
        if span > len(t):
            break
        tail = t[-span:]
        same = sum(a == b for a, b in zip(tail, tail[p:]))
        if same / (span - p) >= match:
            # extend backwards in blocks of p
            start = len(t) - span
            while start - p >= 0:
                blk, nxt = t[start - p:start], t[start:start + p]
                if sum(a == b for a, b in zip(blk, nxt)) / p < match:
                    break
                start -= p
            return p, len(t) - start
    return None


def run(name, X):
    res = [end_loop(c["thinking"]) for c in X]
    L = [(c, r) for c, r in zip(X, res) if r]
    share = [r[1] / len(c["thinking"]) for c, r in L]
    print(f"{name}: n {len(X)}; ends in a loop {len(L)} ({len(L) / max(1, len(X)):.0%})"
          + (f"; loop share of trace median {statistics.median(share):.0%}, min {min(share):.0%}, max {max(share):.0%}; "
             f"period chars median {statistics.median(r[0] for _, r in L)}" if L else ""))
    return L


cap = [c for c in cps if c["generation"]["cap_hit"]]
L = run("8K cap hits", cap)
run("8K non-cap, >=4000 tokens", [c for c in cps if not c["generation"]["cap_hit"] and c["generation"]["thinking_tokens"] >= 4000])
run("8K non-cap, all", [c for c in cps if not c["generation"]["cap_hit"]])
L12 = run("12K cap hits", cap12)
ids = {c["checkpoint_id"] for c, _ in L}
loop = [c for c in cap if c["checkpoint_id"] in ids]
rest = [c for c in cap if c["checkpoint_id"] not in ids]
for nm, X in (("loop cap hits", loop), ("non-loop cap hits", rest)):
    print(f"{nm}: n {len(X)}, visible pass {sum(c['visible_pass'] for c in X)}, hidden pass {sum(c['hidden']['passed'] for c in X)}, "
          f"benchmarks {dict(Counter(c['benchmark'] for c in X))}")
print("loop share bins:", dict(Counter("<10%" if r[1] / len(c["thinking"]) < .1 else "10-50%" if r[1] / len(c["thinking"]) < .5 else ">=50%" for c, r in L)))
# estimated tokens wasted in loops (chars -> tokens by trace ratio)
w = [r[1] / len(c["thinking"]) * c["generation"]["thinking_tokens"] for c, r in L]
print(f"tokens inside end loops: total {sum(w):.0f}, median per loop trace {statistics.median(w):.0f}")
for c in rest[:3]:
    print("\n--- non-loop", c["checkpoint_id"], repr(c["thinking"][-400:]))
for c, r in L[:2]:
    print("\n--- loop", c["checkpoint_id"], "period", r[0], "loop chars", r[1], repr(c["thinking"][-300:]))
