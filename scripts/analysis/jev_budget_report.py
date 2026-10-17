"""Report for jev_budget.py: full-trace vs cut-trace Jev scores against cut-vs-cut noise."""
import json, statistics
from pathlib import Path
from system1.eval.labels import load_labelled
O = Path("results/jev_check_v1")
T = "base+history+trace"
lab = {c["checkpoint_id"]: c for c in load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))}
rd = lambda f: {s["checkpoint_id"]: s for s in map(json.loads, open(O / f)) if s["arm"] == T}
c1, c2, fu = rd("scores.jsonl"), rd("cut_repeat.jsonl"), rd("budget60k.jsonl")
L = [json.loads(l) for l in open(O / "ledger.jsonl")]
new = L[120:]
print("new ledger rows", len(new), {r["status"] for r in new}, "versions", {r["model_returned"] for r in new})
big = [r for r in new if r["request_bytes"] > 28000]; small = [r for r in new if r["request_bytes"] <= 28000]
print("full: input tokens median", statistics.median(r["input_tokens"] for r in big), "max", max(r["input_tokens"] for r in big),
      "| latency median ms full", round(statistics.median(r["latency_ms"] for r in big)), "cut", round(statistics.median(r["latency_ms"] for r in small)))
print("tokens all new rows", sum(r["input_tokens"] for r in new), "cost $", round(sum(r["input_tokens"] for r in new) * 0.042e-6, 4))
print("total Jev spend so far $", round(sum(r["input_tokens"] for r in L) * 0.042e-6, 4))
ids = list(fu)
print("trace kept share (cut)", f"{statistics.median(c1[i]['trace_retained_chars'] / c1[i]['trace_original_chars'] for i in ids):.0%}")
qs = sorted({q for i in ids for q, v in fu[i]["features"].items() if v is not None})
print(f"{'question':36s} n  |cut-cut| mean/max   |full-cut| mean/max   mean full-cut (signed)")
for q in qs:
    ii = [i for i in ids if fu[i]["features"].get(q) is not None]
    noise = [abs(c1[i]["features"][q] - c2[i]["features"][q]) for i in ii]
    d = [fu[i]["features"][q] - (c1[i]["features"][q] + c2[i]["features"][q]) / 2 for i in ii]
    print(f"{q:36s} {len(ii):2d}  {statistics.mean(noise):.3f}/{max(noise):.3f}        {statistics.mean(map(abs, d)):.3f}/{max(map(abs, d)):.3f}        {statistics.mean(d):+.3f}")
print("\nper checkpoint (hidden label, visible pass): code_likely_fails cut1/cut2/full ; unsupported_claim cut1/full ; on_task cut1/full")
for i in ids:
    h = lab[i]["hidden"]["passed"]
    f = lambda s, q: s["features"].get(q)
    print(f"{i:22s} hidden {'P' if h else 'F'} vis {'P' if lab[i]['visible_pass'] else 'F'}  "
          f"{f(c1[i],'code_likely_fails'):.2f}/{f(c2[i],'code_likely_fails'):.2f}/{f(fu[i],'code_likely_fails'):.2f}  ; "
          f"{f(c1[i],'unsupported_claim'):.2f}/{f(fu[i],'unsupported_claim'):.2f}  ; {f(c1[i],'on_task'):.2f}/{f(fu[i],'on_task'):.2f}")
