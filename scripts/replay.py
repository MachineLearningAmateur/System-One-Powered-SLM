"""Replay the escalation policies on logged attempts (descriptive; outside Holm).

    uv run python scripts/replay.py --run-id pilot-v1 --run-id pilot-v1b --frontier-run frontier-dev-v1 --scores dev-oof --routers v2
    uv run python scripts/replay.py --split test --run-id <test-run> --frontier-run <test-frontier-run> --scores final --routers v2

Inputs: the small model's labelled attempts, their Jev records, the frontier
run's hidden labels (one per task and replicate), and configs/routers_<version>.json
(Pinocchio's scores come from each run's pinocchio_scores.jsonl).
Scores: "dev-oof" uses the frozen out-of-fold development scores
(results/dev_router_scores.json; a code check, thresholds were set on them);
"final" applies the frozen final models (the test analysis). A decision
checkpoint whose router needs a missing Jev answer falls back to the cheap LR
at the same operating point.

Two views per router and budget q_VP in {10, 25, 50}%:
  frozen   escalate if s > t, or s = t and u < alpha (deployment view; the
           realized rate is reported);
  top-k    exactly round(q M) decision checkpoints by score (label-free
           ranking view at identical budgets). Scores are ranked as
           percentiles in the router's frozen dev distribution, and a
           cheap-LR fallback score as its percentile in the cheap
           distribution, so the two share one scale.
Each is compared with random escalation at its realized rate (closed form) and
with forced-failure-only. Endpoints: always-small, forced-failure-only,
always-frontier, and the oracle (escalate when the frontier answer passes and
the small model's does not; per replicate). Gains: percentage points of final
hidden pass per attempt, mean over the frontier replicates, with a task
bootstrap within benchmark; the realized rate and the random expectation are
recomputed inside each resample (conditional on the policy's selection).
Frontier labels must belong to the graded session and to the answer's code.

Costs per attempt, two views: the small model's share of its run's energy
(owned hardware) or wall time (cloud equivalent), Jev input tokens at decision
checkpoints for the arms a router uses, counted over the HTTP attempts of the
call behind each stored score (stability repeats excluded; dollars at the
third-party price, unconfirmed), and the frontier's cost over all HTTP
attempts of each call made. Unknown usage is counted and reported, never
treated as zero.
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
from system1.eval.labels import code_sha, load_labelled
from system1.eval.ledger import read_jsonl

JEV_USD_PER_M_INPUT = 0.042  # third-party price, unconfirmed for the direct API (findings.md, Costs)
ARMS = {"cheap": [], "cheap+code": [P.HISTORY_ARM], "cheap+code+thinking": [P.HISTORY_ARM, P.TRACE_ARM],
        "cheap+strong4": [P.HISTORY_ARM, P.TRACE_ARM], "strong4 mean": [P.HISTORY_ARM, P.TRACE_ARM],
        "pinocchio": []}  # Pinocchio runs locally: its cost is reported as CPU seconds, not dollars


def load_rg():
    spec = importlib.util.spec_from_file_location("resource_guide", ROOT / "scripts" / "resource_guide.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _rows(path, what: str) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"STOP: {path} is missing ({what})")
    rows, bad = read_jsonl(path)
    if bad:
        raise SystemExit(f"STOP: {len(bad)} damaged lines in {path}")
    return rows


def call_cost(ledger_rows: list[dict], call_id: str) -> tuple[float, bool]:
    """Dollars of one logical frontier call over all its HTTP attempts. The flag is False when the
    call has no ledger rows or any attempt has no cost: zero billing is never assumed (a timeout
    does not prove that the provider did no billable work)."""
    rows = [r for r in ledger_rows if r["call_id"] == call_id]
    usd, complete = 0.0, bool(rows)
    for r in rows:
        v = r["usd_reported"] if r["usd_reported"] is not None else r["usd_computed"]
        if v is None:
            complete = False
        else:
            usd += v
    return usd, complete


def frontier_outcomes(run_id: str) -> tuple[dict[str, np.ndarray], dict[str, np.ndarray], dict]:
    """Per task: hidden pass of each replicate (0/1) and the cost of each replicate's call.
    Each label must belong to the session in frontier_grade_meta.json and to the answer's exact code."""
    d = RESULTS / "runs" / run_id
    meta = json.loads((d / "frontier_grade_meta.json").read_text(encoding="utf-8"))
    if not meta["protocol"] or meta["labels"]["invalid"]:
        raise SystemExit(f"STOP: {run_id} frontier grades are not a clean protocol session")
    labels: dict[str, dict] = {}
    for lab in _rows(d / "frontier_labels.jsonl", "frontier labels"):
        if lab["checkpoint_id"] in labels:
            raise SystemExit(f"STOP: two frontier labels for {lab['checkpoint_id']}")
        if lab["grade_session"] != meta["session"]:
            raise SystemExit(f"STOP: {lab['checkpoint_id']} was graded in another session")
        labels[lab["checkpoint_id"]] = lab
    ledger = _rows(d / "ledger.jsonl", "frontier ledger")
    z, cost = defaultdict(dict), defaultdict(dict)
    incomplete = 0
    for a in _rows(d / "frontier_answers.jsonl", "frontier answers"):
        cid = f"{a['task_id']}/frontier/s{a['sample']}"
        if a["sample"] in z[a["task_id"]]:
            raise SystemExit(f"STOP: two answers for {cid}")
        lab = labels.get(cid)
        if lab is None or lab["code_sha256"] != code_sha(a["code"]):
            raise SystemExit(f"STOP: the label of {cid} does not belong to its answer's code")
        z[a["task_id"]][a["sample"]] = float(lab["passed"])
        usd, complete = call_cost(ledger, a["call_id"])
        incomplete += not complete
        cost[a["task_id"]][a["sample"]] = usd
    n_rep = {len(v) for v in z.values()}
    if len(n_rep) != 1:
        raise SystemExit(f"STOP: tasks have different numbers of frontier replicates {n_rep}")
    k = n_rep.pop()
    if any(sorted(v) != list(range(k)) for v in z.values()):
        raise SystemExit("STOP: replicate indices are not 0..k-1 for every task")
    info = {"replicates": k, "calls_with_unknown_cost": incomplete, "grade_session": meta["session"]}
    return ({t: np.array([v[s] for s in range(k)]) for t, v in z.items()},
            {t: np.array([v[s] for s in range(k)]) for t, v in cost.items()}, info)


def pinocchio_rows(run_ids: list[str], setup: list, checkpoints: list[dict], require_pinned: bool) -> dict[str, dict]:
    """Input-v1 Pinocchio records per checkpoint id that match the current execution and rebuilt
    input, and the routers file's setup; on test also every pinned field (pinocchio_input.PINNED)."""
    from system1.features import pinocchio_input as PI
    from system1.loop.tasks import load_tasks
    tasks = load_tasks()
    out: dict[str, dict] = {}
    for rid in run_ids:
        cps = [c for c in checkpoints if c["run_id"] == rid]
        recs, counts = PI.select_records(PI.read_records(RESULTS / "runs" / rid, PI.V1), cps, tasks, PI.V1,
                                         require_pinned=require_pinned)
        for cid, r in recs.items():
            if [r["input_version"], r["adapter"], r["base_model"], r["package"]] != setup:
                raise SystemExit(f"STOP: {cid} was scored with another Pinocchio setup")
            out[cid] = r
    return out


def score_final(row: dict, router: dict, pin: dict[str, dict] | None = None) -> float | None:
    """The frozen router's score of one decision checkpoint; None if an input it needs is missing
    (a Jev arm, or a Pinocchio score)."""
    m = router["model"]
    if m["kind"] == "external":
        rec = (pin or {}).get(row["cp"]["checkpoint_id"])
        return None if rec is None else float(rec["score"])
    if m["kind"] == "mean":
        if row["history"] is None or row["trace"] is None:
            return None
        return P.jev_mean(row["history"], row["trace"])
    fs = m["feature_set"]
    if fs != "cheap" and (row["history"] is None or (fs != "cheap+code" and row["trace"] is None)):
        return None
    vec = P.row_vector(row["cp"]["features"], row["has_trace"], row["history"] or {}, row["trace"] or {}, fs)
    return float(P.predict_final(m, P.matrix([vec], m["columns"]))[0])


def jev_tokens(run_ids: list[str]) -> dict[tuple, int | None]:
    """Input tokens of the scoring call behind each stored score, per (checkpoint, arm), over all of
    that call's HTTP attempts. Calls that no stored score uses (the stability repeats, superseded
    rescoring) are experiment cost, not router cost. None = the call's usage is unknown."""
    out: dict[tuple, int | None] = {}
    for rid in run_ids:
        d = RESULTS / "runs" / rid
        scores = {(r["checkpoint_id"], r["arm"]): r for r in _rows(d / "jev_scores.jsonl", "Jev scores")}
        by_call: dict[str, list[dict]] = defaultdict(list)
        for r in _rows(d / "jev_ledger.jsonl", "Jev ledger"):
            by_call[r["call_id"]].append(r)
        for key, rec in scores.items():
            rows = by_call.get(rec.get("call_id"), [])
            out[key] = None if not rows or any(r["input_tokens"] is None for r in rows) else sum(
                r["input_tokens"] for r in rows)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", action="append", required=True)
    ap.add_argument("--frontier-run", required=True)
    ap.add_argument("--split", default="dev", choices=("dev", "test"))
    ap.add_argument("--scores", required=True, choices=("dev-oof", "final"))
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--routers", default="v2", help="frozen routers file: configs/routers_<version>.json")
    args = ap.parse_args()
    if args.split == "test" and args.scores != "final":
        print("test replay uses --scores final")
        return 2
    cfg = json.loads((CONFIGS / f"routers_{args.routers}.json").read_text(encoding="utf-8"))
    prices = load_prices()["local_gpu"]

    # Attempts and their decision checkpoints (build_attempts refuses a checkpoint id in two runs)
    cps = [c for rid in args.run_id for c in load_labelled(RESULTS / "runs" / rid)]
    attempts = R.build_attempts(cps)
    totals, cost_complete = {}, True
    for rid in args.run_id:
        meta = json.loads((RESULTS / "runs" / rid / "run_meta.json").read_text(encoding="utf-8"))
        sess = meta["sessions"]
        cost_complete &= all(s.get("elapsed_s") is not None and s.get("energy_wh") is not None for s in sess)
        totals[rid] = (sum(s.get("elapsed_s") or 0.0 for s in sess), sum(s.get("energy_wh") or 0.0 for s in sess))
    R.allocate_run_costs(attempts, totals)
    z, fcost, finfo = frontier_outcomes(args.frontier_run)
    missing = {a.task_id for a in attempts} - set(z)
    if missing:
        raise SystemExit(f"STOP: {len(missing)} tasks have no frontier answers")

    # Router scores at decision checkpoints
    vp_idx = [i for i, a in enumerate(attempts) if not a.forced]
    ids = [attempts[i].decision_id for i in vp_idx]
    scores: dict[str, np.ndarray] = {}
    fallback_used: dict[str, int] = {}
    if args.scores == "dev-oof":
        dev = json.loads((RESULTS / cfg.get("dev_scores_file", "dev_router_scores.json")).read_text(encoding="utf-8"))
        if dev["runs"] != args.run_id:
            raise SystemExit("STOP: the dev scores were made on other runs")
        for name in cfg["routers"]:
            scores[name] = np.array([dev["scores"][name][c] for c in ids])
            fallback_used[name] = 0
        cheap = scores["cheap"]
    else:
        rg = load_rg()
        rows = {d["cp"]["checkpoint_id"]: d for d in rg.load(args.run_id, split=args.split, require_ok=False)}
        ext = [r for r in cfg["routers"].values() if r["model"]["kind"] == "external"]
        pin = pinocchio_rows(args.run_id, list(ext[0]["model"]["setup"]), cps, args.split == "test") if ext else {}
        cheap = np.array([score_final(rows[c], cfg["routers"]["cheap"]) for c in ids], float)
        for name, router in cfg["routers"].items():
            s = [score_final(rows[c], router, pin) for c in ids]
            fallback_used[name] = sum(v is None for v in s)
            scores[name] = np.array([np.nan if v is None else v for v in s], float)

    # Percentiles in each router's frozen dev distribution: the ranking view's common scale
    def pct(name: str, values: np.ndarray) -> np.ndarray:
        dd = cfg["routers"][name]["dev_distribution"]
        ds, dw = np.array(dd["scores"]), np.array(dd["weights"])
        return np.array([R.dev_percentile(v, ds, dw) for v in values])

    cheap_pct = pct("cheap", cheap)
    tok = jev_tokens(args.run_id)
    jev_unknown: dict[str, int] = {}

    def jev_cost(name: str) -> np.ndarray:
        """Jev dollars per attempt for a router: its arms at the decision checkpoint only."""
        out = np.zeros(len(attempts))
        unknown = 0
        for i in vp_idx:
            n = 0
            for arm in ARMS[name]:
                v = tok.get((attempts[i].decision_id, arm))
                if v is None:
                    unknown += 1
                else:
                    n += v
            out[i] = n * JEV_USD_PER_M_INPUT / 1e6
        jev_unknown[name] = unknown
        return out

    small_owned = np.array([a.energy_wh / 1000 * prices["owned_hardware"]["usd_per_kwh"] for a in attempts])
    small_cloud = np.array([a.gpu_s / 3600 * prices["cloud_equivalent"]["usd_per_hour"] for a in attempts])
    fc = R.frontier_matrix(attempts, fcost)

    def costs(res: R.PolicyResult, router: str | None, small: bool = True) -> dict:
        jev = jev_cost(router) if router else np.zeros(len(attempts))
        front = R.frontier_cost(res, fc)
        base_o, base_c = (small_owned, small_cloud) if small else (0.0, 0.0)
        return {"usd_owned": float(np.mean(base_o + jev + front)), "usd_cloud": float(np.mean(base_c + jev + front)),
                "usd_small_owned": float(np.mean(base_o)), "usd_small_cloud": float(np.mean(base_c)),
                "usd_frontier": float(front.mean()), "usd_jev": float(jev.mean()),
                "jev_price_note": "third-party $0.042/M input, unconfirmed",
                "excludes": "Pinocchio CPU compute (reported separately as elapsed CPU seconds)"}

    def esc_mask(sel: np.ndarray) -> np.ndarray:
        m = np.zeros(len(attempts), bool)
        m[np.array(vp_idx)[sel]] = True
        return m

    pin_cpu = None
    if "pinocchio" in cfg["routers"]:
        recs = pinocchio_rows(args.run_id, list(cfg["routers"]["pinocchio"]["model"]["setup"]), cps,
                              args.split == "test")
        secs = [recs[c]["cpu_seconds"] for c in ids if c in recs]
        # Elapsed inference time on the CPU (perf_counter), loading excluded; not priced in the $ totals.
        pin_cpu = {"elapsed_cpu_s_per_decision": float(np.mean(secs)) if secs else None,
                   "elapsed_cpu_s_per_attempt": float(np.sum(secs) / len(attempts)) if secs else None,
                   "decisions_scored": len(secs), "note": "not included in usd_owned / usd_cloud"}
    out = {"runs": args.run_id, "frontier_run": args.frontier_run, "split": args.split, "scores": args.scores,
           "pinocchio_cpu": pin_cpu,
           "routers_version": cfg["version"], "n_attempts": len(attempts), "n_decisions": len(vp_idx),
           "forced_share": float(np.mean([a.forced for a in attempts])), "fallback_used": fallback_used,
           "frontier": finfo, "small_model_cost_complete": cost_complete, "policies": []}

    forced_only = R.outcome(attempts, z, np.zeros(len(attempts), bool), "forced-failure-only")
    anchors = [(R.outcome(attempts, z, np.zeros(len(attempts), bool), "always-small", forced_to_frontier=False), True),
               (forced_only, True), (R.always_frontier(attempts, z), False), (R.oracle(attempts, z), True)]
    for res, small in anchors:
        out["policies"].append({**R.summarize(res, attempts, z), **costs(res, None, small), "view": "endpoint"})

    fb_name = cfg["fallback_when_jev_missing"]
    for name in cfg["routers"]:
        s = scores[name]
        miss = np.isnan(s)
        rank = np.where(miss, cheap_pct, pct(name, np.where(miss, 0.0, s)))
        for q in R.RATES:
            th = cfg["routers"][name]["thresholds"][f"{q:.2f}"]
            fb = cfg["routers"][fb_name]["thresholds"][f"{q:.2f}"]
            frozen = np.array([R.escalate(cheap[j], fb["t"], fb["alpha"], ids[j]) if miss[j] else
                               R.escalate(s[j], th["t"], th["alpha"], ids[j]) for j in range(len(ids))])
            # Ties: the router's own scores before cheap-fallback scores, raw scores only within a source.
            topk = R.top_k(rank, ids, q, secondary=np.where(miss, cheap, s), priority=(~miss).astype(float))
            for view, sel in (("frozen", frozen), ("top-k", topk)):
                res = R.outcome(attempts, z, esc_mask(sel), f"{name} | {view} | q={q:.2f}")
                g_r = R.gain_vs_random(attempts, z, res, args.n_boot)
                g_f = R.task_bootstrap_gain(attempts, res.final, forced_only.final, args.n_boot)
                bench = {}
                for b in sorted({a.benchmark for a in attempts}):
                    m = np.array([a.benchmark == b for a in attempts])
                    sub = [a for a, k in zip(attempts, m) if k]
                    sub_res = R.PolicyResult(res.name, res.final_by_replicate[:, m], res.escalated_by_replicate[:, m],
                                             res.optional_by_replicate[:, m])
                    bench[b] = {"pass": float(res.final[m].mean()), "q_vp": R.summarize(sub_res, sub, z)["q_vp"],
                                "gain_vs_random_within_benchmark": R.gain_vs_random(sub, z, sub_res, 1)[0]}
                out["policies"].append({**R.summarize(res, attempts, z), **costs(res, name), "router": name,
                                        "view": view, "q_nominal": q, "gain_vs_random": g_r,
                                        "gain_vs_forced_only": g_f, "by_benchmark": bench})
    out["jev_calls_with_unknown_usage"] = jev_unknown

    path = RESULTS / f"replay_{'+'.join(args.run_id)}_{args.scores}_{cfg['version']}.json"
    path.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{len(attempts)} attempts, {len(vp_idx)} decisions, forced share {out['forced_share']:.3f}; "
          f"fallback used {fallback_used}; frontier {finfo}; small-model cost complete {cost_complete}; "
          f"Jev calls with unknown usage {jev_unknown}")
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
