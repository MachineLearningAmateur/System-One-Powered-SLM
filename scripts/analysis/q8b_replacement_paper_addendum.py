"""Post-collection formatting of the frozen q8b replacement replay.

Run from the extension worktree:
  PYTHONPATH=src python scripts/analysis/q8b_replacement_paper_addendum.py

This computes the requested paired comparisons against always-small and
always-frontier. It does not change scores, selections, labels, or samples.
"""

from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from system1.config import RESULTS, ROOT
from system1.eval import replay as R
from system1.eval.labels import load_labelled

HERE = RESULTS / "q8b-replacement-extension-v1"
RUN = "q8b-frontier-replacement-v1"
SOURCE = "q8b-test-v1"
N_BOOT = 5000
SEED = 20261027


def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def main() -> None:
    frozen = json.loads((ROOT / "configs/q8b_replacement_extension_v1.json").read_text())
    prior = json.loads((HERE / "analysis.json").read_text())
    assert prior["manifest_sha256"] == __import__("hashlib").sha256(
        (ROOT / "configs/q8b_replacement_extension_v1.json").read_bytes()).hexdigest()
    replay = module("replay_for_paper_addendum", ROOT / "scripts/replay.py")
    z, _, info = replay.frontier_outcomes(RUN)
    assert set(z) == set(frozen["task_ids"]) and info["replicates"] == 2
    attempts = R.build_attempts(load_labelled(RESULTS / "runs" / SOURCE))
    ids = [a.decision_id for a in attempts]
    selected = frozen["policies"]["selected_checkpoint_ids"]
    results = {}
    for name in ("cheap", "fitted", "direct_jev", "strong4"):
        take = set(selected[name])
        mask = np.array([cid in take if cid is not None else False for cid in ids])
        results[name] = R.outcome(attempts, z, mask, name)
    results["random"] = R.random_expected(attempts, z, 0.25)
    zero = np.zeros(len(attempts), bool)
    results["always-small"] = R.outcome(attempts, z, zero, "always-small", forced_to_frontier=False)
    results["always-frontier"] = R.always_frontier(attempts, z)
    prior_by = {x["policy"]: x for x in prior["policies"]}
    names = ("always-small", "random", "cheap", "fitted", "direct_jev", "strong4", "always-frontier")
    rows = []
    for name in names:
        res = results[name]
        assert abs(float(res.final.mean()) - prior_by[name]["pass"]) < 1e-12
        row = {"policy": name, "pass": float(res.final.mean())}
        for baseline in ("always-small", "cheap", "always-frontier"):
            point, low, high = R.task_bootstrap_gain(
                attempts, res.final, results[baseline].final, N_BOOT, SEED)
            row.update({f"delta_vs_{baseline}": point, f"ci_low_vs_{baseline}": low,
                        f"ci_high_vs_{baseline}": high})
        _, low, high = R.task_bootstrap_gain(attempts, res.final, np.zeros(len(attempts)), N_BOOT, SEED)
        row.update({"pass_ci_low": low, "pass_ci_high": high})
        rows.append(row)
    with (HERE / "paired_all_baselines.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n"); w.writeheader(); w.writerows(rows)

    lookup = {r["policy"]: r for r in rows}
    pp = lambda x: f"{100*x:+.2f}"
    lines = ["# Qwen3-8B task-only replacement: full-system table", "",
             "Exploratory extension of the previously inspected 324-task evaluation set. Two task-only frontier samples per task; each sample is reused across five saved attempts and all policies. No best-of-two selection.",
             "", "| Policy | Final pass (95% task CI) | Δ vs always-small (95% paired CI), pp | Δ vs cheap (95% paired CI), pp | Δ vs always-frontier (95% paired CI), pp | Frontier calls / 1,620 | Rescues | Harms | Failed rescues | Modeled full-system cost |",
             "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"]
    for name in names:
        r, cost = lookup[name], prior_by[name]
        def diff(base):
            return f"{pp(r[f'delta_vs_{base}'])} [{pp(r[f'ci_low_vs_{base}'])}, {pp(r[f'ci_high_vs_{base}'])}]"
        calls = cost["frontier_calls_per_1620_attempts"]
        lines.append(f"| {name} | {100*r['pass']:.2f}% [{100*r['pass_ci_low']:.2f}, {100*r['pass_ci_high']:.2f}] | "
                     f"{diff('always-small')} | {diff('cheap')} | {diff('always-frontier')} | "
                     f"{calls:.0f}{' expected' if name == 'random' else ''} ({100*cost['q_total']:.2f}%) | "
                     f"{cost['rescue_count']:.1f} | {cost['harm_count']:.1f} | "
                     f"{cost['escalated_unrescued_count']:.1f} | ${cost['modeled_deployment_usd_total']:.2f} |")
    lines += ["", "The 25% optional budget is exactly 395 calls for each router and 395 calls in expectation for random; each cascade also makes the same 40 forced calls. Always-small makes zero calls. Always-frontier makes 1,620 calls and incurs no Qwen or Jev inference.",
              "", "Rescues, harms, and failed rescues are expected counts across 1,620 attempts, averaging the two frontier samples. A rescue is a saved Qwen failure replaced by a frontier pass; harm is a saved Qwen pass replaced by a frontier failure. An incorrect answer escalated to another incorrect answer is a failed rescue. Counts can be half-integers because of the two-sample average.",
              "", f"The 648-call research collection cost **${prior['frontier_recorded_collection_usd']:.6f} recorded** (648 successful HTTP attempts, zero retries). This charge is separate from each policy's modeled one-call-per-escalation deployment cost. The old Qwen Azure app is modeled at 9.52 hours × $3.2004/hour; its eligible-task share is $30.20, with the excluded task's share left out. Jev is added only for policies that call it, at $0.042/M saved input tokens. The table includes the prior Qwen work for every cascade policy and always-small. Direct Jev uses one history arm; fitted and strong4 use two arms.",
              "", "The local CPU cost of visible-test execution was not separately recorded or priced. The frontier answer is graded only for research; hidden grading is not charged to a deployment policy. The original EvalPlus base-plus labels, HumanEval/32 exclusion, grader code, dataset cache and sandbox image were retained. A benchmark failure may arise from comparison/type semantics, timeouts or ambiguous task wording; no original label was changed.",
              "", "The intervals resample whole tasks within benchmark and keep all five attempts and both frontier samples together. They are conditional on this already-inspected task set, the frozen selections, and two sampled frontier responses. They do not establish independent confirmation or a live online effect.",
              "", "The frozen threshold sensitivity appears in `frozen_threshold_sensitivity.csv`; its realized optional rates differ from the exact 25% batch comparison. Source data and charges remain in ignored `results/runs/`; this addendum does not modify them.", ""]
    (HERE / "paper_full_system.md").write_text("\n".join(lines))

    plt.rcParams.update({"font.size": 10, "font.family": "DejaVu Sans", "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.6), layout="constrained", sharey=True)
    colors = {"always-small": "#555555", "random": "#999999", "cheap": "#0072B2",
              "fitted": "#D55E00", "direct_jev": "#009E73", "strong4": "#CC79A7",
              "always-frontier": "#000000"}
    for ax, subset in ((axes[0], names), (axes[1], names[:-1])):
        for name in subset:
            r, cost = lookup[name], prior_by[name]
            x = cost["modeled_deployment_usd_total"] / 1620
            y = 100 * r["pass"]
            yerr = [[100 * (r["pass"] - r["pass_ci_low"])],
                    [100 * (r["pass_ci_high"] - r["pass"])]]
            ax.errorbar([x], [y], yerr=yerr, fmt="o", markersize=6, capsize=3,
                        color=colors[name], label=name.replace("_", " "), linewidth=1.3)
        ax.set_xlabel("Modeled USD per attempt")
        ax.grid(alpha=.2)
    axes[0].set_ylabel("Final pass rate (%)")
    axes[0].set_title("Full cost range")
    axes[1].set_title("Cascade detail")
    cascade_x = [prior_by[name]["modeled_deployment_usd_total"] / 1620 for name in names[:-1]]
    axes[1].set_xlim(min(cascade_x) - .00015, max(cascade_x) + .00015)
    axes[1].tick_params(axis="x", labelrotation=30)
    axes[1].legend(frameon=False, fontsize=8, loc="upper left", ncol=2)
    fig.suptitle("Qwen3-8B task-only replacement (exploratory; 324 tasks)", fontsize=13)
    fig.savefig(HERE / "pass_vs_cost_paper.svg", dpi=300, bbox_inches="tight")
    fig.savefig(HERE / "pass_vs_cost_paper.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    svg = HERE / "pass_vs_cost_paper.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text().splitlines()) + "\n")
    print(HERE / "paper_full_system.md")


if __name__ == "__main__":
    main()
