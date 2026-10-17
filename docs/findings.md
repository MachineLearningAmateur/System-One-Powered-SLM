# Findings so far (as of October 16, 2026)

Development data only. No test task has been generated or scored. The Claude
Doc research plan (exported to `docs/research-plan.md`, rev 86) is the source
of truth; this file collects the pilot results in one place. Numbers come from
the scripts in `scripts/` and `scripts/analysis/`; the small result files are
in `docs/results/`.

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
- 12K on the 33 cap-hit tasks: cap hits 52.5% -> 29.8% of checkpoints, final hidden pass 8/33 -> 10/33 (5 gains, 3 losses). Most gains finished under 8K or hit 12K again, so they reflect run-to-run variation; only one gain needed more than 8K. Cost: +25% thinking tokens and 5 KV-cache preemptions (0 at 8K).
- 12K is the most the RTX 3070 (8 GB) allows. Qwen recommends 32,768 output tokens; the paper states the 8K cap as a limitation.
- Cap hits are a strong failure signal and a large cost: hidden pass 9.7% (cap hit) vs 66.4% (no cap hit); 17% of checkpoints but 38% of generated tokens and 40% of generation time; 32% of cap-hit code did not load or crashed (3% otherwise).
- Cap hits are mostly not token loops: 4 of 103 end in a verbatim loop (0 of 518 other checkpoints). The rest is long reasoning that circles with new words, so a presence penalty would not help.

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

## Costs to date

- Jev: about $0.18 of the approved $2 (3.67M input tokens for the full scoring, plus the checks), at the third-party price of $0.042 per million input tokens with free output. The TypeSafe account price is still unconfirmed.
- Frontier model: $0 (no calls yet).
- Local GPU: about 674 Wh for the three runs.

## Still to freeze or do

- Before the replay: the threshold objective (on the out-of-fold dev predictions), tie handling, the fallback for a missing score, and the rule at visible-fail checkpoints.
- Pinocchio-0.8B baseline (install open).
- Frontier client (Claude Sonnet 5.5, 3 samples per task) and the replay evaluator, October 18-21; billed calls need approval.
- Protocol freeze, then the main run on the 325 test tasks.
