"""Replay the escalation policies on logged attempts (descriptive; outside Holm).

    uv run python scripts/replay.py --run-id pilot-v1 --run-id pilot-v1b --frontier-run frontier-dev-v1 --scores dev-oof
    uv run python scripts/replay.py --split test --run-id <test-run> --frontier-run <test-frontier-run> --scores final

Inputs: the small model's labelled attempts, their Jev records, the frontier
run's hidden labels (one per task and replicate), and configs/routers_v1.json.
Scores: "dev-oof" uses the frozen out-of-fold development scores
(results/dev_router_scores.json; a code check, thresholds were set on them);
"final" applies the frozen final models (the test analysis). A decision
checkpoint whose router needs a missing Jev answer falls back to the cheap LR
at the same operating point.

Two views per router and budget q_VP in {10, 25, 50}%:
  frozen   escalate if s > t, or s = t and u < alpha (deployment view; the
           realized rate is reported);
  top-k    exactly round(q M) decision checkpoints by score (label-free
           ranking view at identical budgets).
Each is compared with random escalation at its realized rate (closed form) and
with forced-failure-only. Endpoints: always-small, forced-failure-only,
always-frontier, and the oracle (escalate when the frontier answer passes and
the small model's does not; per replicate). Gains: percentage points of final
hidden pass per attempt, mean over the frontier replicates, with a task
bootstrap within benchmark.

Costs per attempt, two views: the small model's share of its run's energy
(owned hardware) or wall time (cloud equivalent), Jev input tokens at decision
checkpoints for the arms a router uses (dollars at the third-party price,
unconfirmed), and the frontier's reported cost for the calls made.
Writes results/replay_<runs>_<scores>.json.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict

import numpy as np

from system1.config import CONFIGS, RESULTS, ROOT, load_prices
from system1.eval import predict as P
from system1.eval import replay as R
from system1.eval.labels import load_labelled
from system1.eval.ledger import read_jsonl

JEV_USD_PER_M_INPUT = 0.042  # third-party price, unconfirmed for the direct API (findings.md, Costs)
ARMS = {"cheap": [], "cheap+code": [P.HISTORY_ARM], "cheap+code+thinking": [P.HISTORY_ARM, P.TRACE_ARM],
        "cheap+strong4": [P.HISTORY_ARM, P.TRACE_ARM], "strong4 mean": [P.HISTORY_ARM, P.TRACE_ARM]}


def load_rg():
    spec = importlib.util.spec_from_file_location("resource_guide", ROOT / "scripts" / "resource_guide.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frontier_outcomes(run_id: str) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    """Per task: hidden pass of each replicate (0/1) and the reported cost of each replicate."""
    d = RESULTS / "runs" / run_id
    meta = json.loads((d / "frontier_grade_meta.json").read_text(encoding="utf-8"))
    if not meta["protocol"] or meta["labels"]["invalid"]:
        raise SystemExit(f"STOP: {run_id} frontier grades are not a clean protocol session")
    labels = {l["checkpoint_id"]: l for l in read_jsonl(d / "frontier_labels.jsonl")[0]}
    answers = read_jsonl(d / "frontier_answers.jsonl")[0]
    z, cost = defaultdict(dict), defaultdict(dict)
    for a in answers:
        cid = f"{a['task_id']}/frontier/s{a['sample']}"
        z[a["task_id"]][a["sample"]] = float(labels[cid]["passed"])
        cost[a["task_id"]][a["sample"]] = a["usd_reported"] if a["usd_reported"] is not None else a["usd_computed"]
    n_rep = {len(v) for v in z.values()}
    if len(n_rep) != 1:
        raise SystemExit(f"STOP: tasks have different numbers of frontier replicates {n_rep}")
    k = n_rep.pop()
    return ({t: np.array([v[s] for s in range(k)]) for t, v in z.items()},
            {t: np.array([v[s] for s in range(k)]) for t, v in cost.items()})


def score_final(row: dict, router: dict) -> float | None:
    """The frozen router's score of one decision checkpoint; None if a Jev arm it needs is missing."""
    m = router["model"]
    if m["kind"] == "mean":
        if row["history"] is None or row["trace"] is None:
            return None
        return P.jev_mean(row["history"], row["trace"])
    fs = m["feature_set"]
    if fs != "cheap" and (row["history"] is None or (fs != "cheap+code" and row["trace"] is None)):
        return None
    vec = P.row_vector(row["cp"]["features"], row["has_trace"], row["history"] or {}, row["trace"] or {}, fs)
    return float(P.predict_final(m, P.matrix([vec], m["columns"]))[0])


def jev_tokens(run_ids: list[str]) -> dict[tuple, int]:
    """Input tokens per (task, attempt, round, arm) over all HTTP attempts of the scoring calls."""
    out: dict[tuple, int] = defaultdict(int)
    for rid in run_ids:
        for r in read_jsonl(RESULTS / "runs" / rid / "jev_ledger.jsonl")[0]:
            out[(r["task_id"], r["attempt"], r["step"], r["arm"])] += r["input_tokens"] or 0
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    ap.add_argument("--frontier-run", required=True)
    ap.add_argument("--split", default="dev", choices=("dev", "test"))
    ap.add_argument("--scores", required=True, choices=("dev-oof", "final"))
    ap.add_argument("--n-boot", type=int, default=2000)
    args = ap.parse_args()
    if args.split == "test" and args.scores != "final":
        print("test replay uses --scores final")
        return 2
    cfg = json.loads((CONFIGS / "routers_v1.json").read_text(encoding="utf-8"))
    prices = load_prices()["local_gpu"]

    # Attempts and their decision checkpoints
    cps = [c for rid in args.run_id for c in load_labelled(RESULTS / "runs" / rid)]
    attempts = R.build_attempts(cps)
    totals = {}
    for rid in args.run_id:
        meta = json.loads((RESULTS / "runs" / rid / "run_meta.json").read_text(encoding="utf-8"))
        totals[rid] = (sum(s["elapsed_s"] for s in meta["sessions"] if s.get("elapsed_s")),
                       sum(s["energy_wh"] for s in meta["sessions"] if s.get("energy_wh")))
    R.allocate_run_costs(attempts, totals)
    z, fcost = frontier_outcomes(args.frontier_run)
    missing = {a.task_id for a in attempts} - set(z)
    if missing:
        raise SystemExit(f"STOP: {len(missing)} tasks have no frontier answers")

    # Router scores at decision checkpoints
    vp_idx = [i for i, a in enumerate(attempts) if not a.forced]
    ids = [attempts[i].decision_id for i in vp_idx]
    scores: dict[str, np.ndarray] = {}
    fallback_used: dict[str, int] = {}
    if args.scores == "dev-oof":
        dev = json.loads((RESULTS / "dev_router_scores.json").read_text(encoding="utf-8"))
        if dev["runs"] != args.run_id:
            raise SystemExit("STOP: the dev scores were made on other runs")
        for name in cfg["routers"]:
            scores[name] = np.array([dev["scores"][name][c] for c in ids])
            fallback_used[name] = 0
    else:
        rg = load_rg()
        rows = {d["cp"]["checkpoint_id"]: d for d in rg.load(args.run_id, split=args.split, require_ok=False)}
        cheap = np.array([score_final(rows[c], cfg["routers"]["cheap"]) for c in ids])
        for name, router in cfg["routers"].items():
            s = [score_final(rows[c], router) for c in ids]
            fallback_used[name] = sum(v is None for v in s)
            scores[name] = np.array([v if v is not None else np.nan for v in s])
            scores[f"{name}__cheap"] = cheap  # used where the router's own score is missing

    tok = jev_tokens(args.run_id)

    def jev_cost(name: str) -> np.ndarray:
        """Jev dollars per attempt for a router (decision checkpoints only)."""
        out = np.zeros(len(attempts))
        for i in vp_idx:
            a = attempts[i]
            rnd = int(a.decision_id.rsplit("/r", 1)[1])
            n = sum(tok.get((a.task_id, a.attempt, rnd, arm), 0) for arm in ARMS[name])
            out[i] = n * JEV_USD_PER_M_INPUT / 1e6
        return out

    small_owned = np.array([a.energy_wh / 1000 * prices["owned_hardware"]["usd_per_kwh"] for a in attempts])
    small_cloud = np.array([a.gpu_s / 3600 * prices["cloud_equivalent"]["usd_per_hour"] for a in attempts])
    fc = np.array([fcost[a.task_id].mean() for a in attempts])

    def costs(res: R.PolicyResult, router: str | None, small: bool = True) -> dict:
        jev = jev_cost(router) if router else np.zeros(len(attempts))
        front = res.escalated * fc
        base_o, base_c = (small_owned, small_cloud) if small else (0.0, 0.0)
        return {"usd_owned": float(np.mean(base_o + jev + front)), "usd_cloud": float(np.mean(base_c + jev + front)),
                "usd_frontier": float(front.mean()), "usd_jev": float(jev.mean()),
                "jev_price_note": "third-party $0.042/M input, unconfirmed"}

    def esc_mask(sel: np.ndarray) -> np.ndarray:
        m = np.zeros(len(attempts), bool)
        m[np.array(vp_idx)[sel]] = True
        return m

    out = {"runs": args.run_id, "frontier_run": args.frontier_run, "split": args.split, "scores": args.scores,
           "routers_version": cfg["version"], "n_attempts": len(attempts), "n_decisions": len(vp_idx),
           "forced_share": float(np.mean([a.forced for a in attempts])), "fallback_used": fallback_used,
           "policies": []}

    forced_only = R.outcome(attempts, z, np.zeros(len(attempts), bool), "forced-failure-only")
    anchors = [(R.outcome(attempts, z, np.zeros(len(attempts), bool), "always-small", forced_to_frontier=False), None,
                True),
               (forced_only, None, True), (R.always_frontier(attempts, z), None, False)]
    # Oracle per replicate: escalate exactly when that replicate's answer passes and the small model's does not.
    by_rep = np.stack([np.where([a.forced for a in attempts], [z[a.task_id][r] for a in attempts],
                                [max(a.y, z[a.task_id][r]) for a in attempts]) for r in range(len(next(iter(z.values()))))])
    orc_opt = np.mean([[0.0 if a.forced else float(z[a.task_id][r] > a.y) for a in attempts]
                       for r in range(by_rep.shape[0])], axis=0)
    forced_f = np.array([a.forced for a in attempts], float)
    oracle = R.PolicyResult("oracle", by_rep.mean(axis=0), by_rep, forced_f + orc_opt, orc_opt)
    anchors.append((oracle, None, True))
    for res, router, small in anchors:
        out["policies"].append({**R.summarize(res, attempts, z), **costs(res, router, small), "view": "endpoint"})

    for name in cfg["routers"]:
        s = scores[name]
        for q in R.RATES:
            th = cfg["routers"][name]["thresholds"][f"{q:.2f}"]
            fb = cfg["routers"][cfg["fallback_when_jev_missing"]]["thresholds"][f"{q:.2f}"]
            frozen = np.array([
                R.escalate(s[j], th["t"], th["alpha"], ids[j]) if not np.isnan(s[j]) else
                R.escalate(scores[f"{name}__cheap"][j], fb["t"], fb["alpha"], ids[j]) for j in range(len(ids))])
            filled = np.where(np.isnan(s), scores.get(f"{name}__cheap", s), s)
            topk = R.top_k(filled, ids, q)
            for view, sel in (("frozen", frozen), ("top-k", topk)):
                res = R.outcome(attempts, z, esc_mask(sel), f"{name} | {view} | q={q:.2f}")
                q_real = float(sel.mean())
                rnd = R.random_expected(attempts, z, q_real)
                g_r = R.task_bootstrap_gain(attempts, res.final, rnd.final, args.n_boot)
                g_f = R.task_bootstrap_gain(attempts, res.final, forced_only.final, args.n_boot)
                bench = {}
                for b in sorted({a.benchmark for a in attempts}):
                    m = np.array([a.benchmark == b for a in attempts])
                    vb = np.array([not a.forced for a in attempts]) & m
                    qb = float(res.optional[vb].mean())
                    rb = R.random_expected([a for a, k in zip(attempts, m) if k], z, qb)
                    bench[b] = {"pass": float(res.final[m].mean()), "q_vp": qb,
                                "gain_vs_random_within_benchmark": float((res.final[m] - rb.final).mean())}
                out["policies"].append({**R.summarize(res, attempts, z), **costs(res, name), "router": name,
                                        "view": view, "q_nominal": q, "q_vp_realized": q_real,
                                        "gain_vs_random": g_r, "gain_vs_forced_only": g_f,
                                        "random_pass": float(rnd.final.mean()), "by_benchmark": bench})

    path = RESULTS / f"replay_{'+'.join(args.run_id)}_{args.scores}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(attempts)} attempts, {len(vp_idx)} decisions, forced share {out['forced_share']:.3f}")
    print(f"{'policy':42s} {'pass':>6s} {'q_vp':>6s} {'calls':>6s} {'gain vs random (pp)':>24s} {'$ owned':>9s} {'$ cloud':>9s}")
    for p in out["policies"]:
        g = p.get("gain_vs_random")
        gs = f"{100 * g[0]:+.1f} ({100 * g[1]:+.1f} to {100 * g[2]:+.1f})" if g else ""
        print(f"{p['policy']:42s} {p['pass']:6.3f} {p['q_vp']:6.3f} {p['frontier_calls_per_attempt']:6.3f} "
              f"{gs:>24s} {p['usd_owned']:9.5f} {p['usd_cloud']:9.5f}")
    print(f"written {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
