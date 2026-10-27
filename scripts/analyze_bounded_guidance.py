"""Paired intention-to-treat analysis of completed bounded-guidance units.

    uv run python scripts/analyze_bounded_guidance.py --run-id bg-mock-demo

Labels are read only here, after both generation branches and hidden grading.
The output is descriptive for a development run; no test-label tuning occurs.
Bootstrap resamples whole tasks, keeping attempts and arms together.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import sys
from collections import defaultdict

from system1.config import RESULTS
from system1.eval.ledger import read_jsonl


def load_pairs(run_dir, *, require_delivery=False):
    pairs, damaged = read_jsonl(run_dir / "pairs.jsonl")
    labels, bad_labels = read_jsonl(run_dir / "bounded_hidden_labels.jsonl")
    if damaged or bad_labels or not pairs or len(labels) != 2 * len(pairs):
        raise ValueError("missing, damaged, or incomplete pair/label files")
    by_key = {}
    for label in labels:
        key = (label["pair_id"], label["arm"])
        if key in by_key:
            raise ValueError("duplicate paired label")
        by_key[key] = label
    records = []
    for pair in pairs:
        if require_delivery and pair.get("advice_delivery") not in ("delivered", "invalid"):
            raise ValueError("missing or invalid advice delivery in amended pair")
        row_by_id = {r["checkpoint_id"]: r for r in pair["rows"]}
        entry = {"pair_id": pair["pair_id"], "task_id": pair["task_id"],
                 "benchmark": pair["benchmark"], "attempt": pair["attempt"],
                 "first_visible_pass": pair["first_visible_pass"], "plan_call_id": pair["plan_call_id"],
                 "advice_delivery": pair.get("advice_delivery", "delivered")}
        for arm in ("control", "guidance"):
            label = by_key[(pair["pair_id"], arm)]
            row = row_by_id[pair["final_checkpoint_ids"][arm]]
            sha = hashlib.sha256((row["code"] or "").encode()).hexdigest()
            if label["checkpoint_id"] != row["checkpoint_id"] or label["code_sha256"] != sha:
                raise ValueError(f"label/code mismatch at {row['checkpoint_id']}")
            if label["status"] not in ("pass", "fail", "no_code"):
                raise ValueError("invalid grade in analysis")
            entry[arm + "_pass"] = bool(label["passed"])
            entry[arm + "_visible_pass"] = bool(row["visible_pass"])
            entry[arm + "_final_round"] = row["round"]
        records.append(entry)
    return records


def stats(records):
    n = len(records)
    if not n:
        raise ValueError("no paired records")
    return {"n_pairs": n, "n_tasks": len({r["task_id"] for r in records}),
        "n_first_visible_fail": sum(not r["first_visible_pass"] for r in records),
        "control_pass_rate": sum(r["control_pass"] for r in records) / n,
        "guidance_pass_rate": sum(r["guidance_pass"] for r in records) / n,
        "paired_delta": sum(int(r["guidance_pass"]) - int(r["control_pass"]) for r in records) / n,
        "rescues": sum(r["guidance_pass"] and not r["control_pass"] for r in records),
        "harms": sum(r["control_pass"] and not r["guidance_pass"] for r in records),
        "both_pass": sum(r["control_pass"] and r["guidance_pass"] for r in records),
        "both_fail": sum(not r["control_pass"] and not r["guidance_pass"] for r in records)}


def task_bootstrap(records, draws=10000, seed=20261026):
    by_task = defaultdict(list)
    for row in records:
        by_task[row["task_id"]].append(row)
    tasks = sorted(by_task)
    rng = random.Random(seed)
    deltas = []
    for _ in range(draws):
        sample = [r for _ in tasks for r in by_task[rng.choice(tasks)]]
        deltas.append(stats(sample)["paired_delta"])
    deltas.sort()
    return [deltas[int(0.025 * (draws - 1))], deltas[int(0.975 * (draws - 1))]]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--gpu-usd-per-hour", type=float, default=3.20,
                    help="modeled GPU rate for a future run; not a measured invoice")
    args = ap.parse_args()
    out = RESULTS / "runs" / args.run_id
    meta = json.loads((out / "run_meta.json").read_text())
    amended = meta["protocol"].get("amendment") == "invalid-advice-v1a-20261027"
    records = load_pairs(out, require_delivery=amended)
    result = stats(records)
    result["task_cluster_bootstrap_95pct"] = task_bootstrap(records)
    calls, bad_calls = read_jsonl(out / "worker_calls.jsonl")
    plans, bad_plans = read_jsonl(out / "plans.jsonl")
    ledger, bad_ledger = read_jsonl(out / "ledger.jsonl")
    if bad_calls or bad_plans or bad_ledger:
        raise ValueError("damaged call or plan log")
    completed_ids = {r["pair_id"] for r in records}
    completed_plans = [p for p in plans if p["pair_id"] in completed_ids]
    if len(completed_plans) != result["n_pairs"]:
        raise ValueError("exactly one advice delivery is required per completed pair")
    plan_by_pair = {p["pair_id"]: p for p in completed_plans}
    if len(plan_by_pair) != len(completed_plans):
        raise ValueError("duplicate advice delivery record")
    for record in records:
        plan = plan_by_pair.get(record["pair_id"])
        if amended and (plan is None or plan.get("delivery_status") not in ("delivered", "invalid")):
            raise ValueError("missing or invalid advice delivery in amended plan")
        if (plan is None or plan["call_id"] != record["plan_call_id"]
                or plan.get("delivery_status", "delivered") != record["advice_delivery"]):
            raise ValueError("advice delivery join mismatch")
    result["advice_delivery"] = {"delivered": sum(p.get("delivery_status", "delivered") == "delivered" for p in completed_plans),
                                 "invalid": sum(p.get("delivery_status", "delivered") == "invalid" for p in completed_plans),
                                 "orphaned_after_incomplete_pair": len(plans) - len(completed_plans)}
    result["request_counts"] = {"qwen_http": len(calls),
                                 "frontier_plan": sum(r.get("component") == "frontier" for r in ledger) if meta["protocol"]["backend"] == "real" else len(plans),
                                 "mock_or_real": meta["protocol"]["backend"]}
    unknown_cost = sum(r.get("component") == "frontier" and r.get("usd_reported") is None
                       and r.get("usd_computed") is None for r in ledger)
    frontier_cost = sum(
        float(r["usd_reported"] if r["usd_reported"] is not None else r["usd_computed"] or 0)
        for r in ledger if r["component"] == "frontier")
    gpu_modeled = (sum(float(s.get("elapsed_s") or 0) for s in meta["sessions"]) / 3600
                   * args.gpu_usd_per_hour if meta["protocol"]["backend"] == "real" else 0.0)
    result["cost"] = {"frontier_usd_recorded": frontier_cost if unknown_cost == 0 else None,
        "frontier_cost_unknown_rows": unknown_cost,
        "gpu_rate_usd_per_hour_assumption": args.gpu_usd_per_hour,
        "generation_session_elapsed_s": sum(float(s.get("elapsed_s") or 0) for s in meta["sessions"]),
        "modeled_gpu_usd_at_assumed_rate": gpu_modeled,
        "modeled_total_usd": gpu_modeled + frontier_cost if unknown_cost == 0 else None,
        "gpu_invoice_usd": None,
        "mock_inference_charge_usd": 0.0 if meta["protocol"]["backend"] == "mock" else None}
    (out / "bounded_analysis.json").write_text(json.dumps(result, indent=2))
    with open(out / "bounded_pairs.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(main())
