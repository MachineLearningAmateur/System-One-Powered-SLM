# Qwen3.5-9B replication on HumanEval+ (plan)

**Status, November 26, 2026:** part A (setup and recorded changes) is written before any protocol
generation. Nothing in this study changes the finished 1.7B study, the 8B study, their routers, their tags
or their files in `docs/results/`. Branch: `gen-qwen35-9b`.

## Part A: worker, backend, and the recorded changes

The worker is `Qwen/Qwen3.5-9B` in thinking mode. The tokenizer and chat template are pinned to Hugging
Face revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a`. Qwen3.5 is a different model generation from
Qwen3 (hybrid attention, vision encoder, a 248,077-entry vocabulary), so no router, threshold or feature
weight from the 1.7B or 8B studies is reused. All routers are fit again on 9B development data only.

Generation runs on DeepInfra's hosted text-completions endpoint
(`https://api.deepinfra.com/v1/openai/completions`, model `Qwen/Qwen3.5-9B`) through
`scripts/run_loop.py --backend deepinfra`. The operator chose this backend on November 26 after the
probes below. The prompts, visible tests, sandbox, hidden grader, split, HumanEval/32 exclusion, sampling
(temperature 0.6, top-p 0.95, top-k 20), seed scheme, 16,384-token context, 8,192-token thinking cap,
2,048-token answer limit and three repair rounds are unchanged.

Three probes on November 26 (toy prompts, no benchmark task, about USD 0.0002 in total) showed these
differences from the vLLM protocol of the earlier studies. Each is recorded here before any protocol
generation:

1. **Weights are not pinned.** DeepInfra manages the weights and their precision. Its model page data
   suggests a quantized deployment (FP8 or FP4); this could not be tied to the model with certainty. The
   earlier studies used pinned bf16 weights. The run fingerprint records `weights_pinned: false`.
2. **Top-1 logprobs only.** For any requested count (5 or 20 on the completions endpoint; 5 on the chat
   endpoint), DeepInfra returned at most the top-1 alternative per token, plus the sampled token when it
   differs. The chat endpoint returned none. The DeepInfra backend therefore requests 1 alternative and
   computes token confidence from the top-1 value (`confidence_top_k: 1`). The confidence features keep
   their names, but they are top-1 values, not the top-5 DeepConf values of the earlier studies. The
   sampled-token logprobs are complete.
3. **No `stop_reason` field.** The reply's last entry in `logprobs.tokens` gives the cause instead:
   `</think>` for the stop string, `<|im_end|>` or `<|endoftext|>` for the end of the reply. Any other last
   token is an error, never a guess (`stop_reason_source: last_token`).

The Qwen3.5 chat template opens the `<think>` block itself (Qwen3 did not). The generator detects this from
the rendered prompt, so a reply that starts inside the thinking is not counted as a direct answer.

Consequences: the telemetry-only router of this study is not the same feature set as in the 1.7B and 8B
studies. Its results, and any comparison with the earlier workers, are descriptive. Worker latency is
DeepInfra's network and queue time, not local GPU time.

## Scope and run ids

- Benchmark: HumanEval+ only (operator decision, November 26). Development: 66 tasks. Test: 98 tasks.
- Run ids: `q9b-smoke` (5 dev tasks, excluded from all analyses), `q9b-pilot-v1` (attempt 0 on the 66 dev
  tasks), `q9b-pilot-v1b` (attempts 1–4 on the 22 HumanEval+ tasks of `configs/pilot_subsample_v1.json`),
  `q9b-test-v1` (five attempts on the 98 test tasks, only after the freeze tag).
- Concurrency 16 in every run of this study (operator decision, November 26: DeepInfra serves each request
  slowly, 9–45 tokens per second in the smoke run).
- Freeze tag: `q9b-protocol-freeze-v1` (set in `scripts/run_loop.py`). Router version: `q9b-v1`.

## Smoke run

`q9b-smoke` (November 26, non-protocol, dirty tree, concurrency 8, excluded from all analyses): 5
HumanEval+ dev tasks, one attempt each. All 10 calls returned `ok`; all 5 thinking phases stopped at
`</think>` (found from the last token); none was counted as a direct answer; no cap hit; all 5 answers gave
code defining the entry point and passed the visible tests in round 1. Tokens: 8,983 input and 8,374
output (about USD 0.0022). The longest thinking (5,754 tokens) took 634 s. No hidden grading was run.

## Cost and guards

DeepInfra listed USD 0.10 per million input tokens and USD 0.15 per million output tokens on November 26;
the probe replies' `usage.estimated_cost` agreed with these prices. At the 1.7B study's HumanEval+ token
use (about 5,200 input and 4,800 output tokens per attempt), the development design (154 attempts) costs
about USD 0.20 and the test run (490 attempts) about USD 0.60; if every round hit the cap, the test run
would cost about USD 3. Every DeepInfra run needs `--max-billed-tokens`, and every billed step (DeepInfra,
Jev) needs the operator's approval with a dollar limit first.

## Headroom gate

The 8B worker had visible-pass hidden failures on only 10 of 96 HumanEval+ test tasks. Before any router is
fit, apply the runbook's projection rule to the 22-task subsample. If fewer than 30 test tasks are
projected to have a visible-pass hidden failure, stop and ask the operator: add MBPP+, or make the study
descriptive only. Do not change the benchmark, split or cap after the pilot is seen.

## Amendment A1 (November 26, 2026): HumanEval+ and MBPP+

The HumanEval+ part of the development pilot (`q9b-pilot-v1` attempt 0 on 66 tasks, `q9b-pilot-v1b`
attempts 1–4 on the 22 HumanEval+ subsample tasks; 154 attempts, about USD 0.065) was graded first. Of 153
visible-pass checkpoints, 21 failed hidden tests. Six of the 22 subsample tasks had a visible-pass hidden
failure (27.3%, Wilson 13.2%–48.2%), which projects 26.7 of 98 test tasks (12.9–47.2): the headroom gate
failed. As the plan required, generation stopped and the operator decided. The operator chose the task set
of the 1.7B study: HumanEval+ and MBPP+ (217 development and 325 test tasks). This decision used
development labels only; no test task was generated or graded.

The 151 MBPP+ development tasks were added to the same two run ids on the same commit (`258b536`), with the
same protocol fingerprint; the run script allows added tasks. Both runs were then graded again with
`--force`. The HumanEval+-only labels were kept as `hidden_labels.heonly-20261126.jsonl` and
`grade_meta.heonly-20261126.json` in each run folder, and every grading call stays in `hidden_grades.jsonl`.
The new HumanEval+ labels agree with the first ones (the same counts).

Development pilot, both benchmarks (protocol grade sessions `20261126T093724-9c3383` and
`20261126T093901-b63f69`; 0 invalid labels; the first two grades disagree on 0 of 540 codes):

| Benchmark | Attempts | Final hidden pass | Visible-pass checkpoints | Hidden fails among them | Cap hits | Projected test tasks with a visible-pass hidden fail |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| HumanEval+ | 154 | 85.7% | 153 | 21 (13.7%) | 3 of 165 | 26.7 of 98 (12.9–47.2) |
| MBPP+ | 351 | 76.9% | 338 | 68 (20.1%) | 35 of 411 | 77.2 of 227 (50.9–108.6) |
| Both | 505 | 79.6% | 491 | 89 (18.1%) | 38 of 576 | 103.9 of 325 |

The gate passes for the study population (both benchmarks). Generation used 1,152 DeepInfra calls, all
`ok`, with 961,997 input and 919,527 output tokens (about USD 0.23) for the MBPP+ part; the full pilot cost
about USD 0.30.

## Development scoring and results

Jev returned `jev-1.14.0` for all 1,152 arm records of the two pilot runs; every record was `ok`. It used
2,250,682 input tokens (about USD 0.095 at USD 0.042 per million). No request was over the 56,000-byte
budget, no trace was cut, and no base evidence was trimmed. The 30-checkpoint repeat sample had identical
request bytes for all 60 requests; the largest change of any answer was 0.05. Pinocchio input v1 and v2
scored all 576 checkpoints of both runs (`results/jev_gates_q9b-pilot-v1+q9b-pilot-v1b.json`,
`results/resource_guide_q9b-pilot-v1+q9b-pilot-v1b_predict-v2.json`).

Out-of-fold development AUROC on the 491 visible-pass checkpoints (89 hidden fails on 37 tasks; 20
task-grouped splits): telemetry-only router 0.765 (0.680–0.845), code router 0.772, full router 0.765,
cheap + Strong4 0.772, Strong4 mean 0.702, direct Jev (history-request `code_likely_fails`, no fitting)
0.671. Full minus telemetry-only: +0.001 (−0.031 to +0.032). The resource-guide rule (a gain of at least
0.03) is not met. These are development estimates; they do not change the hypotheses below.

## Part B: the frozen test protocol (written November 26, before any test-task generation)

Everything here was set on development data only. After the tag `q9b-protocol-freeze-v1`, any change is
a dated amendment, and its result is exploratory.

**F1. Routers.** `configs/routers_q9b-v1.json` (fit at commit `fe085f9` on `q9b-pilot-v1` and
`q9b-pilot-v1b`; SHA-256 prefix `18c1ffae813c8033`): the telemetry-only, code and full LR routers, cheap +
Strong4, the Strong4 mean, Pinocchio (input v1; 1 − p_correct) and direct Jev. Each LR router is one
logistic regression refitted on all 491 visible-pass development rows. When a Jev answer that a router
needs is missing, the telemetry-only router decides at the same operating point. No 1.7B or 8B router,
threshold or weight is reused.

**F2. H1 and H2 (Holm family of two, as in the 1.7B and 8B studies).** On the visible-pass test
checkpoints, with the Amendment A2 exclusion: H1, AUROC(full router) − AUROC(telemetry-only router); H2,
AUROC(full router) − AUROC(code router). Two-sided paired whole-task bootstrap, tasks resampled within
benchmark, 19,999 draws; Holm over the two at familywise 0.05. Command:
`uv run python scripts/test_analysis.py --run-id q9b-test-v1 --routers q9b-v1`. Everything else that
script reports is descriptive.

**F3. The direct Jev test (prespecified, separate from the Holm family).** AUROC(direct Jev) −
AUROC(telemetry-only router), the same bootstrap and population, two-sided at 0.05 on its own, with no
multiplicity adjustment (operator decision, November 26). Direct Jev is the frozen `direct jev` router:
the `code_likely_fails` probability of the history request, used as is. Command:
`uv run python scripts/analysis/q9b_direct_jev_test.py --run-id q9b-test-v1`. In the 8B study, direct Jev
was chosen after the test results were seen; here it is fixed before them, so its result is confirmatory
for this study only.

**F4. Budgets.** 10%, 25% and 50% of the visible-pass decision checkpoints (`replay.RATES`), for every
router in F1 and for random escalation at the realized rate, with the endpoints always-small,
forced-failure-only, always-frontier and the oracle.

**F5. Score limits.** For each router and budget, the frozen limit (t, alpha) in
`configs/routers_q9b-v1.json`: the weighted development quantile, each row weighted 1 / (the sampled
attempts of its task). The replay applies it to each test checkpoint alone (escalate if s > t, or s = t
with a seeded draw below alpha) and reports the realized rate. It also reports the exact-budget (top-k)
view, for comparison with the 1.7B and 8B papers. Limits for the routers that the paper discusses:

| Router | 10% (t, alpha) | 25% (t, alpha) | 50% (t, alpha) |
| --- | --- | --- | --- |
| Telemetry-only | 0.3878, 0.26 | 0.2254, 0.75 | 0.1010, 0.50 |
| Full | 0.4158, 0.06 | 0.2139, 0.75 | 0.0954, 0.90 |
| Direct Jev | 0.4400, 0.86 | 0.3200, 0.93 | 0.2100, 0.19 |
| Strong4 mean | 0.2650, 0.55 | 0.1900, 0.49 | 0.1500, 0.90 |

Command: `uv run python scripts/replay.py --split test --run-id q9b-test-v1 --frontier-run
frontier-test-v1 --scores final --routers q9b-v1`.

**F6. Frontier answers.** The replay uses the saved task-only answers of `frontier-test-v1` (the 1.7B
study's `anthropic/claude-sonnet-5.5-20260928` answers, 3 replicates for each of the 324 test tasks after
Amendment A2, graded in one protocol session). They do not depend on the worker. No new frontier call is
made.

**F7. Cost and latency.** `uv run python scripts/analysis/q9b_cost_latency.py --run-id q9b-test-v1
--replay results/replay_q9b-test-v1_final_routers-q9b-v1.json --frontier-run frontier-test-v1`. It
reports the median, mean and 90th percentile time of each worker call (thinking and answer), the worker
time for each attempt, each Jev call and each frontier call; the GPU-free worker cost for each attempt
(the run's DeepInfra tokens × USD 0.10 / 0.15 per million input / output tokens ÷ the run's complete
attempts); and for each policy, the break-even worker cost = always-frontier API cost − the policy's API
cost (frontier + Jev) per attempt. A cascade is cheaper than always-frontier only if the worker costs less
than that. Latency is DeepInfra network and queue time at concurrency 16, not local GPU time.

**Test run.** Five attempts on each of the 325 test tasks (HumanEval+ and MBPP+), `q9b-test-v1`,
concurrency 16, the Amendment A2 exclusion at labeling. At the pilot's use (about 4,770 tokens for each
attempt), generation needs about 7.8 million tokens (about USD 1); guard `--max-billed-tokens 15000000`
(at most about USD 2.25). Grading follows generation, in the networkless sandbox. Jev scores both arms of
every checkpoint (about 7 million input tokens, about USD 0.30; guard `--max-input-tokens 10000000`), then
Pinocchio scores both input versions. Each billed step needs the operator's dollar approval first.

**What is descriptive.** Every comparison with the 1.7B and 8B studies (other worker generation,
tokenizer, top-1 instead of top-5 confidence, unpinned hosted weights), the replay pass rates and costs,
results by benchmark, cap hit and round, and Pinocchio.
