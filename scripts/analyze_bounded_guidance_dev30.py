"""Account for every frozen dev30 task, including incomplete runs.

    uv run python scripts/analyze_bounded_guidance_dev30.py \
      --run-id <run-id> --output-prefix results/<new-analysis-prefix>

The two output files are created exclusively. Hidden labels are read only after
generation and sandbox grading; no task or protocol choice is made here.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from system1.bounded_guidance_dev30 import GPU_RATE_USD_PER_HOUR, load_manifest
from system1.config import RESULTS
from system1.eval.ledger import read_jsonl
try:
    from scripts.analyze_bounded_guidance import stats, task_bootstrap
except ModuleNotFoundError:
    from analyze_bounded_guidance import stats, task_bootstrap


def _rows(path: Path) -> list[dict]:
    rows, damaged = read_jsonl(path)
    if damaged:
        raise ValueError(f"damaged JSONL: {path} at {[n for n, _ in damaged]}")
    return rows


def analyze(run_dir: Path, manifest: dict, manifest_sha256: str) -> tuple[dict, list[dict]]:
    meta = json.loads((run_dir / "run_meta.json").read_text())
    protocol = meta["protocol"]
    if (protocol.get("pilot_profile") != "dev30-v1" or protocol.get("task_ids") != manifest["tasks"]
            or protocol.get("task_file_sha256") != manifest_sha256 or protocol.get("split") != "dev"
            or protocol.get("attempts") != 1):
        raise ValueError("run does not match the frozen dev30 manifest")
    pairs, plans, failures = (_rows(run_dir / name) for name in
                            ("pairs.jsonl", "plans.jsonl", "failures.jsonl"))
    labels, calls, exchanges, frontier = (_rows(run_dir / name) for name in
                                        ("bounded_hidden_labels.jsonl", "worker_calls.jsonl",
                                         "worker_exchanges.jsonl", "ledger.jsonl"))
    if len(exchanges) != len(calls) or len(calls) > 180 or len(frontier) > 30:
        raise ValueError("request-count or Qwen exchange/usage integrity failure")
    ids = set(manifest["tasks"])
    for group in (pairs, plans, failures, calls, exchanges, frontier, labels):
        if any(x.get("task_id") not in ids for x in group):
            raise ValueError("run contains an unexpected task")
    by_pair = {p["task_id"]: p for p in pairs}
    if len(by_pair) != len(pairs):
        raise ValueError("duplicate completed task")
    plans_by_task = defaultdict(list)
    failures_by_task = defaultdict(list)
    labels_by_key = defaultdict(list)
    for p in plans:
        plans_by_task[p["task_id"]].append(p)
    for f in failures:
        failures_by_task[f["task_id"]].append(f)
    for label in labels:
        pair = by_pair.get(label["task_id"])
        if pair is None or label.get("pair_id") != pair["pair_id"]:
            raise ValueError("hidden grade does not join to a completed task pair")
        labels_by_key[(label["task_id"], label["arm"])].append(label)
    task_rows, graded = [], []
    for tid in manifest["tasks"]:
        pair = by_pair.get(tid)
        task_calls = [x for x in calls if x["task_id"] == tid]
        task_frontier = [x for x in frontier if x["task_id"] == tid]
        task_plans = plans_by_task[tid]
        failure = failures_by_task[tid]
        row = {"task_id": tid, "benchmark": "humaneval+" if tid.startswith("HumanEval/") else "mbpp+",
               "status": None, "failure_type": failure[0].get("error_type") if failure else None,
               "failure_detail": failure[0].get("error") if failure else None,
               "qwen_http": len(task_calls), "frontier_requests": len(task_frontier),
               "advice_delivery": None, "control_pass": None, "guidance_pass": None}
        if len(task_plans) > 1 or len(failure) > 1 or len(task_frontier) > 1:
            raise ValueError(f"multiple attempts for fixed task {tid}")
        if pair is not None:
            if len(task_plans) != 1 or task_plans[0]["pair_id"] != pair["pair_id"]:
                raise ValueError(f"completed task {tid} lacks its one joined plan")
            plan = task_plans[0]
            if (plan["call_id"] != pair["plan_call_id"] or
                    plan["delivery_status"] != pair["advice_delivery"] or
                    plan["delivery_status"] not in ("delivered", "invalid")):
                raise ValueError(f"plan delivery join failed for {tid}")
            row["advice_delivery"] = plan["delivery_status"]
            complete_labels = []
            for arm in ("control", "guidance"):
                found = labels_by_key[(tid, arm)]
                if len(found) > 1:
                    raise ValueError(f"duplicate grade for {tid}/{arm}")
                if found:
                    label = found[0]
                    code_row = next((x for x in pair["rows"] if
                                     x["checkpoint_id"] == pair["final_checkpoint_ids"][arm]), None)
                    if (code_row is None or label["checkpoint_id"] != code_row["checkpoint_id"]
                            or label["code_sha256"] != hashlib.sha256((code_row["code"] or "").encode()).hexdigest()):
                        raise ValueError(f"grade/code join failed for {tid}/{arm}")
                    complete_labels.append(label)
            if len(complete_labels) == 2:
                row["status"] = "graded"
                row["control_pass"] = bool(complete_labels[0]["passed"])
                row["guidance_pass"] = bool(complete_labels[1]["passed"])
                graded.append({"task_id": tid, "control_pass": row["control_pass"],
                               "guidance_pass": row["guidance_pass"],
                               "first_visible_pass": pair["first_visible_pass"]})
            else:
                row["status"] = "generation_complete_ungraded"
        elif failure or task_calls or task_plans or task_frontier:
            error_type = row["failure_type"] or ""
            row["status"] = ("infrastructure_failed" if error_type in
                             {"ConnectError", "ReadTimeout", "RemoteProtocolError", "ServerMismatch",
                              "HTTPStatusError", "TimeoutError"} else "incomplete")
            row["advice_delivery"] = task_plans[0].get("delivery_status") if task_plans else None
        else:
            row["status"] = "not_started"
        task_rows.append(row)
    # A stopped run may have a billed plan without a completed pair; keep it in
    # cost and task accounting, but never impute an outcome.
    delivery = Counter(x["advice_delivery"] for x in task_rows if x["advice_delivery"])
    completed = [x for x in task_rows if x["status"] in ("graded", "generation_complete_ungraded")]
    completed_valid = sum(x["advice_delivery"] == "delivered" for x in completed)
    known_cost = [float(x["usd_reported"] if x.get("usd_reported") is not None else x["usd_computed"])
                  for x in frontier if x.get("usd_reported") is not None or x.get("usd_computed") is not None]
    cost_unknown = len(frontier) - len(known_cost)
    billing_file = run_dir / "azure_lifecycle.json"
    azure = json.loads(billing_file.read_text()) if billing_file.exists() else None
    modeled_azure = None
    if azure and azure.get("app_created_utc") and azure.get("app_delete_requested_utc"):
        from datetime import datetime
        seconds = (datetime.fromisoformat(azure["app_delete_requested_utc"])
                   - datetime.fromisoformat(azure["app_created_utc"])).total_seconds()
        modeled_azure = max(0, seconds) / 3600 * GPU_RATE_USD_PER_HOUR
    summary = {"version": "bounded-guidance-dev30-v1", "n_manifest_tasks": 30,
               "task_status_counts": dict(Counter(x["status"] for x in task_rows)),
               "delivery_status_counts": dict(delivery),
               "delivery_validity": {"completed_pairs_valid": completed_valid,
                                     "completed_pairs_invalid": len(completed) - completed_valid,
                                     "valid_rate_among_completed":
                                         completed_valid / len(completed) if completed else None,
                                     "plans_after_incomplete_pair": len(plans) - len(completed)},
               "request_counts": {"qwen_http": len(calls), "frontier": len(frontier)},
               "usage": {name: sum(x[name] or 0 for x in calls) for name in
                         ("input_tokens", "output_tokens", "reasoning_tokens")},
               "usage_unknown_qwen_rows": sum(x.get("input_tokens") is None or x.get("output_tokens") is None
                                              for x in calls),
               "cost": {"frontier_recorded_or_computed_usd": sum(known_cost) if not cost_unknown else None,
                        "frontier_unknown_cost_rows": cost_unknown,
                        "azure_invoice_usd": azure.get("invoice_usd") if azure else None,
                        "modeled_azure_app_lifetime_usd": modeled_azure,
                        "gpu_rate_usd_per_hour_assumption": GPU_RATE_USD_PER_HOUR},
               "paired_results": None}
    if graded:
        paired = stats(graded)
        paired["task_bootstrap_95pct"] = task_bootstrap(graded)
        paired["population"] = "all_30_frozen_tasks" if len(graded) == 30 else "graded_subset_only"
        summary["paired_results"] = paired
    return summary, task_rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--output-prefix", required=True)
    args = ap.parse_args()
    manifest, manifest_hash = load_manifest()
    summary, tasks = analyze(RESULTS / "runs" / args.run_id, manifest, manifest_hash)
    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    with prefix.with_suffix(".json").open("x") as f:
        json.dump(summary, f, indent=2)
    with prefix.with_suffix(".csv").open("x", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(tasks[0]))
        writer.writeheader()
        writer.writerows(tasks)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
