"""Byte-budget test (user-approved, inside the $2 Jev cap).

For the checkpoints whose trace was cut at 28,000 bytes in jev_check_v1:
  full: the trace arm again with a 60,000-byte budget (full trace)
  cut:  the trace arm again at 28,000 bytes (same request as before: the noise baseline)
Also, offline (no calls): the request size of every dev checkpoint's trace arm with no budget.
"""
import json
import statistics
import sys
import time
from pathlib import Path

from system1.config import RESULTS, load_prices
from system1.eval.labels import load_labelled
from system1.eval.ledger import CostLedger
from system1.features.evidence import build_arms
from system1.features.jev_scoring import APPLICABLE, JevScorer, ScoreStore, applicability, load_rubric
from system1.loop.runner import to_scoring_checkpoint
from system1.routers.jev import JevClient

OUT = RESULTS / "jev_check_v1"
TRACE = "base+history+trace"
cps = {c["checkpoint_id"]: c for c in load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))}
first = [json.loads(l) for l in open(OUT / "scores.jsonl")]
cut_ids = [s["checkpoint_id"] for s in first if s["arm"] == TRACE and s["trace_truncated"]]
print("cut checkpoints", len(cut_ids))
rubric = load_rubric()

# Offline: full request size for all 621 checkpoints (trace arm, no budget).
sizes = []
for c in cps.values():
    cp = to_scoring_checkpoint(c)
    app = applicability(rubric, cp, TRACE)
    qs = {q: rubric.api_question(q) for q, s in app.items() if s == APPLICABLE}
    ev = build_arms(cp, {TRACE: qs}, model="jev-latest", budget=None)[TRACE]
    sizes.append(ev.payload_bytes)
sizes.sort()
for b in (28_000, 40_000, 50_000, 60_000):
    print(f"offline: trace-arm requests over {b} bytes: {sum(s > b for s in sizes)}/{len(sizes)}")
print(f"offline: max {sizes[-1]}, p99 {sizes[int(0.99 * (len(sizes) - 1))]}, median {sizes[len(sizes) // 2]}")
if "--offline" in sys.argv:
    sys.exit(0)

ledger = CostLedger(OUT / "ledger.jsonl")
with JevClient(ledger=ledger, prices=load_prices(), byte_budget=60_000) as full_client, \
        JevClient(ledger=ledger, prices=load_prices()) as cut_client:
    full = JevScorer(full_client, rubric, ScoreStore(OUT / "budget60k.jsonl"), "jev-budget-60k", "jev-1.13.0")
    cut = JevScorer(cut_client, rubric, ScoreStore(OUT / "cut_repeat.jsonl"), "jev-budget-cut-repeat", "jev-1.13.0")
    for i, cid in enumerate(cut_ids):
        cp = to_scoring_checkpoint(cps[cid])
        for name, sc in (("full", full), ("cut", cut)):
            t0 = time.perf_counter()
            r = sc.score(cp, TRACE)
            print(f"[{i + 1}/{len(cut_ids)}] {cid} {name}: {r.status}, {r.request_bytes} bytes, "
                  f"truncated {r.trace_truncated}, {1000 * (time.perf_counter() - t0):.0f} ms", flush=True)
