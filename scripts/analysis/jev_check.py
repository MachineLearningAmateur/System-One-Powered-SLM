"""Small Jev integration check on 8K pilot dev checkpoints (budget $2, user-approved Oct 16).

50 checkpoints x 2 arms + 10 repeats x 2 arms ~ 120 calls. Hard stop at
MAX_INPUT_TOKENS: at a pessimistic $1/M input (24x the reported $0.042/M)
that is $1.50, and output is priced like input as a further margin.
"""
import json
import random
import sys
from pathlib import Path

from system1.config import RESULTS, load_prices
from system1.eval.labels import load_labelled
from system1.eval.ledger import CostLedger
from system1.features.jev_scoring import JevScorer, ScoreStore, load_rubric
from system1.loop.runner import to_scoring_checkpoint
from system1.routers.jev import JevClient

MAX_INPUT_TOKENS = 750_000
OUT = RESULTS / "jev_check_v1"
OUT.mkdir(parents=True, exist_ok=True)
assert not (OUT / "scores.jsonl").exists(), "check already ran"

cps = load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))
rng = random.Random(20261016)
vphf = [c for c in cps if c["visible_pass"] and not c["hidden"]["passed"]]
vphp = [c for c in cps if c["visible_pass"] and c["hidden"]["passed"]]
vf = [c for c in cps if not c["visible_pass"]]
vf_later = [c for c in vf if c["round"] > 1]
vp_later = [c for c in vphf + vphp if c["round"] > 1]
pick = []
for pool, n in ((vphf, 18), (vphp, 14), (vf_later, 8), (vf, 6), (vp_later, 4)):
    pool = [c for c in pool if c not in pick]
    pick += rng.sample(pool, min(n, len(pool)))
repeat = rng.sample(pick, 10)
print(f"sample {len(pick)}: vphf {sum(c in vphf for c in pick)}, vphp {sum(c in vphp for c in pick)}, "
      f"visible-fail {sum(c in vf for c in pick)}, round>1 {sum(c['round'] > 1 for c in pick)}, "
      f"he+ {sum(c['benchmark'] == 'humaneval+' for c in pick)}", flush=True)

ledger = CostLedger(OUT / "ledger.jsonl")
rubric = load_rubric()


def used_tokens() -> int:
    rows, _ = ledger.read()
    return sum((r.get("input_tokens") or 0) + (r.get("output_tokens") or 0) for r in rows)


version = None
with JevClient(ledger=ledger, prices=load_prices()) as client:
    for name, sample in (("jev-check-v1", pick), ("jev-check-v1-repeat", repeat)):
        # The repeat must see the same model version as the first pass.
        scorer = JevScorer(client, rubric, ScoreStore(OUT / ("scores.jsonl" if name == "jev-check-v1" else "repeat.jsonl")),
                           run_id=name, expected_model_version=version)
        for i, c in enumerate(sample):
            if used_tokens() > MAX_INPUT_TOKENS:
                print("STOP: token guard reached")
                sys.exit(1)
            recs = scorer.score_arms(to_scoring_checkpoint(c))
            print(f"[{name} {i + 1}/{len(sample)}] {c['checkpoint_id']}: "
                  + ", ".join(f"{r.arm} {r.status} {r.request_bytes}" for r in recs), flush=True)
        version = scorer.model_version
print("tokens used", used_tokens())
json.dump({"pick": [c["checkpoint_id"] for c in pick], "repeat": [c["checkpoint_id"] for c in repeat]},
          open(OUT / "sample.json", "w"), indent=1)
