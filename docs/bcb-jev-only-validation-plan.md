# Fresh BigCodeBench validation of the Jev-only router

**Protocol dated October 25, 2026.** This is a new study on branch
`bcb-jev-only-validation-20261025`. The finished EvalPlus studies, their
routers, their result files, and their tags remain unchanged.

## Question and frozen decision rule

Does the equal-weight Jev **strong4 mean** rank hidden failures among
visible-pass Qwen3-8B checkpoints better than the frozen cheap router on new
Python function tasks? The four failure-oriented answers are
`code_likely_fails` and `special_cases_visible_tests` from the history arm,
plus `on_task` and `unsupported_claim` from the trace arm. The rule and its
10%, 25%, and 50% escalation thresholds are exactly those in the existing
`configs/routers_q8b-v1.json`, fitted from the old 8B development data.
No reweighting, threshold change, model choice, or feature selection is
allowed using the new test labels.

The single primary contrast is pooled checkpoint AUROC(strong4 mean) minus
AUROC(cheap), two-sided paired bootstrap by whole task, 19,999 draws, alpha
0.05. The point difference, two-sided p-value and percentile 95% interval
will be reported. The frozen cheap+code+thinking router, task-weighted AUROC,
AUPRC, and realized operating points at the existing thresholds are
descriptive. If the visible-pass population has only one hidden class, the
AUROC test is undefined and no substitute metric becomes primary. There is
no frontier takeover in this validation.

## New tasks and generator

The source is [BigCodeBench v0.1.4](https://huggingface.co/datasets/bigcode/bigcodebench),
repository revision `b74c0d0bf70d2c0bc459be537895cca163007f1a`, parquet
SHA-256 `d9a4965821c9507ebdfb551c288656b2d5fe553234f5183044333ca8a4018267`.
The fixed selector in `scripts/prepare_bcb_validation.py` uses only public
prompt metadata: declared imports must be in the Python standard library
and outside its explicit environment-sensitive exclusion list; the Complete
prompt must yield at least one literal, runnable `task_func` docstring example
under the existing visible-test parser. This gives the **75 task IDs** and
105 visible examples frozen in `configs/bcb_jev_only_tasks_v1.json`. No
BigCodeBench hidden case or candidate outcome selected a task. These tasks
are separate from the HumanEval+/MBPP+ tasks used in both earlier studies.

Use the same pinned Qwen3-8B revision, vLLM image, generation settings,
thinking cap, three-round write/test/revise loop, and disposable networkless
visible sandbox as the prior 8B run. Run five attempts, indices 0–4, on each
of the 75 tasks: 375 attempts total. Use one new run ID:
`bcb-jev-only-test-v1`. The manifest SHA-256, sandbox image ID, remote vLLM
identity, and git commit enter `run_meta.json`. A clean tree and the
`bcb-jev-only-freeze-v1` ancestor tag are required before test generation.
Do not commit between sessions of the run. Do not resume a system-stopped job
without a new operator instruction.

The BigCodeBench hidden tests are public benchmark material, so this checks
transfer to new tasks, not resistance to possible model training exposure.
Its task mix and visible examples also differ from EvalPlus; any change in
absolute AUROC cannot be attributed to the router alone.

## Grading and Jev separation

Only **after generation is complete and vLLM is stopped**, extract the pinned
hidden cases to ignored `results/datasets/bcb_jev_only_hidden_v1.json`.
Mount that file read-only in the dedicated networkless `bcb-sandbox` service.
The candidate code and reference code execute only there, with no network,
read-only root, `/tmp`, memory/process limits, and a per-grade time limit.
The reference must pass each hidden suite before any candidate grade. A failed
reference calibration stops the study and is reported; tasks are not silently
dropped. Grade each distinct candidate code twice, with a third vote only
when needed, using the existing majority rule. Any invalid grade stops the
primary analysis. Checkpoints without code are hidden failures.

Score all complete checkpoints with `scripts/score_jev.py` after grading,
using both existing evidence arms, the same rubric, 56,000-byte budget, and
one Jev model version across the run. The scorer reads trajectories only; it
never receives labels, hidden cases, or reference answers. Stop on a version
change or missing arm in any visible-pass checkpoint. Its input token guard
will be 12,000,000 for this new run. No Pinocchio or frontier calls are needed.

## Spend gate and execution

No Azure or Jev call occurs before a new operator approval with dollar limits.
The same Azure consumption A100 deployment will have at most one replica, a
resource group containing only this run, a separately running deletion
watchdog started before deployment, and a UTC deadline. The resource group
will be deleted and its absence verified after generation. A deadline and
Jev token guard are operational controls, not guaranteed invoice ceilings.

The previous 1,625-attempt 8B run used 9.52 hours of app lifetime. Scaling
to 375 attempts gives 2.20 hours; harder tasks and extra repair rounds could
make it 3–5 hours. At the West US 3 retail meter of about $3.20 per active
hour for one A100 replica with 8 vCPUs and 56 GiB, expected Azure spend is
roughly **$7–$16**. The proposed Azure approval limit is **$40**, with a
10-hour watchdog and headroom for setup and deletion. The previous Jev run
used 8.13 million input tokens for 1,751 checkpoints, about 4,642 per
checkpoint; roughly 400–750 new checkpoints would use 1.9–3.5 million
tokens or **$0.08–$0.15** at $0.042 per million. The proposed Jev approval
limit is **$1**, with the 12 million input-token guard (about $0.50 at that
rate, plus the final call's possible overrun). Actual account charges may
differ from these retail estimates.

Freeze this plan, the manifest, and analysis code in one commit and tag
before any generation. After spend approval, execute generation, local hidden
grading, Jev scoring, and `scripts/analyze_bcb_jev_only.py`. Keep run data in
ignored `results/`. Report result and cost. Do not push or publish results
unless separately asked.
