"""Jev drift check: send a fixed sample of old requests again and compare with the stored scores.

    uv run python scripts/analysis/jev_drift_check.py prepare --source-run main-test-v1 --n 200 --out jev-drift-main-test-v1-a
    uv run python scripts/score_jev.py --run-id jev-drift-main-test-v1-a          # billed; operator's approval first
    uv run python scripts/analysis/jev_drift_check.py compare --source-run main-test-v1 --drift-run jev-drift-main-test-v1-a

prepare: draws a seeded sample of complete checkpoints from the source run, stratified by round
(1 vs 2-3) and by thinking-length tercile, never by any hidden outcome, and writes their trajectory
records to a NEW run folder results/runs/<out>/ (refuses an existing folder). The source run is
only read. score_jev.py then scores the new folder in both arms, with the same rubric, evidence
version and byte budget as before (it stops if the protocol differs from the code's).

compare: for every (checkpoint, arm) of the drift run, checks that the request hash equals the
stored one (the same bytes were sent; a mismatch stops the check), then reports the returned model
versions and, per arm and question, the signed mean change, the mean and largest absolute change and
the Spearman rank correlation. Writes results/jev_drift_<drift-run>.json. The script reports; the
pass/fail tolerances belong to the frozen plan, not to this script.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from collections import defaultdict

import numpy as np
from scipy.stats import spearmanr

from system1.config import RESULTS
from system1.eval.ledger import read_jsonl
from system1.loop.runner import complete_executions

SEED = 20261019


def last_scores(run: str) -> dict[tuple[str, str], dict]:
    rows, bad = read_jsonl(RESULTS / "runs" / run / "jev_scores.jsonl")
    if bad:
        raise SystemExit(f"STOP: {len(bad)} damaged lines in {run}/jev_scores.jsonl")
    return {(r["checkpoint_id"], r["arm"]): r for r in rows}  # the last record per (checkpoint, arm)


def prepare(args) -> int:
    out = RESULTS / "runs" / args.out
    if out.exists():
        raise SystemExit(f"STOP: {out} exists; a drift run is written once")
    rows, bad = read_jsonl(RESULTS / "runs" / args.source_run / "trajectories.jsonl")
    if bad:
        raise SystemExit(f"STOP: {len(bad)} damaged lines in the source trajectories")
    cps = complete_executions(rows)
    tok = np.array([c["generation"]["thinking_tokens"] for c in cps])
    cuts = np.quantile(tok, [1 / 3, 2 / 3])
    strata = defaultdict(list)
    for c, t in zip(cps, tok):
        strata[(c["round"] > 1, int(np.searchsorted(cuts, t, side="right")))].append(c)
    rng = random.Random(args.seed)
    pick = []
    for key in sorted(strata):  # proportional allocation, at least one per stratum
        group = sorted(strata[key], key=lambda c: c["checkpoint_id"])
        k = max(1, round(args.n * len(group) / len(cps)))
        pick += rng.sample(group, min(k, len(group)))
    out.mkdir(parents=True)
    with (out / "trajectories.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for c in sorted(pick, key=lambda c: c["checkpoint_id"]):
            f.write(json.dumps(c) + "\n")
    (out / "drift_sample.json").write_text(json.dumps(
        {"source_run": args.source_run, "seed": args.seed, "n_requested": args.n, "n": len(pick),
         "strata": {f"later_round={a},length_tercile={b}": len(v) for (a, b), v in sorted(strata.items())},
         "thinking_token_cuts": cuts.tolist()}, indent=1), encoding="utf-8")
    print(f"written {len(pick)} checkpoints to {out}; next: uv run python scripts/score_jev.py --run-id {args.out}")
    return 0


def compare(args) -> int:
    old, new = last_scores(args.source_run), last_scores(args.drift_run)
    pairs = [(k, old.get(k), r) for k, r in sorted(new.items()) if r["status"] == "ok"]
    missing = [k for k, o, _ in pairs if o is None or o["status"] != "ok"]
    if missing:
        raise SystemExit(f"STOP: {len(missing)} drift records have no ok source record, e.g. {missing[:2]}")
    diff_bytes = [k for k, o, r in pairs if o["request_sha256"] != r["request_sha256"]]
    if diff_bytes:
        raise SystemExit(f"STOP: {len(diff_bytes)} requests differ from the stored bytes, e.g. {diff_bytes[:2]}")
    versions = {"source": sorted({o["model_returned"] for _, o, _ in pairs}),
                "drift": sorted({r["model_returned"] for _, _, r in pairs})}
    by = defaultdict(lambda: ([], []))
    for (cid, arm), o, r in pairs:
        for q, v in r["features"].items():
            if v is not None and o["features"].get(q) is not None:
                by[(arm, q)][0].append(o["features"][q])
                by[(arm, q)][1].append(v)
    report = {"source_run": args.source_run, "drift_run": args.drift_run, "n_pairs": len(pairs),
              "model_versions": versions, "questions": {}}
    print(f"{len(pairs)} (checkpoint, arm) pairs with identical request bytes; versions {versions}")
    for (arm, q), (a, b) in sorted(by.items()):
        a, b = np.array(a, float), np.array(b, float)
        d = b - a
        rho = float(spearmanr(a, b).statistic) if len(set(a)) > 1 and len(set(b)) > 1 else None
        report["questions"][f"{arm} | {q}"] = {"n": len(d), "mean_change": float(d.mean()),
                                               "mean_abs_change": float(np.abs(d).mean()),
                                               "max_abs_change": float(np.abs(d).max()), "spearman": rho}
        print(f"  {arm:16s} {q:34s} n={len(d):4d} mean {d.mean():+.4f} |mean| {np.abs(d).mean():.4f} "
              f"max {np.abs(d).max():.3f} rho {'-' if rho is None else f'{rho:.3f}'}")
    path = RESULTS / f"jev_drift_{args.drift_run}.json"
    path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"written {path}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--source-run", required=True)
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--seed", type=int, default=SEED)
    p.add_argument("--out", required=True)
    c = sub.add_parser("compare")
    c.add_argument("--source-run", required=True)
    c.add_argument("--drift-run", required=True)
    args = ap.parse_args()
    return prepare(args) if args.cmd == "prepare" else compare(args)


if __name__ == "__main__":
    sys.exit(main())
