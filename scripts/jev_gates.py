"""Technical gates for Jev on development checkpoints (docs/research-plan.md, Go/no-go 1).

    uv run python scripts/jev_gates.py --run-id pilot-v1 --run-id pilot-v1b

Reads jev_scores.jsonl (last record per checkpoint and arm), jev_repeat.jsonl
and the hidden labels. Prints, per arm: the share of final statuses (valid,
failed after retries, too large), the trace cuts and request sizes; per
feature: distinct values, the share at the most common value and at 0 or 1,
the spread, and the share of hidden-fail/hidden-pass pairs on visible-pass
checkpoints with the same score; duplicate feature vectors; and the score
changes in the repeat sample. Writes the same numbers to
results/jev_gates_<runs>.json. These are gates that the measurement can run;
they never decide the result, and nothing here is a test-set number.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter

from system1.config import RESULTS
from system1.eval.labels import load_labelled
from system1.eval.ledger import CostLedger
from system1.features.evidence import ARMS


def last_records(path) -> dict:
    rows, bad = CostLedger(path).read()
    if bad:
        raise RuntimeError(f"{len(bad)} damaged lines in {path}")
    return {(r["checkpoint_id"], r["arm"]): r for r in rows}


def feature_stats(values: list[float], vp_pairs: tuple[list[float], list[float]]) -> dict:
    mode, n_mode = Counter(round(v, 4) for v in values).most_common(1)[0]
    fail, ok = vp_pairs
    n_pairs = len(fail) * len(ok)
    tied = sum(a == b for a in fail for b in ok)
    return {"n": len(values), "distinct": len(set(values)), "mode": mode, "share_at_mode": n_mode / len(values),
            "share_at_0_or_1": sum(v in (0.0, 1.0) for v in values) / len(values),
            "sd": statistics.pstdev(values), "min": min(values), "max": max(values),
            "vp_pairs": n_pairs, "vp_pairs_tied_share": tied / n_pairs if n_pairs else None}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    args = ap.parse_args()

    labels, scores, repeats, ledger = {}, {}, {}, []
    for rid in args.run_id:
        d = RESULTS / "runs" / rid
        for c in load_labelled(d):
            labels[(rid, c["checkpoint_id"])] = c
        for k, r in last_records(d / "jev_scores.jsonl").items():
            scores[(rid, *k)] = r
        if (d / "jev_repeat.jsonl").exists():
            for k, r in last_records(d / "jev_repeat.jsonl").items():
                repeats[(rid, *k)] = r
        ledger += CostLedger(d / "jev_ledger.jsonl").read()[0]
    missing = [k for k in labels if any((*k, arm) not in scores for arm in ARMS)]
    out: dict = {"runs": args.run_id, "checkpoints": len(labels), "unscored_checkpoints": len(missing)}
    print(f"checkpoints {len(labels)}; without a record in every arm: {len(missing)}")

    calls = Counter(r["status"] for r in ledger)
    versions = Counter(r.get("model_returned") for r in ledger if r["status"] == "ok")
    out["http_attempts"] = dict(calls)
    out["model_versions"] = dict(versions)
    out["input_tokens"] = sum(r.get("input_tokens") or 0 for r in ledger)
    print(f"HTTP attempts by status {dict(calls)}; model versions {dict(versions)}; input tokens {out['input_tokens']}")

    out["arms"] = {}
    for arm in ARMS:
        recs = [r for (rid, cid, a), r in scores.items() if a == arm]
        st = Counter(r["status"] for r in recs)
        sent = [r for r in recs if r["request_bytes"] is not None]
        arm_out = {"records": len(recs), "status": dict(st),
                   "valid_share": st["ok"] / len(recs) if recs else None,
                   "failed_after_retries_share": (st["request_error"] + st["protocol_error"]) / len(recs) if recs else None,
                   "max_request_bytes": max((r["request_bytes"] for r in sent), default=None),
                   "over_budget": sum(r["request_bytes"] > r["byte_budget"] for r in sent),
                   "trace_truncated": sum(bool(r["trace_truncated"]) for r in recs),
                   "base_trimmed": sum(bool(r["base_trimmed"]) for r in recs)}
        print(f"\n== {arm}: {arm_out}")
        ok = [r for r in recs if r["status"] == "ok"]
        feats = sorted({q for r in ok for q, v in r["features"].items() if v is not None})
        na = Counter(s for r in recs for q, s in r["applicability"].items() if s != "applicable")
        arm_out["not_applicable"] = dict(na)
        arm_out["features"] = {}
        for q in feats:
            vals, fail, passed = [], [], []
            for r in ok:
                v = r["features"].get(q)
                if v is None:
                    continue
                vals.append(v)
                lab = labels[(r["run_id"], r["checkpoint_id"])]
                if lab["visible_pass"]:
                    (passed if lab["hidden"]["passed"] else fail).append(v)
            s = feature_stats(vals, (fail, passed))
            arm_out["features"][q] = s
            tied = "n/a" if s["vp_pairs_tied_share"] is None else f"{s['vp_pairs_tied_share']:.1%} of {s['vp_pairs']}"
            print(f"  {q:34s} n {s['n']:3d}  distinct {s['distinct']:3d}  at mode {s['share_at_mode']:.1%}  "
                  f"at 0/1 {s['share_at_0_or_1']:.1%}  sd {s['sd']:.3f}  range {s['min']:.2f}-{s['max']:.2f}  "
                  f"VP pairs tied {tied}")
        vecs = Counter(tuple(r["features"][q] for q in feats) for r in ok)
        arm_out["duplicate_feature_vectors"] = sum(n - 1 for n in vecs.values() if n > 1)
        print(f"  duplicate feature vectors: {arm_out['duplicate_feature_vectors']} of {len(ok)}")
        out["arms"][arm] = arm_out

    if repeats:
        rep: dict = {}
        same_req = sum(r["request_sha256"] == scores[k]["request_sha256"] for k, r in repeats.items())
        for k, r in repeats.items():
            if r["status"] != "ok" or scores[k]["status"] != "ok":
                continue
            for q, v in r["features"].items():
                if v is not None and scores[k]["features"].get(q) is not None:
                    rep.setdefault(q, []).append(abs(v - scores[k]["features"][q]))
        out["repeat"] = {"records": len(repeats), "same_request_bytes": same_req,
                         "abs_change": {q: {"n": len(d), "mean": statistics.mean(d), "max": max(d),
                                            "exact_same_share": sum(x == 0 for x in d) / len(d)}
                                        for q, d in sorted(rep.items())}}
        print(f"\nrepeat: {len(repeats)} records, same request bytes {same_req}/{len(repeats)}")
        for q, s in out["repeat"]["abs_change"].items():
            print(f"  {q:34s} n {s['n']:3d}  mean |change| {s['mean']:.4f}  max {s['max']:.4f}  "
                  f"exactly the same {s['exact_same_share']:.0%}")
    path = RESULTS / f"jev_gates_{'+'.join(args.run_id)}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwritten {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
