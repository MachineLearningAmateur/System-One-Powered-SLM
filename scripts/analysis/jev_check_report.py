"""Report for jev_check.py: statuses, request sizes, feature spread, repeat stability."""
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

from system1.eval.labels import load_labelled

OUT = Path("results/jev_check_v1")
lab = {c["checkpoint_id"]: c for c in load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))}
S = [json.loads(l) for l in open(OUT / "scores.jsonl")]
R = [json.loads(l) for l in open(OUT / "repeat.jsonl")]
L = [json.loads(l) for l in open(OUT / "ledger.jsonl")]

print("ledger rows", len(L), "statuses", Counter(r["status"] for r in L), "http retries", sum(r["http_attempt"] > 0 for r in L))
print("model versions", Counter(r["model_returned"] for r in L))
inp, outp = sum(r["input_tokens"] for r in L), sum(r["output_tokens"] for r in L)
print(f"tokens in {inp}, out {outp}; cost at $0.042/M input, free output: ${inp * 0.042 / 1e6:.4f}")
print("latency ms median/max", statistics.median(r["latency_ms"] for r in L), round(max(r["latency_ms"] for r in L)))
for arm in ("base+history", "base+history+trace"):
    A = [s for s in S if s["arm"] == arm]
    print(f"\n== {arm}: {len(A)} records; status {Counter(s['status'] for s in A)}")
    print("  bytes max", max(s["request_bytes"] for s in A), "| at budget", sum(s["request_bytes"] >= 27_900 for s in A),
          "| trace truncated", sum(bool(s["trace_truncated"]) for s in A), "| base trimmed", sum(bool(s["base_trimmed"]) for s in A))
    qs = sorted({q for s in A for q in s["features"]})
    for q in qs:
        vals = [(s["features"][q], s) for s in A if s["features"].get(q) is not None]
        na = Counter(s["applicability"][q] for s in A if s["applicability"][q] != "applicable")
        if not vals:
            print(f"  {q}: never applicable {dict(na)}")
            continue
        v = [x for x, _ in vals]
        mode, mc = Counter(round(x, 3) for x in v).most_common(1)[0]
        vp = [(x, lab[s["checkpoint_id"]]["hidden"]["passed"]) for x, s in vals if s["visible_pass"]]
        hf = [x for x, p in vp if not p]
        hp = [x for x, p in vp if p]
        ties = sum(a == b for a in hf for b in hp)
        auc = (sum((a > b) + 0.5 * (a == b) for a in hf for b in hp) / (len(hf) * len(hp))) if hf and hp else None
        print(f"  {q}: n {len(v)}, distinct {len(set(v))}, mode {mode} x{mc}, at 0/1 {sum(x in (0.0, 1.0) for x in v)}, "
              f"sd {statistics.pstdev(v):.3f}, mean {statistics.mean(v):.3f}; VP pairs tied {ties}/{len(hf) * len(hp)}; "
              f"VP mean HF {statistics.mean(hf) if hf else float('nan'):.3f} vs HP {statistics.mean(hp) if hp else float('nan'):.3f}"
              + (f"; descr. AUROC(HF higher) {auc:.2f}" if auc is not None else ""))
# repeat stability
first = {(s["checkpoint_id"], s["arm"]): s for s in S}
diffs = defaultdict(list)
same_hash = 0
for r in R:
    f = first[(r["checkpoint_id"], r["arm"])]
    same_hash += r["request_sha256"] == f["request_sha256"]
    for q, x in r["features"].items():
        if x is not None and f["features"].get(q) is not None:
            diffs[q].append(abs(x - f["features"][q]))
print(f"\nrepeat: {len(R)} records, same request bytes {same_hash}/{len(R)}")
for q, d in sorted(diffs.items()):
    print(f"  {q}: n {len(d)}, exact same {sum(x == 0 for x in d)}, max |diff| {max(d):.4f}")
