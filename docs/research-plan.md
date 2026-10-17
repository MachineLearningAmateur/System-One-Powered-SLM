<!-- Exported 2026-10-17 from the Claude Doc "Research Plan: When Should a Small Model Ask for Help?" (https://claude.ai/code/artifact/7e826324-5c25-4f14-b827-99cc125a33f8). The Claude Doc is the source of truth; re-export after edits. -->
# Research Plan: When Should a Small Model Ask for Help?

*Status as of October 16, 2026. Updated after three second-opinion reviews (Astra): Jev reads the thinking with typed drift questions; the primary task is checkpoint failure prediction on a fixed 40/60 development/test split; drift labels come from two blind frontier judges as a supporting result; go/no-go gates are technical only; cost savings are measured, not presumed. October 16, after two more reviews: scope narrowed (predict-v2 stays primary with frozen development-selected sensitivities; the extras are cut; the replay is the critical path; new schedule below).*

## Submission

- **Venue:** IEEE BigData 2026 Workshop on Data and Model Efficiency for Scalable AI.
- **Deadline:** October 29, 2026. The confirmed time zone is Anywhere on Earth: 11:59 PM AoE, from the workshop page (efficientaiworkshop.github.io). Plan to submit on October 28.
- **Format:** short paper, up to 5 pages in IEEE two-column format, with references counted inside the limit. Review is single-blind, so author names go on the submission.
- **Presentation:** one author must present in person in Phoenix, AZ. Confirm who.
- **CFP topics this hits:** efficient reasoning and agentic workflows for LLMs, and trade-offs between efficiency, accuracy, robustness and cost.

## Research question and thesis

**Question.** Can a "System One" typed decision model, used as an external judge, predict when a small thinking model's current attempt will fail the withheld tests, so the loop can consult a frontier model? And does it add signal beyond the visible-test result and cheap loop features?

**Thesis.** Zero-shot System One models fail at routing from the prompt alone. In Li (2026), Jev called almost every request "cheap" and Laya scored an AUROC of 0.48. They do better at judging evidence: Jev scored an AUC of 0.95 on groundedness. On answer correctness, though, Jev scored only 0.666 AUROC against 0.868 for Pinocchio on the same 1,718 rows (Pinocchio, Appendix E.10). A small model's partial attempt carries evidence (its reasoning, its code and the visible-test output), so a System One model may judge it even though it cannot predict difficulty from the prompt.

**What we predict, and what we do not claim.** Jev reads the small model's thinking and answers typed drift questions: is it on task, repeating a failed fix, changing approach without new evidence, making unsupported claims, or lost? The only objective label is checkpoint failure: does the current code fail the withheld EvalPlus tests? So the primary claim is that Jev's drift judgments predict failure. The paper never claims that Jev "detects drift". Escalation value (does a takeover improve the outcome enough to pay for itself) is a separate policy question.

**Primary claim, finalized on development data before any test evaluation.** On the visible-pass subset of held-out test tasks, an L2-regularized logistic regression on cheap features plus the Jev feature set (the code answers from the history arm plus the thinking answers from the trace arm) predicts checkpoint failure better than the same pipeline on cheap features alone (paired ΔAUROC with a task-bootstrap interval). Jev is a zero-shot feature extractor; the predictor is supervised.

**Secondary claim, one prespecified contrast.** The budgeted trace view adds signal beyond code, test output and repair history: ΔAUROC between two prespecified feature sets on the same checkpoints: cheap features + the code answers from the history arm, against the same + the six thinking answers from the trace arm. The two sides differ only in the thinking answers. The code answers that the trace arm also returns feed one prespecified descriptive analysis, the same-question contrast (added October 16 on development data only, before any test task was generated): for each code question, the trace-arm answer (with the thinking) against the history-arm answer (without it) on the same visible-pass checkpoints, as standalone AUROC and as cheap + code answers taken from the trace arm against cheap + code answers from the history arm in the frozen predictor, each with paired task-bootstrap intervals (pooled; task-weighted as a sensitivity). It answers the narrowest form of the question (does the same judgment of the code change when Jev also reads the thinking), but it is outside the Holm family and never replaces the contrast above. The standalone AUROC of each thinking answer is reported with it (its sign is not fixed in advance, so it is described, not tested). The detectable difference depends on the positives and the pairing (about 0.08–0.12 with 50–100 positives and strong pairing). Fix a practically meaningful gain in advance. A small gain with a wide interval is inconclusive, and a null means "this budgeted trace view added no detectable value", not "the reasoning has no useful information".

**Supporting result.** Agreement of Jev's drift judgments with two blind frontier labelers (one Claude model, one GPT model), per category. There is no human check, so the claim is agreement under a shared rubric, not detection of drift.

**Framing.** A measurement study by default: the same primary comparison runs whatever the pilot shows, and a negative result is reported as the finding. Detection quality is the primary outcome; cost savings are measured, not presumed.

**Contribution statement.** We give a controlled test of whether low-cost typed-decision judges get more hidden-test failure signal from a 1.7B thinking model's reasoning and repair history, beyond its code, visible-test feedback and cheap features, and whether that signal improves escalation at matched frontier-call budgets (cost-quality trade-offs reported under both cost views, with no single dollar-to-accuracy exchange rate). In short: what the judge buys beyond cheap routing, measured with positive or null results. Do not claim superiority over CodeMonitorBench or other verifiers measured on other populations.

## Setup

### Small model

- **Qwen3-1.7B in thinking mode,** run locally with vLLM (0.8.5 or later) in BF16, with `enable_thinking` set explicitly. Its BF16 weights take 4.08 GB in vLLM, which leaves a KV cache of 16,752 tokens on the 8 GB RTX 3070, so it fits without quantization. It scores 33.2 on LiveCodeBench v5 with thinking on and 11.6 with it off. Thinking-off is not a free "no trace" ablation, because it changes the code the model writes. The trace ablation scores the same thinking-mode checkpoints with the trace shown or hidden.
- **Why the switch:** System One reads the small model's reasoning for failure symptoms, and Qwen2.5-Coder-1.5B-Instruct produces no reasoning trace.
- **Backup from a second model family:** SmolLM3-3B in thinking mode, quantized to fit 8 GB. It checks that System One isn't just learning Qwen's trace style. Off the critical path for October 29.
- **Decoding:** temperature 0.6, top-p 0.95, top-k 20. No greedy decoding, because Qwen warns it causes endless repetition. This departs from EvalPlus's greedy protocol, so say so in the paper. Cap thinking at about 8K tokens per round with `--max-model-len 16384`. That flag sets only the context length: enforce the 8K thinking cap with an explicit generation limit, reserve tokens for the code, and close thinking at the cap: the harness appends the closing think tag, asks for the answer (up to 2,048 tokens), tests it as usual and records the cap hit. A response that ends inside its thinking gives no code. Thinking-token counts include the closing think tag. Cap rule for the pilot: keep 8K; if more than about 15% of checkpoints hit it, rerun about 30 development tasks at a 12K cap (the most the KV cache allows) and compare before the freeze. Log cap hits as a feature. Request logprobs, serve without the reasoning parser, and split on `</think>`.
- **Pilot before the full run:** no candidate has published thinking-mode HumanEval+/MBPP+ scores. Run it on the development tasks only (40% of tasks, stratified by benchmark: about 66 HumanEval+ and 151 MBPP+), one seed on all of them plus a prespecified five-attempt subsample: one third of the development tasks per benchmark (22 HumanEval+, 50 MBPP+), drawn with seed 20261017 and frozen in configs/pilot\_subsample\_v1.json. Test tasks get no generation until the protocol is frozen. Go if the final hidden-test pass rate is about 50–80% and the projected number of test tasks with at least one visible-pass/hidden-fail checkpoint over five attempts is at least 30, projected per benchmark with a task-level interval. If not, apply a short fallback list fixed in advance (thinking cap first, then generator), then freeze. Also measure throughput on the real workload (concurrent trajectories, logprobs on, KV-cache preemption). A bandwidth estimate gives about 150–250 tokens/s, or 18–30 hours for the main run. The smoke run measured about 180 tokens/s with 3–4 concurrent trajectories and about 88 tokens/s for one.
- **Pilot result (October 16): go, thinking cap frozen at 8K.** Runs pilot-v1 (attempt 0 on all 217 development tasks) and pilot-v1b (attempts 1–4 on the subsample); 505 attempts, 621 checkpoints, no harness failures, hidden grading with 0 invalid labels and 0 replicate disagreements.
  - Headroom gate passed. Final hidden pass (attempt 0): 74.2% HumanEval+, 72.8% MBPP+. Subsample tasks with at least one visible-pass/hidden-fail checkpoint over five attempts: 11/22 HumanEval+ and 16/50 MBPP+, projecting 49 of 98 (Wilson 30–68) and 73 of 227 (47–104) positive test tasks. The HumanEval+ lower bound sits at the 30 line. On visible-pass checkpoints, 116 of 470 (24.7%) fail the hidden tests; no visible-fail checkpoint passes them.
  - Cap rule. Cap hits: 12.1% at attempt 0 on all development tasks, 16.6% pooled (the subsample's HumanEval+ tasks hit the cap more). The pooled rate crossed 15%, so attempt 0 of the 33 cap-hit development tasks was rerun at 12K (run pilot-cap12k, configs/cap12k\_tasks\_v1.json): cap hits fell from 52.5% to 29.8% of their checkpoints, but final hidden pass moved only from 8/33 to 10/33 (5 gains, 3 losses; most gains finished under 8K or hit 12K again, so they reflect run-to-run variation), with 25% more thinking tokens and 5 KV-cache preemptions. 12K is the most the RTX 3070 KV cache allows; Qwen recommends 32,768 output tokens, which this GPU cannot hold, so the paper states the 8K cap as a limitation.
  - Cap hits are mostly not token loops: 4 of 103 end in a verbatim loop (0 of 518 other checkpoints); the rest is long reasoning that circles with new words. No presence penalty. A cap hit is a strong failure signal (hidden pass 9.7% vs 66.4%) and a large cost: 17% of checkpoints, 38% of generated tokens.
  - Throughput about 203 generation tokens/s at 3 concurrent trajectories, 0 preemptions at 8K, mean 164 W; about 25 s per attempt, so 5 attempts on the 325 test tasks take about 11 hours.
  - The same seed does not reproduce a trajectory: the 8K and 12K runs diverged within 78–1,766 characters of thinking on all 33 tasks (vLLM batching changes the bf16 numerics). Runs are paired by task and attempt index only; replay uses the logged trajectories, so it is unaffected.
- OpenRouter is for the frontier helper and the hosted routers, not the small model.

### Benchmarks

- **HumanEval+ (164 tasks) and MBPP+ (378 tasks)** from EvalPlus, 542 tasks in all.
- **5 sampled attempts per task** on the test tasks, giving enough trajectories for the paired comparisons. Development tasks get one seed plus the five-attempt subsample.
- **Each attempt is a write → test → revise loop** with at most 3 rounds, so up to 3 checkpoints per attempt.
- **The router sees only the visible example tests.** The hidden EvalPlus tests decide the final pass/fail label.
- **MBPP+'s visible evidence is a single assert,** so expect a weaker signal there than on HumanEval+. Say so in the paper.
- **LiveCodeBench is dropped.** Qwen2.5-Coder-1.5B scored about 6% pass@1 there. Qwen3-1.7B in thinking mode scores about 33% (v5), so it could come back if time allows.
- **Harness rules to fix before the full run:** pin the EvalPlus version (0.3.1) and how the visible tests are built. Visible tests are exactly the examples the model sees: the assert line in the MBPP+ prompt; for HumanEval+, the docstring examples, or, for the 88 tasks without a usable example, the first three original inputs with reference outputs, shown as a test list (a covariate). A build gate checks that every reference solution passes its visible tests; two tasks with wrong docstrings (HumanEval/47 and HumanEval/116) are kept and flagged. Withheld tests and reference solutions stay outside the generation sandbox: each visible check runs in a new disposable container (no network, 2 GB memory, no hidden data, one 10 s deadline for loading the code and all tests); the test cut by the deadline is a timeout and later tests are "not run", not failures. Hidden labels come after generation, with vLLM stopped: the grader first checks that every reference solution passes and that a 1 GiB memory canary passes, then grades each distinct code twice and a third time if the two disagree; the label is the majority, and a worker or out-of-memory failure is an invalid grade, not a vote. Report the disagreement rate. Each run records a protocol fingerprint (model, template, sampling, caps, seeds, frozen files, sandbox image and limits, git commit) and refuses to mix protocols. Fixed loop: after each test run the policy escalates or continues. If it continues and the visible tests pass, the candidate is accepted. If they fail and rounds remain, the model revises. At round 3 it escalates or returns the last candidate. Missing code and test timeouts count as failed checkpoints and are reported. Thinking cut at the cap is closed and its answer tested (cap hit recorded). Harness failures (vLLM or sandbox errors) are logged and the attempt is rerun; the model never sees their text. Replay is valid only for policies whose continuation matches this logged loop. Do not count copies of an already accepted candidate as new checkpoints.

### Frontier helper

- **Model:** Claude Sonnet 5.5 through OpenRouter, at $2 per million input tokens and $10 per million output.
- **Pinned version:** `anthropic/claude-sonnet-5.5-20260928`.
- **Pinned provider:** set `allow_fallbacks: false` with a fixed provider order, so every call comes from the same backend.
- **Low reasoning effort,** because thinking tokens are billed as output. On development data it used no reasoning tokens. One answer per call: transport errors and HTTP 408, 429 and 5xx are retried; a received reply is never retried. Temperature is the provider default (a recorded limitation, unchanged for test).
- **`usage: {include: true}` on every call,** to log tokens and cost.

### Help mode

- **Takeover from scratch is the main mode.** Call the frontier three times per task (independent samples) with only the prompt and visible tests, about 1,600 calls for roughly $30–60, and reuse each answer at every checkpoint of that task. Each sample is one replicate: every policy is replayed once per replicate on the same small-model attempts, and the paper reports the mean and the spread across replicates, with whole tasks bootstrapped. Never score "any of three passes" or a majority: a deployed policy buys one answer, and the extra samples are experiment spend. Frozen acceptance rule: one final answer, no repair, retry or fallback, graded only with the authoritative hidden protocol. The Handoff Tax (2026) supports this, but its evidence comes from repository-level SWE-bench agents, not function-level tasks. Replay is exact conditional on the logged small-model continuations and the sampled takeover answers; it is not a prediction of a fresh live run, and the paper says so. In each simulated policy, charge the full frontier cost when the policy uses it, stop charging small-model and router work after the handoff, and never let the frontier answer or its result enter router features.
- **This also gives a counterfactual label:** whether the frontier solves each task. That supports an oracle "value of escalation" policy as an upper bound.
- **Hint mode is a stretch goal.** It cannot be replayed offline, because after a hint every later checkpoint changes. If kept, allow at most one hint per attempt and precompute the small model's continuation after each hint.
- **Takeover with context is a secondary result (supplement only).** Question: at the same escalation decisions, does passing the small model's code and execution history improve terminal takeover? The frontier gets the task, the visible tests, the current code and its visible-test output, and the previous round's code and output, but no thinking. One call per checkpoint, on attempt 0 of the test tasks only (prespecified; about 500 calls, $10–15). Use the same frozen policies and thresholds as the main mode, compare both modes on exactly the same checkpoints with task-clustered intervals, and label checkpoint-weighted results as such. Never pick a "best policy per mode" on test outcomes. Cut on October 16 to protect the deadline; not run.
- **Replay boundary.** Any mode that returns control to the small model after a frontier call breaks replay, even when the frontier never sees the small model's work. Terminal takeover stays replayable with or without context.
- **Live integration audit (not an equivalence test).** On 10–20 development tasks that cover every branch, plus scripted timeout and missing-score cases: (1) drive the online controller with recorded responses and require the same first-escalation checkpoint, terminal answer, calls, token totals and additive charges as the replay evaluator; (2) run one frozen policy live against the real API and check each decision against its feature vector, the exact helper prompt, one helper call per escalation, no small-model generation after it, the decision order at a visible pass, and that actual usage matches the ledger. A difference in these invariants is a bug; a fresh answer that differs from a logged one is not.

## Routers

**Primary:**

1. **Jev 1.13,** zero-shot, through the vendor's direct API (POST https://api.typesafe.ai/v1/systemone, key in TYPESAFE\_API\_KEY), as a feature extractor. One request asks all the typed drift questions about one state (vendor docs: every question is evaluated against the same state), so each evidence arm gets its own state and its own call. "jev-latest" is an alias with no documented way to pin a version; the API reports jev-1.13.0, and a run stops if the returned version changes. Get the per-option probabilities, check variation and ties, and log bytes, billed usage and the returned model version. The first smoke tests gave yes/no probabilities with two decimals, one saturated choice answer (1.0 and 0.0), and changes of about 0.01–0.02 between identical calls.
2. **Pinocchio-0.8B,** an off-the-shelf correctness calibrator (`pip install pinocchio-uq`; Qwen3.5-0.8B base with adapter `KevinDavidHayes/pinocchio-0.8b`; Apache 2.0; runs on a CPU). It beat Jev directly, 0.868 vs. 0.666 AUROC. Score complete checkpoint answers only: on single reasoning steps it scored 0.53. It is also the operational fallback if the Jev integration fails the technical gates.

**Stretch goal, if time permits:** one fine-tuned Qwen3-1.7B router, LoRA plus a binary failure head. Cut on October 16 to protect the deadline; not run. Train on the MBPP+ development tasks only (about 151), with task-grouped out-of-fold checks inside them, and score it on the test split, with one seed and no recipe search. Give it the same evidence and byte budget as Jev. Qwen3.5 checkpoints include a vision encoder and need nightly vLLM, and the Tev1 recipe is only a starting point. Fine-tuning adds no novelty (SWE-Router already trains a trajectory reader), so report it as a comparison.

**Cut for October 29 (only if time is left after the core results):** Drex v1.5, Liquid d1-3B, hint mode, SmolLM3-3B, thinking-off runs, hidden-state probes, mutated-input disagreement, the base and base + trace ablation cells, and query-only routing.

**Dropped:** Laya (order-sensitive, overconfident, short context), hosted Liquid d1 (free tier unverified), and the 5-fold Qwen3.5-4B fine-tune.

**What System One reads.** One architecture, no score fusion. Each checkpoint gets one canonical base state that all arms share. An arm adds blocks to it, and each arm is a separate Jev call.

- **Base state:** the task, the current code, the visible test output (bounded by a fixed rule), and loop telemetry: change in pass count, similarity to the previous attempt, and whether the same error or failing tests came back.
- **History block:** the previous code and its test output.
- **Trace block:** the current round's thinking, taken from its start and its end in the bytes that remain under the budget, with the omitted middle marked.
- **Byte budget:** every request, with its questions and instructions, stays under 56,000 bytes of text (evidence-v3). The earlier 28,000-byte budget rested on an unconfirmed note about a long-context mode above about 32,000 bytes; third-party sources instead give 32K tokens for the state. Measured on October 16 with jev-1.13.0: at 28,000 bytes the trace was cut on 118 of 621 development checkpoints (Jev read a median 79% of those traces); full-trace requests up to 55,776 bytes (14,320 input tokens) were all valid with unchanged latency (median 130 vs. 128 ms), and on the 15 re-sent checkpoints the thinking-question scores moved 2–4 times the cut-vs-cut noise (mean change at most 0.034). The largest 8K-cap request is 41,855 bytes, so no 8K trace is cut; 56,000 is also the largest size tested live. Enforce bytes directly, not tokens. If the base and history alone are too long, cut the task to 4,000 characters and the current and previous code to 6,000 characters each (start and end kept), for every arm of that checkpoint, and mark the records base\_trimmed. If even that does not fit, record every arm as evidence\_too\_large. Report both kinds of case separately. Log original and retained trace lengths.
- **Arms:** base + history, and base + history + trace. Both arms are built together on one shared base. The history arm answers the three code questions; the trace arm answers the same three plus the six thinking questions. The trace contrast is defined by feature sets, not by arms (see the secondary claim): it adds the block of thinking answers to the code-and-history predictor, and its code answers always come from the history arm.
- **Why the trace is a separate block:** confident traces can talk monitors out of obvious failures (CoT Red-Handed, a study of sabotage, not ordinary bugs), so the trace adds features and the predictor sets their weight.
- **No trace statistics in System One's base state.** It gets six code-and-test telemetry numbers (visible pass fraction, pass-count change, similarity to the previous code, same error, same failing tests, return to earlier code). The cheap baseline has the same numbers, so Jev's gain is measured over them. Trace length, cap hits and marker counts stay in the baseline only.

**Typed drift questions** (yes/no questions with explicit true and false criteria, frozen before the pilot; results per question are exploratory). On development data only, also try one 3-level score question, read as its probability-weighted level; in Just Ask Jev the generic 3-level score beat the generic yes/no question by +0.024 AUROC on average over 31 benchmarks:

| Question about the thinking | Evidence it needs | Not applicable when |
| --- | --- | --- |
| Is the model working on the assigned problem as it is stated? (a bug it does not notice is still on task) | task + trace | never |
| Is it repeating a fix that already failed? | history + trace | round 1 |
| Does it change approach without new evidence? | history + trace | round 1 |
| Does it make claims about the code or API that the evidence does not support? | code + trace | never |
| Does the stated fix match the code change? | history + code + trace | round 1 |
| Does it have a clear next step? | trace | the visible tests pass |

The three code questions need no thinking and are asked in both arms: is the current code likely to fail on valid inputs beyond the visible tests; does it special-case the visible test inputs; is it essentially the same as the previous attempt (not applicable in round 1). Empty thinking makes every thinking question "not applicable". "Not applicable" is coded separately from "symptom absent". The models are never asked to reconstruct missing history.

**Design details:**

- **Router question:** the typed drift questions above, in the original framing ("is the model drifting, lost or hallucinating?"). The escalate-or-continue decision comes from the supervised predictor's failure probability and a threshold chosen on development tasks.
- **Option order:** for choice questions, score both option orders and average them; both requests must fit the byte budget. Yes/no questions return one probability.
- **Fitting:** one L2-regularized logistic regression per pipeline, with the same scaling, data and regularization rule for both. Use task-grouped out-of-fold predictions on development tasks. No separate calibration split, no extra Platt layer, and no feature-subset or interaction search.
- **Labels, kept apart:** (1) checkpoint failure, where the current code fails the withheld tests, is the primary label. (2) Continuation failure: the rest of the small model's loop ends in failure. (3) Escalation value: the signed outcome difference between takeover and continuation, with their remaining costs. This also counts harmful switches, where the small model would pass and the frontier fails.

## Drift labels (supporting result)

Cut on October 16: the resource guide fell below its rule, and the cut is now final, not provisional. As planned before the cut: two frontier models label drift on a fixed, task-diverse sample of development checkpoints. The result supports the primary claim; it never claims that Jev detects drift.

- **Labelers:** one Claude model and one GPT model, through OpenRouter. They never see hidden-test results, later rounds, the frontier helper's output, Jev's scores, or each other's labels.
- **One labeling guide** for the labelers and for Jev's typed questions: task drift, reasoning drift, hallucination (a claim the supplied evidence does not support; unsupported does not mean false), and lost. Categories can overlap. Each has examples and exclusions: a tentative hypothesis, or an error the model corrects later, is not a hallucination.
- **Evidence spans:** labelers quote the span behind each label and may answer "insufficient evidence".
- **Freeze** the guide and Jev's thresholds before the agreement analysis. If labels on development data guide a change, report agreement on an untouched subset.
- **Report** Claude–GPT, Jev–Claude and Jev–GPT agreement separately per category, with prevalence, raw agreement, Cohen's kappa and task-clustered intervals. Keep disagreements; do not build a consensus "gold" set.
- **Sample:** a fixed sample of about 300 checkpoints from many tasks, not every development checkpoint (labeling all of them would cost about $90).
- **Limit:** with no human check, agreement shows reproducibility under one rubric, not independent truth. Frontier judges can also be persuaded by confident traces.

## Baselines

- Always use the small model; always use the frontier.
- Escalate if the visible tests fail.
- Escalate after k failed rounds.
- Rule baseline (if statements): escalate if the pass count didn't rise, the new code is a near-copy of the last attempt, or the same error came back.
- **Cheap-feature logistic regression (mandatory):** visible tests passed, round number, error or traceback type, code length, trace statistics (length, cap hit, "wait"-marker count), simple structural repeats (repeated code or error, return to earlier code), and a small prespecified logprob summary. The primary test compares it with and without the Jev features.
- Token-entropy threshold, and an adaptation of DeepConf's logprob confidence. Collect top-k logprobs from the start, because selected-token logprob alone is not its metric. Mandatory, because it needs no extra generations.
- Pinocchio-0.8B on the full checkpoint answer. Time-boxed: install it and pass a development smoke test on October 16–17; if that fails, report it as a missing comparison.
- Blind resampling: retry from scratch instead of revising. At 1.5B on MBPP+, this beat revising with test feedback. Whether that holds for a thinking model is unknown. Run only if it needs no new code path; otherwise cut (October 16).
- Random escalation at the same rate as each policy.
- Oracle value-of-escalation policy, as an upper bound.
- Optional: a generic LLM judge (Claude Haiku 5.5) as a control. Cut unless it needs no new code path (October 16).
- Cut for October 29: the thinking-off generator, query-level routing, the hidden-state probe, the extra ablation cells, and an always-Haiku solver (needed only for a "cheapest solution" claim, which the paper does not make).

Prior work, Model Cascading for Code (2024), already escalates on self-generated tests and cut cost 26% on average (up to 70%). Our test-based baselines use only the fixed visible tests, not generated tests, so they are not its equivalent: policies that use only the visible-test outcome are blind within the visible-pass subset, and a generated-test baseline is a stated limitation. We must still beat the visible-test baselines, not just the always-small model. Newer close work (CodeMonitorBench, SWE-Router) is listed under Related work.

## Evaluation and statistics

- **The unit of analysis is the task.** Attempts from the same task are correlated. Point estimates are pooled over checkpoints, and the paper says so; report task-weighted results where they differ.
- **Fixed 40/60 development/test split by task,** stratified by benchmark (about 217 development and 325 test tasks), frozen before the pilot. Development data fits the logistic regressions, picks thresholds and runs the gates, with task-grouped out-of-fold predictions. Test outputs and labels stay unopened until the protocol is frozen. The stretch fine-tune trains on MBPP+ development tasks only.
- **Confidence intervals from a bootstrap that resamples whole tasks.**
- **One primary comparison:** the cheap-feature L2 logistic regression with vs. without the Jev features, on the whole visible-pass subset of held-out test tasks (paired ΔAUROC). One explanatory contrast: the feature-set trace contrast defined in the secondary claim. Use Holm across these two tests (familywise α = 0.05); all other comparisons are descriptive. The test (frozen October 16): a two-sided paired task bootstrap centered on the null (Hall and Wilson), 19,999 replicates, resampling whole test tasks within benchmark with all their rows and both predictors' scores; p = (1 + #{|Δ\* − Δ̂| ≥ |Δ̂|}) / (B + 1). Report Δ̂, the Holm-adjusted p and the unadjusted 95% interval (predict.bootstrap\_test and predict.holm). Frozen descriptive sensitivities, selected on development data on October 16 after the predict-v2 freeze, before any test trajectory existed: cheap + the four answers code\_likely\_fails, special\_cases\_visible\_tests, on\_task and unsupported\_claim (one LR refitted on all development visible-pass rows), and the equal-weight mean of the same four answers oriented by the rubric (on\_task as 1 − p; a structural NA counts as 0.5 and the denominator stays 4; a failed scoring call leaves the row out of that comparison, with counts). It is a dev-selected heuristic score, not a calibrated probability. These sensitivities never change which analysis gives the primary conclusion. Descriptive audit on test: the standalone AUROC of each answer, with applicable rows and positive tasks, by benchmark and cap hit. Operating points: at escalation rates frozen on development data, for cheap, cheap+code and the full set, the share of hidden fails escalated and the residual hidden-fail rate among accepted checkpoints; with frontier outcomes, rescues, harmful switches, the net pass gain and the total cost. Never pick a "best router" on test results.
- **Choose thresholds on development tasks,** and report the realized test FPR and FNR.
- **Router metrics:** AUROC, AUPRC with prevalence and task counts, Brier score, and FNR at 5% FPR (1% and 10% exploratory), split by visible-test status, benchmark and checkpoint. These match CodeMonitorBench's metrics. Compute Brier on the predictor's failure probability, not on raw Jev answers. Also report AUROC within each task across its 5 attempts, with the count of tasks that have both outcomes. ECE and per-round detail go to the supplement.
- **Power:** the detectable difference depends on the positives and the pairing: about 0.08–0.12 with 50–100 positives and strong pairing, and 0.13–0.18 with weak pairing. Estimate the standard error of the paired difference on development data with a task-level bootstrap. Use CodeMonitorBench's verifier results (AUROC 0.54–0.67 for 7–8B open verifiers) as context only, not as a prediction for Jev.
- **Policy metrics:**
  - pass rate vs. cost per task, under both named cost views (see Cost ledger)
  - frontier tokens and calls per task, and local GPU seconds per task, reported separately
  - escalation rate, and the break-even escalation rate under each cost view
  - router overhead, as a share of total cost and per decision
  - always-small and always-frontier on every curve, even if always-frontier wins
  - no presumed headline: report "X% of always-frontier accuracy at Y% of its cost" only if a policy achieves it
- **Latency:** dollars, tokens and GPU time are the primary cost measures. Latency from offline replay is reconstructed, not measured end to end, and is labeled so. Report hosted routers as network-inclusive, Pinocchio as CPU time, and the small model as GPU time on the RTX 3070. Do not rank routers by latency.

## Go/no-go after the pilot

The gates check that the measurement can run. They never decide the result, and the primary comparison stays the same whatever they show. Fix them before the pilot.

1. **Technical gates for Jev:** measured on development checkpoints. Record the share of valid responses and of calls that fail after retries, per arm, with "not applicable" kept apart from failure. For each feature, record the count of distinct values, the share at the most common value and at 0 or 1, and the spread. Record the share of failing/passing pairs on visible-pass checkpoints with the same score, the duplicate feature vectors, and the score changes on a small repeat sample with the same evidence and model version. Every request must fit the byte budget. Do not gate on distinct values divided by sample size, and do not reject a feature only because many values are at 0 or 1. If Jev fails them, Pinocchio-0.8B becomes the main judge, and the paper says why.
2. **Headroom gate for the generator:** a final hidden-test pass rate of about 50–80%, and at least 30 projected positive test tasks (see the pilot). If not, apply the fixed fallback list, then freeze.
3. **Resource guide, not a result:** if LR + Jev beats LR by at least 0.03 AUROC out of fold on development tasks, spend the time on the full typed questions and the drift labels. If not, keep Jev in the primary comparison but cut those extras first.

**Gate results (October 16, development data only).**

- **Jev technical gates passed.** 621 checkpoints in both arms plus a 40-checkpoint repeat sample: 1,322 calls, all valid on the first try, one model version (jev-1.13.0), no trace cut, no request over the budget, about $0.15. No feature sits at 0 or 1. Repeat scores with identical request bytes moved by at most 0.05. Weakest code feature: special\_cases\_visible\_tests (history arm: 41% of values at its mode, 24% of visible-pass fail/pass pairs tied). Gates in results/jev\_gates\_pilot-v1+pilot-v1b.json.
- **Resource guide: below the rule, so the drift labels and the 3-level score question are cut first** (revisit on Oct 21 for schedule reasons only, never after a result). Visible-pass development checkpoints: 470, with 116 hidden fails from only 49 tasks; 431 are round 1, so the history questions rest on 39 checkpoints and clear\_next\_step never applies. Out-of-fold AUROC, pooled over checkpoints (task bootstrap): cheap 0.796 (0.721–0.864), cheap+code 0.815, cheap+code+thinking 0.803; primary gain +0.007 (−0.045 to +0.046), below the 0.03 rule. Task-weighted sensitivity: cheap 0.770, cheap+code 0.822, full 0.806; gain +0.036 (−0.011 to +0.087). The rule stays pooled; the weighting result is reported, not used. The secondary contrast is −0.012 (−0.042 to +0.008) pooled. Same-question contrast (descriptive): code\_likely\_fails 0.786 without the thinking vs 0.796 with it (+0.009, −0.027 to +0.054); special\_cases\_visible\_tests 0.778 vs 0.750 (−0.028, −0.093 to +0.044); in the predictor, cheap + code answers 0.815 (history arm) vs 0.810 (trace arm), −0.018 to +0.009 pooled. Thinking answers alone: on\_task 0.194 (higher on\_task, fewer fails; 0.806 as a separator), unsupported\_claim 0.718; the round-2+ questions rest on 39 checkpoints. Reading: the thinking answers carry signal alone, but on development data they add little to the cheap features and the code answers. Overlap is a possible explanation, not an established mechanism (removing the logprob columns lowers cheap only to 0.789), and the trace-arm answers also see the code, so their signal is not from the thinking alone. Script: scripts/analysis/trace\_effect.py.
- **What it means:** no incremental gain shown under this pipeline, not equivalence (the interval includes +0.03). The cheap baseline is strong (logprob confidence, thinking length, code similarity). Framing to keep: the primary test is about typed judgments of the code and of the reasoning, and the trace contrast is about semantic judgments beyond cheap trace statistics and logprob summaries, not reasoning access against none.
- **Corrections before the freeze (predict-v2, made once after a second-opinion review, defined from the schema):** the first run (predict-v1: 0.794 / 0.814 / 0.802, gain +0.008) had one identical missing-value indicator per round-1 feature, which changed the L2 penalty between the compared models; the timeout error was matched in the wrong case; the cheap baseline lacked same\_failing\_tests\_as\_previous; and the columns depended on the data. predict-v2 fixes the columns by a schema, uses one shared first\_round and trace\_missing indicator in every feature set, keeps per-feature indicators only for non-structural missing values, refits one LR per feature set on all visible-pass development rows as the test predictor, and accepts only development runs and scores whose request hash matches the trajectory. C = 1, the feature sets and the rule are unchanged. Both results stay on record; the pipeline is frozen after this rerun.
- **Still to freeze before the replay:** nothing in this item (all frozen on October 17). Threshold objective: escalation budgets, not a dollar objective. Three operating points by the share of visible-pass decisions escalated (q\_VP = 10%, 25%, 50%), plus the 0% and 100% endpoints. Each threshold is the weighted quantile of the router's out-of-fold development scores (the strong4 mean: its scores), each visible-pass row weighted 1 / (the number of sampled attempts of its task), which reduces to the pooled quantile when every task has five attempts as on test; pooled and attempt-0-only quantiles are sensitivities. Ties: escalate if s > t, or s = t and u < α, with α filling the boundary mass on development data and u a frozen hash of the checkpoint; t and α are frozen in configs. Missing score (a failed Jev call): the cheap LR at the same operating point decides, and the failed call is charged. Two analyses on test: (a) deployment view, the frozen threshold values with the frozen final models, reporting the realized rates; (b) ranking view, label-free top-K on the test scores at exactly 10/25/50% (ties by the same hash), which compares ranking at identical budgets and is labeled as a batch analysis. Central replay result: the paired net pass gain (percentage points of final hidden pass per attempt, mean over the three frontier replicates) over random escalation at each policy's realized rate, computed in closed form, plus the gain over forced-failure-only (q\_VP = 0), rescues, harmful switches, and frontier calls per attempt with optional and forced calls separated (q\_total = f + (1 − f) q\_VP; f = 6.9% on development data). Endpoints: always-small (no frontier calls), forced-failure-only, and always-frontier (frontier answers directly, no small-model run). Within-benchmark matched random is descriptive. Bootstrap whole tasks within benchmark with all attempts, replicates and scores; the replay is descriptive, outside Holm. Frozen on October 16, the rule at visible-fail checkpoints, the same for every visible-pass routing policy and its rate-matched random comparator: in rounds 1 and 2, continue the small model's repair loop with no judge call and no escalation; in round 3, a terminal frontier takeover (one answer, no repair). Missing code and timeouts count as visible failures. The policies therefore differ only at visible-pass checkpoints; always-small and always-frontier stay separate anchors, and any early visible-fail cascade is a separately named baseline. Frontier samples: three per task stay the target; one per task (325 calls), chosen uniformly before any test outcome, is the emergency floor. Fallback: if the replay is not validated by October 20 (decisions, charging and paired outcomes checked), the paper narrows to failure prediction and selective acceptance and drops the escalation claims.

## Offline replay

At every checkpoint, log the small model's state, every router's score, and the frontier takeover result for that task. Any threshold policy can then be simulated offline with no new API calls. Conditions: continuing never changes prompts, decoding, revision rules or visible-test stopping; decisions use only evidence available at that checkpoint; router scores follow the deployed procedure, including missing scores; and the escalation decision comes before a visible-pass candidate is accepted (the loop never revises after a visible pass, so at a visible pass the only actions are accept or escalate). Charge generation, visible execution and every router call the policy needs up to the escalation checkpoint, then the frontier call; charge nothing from the unused rest, and charge Jev only to policies that use it. Token counts and additive charges replay exactly; electricity and wall time for a hypothetical policy are an allocation model, because early exits change batching, and the paper labels them as estimates.

## Cost ledger

- **One row per HTTP attempt, linked by call\_id and http\_attempt and with a status field; retries and failures are included, and unknown usage stays null** in an append-only JSONL file, for the small model, routers and frontier alike. Fields: `task_id`, `attempt`, `step`, `component`, `model`, `provider`, `input_tokens`, `output_tokens`, `reasoning_tokens`, `usd_reported`, `latency_ms`, `gpu_seconds`, `ts`.
- **Pin a dated `prices.yaml`.** Compute dollars as tokens × pinned price and cross-check against OpenRouter's reported cost.
- **Price local GPU time** in two named cost views. Owned hardware (main view): API spend plus electricity for the local GPU; an RTX 3070 draws about 220 W, so at an assumed $0.15/kWh one attempt costs about $0.0003. Measure it: each run samples GPU board power every 2 s and integrates it per session, and records vLLM's own counters (tokens, KV-cache preemptions) at the start and end of each session. Cloud-equivalent (sensitivity view): GPU time at the A10G on-demand EC2 rate of $1.006/hour, a hypothetical normalization of 3070 runtime. Report the break-even escalation rate under each view: local work plus judging must cost less than the frontier calls it avoids. Never call local inference free; say "electricity-only marginal cost".
- **Log router calls even when the router says "continue."** Li (2026) left out the pre-screen model's own cost, and a reported 23.9% saving turned out to be 4.3%.
- **Track actual spend separately** on OpenRouter's Activity page and on the TypeSafe account, and set a credit limit on both keys. A sum of computed dollars is not total spend: report the attempts with unknown cost (for example timeouts) next to it.
- **Charge everything a policy needs:** every resample, probe-input generation, execution, feature extraction, retry, and every view and option-order call. Keep experiment spend, simulated deployment cost and training amortization separate.

## Budget

- Frontier takeover calls (measured October 17): 651 development calls (217 tasks × 3) cost $1.30, $0.0020 per call; 975 test calls are expected to cost about $2–3. Takeover with context and hint mode are cut.
- Router calls (Jev, direct API): the vendor docs give no price. One smoke call used 502 input and 70 output tokens. Confirm both token prices on the TypeSafe account; until then the ledger leaves dollars empty, and the estimate is two arms × every checkpoint at that price. Pinocchio-0.8B runs locally at no API cost.
- Rented A10G for fine-tuning and full-precision runs: about $10–25.
- Drift labels: about $12–20 for two labelers on about 300 checkpoints (about $3 per labeler per 150 checkpoints at Sonnet 5.5 prices; check the GPT labeler's price).

## Compute and environment

- **Local machine:** Windows with an RTX 3070 (8 GB).
- **Docker setup:** Docker Desktop with the WSL 2 backend, a current NVIDIA driver installed on Windows, and an up-to-date WSL kernel (`wsl --update`). Confirm GPU access with the CUDA nbody sample container.
- **Two images:**
  - a `gpu` image built on a pinned official vLLM image, for the small model and any local routers
  - a slim `cpu` image for API routers, replay and analysis, which runs on any laptop, including Macs
- **Pin every version** in a locked requirements file plus `docker-compose.yml`.
- **Secrets** go in a `.env` file listed in `.gitignore`.
- **Mount `data/` and the Hugging Face cache as volumes** rather than baking them into the image.
- **Sandbox generated code:** run the tests with timeouts and `--network none`.
- **Generate the small model's trajectories once** on one machine and share the logs. Different GPUs produce slightly different outputs, and Docker does not fix hardware differences.
- **Windows tips:**
  - Keep the repo inside the WSL filesystem, not on `C:`.
  - Raise WSL's memory limit in `.wslconfig` if needed.
  - Start vLLM with `--gpu-memory-utilization` and `--max-model-len` set so the model fits in 8 GB.
- **Cloud GPU:** a plain EC2 `g5.xlarge` (A10G, 24 GB) at $1.006/hour runs the same image and is cheaper than a SageMaker notebook at $1.41/hour. Shut it down when idle.
- **First milestone:** a `make smoke` command that runs 5 HumanEval+ tasks end to end, including the cost ledger.

## Timeline

| Dates | Work |
| --- | --- |
| Oct 16–17 | Done: the split, loop rules, typed questions, byte budget, images, harness, cost ledger, pilot, gates and resource guide. Now: freeze the predictor, the sensitivities, the policies, the thresholds, the missing-score rule, the test procedure and the paper scope. Time-box the Pinocchio install. Start the paper skeleton and methods. |
| Oct 18 | A working development replay with branch and cost checks, and a verified frontier route. Freeze the protocol. |
| Oct 19–20 | Generate test trajectories (325 tasks × 5), grade them, and collect three from-scratch takeover answers per task (one is the floor); run the live integration audit. If the replay is not validated by Oct 20, narrow the paper (fallback). |
| Oct 21–23 | Score test checkpoints with the frozen pipelines, run the two tests and the sensitivities, replay the policies under both cost views, and write a complete five-page draft. (The fine-tune stretch goal is cut.) |
| Oct 24 | Lock the experiments. |
| Oct 25–27 | Audit the claims, reproduce the headline results, and edit the paper. |
| Oct 28 | Audit claims and figures, reproduce the headline results, and submit. |
| Oct 29 | Hard deadline, 11:59 PM AoE. Buffer only. |

## Paper outline (5 pages)

- **Sections:** introduction, related work, method, setup, results, and discussion with limitations.
- **Exhibits:**
  - Table 1: LR, LR + Jev, Pinocchio and the logprob comparator on the visible-pass test subset, with AUROC and CI, the paired ΔAUROC and CI, AUPRC and FNR at 5% FPR. The caption gives prevalence and task counts and separates standalone judges from feature additions.
  - Figure 1A: the paired trace contrast (ΔAUROC and CI), with zero and the prespecified meaningful gain marked.
  - Figure 1B: pass rate vs. cost under the owned-hardware view, with always-small and always-frontier; break-even values in the caption.
  - Drift-label agreement: a few sentences; per-category tables in the supplement.
- **Supplement:** ECE, Brier detail, per-round results, the full cost ledger and extra evidence cells.

## Related work to cite and differentiate

**Must cite:**

- **Fast Models, Slow Evidence** (Li, 2026), arXiv:2610.02267. Neither Jev nor Laya beats chance at zero-shot model routing, while evidence-judging works. This is our motivating null result. Jev's 99.5% "cheap" decisions do not by themselves prove chance-level ranking.
- **CodeMonitorBench** ("Code Monitor Red Teaming for Public-Test-Passing Code"), [arXiv:2607.20852](https://arxiv.org/abs/2607.20852). Weak LLM verifiers look for hidden bugs in code that passed the public tests: 7–8B open verifiers reach AUROC 0.54–0.67, GLM-5.1 0.83. It already defines the visible-pass/hidden-fail setup. It has no reasoning trace, no repair history and no cost analysis; those are our differences.
- **SWE-Router,** [arXiv:2607.00053](https://arxiv.org/html/2607.00053v1). A LoRA value head on Qwen2.5-Coder-7B reads a cheap agent's partial trajectory and chooses to continue or to restart with a strong model, on SWE-bench. It already covers trajectory-based code routing. We differ with a zero-shot typed judge, a 1.7B generator and controlled evidence ablations.
- **Playing Psychic,** [arXiv:2604.16931](https://arxiv.org/abs/2604.16931). Thought-tree features of reasoning traces predict coding-task correctness for frontier reasoning models. "Traces reveal coding failures" is therefore taken; our question is the trace's added value beyond code, tests and history.
- **Pinocchio,** [arXiv:2609.24881](https://arxiv.org/html/2609.24881v2). An external black-box correctness calibrator. Appendix E.10 tests Jev directly: 0.666 vs. 0.868 AUROC on the same rows. Also one of our comparators.
- **Structural Baselines Matter,** [arXiv:2610.16661](https://arxiv.org/html/2610.16661). For agent failure detection, a zero-shot LLM judge scored 0.433 AUROC, below length (0.640) and step count (0.716). Report gains over content-blind baselines.
- **R2V-Agent,** arXiv:2605.16604. A step-level small-to-large router for agents, including HumanEval+ with write, test and submit actions. It needs an expensive distilled small model and measures cost as the share of steps escalated (cost ratio 50), not dollars. Its teacher acts on the full history state (Eq. 1, Algorithm 2) for one step, then control returns to the small model; the paper does not say clearly whether the reported results come from live teacher calls or logged rollouts. It is related work, not a protocol to reproduce: do not compare headline success rates, and do not use its routed-vs-oracle gap as evidence of missed visible-pass failures (the paper gives no such breakdown). Our position: we isolate whether typed judgments of reasoning add failure-prediction signal beyond execution evidence and telemetry, then measure their utility under a reproducible terminal-escalation policy.
- **Faithfulness as Information Flow,** arXiv:2605.24286. An LLM judge reads traces for hard-coding of visible tests, and RL-trained models often stop saying this in their reasoning. A direct risk for our trace questions: the thinking can hide the cause of a false pass.
- **Knowing When to Ask for Help: Bayesian Self-Escalation,** arXiv:2608.24087. Theory of escalation during generation, with only a small real-model test.
- **STEPGATE: "Do I Need the Cloud?"** [arXiv:2610.07816](https://arxiv.org/html/2610.07816). The paper header names the "SLMs for Agentic Systems" workshop (Paris, 2026) and gives no acceptance; the earlier NeurIPS attribution is unconfirmed. Uncertainty-based step-level handoff from Qwen2.5-1.5B to 7B on BFCL function calling and scripted multi-turn tasks. It has no code tasks and no dollar costs.
- **Model Cascading for Code,** arXiv:2405.15842. Escalation driven by self-generated tests, the prior form of our heuristic baseline.
- **The Handoff Tax,** arXiv:2608.24358. Escalating with the weak model's full trajectory recovers less than half the quality gap, which supports takeover from scratch. Its evidence is repository-level SWE-bench.
- **Just Ask Jev,** [arXiv:2609.29429](https://arxiv.org/html/2609.29429). Zero-shot Jev detects ten kinds of alignment failure, such as hallucination and reward hacking. One generic question reaches a median AUROC of 0.886 over 31 benchmarks, and targeted questions add only +0.006 (interval includes zero). So "Jev detects failures" is not new, and six questions are not expected to beat one on their own.
- **Automata from Agent Traces,** [arXiv:2608.23670](https://arxiv.org/html/2608.23670). A small state machine built from agent traces ranks failing runs from a partial trace (AUROC up to 0.94 on 12 datasets, including SWE-agent and SWE-smith). Cheap structural features can be strong, so our cheap-feature baseline includes simple repeat features.
- **The Tell-Tale Trace,** [arXiv:2608.03291](https://arxiv.org/abs/2608.03291). Reasoning-trace dynamics predict failures on SAT/UNSAT logic problems. Conceptual background only: no code, tests or escalation.

**Flagged by the reviewer, now read (summaries in research/drift-signals.md):**

- TACIT-Switch, arXiv:2608.27911
- TSDS, arXiv:2607.26865
- AgentCollab, arXiv:2603.26034
- GMI Router experiment: https://www.gmicloud.ai/en/blog/dynamic-model-escalation-for-coding-agents-a-gmi-router-experiment-across-two-harnesses
- Pinocchio, arXiv:2609.24881, an external calibrator for black-box models. It is the closest design to System One and a likely baseline.

**Background to cite:** FrugalGPT, RouteLLM, AutoMix, Co-LLM, Self-REF confidence tokens (arXiv:2410.13284), R2R token routing (arXiv:2505.21600), and a routing and cascading survey (arXiv:2603.04445).

**Claims to drop or soften:** do not claim to be first at public-pass monitoring, at trajectory-based code routing, or at using Jev as a correctness judge. Say "predicts checkpoint failure", not "detects drift or confusion". Treat the 1.7B model, the two benchmarks and the cost ledger as setting and design strengths, not contributions. Do not presume cost savings, and do not call local inference free. Correct two notes in research/: CoT Red-Handed's "CoT monitor" reads reasoning plus code, and Code-MUE's AUROC above 0.85 predicts whether any of N samples solves the task (0.635 at N=5).

## Open items

- Confirm the in-person presenter. The deadline is confirmed: October 29, 11:59 PM AoE.
- Jev smoke test done on the direct API (October 16): the key works, several typed questions per call work, responses pass validation, and the model reports jev-1.13.0. Still open: the token prices on the TypeSafe account, and whether the direct API has the long-context mode above about 32,000 bytes that OpenRouter describes.
- Write and freeze the labeling guide, the typed questions with their applicability table, the fallback list and the 0.03 resource guide before the pilot.
- Pick the GPT labeler and check its route and price on OpenRouter.
- Install `pinocchio-uq` and confirm that the weights load.
- Check whether CodeMonitorBench's data is released.
- Set a credit limit on the OpenRouter key.
