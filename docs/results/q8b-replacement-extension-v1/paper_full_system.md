# Qwen3-8B task-only replacement: full-system table

Exploratory extension of the previously inspected 324-task evaluation set. Two task-only frontier samples per task; each sample is reused across five saved attempts and all policies. No best-of-two selection.

| Policy | Final pass (95% task CI) | Δ vs always-small (95% paired CI), pp | Δ vs cheap (95% paired CI), pp | Δ vs always-frontier (95% paired CI), pp | Frontier calls / 1,620 | Rescues | Harms | Failed rescues | Modeled full-system cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| always-small | 82.10% [78.15, 85.68] | +0.00 [+0.00, +0.00] | -5.25 [-7.75, -3.02] | -7.72 [-11.14, -4.54] | 0 (0.00%) | 0.0 | 0.0 | 0.0 | $30.20 |
| random | 85.56% [82.21, 88.74] | +3.46 [+2.03, +5.07] | -1.79 [-3.22, -0.49] | -4.26 [-6.46, -2.11] | 435 expected (26.85%) | 65.0 | 9.0 | 36.8 | $31.11 |
| cheap | 87.35% [84.01, 90.43] | +5.25 [+3.02, +7.75] | +0.00 [+0.00, +0.00] | -2.47 [-4.48, -0.56] | 435 (26.85%) | 100.0 | 15.0 | 68.0 | $31.46 |
| fitted | 87.50% [84.17, 90.59] | +5.40 [+3.18, +7.81] | +0.15 [-0.46, +0.74] | -2.31 [-4.29, -0.46] | 435 (26.85%) | 103.5 | 16.0 | 73.5 | $31.75 |
| direct_jev | 88.49% [85.19, 91.57] | +6.39 [+4.04, +8.98] | +1.14 [-0.59, +2.93] | -1.33 [-3.36, +0.59] | 435 (26.85%) | 114.0 | 10.5 | 87.0 | $31.43 |
| strong4 | 88.36% [85.00, 91.54] | +6.27 [+3.86, +8.86] | +1.02 [-0.59, +2.69] | -1.45 [-3.33, +0.34] | 435 (26.85%) | 117.0 | 15.5 | 88.0 | $31.70 |
| always-frontier | 89.81% [86.57, 92.90] | +7.72 [+4.54, +11.14] | +2.47 [+0.56, +4.48] | +0.00 [+0.00, +0.00] | 1620 (100.00%) | 161.0 | 36.0 | 129.0 | $3.20 |

The 25% optional budget is exactly 395 calls for each router and 395 calls in expectation for random; each cascade also makes the same 40 forced calls. Always-small makes zero calls. Always-frontier makes 1,620 calls and incurs no Qwen or Jev inference.

Rescues, harms, and failed rescues are expected counts across 1,620 attempts, averaging the two frontier samples. A rescue is a saved Qwen failure replaced by a frontier pass; harm is a saved Qwen pass replaced by a frontier failure. An incorrect answer escalated to another incorrect answer is a failed rescue. Counts can be half-integers because of the two-sample average.

The 648-call research collection cost **$1.278828 recorded** (648 successful HTTP attempts, zero retries). This charge is separate from each policy's modeled one-call-per-escalation deployment cost. The old Qwen Azure app is modeled at 9.52 hours × $3.2004/hour; its eligible-task share is $30.20, with the excluded task's share left out. Jev is added only for policies that call it, at $0.042/M saved input tokens. The table includes the prior Qwen work for every cascade policy and always-small. Direct Jev uses one history arm; fitted and strong4 use two arms.

The local CPU cost of visible-test execution was not separately recorded or priced. The frontier answer is graded only for research; hidden grading is not charged to a deployment policy. The original EvalPlus base-plus labels, HumanEval/32 exclusion, grader code, dataset cache and sandbox image were retained. A benchmark failure may arise from comparison/type semantics, timeouts or ambiguous task wording; no original label was changed.

The intervals resample whole tasks within benchmark and keep all five attempts and both frontier samples together. They are conditional on this already-inspected task set, the frozen selections, and two sampled frontier responses. They do not establish independent confirmation or a live online effect.

The frozen threshold sensitivity appears in `frozen_threshold_sensitivity.csv`; its realized optional rates differ from the exact 25% batch comparison. Source data and charges remain in ignored `results/runs/`; this addendum does not modify them.

## Provenance and reproduction

The frozen protocol was committed as `4606dbccd64484d54c091fbd6f9e502824e21d6f` before collection. Its manifest SHA256 is `149a405deea353b8f4503791b83fa6c61840d7c784af578494ce6262f3464e7a`. The saved run IDs are `q8b-test-v1` and `q8b-frontier-replacement-v1`. The original labels' SHA256 after this extension is `47857f079df2cbfa85cdfed922cde6f411542b45375dcf9d8505ed01635429f5`.

The full-system comparison columns and Matplotlib figure were formatted on October 28 after frontier outcomes existed. This dated presentation addendum implements the previously requested comparisons against always-small and always-frontier; it does not change selection, scoring, labels, samples, or the frozen analysis. The figure was rendered with Matplotlib 3.8.4. Given the operator-held ignored run artifacts, reproduce the outputs with:

```bash
PYTHONPATH=src python scripts/analysis/q8b_replacement_extension.py analyze \
  --frontier-run q8b-frontier-replacement-v1
PYTHONPATH=src python scripts/analysis/q8b_replacement_paper_addendum.py
```

The first command verifies the manifest, matching grader and dataset, prompt hashes, task/sample grid, labels, and call costs before writing results. The second command makes the paired baseline table and figure. The aggregate machine-readable outputs are alongside this report. Raw candidate responses, grader calls, and cost-ledger rows remain git-ignored on the operator machine.
