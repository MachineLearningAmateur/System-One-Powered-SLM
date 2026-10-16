# Execution evidence, not confidence, exposes hidden drift

> **Corrections (2026-10-16, after a second-opinion review; sources re-checked):**
> - **Code-MUE's "AUROC above 0.85"** predicts whether *any* of N sampled programs solves the task, not whether the current program is correct. AUROC is 0.635 at N=5 and 0.782 at N=100 ([arXiv 2607.12273, §5.2.1, Table 3](https://arxiv.org/html/2607.12273v2)). Do not expect 0.85 from a 2–4-resample detector.
> - **The novelty claim below is superseded.** CodeMonitorBench ([arXiv 2607.20852](https://arxiv.org/abs/2607.20852)) already has weak LLM verifiers judge public-test-passing code for hidden bugs (7–8B open verifiers: AUROC 0.54–0.67). SWE-Router ([arXiv 2607.00053](https://arxiv.org/html/2607.00053v1)) already reads partial coding trajectories to choose continue vs. restart. The surviving contribution is the trace's added value beyond code, tests and repair history; see `docs/research-plan.md`.
> - **Jev on correctness:** Pinocchio Appendix E.10 reports Jev at 0.666 AUROC vs. Pinocchio's 0.868 on the same 1,718 text rows ([arXiv 2609.24881](https://arxiv.org/html/2609.24881v2)).
> - **SWE-Router**, listed below as unidentified, is arXiv 2607.00053. **Structural Baselines Matter** (2610.16661), listed below as unread, compares a zero-shot LLM judge (AUROC 0.433) with length (0.640) and step-count (0.716) baselines for agent failure detection.

The signals that best show a Qwen2.5-Coder-1.5B write→test→revise loop heading for failure are **trajectory and execution signals**, not the model's own confidence. The strongest are:

- stagnation of the visible-test pass count between rounds;
- near-duplicate consecutive attempts, which show anchoring;
- the class of error that persists (wrong-answer AssertionErrors are the hardest to repair);
- for the visible-pass/hidden-fail case specifically, **behavioral disagreement among independent resamples on new, mutated inputs**.

Token log-probabilities, verbalized confidence and the small model's self-judgment are weak, with AUROC around 0.5–0.67 on HumanEval+/MBPP+ even at 7B. They fail precisely on fluent, confidently wrong code, which is what the visible-pass/hidden-fail subset consists of.

This matters for the router. In a visible-pass case, "System One" sees only "all tests passed" plus the code. That makes it a black-box correctness judge in the style of Pinocchio, and published black-box judges partly predict task difficulty rather than the specific solution's correctness.

The practical recommendation is to have the harness compute a compact, cheap feature block at each checkpoint (after attempt 1, round 1 and round 2) and show it to the router alongside the task, code and test output. Then test whether the router beats four baselines: visible pass/fail, a logistic model on the same features, a token-statistics posterior (Bayesian Self-Escalation style), and blind resampling.

None of the eleven papers reviewed evaluates an external judge that reads execution feedback across revise rounds and is scored against hidden EvalPlus tests. That is the paper's opening. Its main risks are:

- small headroom and few visible-pass/hidden-fail cases;
- evidence that, at 1.5B, the repair loop itself underperforms blind resampling;
- several numbers in the notes that are unverified or internally inconsistent, flagged throughout.

## Confidence signals fail exactly where hidden tests bite

The intuitive first signal (the small model's own uncertainty) is the weakest one for this problem.

**Token statistics are weak.** On HumanEval+ and MBPP+ with four 7–8B code models including Qwen2.5-Coder-7B-Instruct, "**no metric exceeds 0.70**" AUC across 17 generation-stage and 6 prefill signals. Token log-prob AUC on HumanEval+ is 0.617–0.670 and entropy 0.615–0.639 ([arXiv 2610.11300](https://arxiv.org/html/2610.11300v1)). The same study finds models "most confident precisely when they are wrong": on BigCodeBench, incorrect generations carried *higher* mean confidence than correct ones (QwenCoder 0.920 vs 0.897). Platt scaling on MBPP+ cut Brier from 0.459 to 0.248 but left a Brier Skill Score of about 0.001 ([arXiv 2610.11300](https://arxiv.org/html/2610.11300v1)). Calibration can be repaired; discrimination cannot.

At the small end, mean token entropy correlates with HumanEval pass/fail at only −0.234 for Qwen2.5-Coder-3B ([arXiv 2608.14659](https://arxiv.org/html/2608.14659)). An ICSE 2025 study found that when average probability exceeded 90%, **only 52% of completions passed tests** ([arXiv 2402.02047](https://arxiv.org/html/2402.02047v4)). The notes contain no directly measured AUROC for the 1.5B checkpoint, so a 0.55–0.70 band is an extrapolation.

**Self-assessment is no better.** Judge-style self-assessment by 7–8B models on HumanEval+ scores AUC 0.507–0.601 ([arXiv 2610.11300](https://arxiv.org/html/2610.11300v1)). Verbalized confidence at 1.3–3B is essentially uncorrelated with correctness ([arXiv 2608.14659](https://arxiv.org/html/2608.14659)). Multi-sample P(True) is the exception: Pearson **0.78 for Qwen2.5-Coder-3B**, but only 0.30 for DeepSeek-Coder-1.3B ([arXiv 2608.14659](https://arxiv.org/html/2608.14659)). It must be validated on the actual 1.5B checkpoint before anyone relies on it. External judges do far better than in-house ones: an o4-mini judge reached F1 0.70–0.94, against 0.26–0.57 for DeepSeek-Coder models judging their own code ([OPENIA, arXiv 2501.12934](https://arxiv.org/pdf/2501.12934)). This is the core argument for an external System One.

**The failures that slip past visible tests are subtle logic errors**, such as comparing only adjacent pairs instead of all pairs, or sum vs difference of squares on MBPP/72 ([arXiv 2610.11300](https://arxiv.org/html/2610.11300v1)). The model emits these as fluent, high-probability tokens.

**Bayesian Self-Escalation**, the paper closest to this setup (Qwen2.5-Coder 1.5B→7B on sanitized MBPP), concedes this point. Its token-entropy/logprob/margin posterior reaches cross-validated AUROC 0.758, rising from 0.51 to 0.76 over the course of generation. But the authors state that **confidently wrong outputs cannot be rescued by thresholds** ([arXiv 2608.24087](https://arxiv.org/pdf/2608.24087)). The paper also has known limits: a single seed, greedy decoding, plain MBPP rather than MBPP+, no revise loop and no feedback from test execution.

**Hidden-state probes are the one white-box exception.** A correctness direction exists in the residual stream of Qwen2.5-Coder-1.5B-Instruct itself; steering along it moved MBPP+ pass@1 by up to +15.6% ([ICML 2026 DL4Code workshop](https://icml.cc/virtual/2026/82743)). That work reports steering effects, not detection AUROC. A linear pre-generation probe on Qwen3-4B reached AUC 0.881 on LiveCodeBench ([arXiv 2606.14530](https://arxiv.org/abs/2606.14530)). This conflicts with the 7B study's prefill signals, which peaked at 0.70 ([arXiv 2610.11300](https://arxiv.org/html/2610.11300v1)); the two differ in model, benchmark and the use of a trained probe versus raw signals. Probes fall outside the black-box router framing, so they work best as an optional "white-box ceiling" ablation, not the main method.

## Trajectory dynamics reveal stuck loops by round one

The repair-loop literature agrees on two points. Gains concentrate early, and stuck loops are visible early.

**Gains come in the first two rounds.** Across seven models on HumanEval and MBPP-sanitized, two repair rounds captured **76–95% of achievable gain**, and the first round was always the largest ([arXiv 2604.10508](https://arxiv.org/html/2604.10508v1)). Llama 3.1 8B repaired only 29.6% of initially failing HumanEval problems. By error type, about 77% of NameErrors and 66% of SyntaxErrors were repaired, against only about **45% (HumanEval) and about 63% (MBPP) of AssertionErrors** ([arXiv 2604.10508](https://arxiv.org/html/2604.10508v1)).

**Recovering and failing runs separate by the first refinement.** Holloway and Amin (ICML 2026) report that recovering and non-recovering seeds already differ by **42 points of pass fraction at the first refinement**. About **45% of non-recovering seeds stagnate**, passing the same number of tests round after round. Recovery was 76.6% when any of five seeds had solved the task and 22.9% when none had ([Lacuna summary](https://lacuna.tiptreesystems.com/work/rapid-fixes-gradual-failures-exploring-iterative-self-correction-dynamics-in/wrk_df921d1700de9c371cdfd5749b5f49de)). These numbers come from a third-party summary page, not the paper itself, so verify them against [OpenReview](https://openreview.net/forum?id=QSO4fnmXfR) before quoting.

**The most important result for this exact model** comes from a study of Qwen2.5-Coder 1.5B/3B/7B on 378 MBPP+ tasks:

- At 1.5B, feedback-conditioned repair is **no better than a content-free "placebo" retry**.
- Showing the model its own failed output cost **−0.061 pass@1 relative to blind resampling** (p=0.006).
- Conditioning on its own output raised similarity between consecutive attempts by 0.30–0.38. Near-identical retries (similarity >0.95) occurred in **33–68% of own-output retries**, against 2–14% for blind resampling.
- Higher similarity went with lower pass@1 ([arXiv 2607.26117](https://arxiv.org/html/2607.26117v1)).

The authors describe the similarity effect as directional, not a validated per-instance predictor, and found HumanEval+ underpowered for these contrasts. Two consequences follow. Consecutive-attempt similarity is a cheap and well-motivated drift feature. And the paper must treat blind resampling as a baseline; reviewers who know this result will ask for it.

**Agent-scale evidence points the same way.** Failed SWE-bench trajectories run 12.6–82.5% longer ([arXiv 2511.00197](https://arxiv.org/pdf/2511.00197)). Trajectory structure (read-first vs patch-first, and post-patch test-and-iterate loops) predicts outcomes better than length does ([arXiv 2604.02547](https://arxiv.org/pdf/2604.02547), via a secondary summary).

**Unquantified and unread items.** Oscillation (reverting to an earlier version) and identical repeated error messages are cited as reasons for iteration caps, but no source quantified them as predictors ([arXiv 2607.05197](https://arxiv.org/html/2607.05197v1)). The 2026 paper most likely to report structural-baseline AUROCs for agent failure detection, [arXiv 2610.16661](https://arxiv.org/html/2610.16661), could not be read: the request was rate-limited. It is a must-read before submission, because it could pre-empt the "structural features vs LLM judge" comparison.

## Differential behavior on new inputs targets visible-pass/hidden-fail

When every visible test passes, the router gets no failure signal from them. Something else must stand in for the hidden tests.

**The gap is real but poorly measured.** In a practitioner benchmark (a blog, not peer-reviewed), only **74% of MBPP+ tasks that Qwen2.5-Coder-7B recovered on visible tests also passed hidden EvalPlus tests** ([LeanLM blog](https://leanlm.ai/blog/llm-self-correction)). That sample is small (about 20 recovered tasks), the model is 7B rather than 1.5B, and the result needs replication in the team's own logs. No source in the notes measures the visible-pass/hidden-fail base rate for a 1.5B model. That number determines whether the paper's headline subset has enough cases to support AUROC claims.

**Execution-based agreement among samples is the strongest black-box signal.** Code-MUE samples programs, runs them on type-based boundary inputs plus LLM-proposed inputs, and computes von Neumann entropy over pairwise behavioral agreement. It reports **AUROC above 0.85 on multiple benchmarks** across 8 LLMs ([arXiv 2607.12273](https://arxiv.org/html/2607.12273v2)); the per-model tables were not retrieved. Self-generated tests reach AUROC **0.73–0.86 on HumanEval/MBPP** for 14–32B models. Dropping that functional axis cost 13.1 AUROC points ([arXiv 2606.09577](https://arxiv.org/html/2606.09577)). There is no evidence yet for either signal at ≤7B.

**The failure mode is common-mode error.** A prompt-diversity entropy ensemble showed **no signal on DeepSeek-Coder-1.3B** (Pearson +0.021) ([arXiv 2608.14659](https://arxiv.org/html/2608.14659)). That is consistent with small models sharing misconceptions across samples. The fix is to compare the loop's current code against resamples and against inputs a 1.5B model would not think of. Type-aware mutation of the visible inputs (EvalPlus-style) is the cleanest source. Fresh inputs proposed by the frontier model are an option, but they spend the budget the router exists to save.

**This feature has a leakage constraint.** The probe inputs must never come from the hidden EvalPlus suite. The harness records only whether programs *agree*, never whether they are *correct*.

**Special-casing is a second, near-free check.** Frontier agents cheat in documented ways: modifying tests, overloading `__eq__`, recording state across calls, and special-casing test inputs. LLM monitors catch 86–89% of this on Impossible-LiveCodeBench ([ImpossibleBench, arXiv 2510.20270](https://arxiv.org/pdf/2510.20270)). A 1.5B model is unlikely to cheat deliberately. Incomplete edge-case handling is the likelier cause. Still, a static AST scan for visible-test literals inside conditionals, plus a count of new `if`/`return` branches added in a repair round, costs nothing. No paper reports AUROC for these static checks.

## Black-box judges partly predict task difficulty, and the router must not

**Pinocchio's limits apply directly to System One.** Pinocchio is an external 8B (and 0.8B) calibrator that reads (question, response) and outputs P(correct). It reaches **AUROC 0.863**, against 0.649 for the best single-pass black-box baseline. The abstract says 0.862, a minor inconsistency ([alphaXiv](https://www.alphaxiv.org/abs/2609.24881v2)). With the question blanked, AUROC still reaches 0.805, which shows heavy reliance on response features. Within-question AUROC falls to **0.726** ([alphaXiv](https://www.alphaxiv.org/abs/2609.24881v2)). Pinocchio was not evaluated on code or routing, and it is not confirmed that the reviewer meant this paper rather than the 2024 factual-knowledge benchmark of the same name ([ICLR 2024](https://iclr.cc/virtual/2024/poster/19298)). Even so, its ablation template is exactly what a reviewer will ask for: show that the router separates good from bad attempts *within* a task, not just easy tasks from hard ones.

**Zero-shot routers can collapse.** For Jev, the evidence is a direct warning. In "Fast Models, Slow Evidence", **Jev answered "cheap" for 99.5% of routing requests**, which is chance on a balanced set, and Laya's AUROC was 0.48 ([arXiv 2610.02267](https://arxiv.org/html/2610.02267)). That test was pre-execution routing from request text alone, on mostly multiple-choice items labeled from single runs. It does not prove Jev fails mid-loop with execution evidence, but it predicts majority-class collapse when "on track" dominates. The same audit supplies a checklist: count the router's own token cost (a claimed 23.9% saving shrank to 4.3%); report end-to-end outcomes rather than gate accuracy; fit thresholds out of sample (in-sample thresholds gave held-out miss rates of 16.7–17% against a 5% target) ([arXiv 2610.02267](https://arxiv.org/html/2610.02267)). The notes contain nothing on Drex. Its architecture and any prior routing results must be supplied by the team.

**What the router should be shown.** At each checkpoint, show the task, the current code and the raw visible-test output, plus a short structured "loop telemetry" block the harness computes:

| Checkpoint | Telemetry fields shown to the router | Evidence basis |
|---|---|---|
| **After attempt 1 (R0)** | visible pass fraction; error class (Syntax / Name / Runtime / Assertion / Timeout); whether any of 2–4 cheap resamples passes visible tests; behavioral agreement of current code vs resamples on mutated inputs; hardcoded-literal flag; optional mean code-token logprob | first-round gains are largest; Assertion errors hardest; "any seed solved" prior ([2604.10508](https://arxiv.org/html/2604.10508v1); [Lacuna](https://lacuna.tiptreesystems.com/work/rapid-fixes-gradual-failures-exploring-iterative-self-correction-dynamics-in/wrk_df921d1700de9c371cdfd5749b5f49de)) |
| **After round 1 (R1)** | Δ visible pass count (0 = stagnation); similarity R1 vs R0 (>0.95 = anchoring); error-class transition and identical error signature; identical failing-test set; new-branch count when Δpass>0; refreshed disagreement score | 42-point early divergence; 45% stagnation; 33–68% near-duplicates ([Lacuna](https://lacuna.tiptreesystems.com/work/rapid-fixes-gradual-failures-exploring-iterative-self-correction-dynamics-in/wrk_df921d1700de9c371cdfd5749b5f49de); [2607.26117](https://arxiv.org/html/2607.26117v1)) |
| **After round 2 (R2)** | pass-fraction trend (rising / flat / regressing); max similarity of R2 to {R0, R1} (oscillation); repeated-signature count; tokens spent; for visible-pass code, the disagreement score and special-casing flags as a hidden-risk summary | about 50% of gain by k=2; visible-pass ≠ hidden-pass in about 26% of recovered tasks (7B blog) ([2607.26117](https://arxiv.org/html/2607.26117v1); [LeanLM](https://leanlm.ai/blog/llm-self-correction)) |

Two design choices follow.

First, run three router conditions with the same backbone: (a) task, code and test output only, as currently specified; (b) plus the telemetry block; (c) telemetry fed to a logistic regression with no LLM. Condition (c) is TACIT-Switch's approach in miniature. That paper learns a cumulative risk over hand-built diagnostics (repeated or invalid actions, uncertainty, stalled progress) and found online trajectory risk outweighed task features (71.35% vs 66.62% in its simulation) ([arXiv 2608.27911](https://arxiv.org/html/2608.27911v2)). If (c) matches (b), the contribution becomes "cheap features suffice", which is still a publishable finding. The note that STEPGATE's AUROC *rose* from 0.829 to 0.886 when its risk features were removed ([arXiv 2610.07816](https://arxiv.org/html/2610.07816)) is a reminder that adding features can hurt; ablate them.

Second, define what "needs help" triggers. The Handoff Tax found that continuing a weak model's full trajectory on a strong model recovered only **36–47% of the quality gap**, and aborting and restarting fresh dominated in the Claude pair ([arXiv 2608.24358](https://arxiv.org/html/2608.24358)). That evidence comes from SWE-bench with frontier pairs, not function-level code. "Consult" (frontier advice returned to the 1.5B model) and "restart" (frontier writes fresh code) differ, and reviewers will want both arms compared.

## Prior work leaves the execution-aware external judge unclaimed

The eleven papers cover adjacent ground, but none occupies this paper's cell:

| Paper | Signal | When | Code? | Key finding / caveat |
|---|---|---|---|---|
| TACIT-Switch ([2608.27911](https://arxiv.org/html/2608.27911v2)) | learned cumulative risk over diagnostics + task features; teacher-labeled censored intervention times | per checkpoint, permanent handoff | No (ALFWorld, DABench) | 4B pair 48.5% at cost 191 vs Pure 27B 50.7% at 231; DABench CI vs SWE-Router includes zero; diagnostic list φ not fully verified |
| TSDS ([2607.26865](https://arxiv.org/abs/2607.26865)) | edge-model perplexity on action, LTT-calibrated | per step | MBPP included | 43–65% thinking-compute cut (v3) vs 43–73% (alphaXiv, earlier version), unresolved; MBPP setup unread |
| AgentCollab ([2603.26034](https://arxiv.org/pdf/2603.26034v1)) | small model's own TRUE/FALSE "progress" self-check | per step, temporary escalation | No | 33.9% vs Large 34.6% at 1.36× speed; false-progress rate about 3–7% |
| GMI Router blog ([GMI Cloud](https://www.gmicloud.ai/en/blog/dynamic-model-escalation-for-coding-agents-a-gmi-router-experiment-across-two-harnesses)) | undisclosed P(fail) + loop/overrun head | live, mid-trajectory | Yes (Terminal-Bench) | rescued 3/9 always-failed tasks; 2/6 controls escalated falsely; n=15 trials, anecdotal |
| Pinocchio ([2609.24881](https://www.alphaxiv.org/abs/2609.24881v2)) | external black-box P(correct) | post-hoc | Unknown | AUROC 0.863; 0.805 with question blanked; identity of reviewer's "Pinocchio" unconfirmed |
| Fast Models, Slow Evidence ([2610.02267](https://arxiv.org/html/2610.02267)) | single-pass System-1 classifier | pre-execution | No | Jev at chance on routing; audit pitfalls |
| STEPGATE ([2610.07816](https://arxiv.org/html/2610.07816)) | six families incl. token uncertainty, K-sample consistency, history | before each action | No (tool calls) | 1.5B→7B: 69.0% vs 57.0% query-level at 30% cloud; **workshop acceptance unverified** |
| R2V-Agent ([2605.16604](https://arxiv.org/html/2605.16604)) | 15 features incl. entropy, verifier stats, step index | per step | Yes (HumanEval+, full EvalPlus label) | 94.3% at 0.6% calls vs oracle 98.6% at 8.1%; Table 9 (93.3% / 0.65%) conflicts with Table 2; 7–14B only |
| Bayesian Self-Escalation ([2608.24087](https://arxiv.org/pdf/2608.24087)) | token entropy/logprob/margin posterior | per token, one generation | Yes (MBPP, same 1.5B) | AUROC 0.758; "two of three predictions confirmed" means one untested; single seed |
| Model Cascading for Code ([2405.15842](https://arxiv.org/html/2405.15842)) | agreement on self-generated tests | between tiers, post-hoc | Yes (base HE/MBPP) | 26% average savings; negative savings with weak small models |
| Handoff Tax ([2608.24358](https://arxiv.org/html/2608.24358)) | none (fixed percentiles) | fixed | SWE-bench | handoff recovers 36–47% of gap; restart dominated |

**The novelty claim has four parts:**

1. An *external, black-box* judge that conditions on *execution feedback* across revise rounds. The nearest neighbors are white-box (Bayesian, STEPGATE, TSDS), self-judged (AgentCollab), or pre-execution (Fast Models).
2. A *visible-vs-hidden* split that isolates the subset where pass/fail carries no information.
3. Both HumanEval+ and MBPP+ at 1.5B.
4. A direct comparison of LLM judgment with structural telemetry.

R2V-Agent is the reviewer's likely "already done" objection, since it uses HumanEval+ with a test action and full-EvalPlus labels. The answer is its under-escalation: 0.6% routed against an 8.1% oracle. That gap fits failures that look fine to step-level features, which is this paper's thesis. This reading is an inference; R2V gives no breakdown by visible vs hidden outcome. Do not use this argument in the paper (Oct 16 review): see the R2V-Agent entry in docs/research-plan.md. Before claiming novelty, check [arXiv 2610.16661](https://arxiv.org/html/2610.16661), "Agent-as-a-Router" ([2606.22902](https://alphaxiv.org/audio/2606.22902v1)) and the unidentified SWE-Router paper. None was read.

**Reviewers will expect these baselines**, all evaluated at matched frontier-call rates:

- visible-test pass/fail alone (the claim's null);
- random escalation at the same rate (STEPGATE);
- the Bayesian token-statistics logistic posterior, refit per checkpoint;
- an entropy/perplexity threshold (TSDS/ReDAct, R2V's entropy router);
- the 1.5B model's own progress or P(True) self-check (AgentCollab-style);
- a logistic or cumulative-risk model on the telemetry (TACIT analogue);
- blind resampling with the same budget and no frontier call ([arXiv 2607.26117](https://arxiv.org/html/2607.26117v1));
- always-frontier and a hindsight oracle as bounds.

Report all of the following:

- AUROC overall and **on the visible-pass subset**;
- within-task or difficulty-matched AUROC (the Pinocchio template);
- end-to-end hidden-test pass rate vs frontier calls, *including router tokens*;
- escalation precision, since GMI's false escalations on easy controls cost $0.93–$1.51 each;
- thresholds fit out of sample, optionally with Learn-Then-Test guarantees as in TSDS.

## Conclusion

The evidence reframes the paper's claim. "The router adds signal beyond pass/fail" is too weak, and if the router sees only the code it is probably false on the visible-pass subset: published black-box and self-judges there sit near AUROC 0.5–0.7 and lean on task difficulty. The defensible and novel claim is narrower and stronger: **an external judge given cheap execution telemetry flags drift earlier and more precisely than either the telemetry or the code alone**. Its visible-pass leverage comes from differential behavior on mutated inputs, not from reading the code more cleverly. One more point argues for telemetry over confidence: at 1.5B the repair loop itself barely beats a placebo retry, so the router's real choice at round 1 is likely between three actions (keep repairing, resample, or escalate), not two.

The open risks are concrete:

- **Headroom and sample size.** HumanEval+ has 164 tasks and the visible-pass/hidden-fail base rate at 1.5B is unmeasured. Measure that rate first, since it decides whether the headline subset holds enough cases.
- **Label noise** from single seeds.
- **Majority-class collapse** in zero-shot routers like Jev.
- **Hidden-test leakage** when fine-tuning Qwen3.5-4B. Split by task, and ideally train on MBPP+ and test on HumanEval+.
- **Interpreting a negative result.** If consultation fails to rescue, that may reflect the Handoff Tax rather than detection quality.
- **Unverified numbers.** Several numbers this argument rests on are unverified or inconsistent: the Holloway and Amin figures (summary page only), the 74% hidden-pass rate (7B blog, about 20 tasks), STEPGATE's venue, R2V's table conflict, TSDS's 65% vs 73%, and the unread 2610.16661.

Run a small pilot logging all three checkpoints with hidden labels before writing results prose.
