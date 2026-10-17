"""Size probe: the largest natural trace requests (12K-cap run, thinking up to 12,288 tokens)."""
import time
from pathlib import Path

from system1.config import RESULTS, load_prices
from system1.eval.labels import load_labelled
from system1.eval.ledger import CostLedger
from system1.features.evidence import build_arms
from system1.features.jev_scoring import APPLICABLE, applicability, load_rubric
from system1.loop.runner import to_scoring_checkpoint
from system1.routers.jev import JevClient

T = "base+history+trace"
rubric = load_rubric()
rows = []
for c in load_labelled(Path("results/runs/pilot-cap12k")):
    cp = to_scoring_checkpoint(c)
    app = applicability(rubric, cp, T)
    qs = {q: rubric.api_question(q) for q, s in app.items() if s == APPLICABLE}
    ev = build_arms(cp, {T: qs}, model="jev-latest", budget=None)[T]
    rows.append((ev.payload_bytes, c["checkpoint_id"], ev, qs))
rows.sort(key=lambda r: r[0])
print("12K-run full trace requests: max", rows[-1][0], "| over 50,000:", sum(r[0] > 50_000 for r in rows), "of", len(rows))
# probe: the largest, plus ones near 50K and 60K
targets = [rows[-1]] + [min(rows, key=lambda r: abs(r[0] - t)) for t in (50_000, 60_000)]
ledger = CostLedger(RESULTS / "jev_check_v1" / "ledger.jsonl")
with JevClient(ledger=ledger, prices=load_prices(), byte_budget=None) as client:
    for n, cid, ev, qs in dict((r[1], r) for r in targets).values():
        t0 = time.perf_counter()
        try:
            r = client.ask(ev.state, qs, task_id=cid, arm=T)
            print(f"{cid}: {n} bytes -> ok, {r.input_tokens} input tokens, {r.latency_ms:.0f} ms, model {r.model_returned}")
        except Exception as e:
            print(f"{cid}: {n} bytes -> {type(e).__name__}: {e} ({1000 * (time.perf_counter() - t0):.0f} ms)")
