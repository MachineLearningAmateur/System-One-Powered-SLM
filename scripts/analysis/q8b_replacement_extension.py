"""Freeze and analyze the exploratory Qwen3-8B task-only replacement replay.

Offline preparation:
  PYTHONPATH=src python scripts/analysis/q8b_replacement_extension.py freeze
Offline analysis, only after the separately approved frontier collection and grading:
  PYTHONPATH=src python scripts/analysis/q8b_replacement_extension.py analyze --frontier-run q8b-frontier-replacement-v1

No command in this file makes model requests or executes candidate code. The
collector and existing sandbox grader remain separate steps.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

import numpy as np

from system1.config import CONFIGS, RESULTS, ROOT
from system1.eval import predict as P
from system1.eval import replay as R
from system1.eval.exclusions import load_exclusions
from system1.eval.labels import load_labelled
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
from system1.loop.runner import complete_executions, shown_task
from system1.loop.tasks import VISIBLE_TESTS_PATH, first_round_messages, load_tasks, render_test

SOURCE_RUN = "q8b-test-v1"
MANIFEST = CONFIGS / "q8b_replacement_extension_v1.json"
FRONTIER_RUN = "q8b-frontier-replacement-v1"
OUT = RESULTS / "q8b-replacement-extension-v1"
RATE = 0.25
BOOT_SEED = 20261027
N_BOOT = 5000
AZURE_USD_PER_HOUR = 3.2004  # reported West US 3 retail configuration; modeled, not invoice
AZURE_APP_HOURS = 9.52  # reported app lifetime; includes startup/cleanup, not just generation
JEV_USD_PER_M_INPUT = 0.042  # third-party public rate; direct account charge unconfirmed


def _sha_json(x: object) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _sources() -> dict[str, str]:
    names = ["configs/split_v1.json", "configs/visible_tests_v2.json", "configs/prices.yaml",
             "configs/grading_exclusions_v1.json", "configs/routers_q8b-v1.json", "configs/rubric_v2.yaml",
             "src/system1/loop/tasks.py", "src/system1/eval/replay.py", "src/system1/eval/predict.py",
             "src/system1/features/jev_scoring.py", "src/system1/features/evidence.py",
             "src/system1/routers/jev.py",
             "src/system1/frontier/client.py", "scripts/run_frontier.py",
             "scripts/grade_hidden.py", "scripts/replay.py", "scripts/resource_guide.py",
             "scripts/analysis/q8b_replacement_extension.py",
             f"results/runs/{SOURCE_RUN}/trajectories.jsonl",
             f"results/runs/{SOURCE_RUN}/hidden_labels.jsonl",
             f"results/runs/{SOURCE_RUN}/grade_meta.json",
             f"results/runs/{SOURCE_RUN}/run_meta.json",
             f"results/runs/{SOURCE_RUN}/jev_scores.jsonl",
             f"results/runs/{SOURCE_RUN}/jev_meta.json",
             f"results/runs/{SOURCE_RUN}/jev_ledger.jsonl"]
    return {name: file_sha256(ROOT / name) for name in names}


def _population():
    report: dict = {}
    cps = load_labelled(RESULTS / "runs" / SOURCE_RUN, report=report)
    attempts = R.build_attempts(cps)
    split, exclusion, tasks = load_split(), load_exclusions(), load_tasks()
    expected = {t for b in split["benchmarks"].values() for t in b["test"]} - set(exclusion["tasks"])
    actual = {a.task_id for a in attempts}
    if actual != expected or len(attempts) != 5 * len(expected):
        raise ValueError(f"source population mismatch: {len(actual)} tasks, {len(attempts)} attempts")
    for c in cps:
        task = tasks[c["task_id"]]
        if c["task_shown"] != shown_task(task) or c["visible_tests"] != [render_test(t) for t in task.visible_tests]:
            raise ValueError(f"visible evidence mismatch at {c['checkpoint_id']}")
        if c["benchmark"] != task.benchmark or c["split"] != "test":
            raise ValueError(f"task/split mismatch at {c['checkpoint_id']}")
    return cps, attempts, tasks, report


def _policy_masks(attempts: list[R.Attempt]) -> tuple[dict[str, list[str]], dict[str, list[str]], dict]:
    """Use only frozen scores and checkpoint IDs. Hidden outcomes never select a row."""
    rg = _module("resource_guide_q8b_replacement", ROOT / "scripts" / "resource_guide.py")
    replay = _module("replay_q8b_replacement", ROOT / "scripts" / "replay.py")
    cfg = json.loads((CONFIGS / "routers_q8b-v1.json").read_text())
    rows = {d["cp"]["checkpoint_id"]: d for d in rg.load([SOURCE_RUN], split="test", require_ok=False)}
    ids = [a.decision_id for a in attempts if not a.forced]
    if len(ids) != len(set(ids)) or set(ids) - set(rows):
        raise ValueError("decision IDs are missing or duplicated")
    names = {"cheap": "cheap", "fitted": "cheap+code+thinking", "strong4": "strong4 mean"}
    selected: dict[str, list[str]] = {}
    frozen_selected: dict[str, list[str]] = {}
    diagnostics = {}
    for short, name in names.items():
        router = cfg["routers"][name]
        raw = np.array([replay.score_final(rows[c], router) for c in ids], float)
        if not np.isfinite(raw).all():
            raise ValueError(f"{name}: missing/nonfinite score; fallback must be resolved before freeze")
        dd = router["dev_distribution"]
        ds, dw = np.array(dd["scores"]), np.array(dd["weights"])
        pct = np.array([R.dev_percentile(v, ds, dw) for v in raw])
        mask = R.top_k(pct, ids, RATE, secondary=raw)
        selected[short] = sorted(c for c, take in zip(ids, mask) if take)
        th = router["thresholds"][f"{RATE:.2f}"]
        frozen_selected[short] = sorted(c for c, value in zip(ids, raw)
                                        if R.escalate(value, th["t"], th["alpha"], c))
        diagnostics[short] = {"score_min": float(raw.min()), "score_max": float(raw.max()),
                              "score_ties": len(raw) - len(np.unique(raw)), "fallback_count": 0,
                              "router": name}
    # The direct comparator is the history-only code_likely_fails answer,
    # already collected for the source run. Higher means greater failure risk.
    direct = []
    for cid in ids:
        h = rows[cid]["history"]
        if h is None or h["applicability"]["code_likely_fails"] != "applicable":
            raise ValueError(f"direct Jev missing/inapplicable at {cid}")
        v = h["features"].get("code_likely_fails")
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            raise ValueError(f"direct Jev nonnumeric at {cid}")
        direct.append(float(v))
    raw = np.array(direct)
    mask = R.top_k(raw, ids, RATE)
    selected["direct_jev"] = sorted(c for c, take in zip(ids, mask) if take)
    diagnostics["direct_jev"] = {"score_min": float(raw.min()), "score_max": float(raw.max()),
                                  "score_ties": len(raw) - len(np.unique(raw)), "fallback_count": 0,
                                  "arm": P.HISTORY_ARM, "question": "code_likely_fails"}
    n = math.floor(RATE * len(ids) + 0.5)
    if any(len(v) != n for v in selected.values()):
        raise ValueError("optional escalation counts differ")
    return selected, frozen_selected, diagnostics


def freeze() -> dict:
    if MANIFEST.exists():
        raise SystemExit(f"STOP: {MANIFEST} already exists; never overwrite a freeze")
    cps, attempts, tasks, report = _population()
    selected, frozen_selected, diagnostics = _policy_masks(attempts)
    task_ids = sorted({a.task_id for a in attempts})
    prompts = {t: _sha_json(first_round_messages(tasks[t])) for t in task_ids}
    payload = {
        "version": "q8b-replacement-extension-v1", "status": "exploratory_after_test_inspection",
        "source_run": SOURCE_RUN, "frontier_run": FRONTIER_RUN,
        "task_ids": task_ids, "task_prompt_sha256": prompts,
        "frontier": {"mode": "task_only_takeover_from_scratch", "samples_per_task": 2,
                     "model": "anthropic/claude-sonnet-5.5-20260928", "provider": "anthropic_pinned_no_fallback",
                     "reasoning_effort": "low", "max_tokens": 8000,
                     "no_content_retry": True, "request_count": 2 * len(task_ids)},
        "policies": {"primary": "exact_top_k_optional_25_percent", "optional_budget": RATE,
                     "optional_count": len(next(iter(selected.values()))), "forced_rule": "terminal_visible_fail",
                     "forced_count": sum(a.forced for a in attempts),
                     "selected_checkpoint_ids": selected, "tie_tag": R.TIE_TAG,
                     "frozen_threshold_selected_checkpoint_ids": frozen_selected,
                     "random_policy": "closed_form_expected_25_percent_as_in_eval.replay.random_expected",
                     "score_diagnostics": diagnostics,
                     "anchors": ["always-small", "always-frontier"],
                     "deployment_sensitivity": "existing frozen 0.25 thresholds; realized counts reported separately"},
        "analysis": {"unit": "saved_attempt", "n_attempts": len(attempts),
                     "n_distinct_tasks": len(task_ids), "n_decisions": sum(not a.forced for a in attempts),
                     "frontier_outcome": "mean_of_two_matching_samples_per_task_reused_across_policies",
                     "primary_contrast": "fitted_minus_cheap_final_pass_at_equal_optional_count",
                     "other_comparisons": "descriptive", "bootstrap": "5000_task_clusters_stratified_by_benchmark",
                     "bootstrap_seed": BOOT_SEED, "n_boot": N_BOOT,
                     "cost_model": {"azure_usd_per_hour": AZURE_USD_PER_HOUR,
                                    "azure_app_hours": AZURE_APP_HOURS,
                                    "jev_usd_per_m_input": JEV_USD_PER_M_INPUT,
                                    "frontier_cost": "recorded_ledger_mean_across_samples"}},
        "source_hashes": _sources(), "source_grade_session": report["grade_session"],
        "source_excluded_checkpoints": report["excluded_checkpoints"],
        "source_code_hash_rule": "sha256_utf8_code_checked_by_load_labelled",
        "source_visible_evidence_checkpoints": len(cps),
    }
    MANIFEST.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def verify_manifest() -> dict:
    manifest = json.loads(MANIFEST.read_text())
    if manifest["source_hashes"] != _sources():
        raise ValueError("source artifact/code hashes differ from the freeze")
    cps, attempts, tasks, report = _population()
    if report["grade_session"] != manifest["source_grade_session"]:
        raise ValueError("grading session changed")
    if sorted({a.task_id for a in attempts}) != manifest["task_ids"]:
        raise ValueError("task set changed")
    if {t: _sha_json(first_round_messages(tasks[t])) for t in manifest["task_ids"]} != manifest["task_prompt_sha256"]:
        raise ValueError("frontier prompt hashes changed")
    selected, frozen_selected, _ = _policy_masks(attempts)
    if selected != manifest["policies"]["selected_checkpoint_ids"]:
        raise ValueError("policy decisions changed")
    if frozen_selected != manifest["policies"]["frozen_threshold_selected_checkpoint_ids"]:
        raise ValueError("frozen-threshold decisions changed")
    return manifest


def _frontier_data(run_id: str, manifest: dict):
    replay = _module("replay_q8b_replacement_outcomes", ROOT / "scripts" / "replay.py")
    d = RESULTS / "runs" / run_id
    run_meta = json.loads((d / "run_meta.json").read_text())
    proto = run_meta["protocol"]
    frozen = manifest["frontier"]
    if (run_meta["split"] != "test" or proto["mode"] != "takeover_from_scratch" or
            proto["model"] != frozen["model"] or proto["reasoning"] != {"effort": frozen["reasoning_effort"]} or
            proto["max_tokens"] != frozen["max_tokens"] or proto.get("frozen_manifest_sha256") != file_sha256(MANIFEST) or
            not proto.get("strict_spend")):
        raise ValueError("frontier run metadata differs from frozen protocol")
    source_grade = json.loads((RESULTS / "runs" / SOURCE_RUN / "grade_meta.json").read_text())
    frontier_grade = json.loads((d / "frontier_grade_meta.json").read_text())
    for key in ("grading_code_sha256", "evalplus_cache_sha256", "grader_version", "grader_settings", "container"):
        if frontier_grade.get(key) != source_grade.get(key):
            raise ValueError(f"frontier and Qwen grading differ on {key}")
    answers = [json.loads(line) for line in (d / "frontier_answers.jsonl").read_text().splitlines()]
    if len(answers) != manifest["frontier"]["request_count"]:
        raise ValueError("frontier answer count differs from freeze")
    seen = set()
    for a in answers:
        pair = (a["task_id"], a["sample"])
        if pair in seen or a["sample"] not in (0, 1) or a["task_id"] not in manifest["task_ids"]:
            raise ValueError(f"extra/duplicate frontier answer: {pair}")
        seen.add(pair)
        if a["prompt_sha256"] != hashlib.sha256(json.dumps(first_round_messages(load_tasks()[a["task_id"]])).encode()).hexdigest():
            raise ValueError(f"frontier prompt mismatch: {pair}")
    if seen != {(t, s) for t in manifest["task_ids"] for s in (0, 1)}:
        raise ValueError("frontier task/sample grid incomplete")
    z, dollars, info = replay.frontier_outcomes(run_id)
    if set(z) != set(manifest["task_ids"]) or info["replicates"] != 2 or info["calls_with_unknown_cost"]:
        raise ValueError("frontier labels/costs incomplete or unmatched")
    return z, dollars, info


def analyze(run_id: str) -> Path:
    manifest = verify_manifest()
    if run_id != manifest["frontier_run"]:
        raise ValueError("wrong frontier run ID")
    z, dollars, info = _frontier_data(run_id, manifest)
    cps, attempts, _, _ = _population()
    trajectories = [json.loads(line) for line in (RESULTS / "runs" / SOURCE_RUN / "trajectories.jsonl").read_text().splitlines()]
    all_cps = complete_executions(trajectories)
    total_tokens = sum(c["generation"]["thinking_tokens"] + c["generation"]["answer_tokens"] for c in all_cps)
    if total_tokens <= 0:
        raise ValueError("no Qwen token allocation denominator")
    # App lifetime and rate are a frozen model. It includes startup and the
    # excluded task's original share; excluded work is not shifted onto kept attempts.
    qwen_cost = np.array([a.gen_tokens / total_tokens * AZURE_APP_HOURS * AZURE_USD_PER_HOUR for a in attempts])
    replay = _module("replay_q8b_replacement_cost", ROOT / "scripts" / "replay.py")
    jev_tokens = replay.jev_tokens([SOURCE_RUN])
    frontier_costs = R.frontier_matrix(attempts, dollars)
    forced = np.array([a.forced for a in attempts])
    y = np.array([a.y for a in attempts])
    zbar = R.frontier_matrix(attempts, z).mean(axis=0)
    ids = [a.decision_id for a in attempts]
    decisions = np.flatnonzero(~forced)
    n = len(attempts)

    def judge_cost(name: str) -> np.ndarray:
        arms = {"cheap": [], "fitted": [P.HISTORY_ARM, P.TRACE_ARM],
                "direct_jev": [P.HISTORY_ARM], "strong4": [P.HISTORY_ARM, P.TRACE_ARM],
                "random": []}[name]
        out = np.zeros(n)
        for i in decisions:
            vals = [jev_tokens.get((ids[i], arm)) for arm in arms]
            if any(v is None for v in vals):
                raise ValueError(f"unknown Jev usage: {name} {ids[i]}")
            out[i] = sum(vals) * JEV_USD_PER_M_INPUT / 1e6
        return out

    selected = manifest["policies"]["selected_checkpoint_ids"]
    frozen_selected = manifest["policies"]["frozen_threshold_selected_checkpoint_ids"]
    results = {}
    for name in ("cheap", "fitted", "direct_jev", "strong4", "random", "always-small", "always-frontier"):
        chosen = set(selected.get(name, []))
        opt = np.array([cid in chosen if cid is not None else False for cid in ids])
        if name == "always-frontier":
            res = R.always_frontier(attempts, z)
        elif name == "random":
            res = R.random_expected(attempts, z, RATE)
        else:
            res = R.outcome(attempts, z, opt, name, forced_to_frontier=name != "always-small")
        summary = R.summarize(res, attempts, z)
        summary["policy"] = name
        small = np.zeros(n) if name == "always-frontier" else qwen_cost
        judge = np.zeros(n) if name in ("always-small", "always-frontier") else judge_cost(name)
        front = R.frontier_cost(res, frontier_costs)
        all_rescues = float(((1 - y) * res.escalated * zbar).sum())
        all_harms = float((y * res.escalated * (1 - zbar)).sum())
        summary.update({"optional_count": RATE * len(decisions) if name == "random" else int(opt.sum()),
                        "forced_count": 0 if name == "always-frontier" else int((res.escalated * forced).mean() * n),
                        "frontier_calls_per_1620_attempts": float(res.escalated_by_replicate.sum(axis=1).mean()),
                        "modeled_qwen_usd_total": float(small.sum()), "modeled_jev_usd_total": float(judge.sum()),
                        "recorded_frontier_usd_if_deployed": float(front.sum()),
                        "modeled_deployment_usd_total": float((small + judge + front).sum()),
                        "rescue_count": all_rescues, "harm_count": all_harms,
                        "rescues_per_attempt": all_rescues / n, "harms_per_attempt": all_harms / n,
                        "escalated_already_correct_count": float((y * res.escalated).sum()),
                        "escalated_unrescued_count": float(((1 - y) * res.escalated * (1 - zbar)).sum())})
        results[name] = (res, summary)
    cheap = results["cheap"][0]
    comparisons = []
    for name in ("fitted", "direct_jev", "strong4", "random", "always-small", "always-frontier"):
        res = results[name][0]
        point, lo, hi = R.task_bootstrap_gain(attempts, res.final, cheap.final, N_BOOT, BOOT_SEED)
        comparisons.append({"policy": name, "vs": "cheap", "pass_difference": point, "ci_low": lo, "ci_high": hi,
                            "bootstrap_tasks": len({a.task_id for a in attempts})})
    # The equal-budget identity is computed directly on discordant optional decisions.
    gains = zbar - y
    disagreement = []
    for name in ("fitted", "direct_jev", "strong4"):
        s = set(selected[name]); c = set(selected["cheap"])
        a_idx = [i for i in decisions if ids[i] in s - c]
        b_idx = [i for i in decisions if ids[i] in c - s]
        discrepancy = (gains[a_idx].sum() - gains[b_idx].sum()) / n
        delta = results[name][0].final.mean() - cheap.final.mean()
        if abs(discrepancy - delta) > 1e-12:
            raise ValueError(f"discordant-gain identity failed for {name}")
        disagreement.append({"policy": name, "jev_only_count": len(a_idx), "cheap_only_count": len(b_idx),
                             "sum_gain_policy_only": float(gains[a_idx].sum()),
                             "sum_gain_cheap_only": float(gains[b_idx].sum()),
                             "pass_difference": float(discrepancy)})
    threshold_sensitivity = []
    for name in ("cheap", "fitted", "strong4"):
        fixed = set(frozen_selected[name])
        mask = np.array([cid in fixed if cid is not None else False for cid in ids])
        res = R.outcome(attempts, z, mask, name + "_frozen_threshold")
        judge = judge_cost(name)
        front = R.frontier_cost(res, frontier_costs)
        threshold_sensitivity.append({"policy": name, "optional_count": int(mask.sum()),
                                      "optional_rate": float(mask.sum() / len(decisions)),
                                      "forced_count": int(forced.sum()), "pass": float(res.final.mean()),
                                      "frontier_call_rate": float(res.escalated.mean()),
                                      "modeled_deployment_usd_total": float((qwen_cost + judge + front).sum())})
    OUT.mkdir(parents=True, exist_ok=True)
    payload = {"version": manifest["version"], "frontier_run": run_id, "frontier_info": info,
               "manifest_sha256": file_sha256(MANIFEST), "n_attempts": n,
               "n_tasks": len({a.task_id for a in attempts}), "n_forced": int(forced.sum()),
               "source_grade_session": manifest["source_grade_session"],
               "frontier_recorded_collection_usd": float(sum(v.sum() for v in dollars.values())),
               "policies": [summary for _, summary in results.values()], "comparisons": comparisons,
               "frozen_threshold_sensitivity": threshold_sensitivity,
               "discordant_optional": disagreement,
               "cost_limitations": ["Qwen Azure price and app lifetime are modeled from the prior report, not an invoice.",
                                    "Visible-test host CPU time was not separately recorded or priced.",
                                    "Jev is modeled at a public rate; direct account charges are unconfirmed.",
                                    "Frontier deployment cost uses mean recorded cost of two samples, not both calls per escalation."]}
    output = OUT / "analysis.json"
    output.write_text(json.dumps(payload, indent=2) + "\n")
    with (OUT / "policy_table.csv").open("w", newline="") as f:
        rows = payload["policies"]
        w = csv.DictWriter(f, fieldnames=[k for k in rows[0] if k != "pass_by_replicate"])
        w.writeheader(); w.writerows({k: v for k, v in row.items() if k != "pass_by_replicate"} for row in rows)
    with (OUT / "paired_comparisons.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(comparisons[0])); w.writeheader(); w.writerows(comparisons)
    with (OUT / "discordant_optional.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(disagreement[0])); w.writeheader(); w.writerows(disagreement)
    with (OUT / "frozen_threshold_sensitivity.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(threshold_sensitivity[0])); w.writeheader(); w.writerows(threshold_sensitivity)
    by_name = {r["policy"]: r for r in payload["policies"]}
    ci = {r["policy"]: r for r in comparisons}
    lines = ["# Qwen3-8B task-only replacement: exploratory extension", "",
             "This replays the 324 already inspected test tasks. It is an exploratory extension, not independent confirmation.",
             f"The same two frontier samples per task were reused across all policies. Source grade session: `{manifest['source_grade_session']}`.",
             "", "| Policy | Final pass | vs cheap, task-bootstrap 95% CI | Optional/forced calls | Total call rate | Modeled deployment $/1,620 |",
             "| --- | ---: | ---: | ---: | ---: | ---: |"]
    for name in ("always-small", "random", "cheap", "fitted", "direct_jev", "strong4", "always-frontier"):
        r = by_name[name]
        delta = "reference" if name == "cheap" else (f"{100*ci[name]['pass_difference']:+.2f} pp "
                 f"[{100*ci[name]['ci_low']:+.2f}, {100*ci[name]['ci_high']:+.2f}]")
        lines.append(f"| {name} | {100*r['pass']:.2f}% | {delta} | {r['optional_count']}/{r['forced_count']} | "
                     f"{100*r['q_total']:.2f}% | ${r['modeled_deployment_usd_total']:.2f} |")
    lines += ["", "Rescues, harms, already-correct escalations, unrescued escalations, and recorded collection charges are in `analysis.json` and `policy_table.csv`.",
              "", "## Accounting and limits", "",
              f"- Recorded frontier collection cost for all 648 research requests: ${payload['frontier_recorded_collection_usd']:.4f}. This is separate from a deployed policy's one-call-per-escalation estimate.",
              f"- The modeled Qwen cost allocates {AZURE_APP_HOURS:.2f} hours at ${AZURE_USD_PER_HOUR:.4f}/hour by generated tokens, retaining the excluded task's original share in the denominator.",
              "- Jev is charged only to policies that call it. Direct Jev uses the history-only `code_likely_fails` question; strong4 and fitted use both saved Jev arms.",
              "- The saved visible-test execution ran during the Qwen app lifetime. Its separate host CPU seconds and price were not recorded, so the deployment-dollar totals omit that CPU component. Frontier grading is an offline research cost, not a deployment inference cost.",
              "- Repeated attempts from each task stay together in the paired, benchmark-stratified bootstrap. The interval is conditional on these frozen policy selections and two frontier samples.",
              "- The original HumanEval/32 exclusion remains. EvalPlus base-plus comparison and its type/runtime behavior are unchanged; a failing label can reflect a type/comparison issue or ambiguous prompt, and is not automatically a clear requirement violation.",
              "- No selection, threshold, router fitting, or sample count was changed after frontier outcomes. The optional 25% result is a top-k batch comparison; frozen thresholds have a separately measured realized rate.",
              ""]
    (OUT / "paper_table.md").write_text("\n".join(lines))
    names = ("always-small", "random", "cheap", "fitted", "direct_jev", "strong4", "always-frontier")
    colors = ("#555555", "#999999", "#0072b2", "#d55e00", "#009e73", "#cc79a7", "#000000")
    points = [(name, by_name[name]["modeled_deployment_usd_total"] / n, by_name[name]["pass"])
              for name in names]
    minx, maxx = min(x for _, x, _ in points), max(x for _, x, _ in points)
    miny, maxy = min(y for _, _, y in points), max(y for _, _, y in points)
    padx = max((maxx - minx) * .08, .001); pady = max((maxy - miny) * .15, .01)
    x0, x1 = minx - padx, maxx + padx
    y0, y1 = max(0, miny - pady), min(1, maxy + pady)
    def px(x): return 80 + (x - x0) / (x1 - x0) * 620
    def py(y): return 430 - (y - y0) / (y1 - y0) * 350
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="550" viewBox="0 0 1000 550">',
           '<rect width="1000" height="550" fill="white"/>',
           '<text x="80" y="30" font-family="sans-serif" font-size="19">Qwen3-8B task-only replacement replay</text>',
           '<text x="80" y="50" font-family="sans-serif" font-size="12" fill="#555">Exploratory extension; 324 tasks, two frontier samples per task</text>',
           '<path d="M80 80V430H700" fill="none" stroke="#444" stroke-width="2"/>',
           '<text x="260" y="500" font-family="sans-serif" font-size="14">Modeled deployment cost (USD per attempt)</text>',
           '<text x="10" y="70" font-family="sans-serif" font-size="14">Final pass rate</text>']
    for j in range(5):
        xv = x0 + (x1 - x0) * j / 4
        yv = y0 + (y1 - y0) * j / 4
        svg += [f'<path d="M{px(xv):.1f} 430v5" stroke="#444"/>',
                f'<text x="{px(xv):.1f}" y="451" text-anchor="middle" font-family="sans-serif" font-size="11">${xv:.3f}</text>',
                f'<path d="M75 {py(yv):.1f}h5" stroke="#444"/>',
                f'<text x="68" y="{py(yv)+4:.1f}" text-anchor="end" font-family="sans-serif" font-size="11">{100*yv:.0f}%</text>']
    for i, (name, x, y) in enumerate(points):
        svg += [f'<circle cx="{px(x):.1f}" cy="{py(y):.1f}" r="6" fill="{colors[i]}" stroke="white" stroke-width="1"/>',
                f'<circle cx="745" cy="{110+i*37}" r="6" fill="{colors[i]}"/>',
                f'<text x="760" y="{114+i*37}" font-family="sans-serif" font-size="13">{escape(name)} ({100*y:.1f}%)</text>']
    svg.append('<text x="80" y="530" font-family="sans-serif" font-size="11" fill="#555">Costs use modeled Qwen Azure time, policy-specific Jev, and mean recorded frontier call cost. Separate host CPU cost unavailable.</text>')
    svg.append('</svg>')
    (OUT / "pass_vs_cost.svg").write_text("\n".join(svg))
    return output


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("freeze", "verify", "analyze"))
    ap.add_argument("--frontier-run", default=FRONTIER_RUN)
    args = ap.parse_args()
    if args.action == "freeze":
        m = freeze()
        print(f"froze {len(m['task_ids'])} tasks, {m['frontier']['request_count']} frontier requests, "
              f"{m['policies']['optional_count']} optional and {m['policies']['forced_count']} forced calls per policy: {MANIFEST}")
    elif args.action == "verify":
        m = verify_manifest()
        print(f"verified {m['version']}: {len(m['task_ids'])} tasks; manifest SHA256 {file_sha256(MANIFEST)}")
    else:
        print(analyze(args.frontier_run))


if __name__ == "__main__":
    main()
