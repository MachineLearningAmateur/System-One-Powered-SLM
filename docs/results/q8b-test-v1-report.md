# Qwen3-8B held-out experiment — October 24, 2026

This is the aggregate report for run `q8b-test-v1`. The complete frozen
analysis is in [test_analysis_q8b-test-v1.json](test_analysis_q8b-test-v1.json).
Raw run data remain git-ignored under `results/runs/q8b-test-v1/` on the
operator's machine. No finished 1.7B result, frozen router, or old run was
changed.

## Protocol completion

- The frozen `q8b-protocol-freeze-v1` commit was `04a4306`. Qwen3-8B generated
  all 1,625 requested attempts on the 325 test tasks: 1,751 checkpoints, zero
  incomplete attempts or driver failures, 9.37 hours of generation.
- The Azure GPU app was deleted at 2026-10-24 05:32 UTC and the test resource
  group deletion was confirmed. Hidden grading started only after that, with
  the networkless sandbox. Both dataset reference calibrations and the 1 GiB
  memory canaries passed. The first two grades agreed on all 1,172 distinct
  candidate codes. After the prespecified HumanEval/32 exclusion, 1,745
  checkpoint labels were: 1,331 pass, 413 fail, 1 no-code, 0 invalid.
- Jev returned `jev-1.14.0` for all 3,502 scoring arms; every arm was `ok`.
  It used 8,128,261 input tokens, below the 15-million-token guard. No base
  evidence was trimmed and none of the 1,751 trace requests cut thinking;
  minimum and median retained thinking share were both 1.0. The largest
  request was 42,652 bytes against the frozen 56,000-byte limit.
- Local Pinocchio input v1 produced 1,751 `ok` records. Input v2 produced
  1,750 `ok` records and one expected `empty_answer` for a checkpoint without
  code. Every visible-pass analysis row had both Pinocchio scores. The planned
  analysis completed and all primary scores were present.

## Frozen held-out results

The confirmatory population has 1,580 visible-pass checkpoints from 321
tasks. Of these, 251 (15.9%) fail hidden tests, spanning 68 tasks.

| Frozen two-sided Holm test | AUROC comparison | Difference | 95% task-bootstrap CI | Holm p | At 0.05 |
| --- | --- | ---: | --- | ---: | --- |
| Primary: full vs cheap | 0.766 vs 0.750 | +0.0164 | −0.0001 to +0.0333 | 0.1099 | No rejection |
| Secondary: thinking beyond code | 0.766 vs 0.765 | +0.0014 | −0.0103 to +0.0127 | 0.8160 | No rejection |

Both tests used the frozen 19,999 paired whole-task bootstrap draws and the
two-sided Holm family. Neither planned gain is supported at familywise 0.05.
The task-weighted AUROCs, a named sensitivity, are 0.756 cheap, 0.771 code,
and 0.772 full.

Descriptively, the frozen strong4 mean reached AUROC 0.837, Pinocchio input
v1 reached 0.633, input v2 reached 0.551, and the logprob comparator reached
0.747. These are outside the Holm family. By benchmark, the full router
reached 0.809 AUROC on 477 HumanEval+ visible-pass checkpoints (40 failures)
and 0.765 on 1,103 MBPP+ checkpoints (211 failures). The 62 visible-pass
cap-hit checkpoints included 29 hidden failures. Round-specific visible-pass
support was 1,542 / 31 / 7 for rounds 1 / 2 / 3, so later-round contrasts
have limited support.

For the same-question code judgments, `code_likely_fails` had AUROC 0.831
from history and 0.834 with thinking. `special_cases_visible_tests` had 0.733
and 0.729. The code-only predictor had 0.765 and 0.766 using those respective
arms. Thinking-question AUROCs were 0.771 for `on_task` and 0.747 for
`unsupported_claim` on all 1,580 visible-pass rows. The round 2–3 questions
applied to only 38 visible-pass rows, including 19 failures on 10 tasks:
`repeating_failed_fix` AUROC 0.654 and `stated_fix_matches_change` 0.521.

## Descriptive comparison with the finished 1.7B study

The original 1.7B test had 1,457 visible-pass checkpoints, 280 hidden failures
(19.2%) on 89 tasks. Its cheap, code, and full AUROCs were 0.689, 0.744,
and 0.732. Its primary full-minus-cheap difference was +0.0437 (Holm p
0.0006); its thinking-beyond-code difference was −0.0121 (Holm p 0.01035).
The 8B population, failure prevalence, fitted routers, generator, and Jev
version differ. The old raw trajectories are unavailable in this clone, so
the prespecified same-request Jev drift replay could not run. The original
used `jev-1.13.0`; this 8B run used `jev-1.14.0`. These side-by-side values
are descriptive and do not identify an effect of model size.

## Spend and scope

- Azure app lifetime from the activity log: about 9.52 hours. At the queried
  West US 3 retail configuration rate of about $3.2004/hour, estimated active
  compute was **$30.47**, below the approved $60 test limit. The actual Azure
  invoice may lag and could differ.
- Jev's 8.128 million input tokens estimate to **$0.34** at TypeSafe's listed
  $0.042 per million input tokens, below the approved $2 limit. The actual
  account charge has not been reconciled.
- No new frontier calls or optional replay were part of the frozen core test.
  No test result was used to refit, select, or tune a router.

Sources: the operator-held `results/runs/q8b-test-v1/run_meta.json`,
`grade_meta.json`, `jev_meta.json`, `jev_ledger.jsonl`, and both Pinocchio
files; the aggregate analysis linked above; the original
[1.7B aggregate analysis](test_analysis_main-test-v1.json); and the Azure
activity log. Raw trajectories, scores, and labels are not included in git.
