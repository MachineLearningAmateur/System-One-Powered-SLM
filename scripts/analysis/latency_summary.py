"""Measured call latency of the worker, Jev and the frontier model for the paper revision, version 1. Descriptive.

    uv run python scripts/analysis/latency_summary.py

From the saved ledgers (latency_ms of each HTTP attempt with status ok). Worker: each thinking and answer call,
and the worker time per attempt (the sum of its calls over all rounds), with output tokens per second per
call. Qwen3-1.7B ran on a local RTX 3070 with vLLM at generation concurrency 3 (main-test-v1); Qwen3.5-9B ran
on the DeepInfra hosted API at concurrency 16 (q9b-test-v1). Both latencies include the queueing of their own
concurrent requests; neither is a single-request benchmark. Jev: each scoring call of the same two test runs.
Frontier: each call of frontier-test-v1 (task-only Claude Sonnet 5.5 answers shared by both replays).
Writes results/latency_summary_v1.json.
"""

from __future__ import annotations

import json
import sys

import numpy as np

from system1.config import RESULTS
from system1.eval.ledger import read_jsonl

VERSION = "latency-summary-v1"
WORKERS = {"Qwen3-1.7B (local RTX 3070, concurrency 3)": "main-test-v1",
           "Qwen3.5-9B (DeepInfra, concurrency 16)": "q9b-test-v1"}
FRONTIER = "frontier-test-v1"


def rows(path) -> list[dict]:
    out, bad = read_jsonl(path)
    if bad:
        raise SystemExit(f"STOP: {len(bad)} damaged lines in {path}")
    return out


def stats(ms) -> dict:
    a = np.asarray(list(ms), float) / 1000
    return {"n": int(len(a)), "median_s": float(np.median(a)), "mean_s": float(a.mean()),
            "p90_s": float(np.percentile(a, 90))}


def main() -> int:
    out: dict = {"version": VERSION, "workers": {}}
    for name, run in WORKERS.items():
        led = [r for r in rows(RESULTS / "runs" / run / "ledger.jsonl")
               if r["component"] == "small_model" and r["status"] == "ok"]
        per_attempt: dict = {}
        for r in led:
            per_attempt[(r["task_id"], r["attempt"])] = per_attempt.get((r["task_id"], r["attempt"]), 0.0) + r["latency_ms"]
        tps = [r["output_tokens"] / (r["latency_ms"] / 1000) for r in led if r["output_tokens"] and r["latency_ms"]]
        jev = [r for r in rows(RESULTS / "runs" / run / "jev_ledger.jsonl") if r["status"] == "ok"]
        out["workers"][name] = {
            "run": run, "thinking_call": stats(r["latency_ms"] for r in led if r["arm"] == "thinking"),
            "answer_call": stats(r["latency_ms"] for r in led if r["arm"] == "answer"),
            "per_attempt": stats(per_attempt.values()),
            "output_tokens_per_s_per_call": {"median": float(np.median(tps)), "p10": float(np.percentile(tps, 10)),
                                             "p90": float(np.percentile(tps, 90))},
            "jev_call": stats(r["latency_ms"] for r in jev)}
    front = [r for r in rows(RESULTS / "runs" / FRONTIER / "ledger.jsonl") if r["component"] == "frontier" and r["status"] == "ok"]
    out["frontier_call"] = {"run": FRONTIER, **stats(r["latency_ms"] for r in front)}
    for name, w in out["workers"].items():
        print(f"{name}: per attempt median {w['per_attempt']['median_s']:.1f} s, p90 {w['per_attempt']['p90_s']:.1f} s; "
              f"thinking call median {w['thinking_call']['median_s']:.1f} s; answer call {w['answer_call']['median_s']:.1f} s; "
              f"{w['output_tokens_per_s_per_call']['median']:.1f} tok/s; Jev call median {w['jev_call']['median_s']:.3f} s")
    f = out["frontier_call"]
    print(f"frontier call median {f['median_s']:.2f} s, p90 {f['p90_s']:.2f} s (n {f['n']})")
    (RESULTS / "latency_summary_v1.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("written results/latency_summary_v1.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
