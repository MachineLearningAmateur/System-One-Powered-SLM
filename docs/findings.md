# Findings so far (as of October 18, 2026)

Sections 1-13 cover the development phase (October 16-17). The test phase
(frozen primary test, Table 1, replay, transfer, exploratory diagnostics) is
summarized with all tables in the top-level [README](../README.md); its result
files are `docs/results/test_analysis_main-test-v1.json`,
`docs/results/replay_main-test-v1_final_routers-v2.json` and
`docs/results/transfer_main-test-v1.json`. The Claude Doc research plan
(exported to `docs/research-plan.md`) is the source of truth. Numbers come from
the scripts in `scripts/` and `scripts/analysis/`.

## Runs

| Run | Commit | What | Size |
|---|---|---|---|
| `pilot-v1` | c86d88d | Attempt 0 on all 217 dev tasks, 8K cap | 217 attempts, 264 checkpoints, 4,614 s, 209 Wh |
| `pilot-v1b` | 00cea61 | Attempts 1-4 on the frozen 72-task subsample, 8K cap | 288 attempts, 357 checkpoints, 7,103 s, 323 Wh |
| `pilot-cap12k` | 7dde584 | Attempt 0 on the 33 dev tasks with an 8K cap hit, 12K cap | 33 attempts, 57 checkpoints, 3,037 s, 142 Wh |

The two pilot runs differ only in a driver fix (protocol JSON round trip and
`--first-attempt`). No harness failures. Hidden grading: every session was a
protocol session, 0 invalid labels, 0 disagreements between the first two
replicates.

## 1. Headroom gate: passed

| | HumanEval+ | MBPP+ | All |
|---|---|---|---|
| Final hidden pass, attempt 0 | 74.2% (49/66) | 72.8% (110/151) | 73.3% |
| Round-1 hidden pass, attempt 0 | 71.2% | 69.5% | 70.0% |
| Subsample tasks with >=1 visible-pass/hidden-fail checkpoint in 5 attempts | 11/22 | 16/50 | |
| Projected positive test tasks (Wilson interval) | 49 of 98 (30-68) | 73 of 227 (47-104) | |

- Target 50-80% hidden pass: met. Target >= 30 projected positive test tasks per benchmark: met; the HumanEval+ lower bound is at the line.
- Visible-pass checkpoints: 470, of which 116 (24.7%) fail the hidden tests. No visible-fail checkpoint passes them.
- Repair rounds add little: 29 attempts went to revision, 7 of them ended with a hidden pass (+3 points). 36 attempts passed the visible tests in round 1 but failed the hidden tests; the loop stops there, so only an escalation can catch them.
- These are not leaderboard scores: sampling at temperature 0.6 with thinking, and up to 3 rounds with visible feedback.

## 2. Thinking cap: frozen at 8K, no presence penalty

- Cap hits: 12.1% at attempt 0 on all dev tasks; 16.6% pooled over 621 checkpoints (the subsample's HumanEval+ tasks hit the cap more). The pooled rate crossed the 15% rule, so the 12K comparison ran.
- 12K on the 33 cap-hit tasks: cap hits 52.5% -> 29.8% of checkpoints, final hidden pass 8/33 -> 10/33 (5 gains, 3 losses). Most gains finished under 8K or hit 12K again, which is consistent with run-to-run variation (not proof of it); only one gain needed more than 8K. Cost: +25% thinking tokens and 5 KV-cache preemptions (0 at 8K).
- 12K is the most the RTX 3070 (8 GB) allows. Qwen recommends 32,768 output tokens; the paper states the 8K cap as a limitation.
- Cap hits are a strong failure signal and a large cost: hidden pass 9.7% (cap hit) vs 66.4% (no cap hit); 17% of checkpoints but 38% of generated tokens and 40% of generation time; 32% of cap-hit code did not load or crashed (3% otherwise).
- Cap hits are mostly not token loops: 4 of 103 end in a verbatim loop (0 of 518 other checkpoints). The rest is long reasoning that circles with new words, so a presence penalty has no clear target here (we did not test one).

## 3. Reproducibility

The same seed and prompt do not reproduce a trajectory in vLLM: the 8K and
12K thinking diverged within 78-1,766 characters on all 33 tasks (batching
changes the bf16 numerics). Runs are paired by task and attempt index only.
The replay uses the logged trajectories, so it is not affected.

## 4. Throughput

About 203 generation tokens/s with 3 concurrent trajectories, 0 KV-cache
preemptions at 8K, mean GPU power 164 W, about 25 s per attempt. Five
attempts on the 325 test tasks: about 11 hours.

## 5. Jev integration and byte budget

- 1,322 scoring calls on the 621 dev checkpoints (two arms plus a 40-checkpoint repeat sample): all valid on the first try, one model version (jev-1.13.0), median latency about 130 ms.
- Byte budget raised from 28,000 to 56,000 bytes (evidence-v3). At 28,000 bytes the trace was cut on 118 of 621 checkpoints, and Jev read a median 79% of those traces. The 28,000 limit came from an unconfirmed "long-context mode above about 32,000 bytes" note; third-party sources give 32K tokens for the state. Requests up to 55,776 bytes (14,320 input tokens) were valid with unchanged latency. The largest 8K request is 41,855 bytes, so no 8K trace is cut.
- Full vs cut traces (15 checkpoints): code questions almost unchanged; thinking questions moved 2-4 times the cut-vs-cut noise (mean change at most 0.034).

## 6. Jev technical gates: passed

- 100% valid responses in both arms, 0 failures after retries, 0 requests over the budget, no feature with all values at 0 or 1.
- Repeat with identical request bytes: scores moved by at most 0.05 (Jev is almost, not fully, deterministic).
- Weakest code feature: `special_cases_visible_tests` (history arm: 41% of values at its mode, 24% of visible-pass fail/pass pairs tied). Kept, as the plan says.
- Details: `docs/results/jev_gates_pilot-v1+pilot-v1b.json`.

## 7. Resource guide: below the 0.03 rule

Visible-pass dev checkpoints: 470, with 116 hidden fails from only 49 tasks;
431 are round 1. Task-grouped out-of-fold AUROC (5 folds x 20 splits),
task bootstrap:

| Feature set | predict-v1 (first) | predict-v2 (frozen) | predict-v2, task-weighted |
|---|---|---|---|
| cheap | 0.794 | 0.796 (0.721-0.864) | 0.770 |
| cheap+code | 0.814 | 0.815 | 0.822 |
| cheap+code+thinking | 0.802 | 0.803 | 0.806 |
| Primary gain (full - cheap) | +0.008 | +0.007 (-0.045 to +0.046) | +0.036 (-0.011 to +0.087) |
| Secondary (thinking on top of code) | -0.012 | -0.012 (-0.042 to +0.008) | -0.017 |
| Code answers only | +0.020 | +0.020 (-0.007 to +0.048) | +0.052 (+0.014 to +0.098) |

- Decision (pooled rule): keep Jev in the primary test; cut the drift labels and the 3-level score question first. Revisit on October 21 for schedule reasons only.
- Meaning: no incremental gain shown under this pipeline, not equivalence. The cheap baseline is strong: the largest coefficients are the logprob confidence of the thinking and the answer, and code similarity. The task-weighted result is a reported sensitivity, never the rule.
- predict-v2 corrected defects found in a second-opinion review (duplicate missing indicators that changed the L2 penalty, a timeout case error, a missing telemetry feature, data-dependent columns). C = 1, the feature sets and the rule did not change. Both results are on record; the pipeline is frozen.
- Details: `docs/results/resource_guide_pilot-v1+pilot-v1b_predict-v1.json` and `..._predict-v2.json`.

## 8. Does the thinking change Jev's judgment? (same-question contrast)

The trace arm answers the same three code questions as the history arm, but
also reads the thinking. Comparing the two answers to the same question on the
same checkpoints isolates the effect of the chain of thought. Prespecified on
October 16 as a descriptive analysis (outside the Holm family). Visible-pass dev
checkpoints, no new Jev calls (`scripts/analysis/trace_effect.py`).

| Answer (standalone AUROC) | Without thinking | With thinking | Difference (task bootstrap) |
|---|---|---|---|
| `code_likely_fails` | 0.786 | 0.796 | +0.009 (-0.027 to +0.054) |
| `special_cases_visible_tests` | 0.778 | 0.750 | -0.028 (-0.093 to +0.044) |
| `repeats_previous_code` (39 rows) | 0.325 | 0.351 | |

| Thinking answer (standalone AUROC) | Value |
|---|---|
| `on_task` | 0.194 (higher `on_task`, fewer fails: 0.806 as a separator) |
| `unsupported_claim` | 0.718 |
| `approach_change_without_evidence` (39 rows) | 0.776 |
| `repeating_failed_fix` (39 rows) | 0.643 |
| `stated_fix_matches_change` (39 rows) | 0.325 |

| Frozen predictor (out-of-fold) | AUROC | Task-weighted |
|---|---|---|
| cheap | 0.796 | 0.770 |
| cheap + code answers, history arm | 0.815 | 0.822 |
| cheap + code answers, trace arm | 0.810 | 0.806 |
| cheap + code + thinking (frozen) | 0.803 | 0.806 |
| cheap + all trace-arm answers | 0.800 | 0.794 |

- Trace arm minus history arm code answers in the predictor: -0.018 to +0.009 pooled; -0.031 to -0.002 task-weighted.
- Reading: the thinking answers carry signal alone (`on_task` is as strong as the best code answer), but on dev they add little to the cheap features and the code answers. Overlap is a possible explanation, not an established mechanism: removing the logprob columns lowers cheap only to 0.789. The trace-arm answers also see the code, so their signal is not from the thinking alone. Not evidence of no effect: 49 positive tasks, wide intervals, and the round-2+ questions rest on 39 checkpoints.

## 9. Strong Jev answers: frozen as a descriptive sensitivity

A dev heuristic (standalone AUROC >= 0.70 or <= 0.30 on >= 100 applicable rows,
chosen after the per-answer results above) kept four answers:
`code_likely_fails`, `special_cases_visible_tests`, `on_task`,
`unsupported_claim`. They are frozen by name (`predict.STRONG_QS`), not the
rule. Scripts: `scripts/analysis/jev_select.py`, `scripts/analysis/jev_strong.py`.

| Predictor (visible-pass dev, out-of-fold) | AUROC | Gain over cheap (task bootstrap) | Task-weighted gain |
|---|---|---|---|
| cheap (predict-v2) | 0.796 | | |
| cheap + code + thinking (predict-v2 primary) | 0.803 | +0.007 (-0.045 to +0.046) | +0.036 |
| cheap + code | 0.815 | +0.020 (-0.007 to +0.048) | +0.052 |
| cheap + strong4 (sensitivity) | 0.814 | +0.018 (-0.022 to +0.050) | +0.047 |
| strong4 mean, no fitting (sensitivity) | 0.803 | +0.008 (-0.044 to +0.059) | +0.058 |
| Nested: rule applied inside each fold, cheap on the same folds | 0.811 vs 0.792 | +0.019 (-0.009 to +0.046) | +0.044 |
| Nested forward selection | 0.813 vs 0.802 | +0.011 (-0.016 to +0.041) | |

- The rule picked the same four answers in 20 of 25 nested folds (three in the other 5). The nested check guards against within-fold selection leakage; it does not validate the rule, which was chosen after looking.
- strong4 mean by subgroup: HumanEval+ 0.878 vs cheap 0.778; MBPP+ 0.769 vs 0.802; cap hit (30 rows) 0.768 vs 0.395. Hypotheses for the test data, not results.
- A rank-based mean (0.839) and a three-answer mean (0.821) were also looked at after the plain mean was defined. They stay in this audit and are not used (forking paths).
- Decision (October 16, after two second-opinion reviews): predict-v2 stays primary. cheap + strong4 (one LR refitted on all dev visible-pass rows) and the strong4 mean are computed on test exactly as frozen and reported as "selected on dev after the freeze; descriptive". They cannot change the primary conclusion.

## 10. Scope and schedule decisions (October 16)

- Holm test: two-sided paired task bootstrap centered on the null, 19,999 replicates, stratified by benchmark (`predict.bootstrap_test`, `predict.holm`).
- Visible-fail rule, the same for every routing policy: rounds 1-2 continue the repair loop with no judge call; round 3 is a terminal frontier takeover. Policies differ only at visible-pass checkpoints.
- Frontier: 3 takeover samples per task (target), 1 per task (floor, 325 calls).
- Fallback: if the replay is not validated by October 20, narrow the paper to failure prediction and selective acceptance.
- Cut: the fine-tune stretch goal, takeover with context, drift labels and the 3-level question; blind resampling and the generic judge unless they need no new code path. Pinocchio is time-boxed.
- Our visible-test baselines are not the equivalent of Model Cascading for Code (which generates tests); this is a stated limitation.

## 11. Frontier takeover on dev (October 17)

Run `frontier-dev-v1` (commit c22634a): Claude Sonnet 5.5 through OpenRouter,
provider Anthropic pinned without fallbacks, low reasoning effort, the small
model's round-1 message, 217 dev tasks x 3 independent samples.

| | HumanEval+ | MBPP+ |
|---|---|---|
| Frontier hidden pass | 96.0% (190/198) | 85.9% (389/453) |
| Small model final hidden pass, attempt 0 | 74.2% | 72.8% |

- 651 calls, all valid, every answer with a code block; 0 reasoning tokens at low effort; $1.30 in total ($0.0020 per call, reported = computed). Price checked on OpenRouter on October 17: $2 / $10 per million tokens.
- Hidden grading: protocol session, 0 invalid, the first two grades agree on all 374 distinct codes.
- Samples agree almost always: 191 tasks pass in all 3, 21 fail in all 3, 5 are mixed.
- Headroom on the 470 visible-pass dev checkpoints: the frontier fixes 60.3% of the 116 hidden fails (mean over samples) and would break 1.8% of the 354 hidden passes.
- Attempts that end in a visible fail after round 3 (forced escalations): 35 of 505 (6.9%).

Cost per attempt (corrected; the pilot times already include the 3 parallel trajectories):

| Cost view | Small model, one attempt | Frontier, one answer |
|---|---|---|
| Owned hardware (electricity, $0.15/kWh) | about $0.00015 | $0.0020 |
| Cloud equivalent (A10G, $1.006/h) | about $0.0065 | $0.0020 |

So budgets are set in frontier calls, not dollars, and the paper reports both cost views; it does not claim savings in general.

## 12. Dev replay (code check, October 17)

The evaluator (`scripts/replay.py`, `src/system1/eval/replay.py`) passed a
three-round code review. Routers frozen in `configs/routers_v1.json`. On dev the
thresholds were set on the same out-of-fold scores, so this is a code check and
a descriptive dev result, not an estimate for the test data.

| Policy (505 dev attempts, 470 decisions) | Final hidden pass | Frontier calls per attempt | Gain over random at the same rate (pp) |
|---|---|---|---|
| always-small | 0.701 | 0.000 | |
| forced-failure-only (q_VP = 0) | 0.755 | 0.069 | |
| cheap, top-K 25% | 0.840 | 0.303 | +5.3 (+2.3 to +8.4) |
| cheap+code, top-K 25% | 0.844 | 0.303 | +5.7 (+2.2 to +9.1) |
| cheap+code+thinking (primary), top-K 25% | 0.844 | 0.303 | +5.7 (+2.2 to +9.0) |
| strong4 mean, top-K 25% | 0.848 | 0.303 | +6.1 (+3.0 to +9.2) |
| always-frontier | 0.881 | 1.000 | |
| oracle | 0.894 | 0.208 | |

- Every router beats random escalation at the same rate at all three budgets (+2 to +6 pp); the routers differ from each other by at most about 1 pp, which is within the noise.
- At a 25% budget (30% of attempts call the frontier), the routers reach about 0.84-0.85 against 0.88 for always-frontier.
- Full table: `docs/results/replay_pilot-v1+pilot-v1b_dev-oof.json`.

## 13. Pinocchio-0.8B on dev (October 17)

`pinocchio-uq==0.1.1` (Apache 2.0, CPU), added as a router (configs/routers_v2.json;
the five v1 routers unchanged). Input pinocchio-input-v1 frozen before any score;
pinocchio-input-v2 (the executed code as the answer) frozen before it was scored,
as the one dev-informed sensitivity. Pinned setup: configs/pinocchio_setup_v1.json.
Scripts: scripts/score_pinocchio.py, scripts/analysis/pinocchio_dev.py. Two rounds of
code and results review.

| Predictor (470 visible-pass dev checkpoints, 116 fails from 49 tasks) | AUROC (95%) | AUPRC | FNR at 5% FPR |
|---|---|---|---|
| cheap LR | 0.796 (0.721-0.864) | 0.510 | 0.828 |
| cheap + code + thinking (primary) | 0.803 (0.723-0.878) | 0.567 | 0.724 |
| strong4 mean (sensitivity) | 0.803 (0.719-0.878) | 0.593 | 0.621 |
| Pinocchio-0.8B, input-v1 (frozen router) | 0.616 (0.520-0.716) | 0.325 | 0.905 |
| Pinocchio-0.8B, input-v2 (code only, sensitivity) | 0.566 (0.463-0.672) | 0.295 | 0.940 |
| Logprob comparator (minus thinking tail confidence) | 0.813 (0.740-0.876) | 0.592 | 0.716 |

Prevalence 0.247 (the AUPRC of a random score). Intervals bootstrap tasks over fixed scores.

- Pinocchio is much weaker here: cheap minus Pinocchio +0.180 (+0.105 to +0.252); it adds nothing to the cheap LR (+0.005, -0.010 to +0.020). On all 621 dev checkpoints (visible fails included) it reaches 0.731.
- The package cuts answers at 800 characters (its training format); in about 30 of the 470 answers the graded code started after the cut. This does not explain the result: uncut answers give 0.570, and the code-only input-v2 is lower still (0.566; v2 minus v1 -0.050, -0.110 to +0.011).
- Underconfident: mean p_correct 0.499 against an observed pass rate of 0.753 on these rows (calibration, not ranking).
- Not a controlled replication of the paper's 0.868 vs 0.666: the paper used its 8B calibrator and gave both tools only question-answer pairs on QA and math benchmarks. Distribution shift (code, a 1.7B generator, visible-pass errors) is plausible, not established.
- The logprob comparator is not shown to beat the cheap LR (+0.017, -0.031 to +0.067; task-weighted -0.018). The primary stays unchanged.
- Dev replay: Pinocchio beats random at the same rate by about half as much as the other routers (top-K 25%: +2.8 pp, +0.4 to +5.4).
- Cost: about 1.85 s of elapsed CPU inference per checkpoint; not included in the dollar totals.
- Two input-v2 checkpoints without code have no score (the package refuses an empty answer); they are visible fails, so no decision uses them.

## Costs to date

- Jev: about $0.18 of the approved $2 (3.67M input tokens for the full scoring, plus the checks), at the third-party price of $0.042 per million input tokens with free output. The TypeSafe account price is still unconfirmed.
- Frontier model: $1.30 of the approved $5 (dev takeover answers).
- Local GPU: about 674 Wh for the three runs.

## Still to freeze or do

- Frozen on October 17 (plan, "Still to freeze before the replay"): escalation budgets q_VP = 10/25/50% from dev OOF quantiles weighted 1 / attempts of the task, tie rule, cheap-LR fallback for a missing Jev score, deployment view and label-free top-K ranking view, net gain over realized-rate random as the central replay result.
- Replay evaluator: done and reviewed; dev replay done (section 12).
- Pinocchio-0.8B: installed, scored on dev and frozen as a router (section 13).
- Protocol freeze, then the main run on the 325 test tasks and the test takeover answers (new approval).
