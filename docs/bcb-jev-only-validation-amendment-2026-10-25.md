# BigCodeBench Jev-only validation: visible-reference amendment

**Dated October 25, 2026, after `bcb-jev-only-freeze-v1` and before any v2 task generation.**
The original [frozen plan](bcb-jev-only-validation-plan.md) and manifest remain
in git unchanged. This amendment documents a new protocol and run ID.

## Why the v1 run stopped

The v1 run `bcb-jev-only-test-v1` was voluntarily stopped after generating
14 checkpoints, all on `BigCodeBench/1`. No BigCodeBench hidden test ran, no
hidden label was produced, and no Jev call was made. The Azure resource group
was submitted for deletion. The incomplete run stays in ignored `results/`.

The fixed EvalPlus visible-example parser loses setup statements in some
BigCodeBench docstrings. For example, a random seed shown before a function
call is not executed as part of that call's visible test. To measure the
scope, `scripts/prepare_bcb_validation_v2.py` ran **public reference code**
against the frozen visible examples in disposable networkless containers.
Only 45 of 75 tasks passed every visible example with their own reference
solution; 30 did not. This check used no hidden test, candidate grade, Jev
answer, or model output. Its per-task status audit is ignored at
`results/bcb_jev_only_reference_visible_v2.json`.

## Corrected v2 protocol

The eligible test set is the **45 tasks** in
`configs/bcb_jev_only_tasks_v2.json`: a task must meet the v1 public-metadata
selector and its public canonical solution must pass all its frozen visible
examples in the local sandbox. `BigCodeBench/1` is outside this set; no v2
task had been generated in the stopped v1 run. Freeze this amendment, new
manifest, and updated scripts under `bcb-jev-only-freeze-v2` before any v2
generation. Use the fresh run ID `bcb-jev-only-test-v2`; never resume or
analyze the v1 run. Five attempt indices per task make **225 attempts**.

Everything else in the v1 plan stays the v2 rule: Qwen3-8B revision and vLLM
settings, networkless visible and hidden execution, post-generation hidden
grading and reference calibration, both Jev arms, the frozen strong4 mean and
cheap router, one two-sided paired task-bootstrap AUROC comparison with
19,999 draws, and descriptive frozen thresholds. No model, feature, score
weight, or threshold changes. Any hidden calibration failure or invalid
grade stops the test. The smaller task count may give an imprecise estimate.

The earlier spending approval remains a **combined ceiling** for this one
validation: $40 Azure and $1 Jev including the aborted v1 deployment. The
v2 GPU group has its own deletion watchdog, no more than one replica, and a
shorter 9-hour deadline so the combined retail estimate stays below the
approved ceiling. The Jev v2 run keeps a 12-million-input-token guard.
Stop and report if the observed pace threatens the approved ceiling; do not
restart a system-stopped job without a new operator instruction. No push or
publication is authorized by this amendment.
