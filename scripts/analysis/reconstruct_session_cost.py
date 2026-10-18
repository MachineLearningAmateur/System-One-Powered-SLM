"""Rebuild the elapsed time and GPU energy of a run session that was killed before its
`finally` step wrote them (scripts/run_loop.py), from the session's own power samples.

    uv run python scripts/analysis/reconstruct_session_cost.py --run-id main-test-v1 --session 0          # check only
    uv run python scripts/analysis/reconstruct_session_cost.py --run-id main-test-v1 --session 0 --write

The session's samples are the rows of power.jsonl from its start to the next session's start.
Energy uses monitor.energy_wh (the runner's trapezoid rule). The elapsed time runs from the
first to the last sample: an estimate of the sampled window, not a bound. The method is
first checked on every complete session: its stored energy must match its samples.
The session keeps its original null values under "reconstruction".
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone

from system1.config import RESULTS
from system1.eval.ledger import read_jsonl
from system1.loop import monitor

TOLERANCE_WH = 0.5
NOTE = ("an estimate of the sampled window, not a bound: the runner's timer starts after the sampler and "
        "uses perf_counter, and nothing records how long after the last sample the process stopped; "
        "last_ledger_utc is independent evidence of when the work stopped")


def ts(iso: str) -> float:
    return datetime.fromisoformat(iso).timestamp()


def last_ledger(run_dir, sessions: list[dict], i: int) -> str | None:
    """The newest ledger row inside the session's window (independent of the power sampler)."""
    lo = ts(sessions[i]["started"])
    hi = ts(sessions[i + 1]["started"]) if i + 1 < len(sessions) else float("inf")
    rows, _ = read_jsonl(run_dir / "ledger.jsonl")
    t = [ts(r["ts"]) for r in rows if r.get("ts") and lo <= ts(r["ts"]) < hi]
    return datetime.fromtimestamp(max(t), timezone.utc).isoformat() if t else None


def window(samples: list[dict], sessions: list[dict], i: int) -> list[dict]:
    lo = ts(sessions[i]["started"])
    hi = ts(sessions[i + 1]["started"]) if i + 1 < len(sessions) else float("inf")
    return [s for s in samples if lo <= s["t"] < hi]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--session", type=int, required=True, help="index in run_meta.json sessions")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    d = RESULTS / "runs" / args.run_id
    meta_path = d / "run_meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    sessions = meta["sessions"]
    samples, bad = read_jsonl(d / "power.jsonl")
    if bad:
        raise SystemExit(f"STOP: {len(bad)} damaged lines in power.jsonl")
    samples.sort(key=lambda s: s["t"])

    for i, s in enumerate(sessions):  # check the method on the sessions that recorded their energy
        if s.get("energy_wh") is None or "reconstruction" in s:
            continue
        e = monitor.energy_wh(window(samples, sessions, i))
        print(f"session {i}: stored {s['energy_wh']:.1f} Wh, rebuilt {e:.1f} Wh, {s['power_samples']} samples")
        if abs(e - s["energy_wh"]) > TOLERANCE_WH:
            raise SystemExit(f"STOP: the rebuilt energy of session {i} does not match its stored value")

    s = sessions[args.session]
    if s.get("elapsed_s") is not None or s.get("energy_wh") is not None:
        raise SystemExit(f"STOP: session {args.session} already has elapsed_s or energy_wh")
    w = window(samples, sessions, args.session)
    if len(w) < 2:
        raise SystemExit("STOP: fewer than two power samples in the session")
    gaps = [b["t"] - a["t"] for a, b in zip(w, w[1:])]
    rec = {"energy_wh": round(monitor.energy_wh(w), 4), "elapsed_s": round(w[-1]["t"] - w[0]["t"], 1),
           "power_samples": len(w), "mean_power_w": round(sum(x["power_w"] for x in w) / len(w), 1)}
    last = datetime.fromtimestamp(w[-1]["t"], timezone.utc).isoformat()
    print(f"session {args.session}: {rec}; last sample {last}; largest gap {max(gaps):.1f} s")
    if not args.write:
        print("check only; use --write to store it")
        return 0
    s["reconstruction"] = {
        "source": "power.jsonl", "method": "monitor.energy_wh over the session's samples; elapsed = first to last sample",
        "estimate": NOTE, "last_sample_utc": last, "last_ledger_utc": last_ledger(d, sessions, args.session),
        "largest_gap_s": round(max(gaps), 1),
        "original": {k: s.get(k) for k in ("ended", "elapsed_s", "energy_wh", "outcome")},
        "reason": "the process was killed before the runner's finally step wrote the session's cost",
        "made_utc": datetime.now(timezone.utc).isoformat()}
    s.update(rec)
    s["outcome"] = "killed"
    meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"written {meta_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
