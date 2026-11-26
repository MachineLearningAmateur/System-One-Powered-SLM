"""Worker cost, latency and break-even report of the Qwen3.5-9B study (docs/q9b-plan.md, part B), version 1.

    uv run python scripts/analysis/q9b_cost_latency.py --run-id q9b-test-v1 \
        --replay results/replay_q9b-test-v1_final.json --frontier-run frontier-test-v1

Descriptive; it fits and selects nothing. From the ledgers (latency_ms, all HTTP attempts, status ok):
median, mean and 90th percentile time of each worker call (thinking and answer phases, and the
worker time per attempt summed over its calls), each Jev call, and each frontier call. Worker cost
per attempt = the run's DeepInfra tokens x the listed prices below / the run's complete attempts
(every attempt, excluded tasks included, as in the replay's cost denominator). From the replay
output, for every policy: its API cost per attempt (frontier + Jev, the replay's usd_frontier +
usd_jev) and the break-even worker cost = always-frontier API cost - the policy's API cost. A
cascade policy, which always runs the worker, is cheaper than always-frontier only if the worker
costs less than that per attempt. The replay's own small-model cost views (energy, wall time) do
not apply to a hosted worker and are not used.
Writes results/q9b_cost_latency_<run-id>.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from system1.config import RESULTS, ROOT
from system1.eval.ledger import read_jsonl
from system1.loop.runner import complete_executions

VERSION = "q9b-cost-latency-v1"
# DeepInfra standard tier for Qwen/Qwen3.5-9B, listed November 26, 2026; the probe replies'
# usage.estimated_cost agreed with these values. Not an invoice.
USD_PER_M_INPUT, USD_PER_M_OUTPUT = 0.10, 0.15


def stats(ms: list[float]) -> dict:
    if not ms:
        return {"n": 0, "median_s": None, "mean_s": None, "p90_s": None}
    a = np.array(ms, float) / 1000
    return {"n": int(len(a)), "median_s": float(np.median(a)), "mean_s": float(a.mean()),
            "p90_s": float(np.percentile(a, 90))}


def rows(path: Path) -> list[dict]:
    out, damaged = read_jsonl(path)
    if damaged:
        raise SystemExit(f"STOP: {len(damaged)} damaged lines in {path}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--replay", required=True, help="the replay output JSON of the same run")
    ap.add_argument("--frontier-run", required=True)
    args = ap.parse_args()
    run = RESULTS / "runs" / args.run_id
    meta = json.loads((run / "run_meta.json").read_text(encoding="utf-8"))
    if meta["protocol"].get("backend") != "deepinfra":
        raise SystemExit("STOP: this report is for a DeepInfra worker run")
    led = rows(run / "ledger.jsonl")
    worker = [r for r in led if r["component"] == "small_model"]
    ok = [r for r in worker if r["status"] == "ok"]
    n_in = sum(r["input_tokens"] or 0 for r in worker)
    n_out = sum(r["output_tokens"] or 0 for r in worker)
    unknown_usage = sum(r["input_tokens"] is None or r["output_tokens"] is None for r in worker)
    traj = complete_executions(rows(run / "trajectories.jsonl"))
    attempts = {(c["task_id"], c["attempt"]) for c in traj}
    usd_worker = n_in * USD_PER_M_INPUT / 1e6 + n_out * USD_PER_M_OUTPUT / 1e6
    per_attempt_ms: dict[tuple, float] = {}
    for r in ok:
        k = (r["task_id"], r["attempt"])
        per_attempt_ms[k] = per_attempt_ms.get(k, 0.0) + r["latency_ms"]
    jev = [r for r in rows(run / "jev_ledger.jsonl") if r["status"] == "ok"]
    front = [r for r in rows(RESULTS / "runs" / args.frontier_run / "ledger.jsonl")
             if r["component"] == "frontier" and r["status"] == "ok"]
    replay = json.loads((ROOT / args.replay).read_text(encoding="utf-8"))
    if replay["runs"] != [args.run_id] or replay["frontier_run"] != args.frontier_run:
        raise SystemExit("STOP: the replay output is for other runs")
    pol = replay["policies"]
    af = [p for p in pol if p["policy"] == "always-frontier"]
    if len(af) != 1:
        raise SystemExit("STOP: the replay output has no single always-frontier policy")
    af_api = af[0]["usd_frontier"] + af[0]["usd_jev"]
    worker_pa = usd_worker / len(attempts)
    policies = []
    for p in pol:
        api = p["usd_frontier"] + p["usd_jev"]
        runs_worker = p["policy"] != "always-frontier"
        policies.append({k: p.get(k) for k in ("policy", "router", "view", "q_vp", "pass")} | {
            "usd_api_per_attempt": api, "break_even_worker_usd_per_attempt": af_api - api if runs_worker else None,
            "usd_total_per_attempt": api + (worker_pa if runs_worker else 0.0),
            "cheaper_than_always_frontier": (api + worker_pa < af_api) if runs_worker else None})
    out = {"version": VERSION, "run": args.run_id, "frontier_run": args.frontier_run, "replay": args.replay,
           "prices": {"usd_per_m_input": USD_PER_M_INPUT, "usd_per_m_output": USD_PER_M_OUTPUT,
                      "source": "DeepInfra listing, 2026-11-26"},
           "worker": {"calls": len(worker), "calls_ok": len(ok), "calls_with_unknown_usage": unknown_usage,
                      "input_tokens": n_in, "output_tokens": n_out, "usd": usd_worker,
                      "complete_attempts": len(attempts), "usd_per_attempt": worker_pa,
                      "concurrency": meta["protocol"].get("generation_concurrency"),
                      "wall_hours": sum(s.get("elapsed_s") or 0 for s in meta["sessions"]) / 3600},
           "latency": {"worker_call_thinking": stats([r["latency_ms"] for r in ok if r["arm"] == "thinking"]),
                       "worker_call_answer": stats([r["latency_ms"] for r in ok if r["arm"] == "answer"]),
                       "worker_per_attempt": stats(list(per_attempt_ms.values())),
                       "jev_call": stats([r["latency_ms"] for r in jev]),
                       "frontier_call": stats([r["latency_ms"] for r in front])},
           "always_frontier_usd_api_per_attempt": af_api, "policies": policies}
    print(f"worker: {len(attempts)} attempts, USD {usd_worker:.4f} ({worker_pa:.6f} per attempt); "
          f"always-frontier API USD {af_api:.6f} per attempt")
    for k, v in out["latency"].items():
        print(f"  {k:22s} n {v['n']:5d}  median {v['median_s']}  mean {v['mean_s']}  p90 {v['p90_s']}")
    path = RESULTS / f"q9b_cost_latency_{args.run_id}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
