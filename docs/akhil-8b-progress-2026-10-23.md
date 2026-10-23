# Qwen3-8B replication progress — October 23, 2026

This is a status handoff for the new 8B data collection on branch `akhil-8b`. It does not amend the finished 1.7B study. Read `AGENTS.md`, `docs/new-generator-runbook.md`, and `docs/q8b-plan.md` before continuing.

## Repository and protocol state

- Preparation was committed as `4d5b7cf` (`Prepare Qwen3-8B replication and Azure development protocol`). The 8B runs and hidden grading used a clean tree at that commit. No push was made.
- The development runs are `q8b-pilot-v1` and `q8b-pilot-v1b`; their raw data is under ignored `results/runs/`. Existing 1.7B runs, frozen configs, results, and `protocol-freeze-v1` were not changed.
- The 8B router file `configs/routers_q8b-v1.json` and October 23 part B of `docs/q8b-plan.md` are the freeze artifacts. Verify that `q8b-protocol-freeze-v1` tags their commit before test generation. No 8B test-split generation has started as of this handoff.
- The official EvalPlus JSONL hash discrepancy was traced to LF versus CRLF record separators. The parsed 164 HumanEval+ and 378 MBPP+ records are identical; the frozen source hashes and split were left unchanged.
- `uv run pytest -q` passed 175 tests after the 8B preparation commit. The earlier five-task Azure smoke passed visible tests and, in a separate exploratory local grade, all five hidden tests. It is not protocol data.

## Development generation and grading

The protocol development runs used BF16 `Qwen/Qwen3-8B` at revision `b968826d9c46dd6066d109eabc6255188de91218`, the pinned vLLM `v0.30.0` image, one Azure A100 replica, and concurrency 2. The first run covered attempt 0 on all 217 development tasks; the second covered attempts 1–4 on the frozen 72-task subsample.

| Run | Attempts complete | Checkpoints | Hidden pass | Hidden fail | Invalid grades |
| --- | ---: | ---: | ---: | ---: | ---: |
| `q8b-pilot-v1` | 217/217 | 228 | 178 | 50 | 0 |
| `q8b-pilot-v1b` | 288/288 | 310 | 225 | 85 | 0 |

- Both generation runs had zero driver failures, missing attempts, or KV preemptions. Generation took 4,548.3 and 6,981.3 seconds, respectively. Across the 505 attempts, final hidden outcomes were 403 pass and 102 fail; 56 of 538 checkpoints hit the thinking cap.
- Hidden grading ran locally only after the Azure vLLM app was deleted, in the networkless evaluation sandbox. Both grading sessions are marked protocol, with clean calibration and memory canaries, zero invalid labels, and no disagreement between the first two grades of any code. The sandbox was stopped afterward.
- The prespecified headroom gate passed. In the 72-task subsample, 9/22 HumanEval+ tasks and 14/50 MBPP+ tasks had at least one visible-pass hidden failure. Projected onto the test split, that is about 40.1 and 63.6 tasks respectively, or 103.7 total versus the required 30. The per-benchmark Wilson projected intervals were 22.8–60.0 and 39.7–94.6. All 20 planned seeds of five task-grouped folds had both classes in every fold, for both the visible-pass and all-checkpoint populations. No model fitting was done for this gate.
- Locally rebuilt Jev evidence fits the 56,000-byte request cap for all 538 checkpoints; none of the trace arms would truncate thinking. This is a request-size check, not Jev scoring.

## Pinocchio and Jev status

Pinocchio-0.8B is a local CPU comparison judge. Input version 1 scores the model's answer text; version 2 scores the executed code. Both use the pinned model, adapter, and package recorded in `src/system1/features/pinocchio_input.py`. Pinocchio reads trajectories only, not hidden labels.

| Run | Input v1 valid / expected | Input v2 valid / expected |
| --- | ---: | ---: |
| `q8b-pilot-v1` | 228/228 | 228/228 |
| `q8b-pilot-v1b` | 310/310 | 310/310 |

The two input-v1 processes were interrupted after 50 records each when the Codex server restarted. After the operator's October 23 request to complete the remaining steps, both resumed and exited successfully, preserving the original records. All four files now have complete, `ok` scores, with no damaged, stale, duplicate, or rejected records. On the 499 visible-pass development checkpoints (96 hidden failures), the descriptive AUROC is 0.603 for input v1 and 0.499 for input v2; task-weighted AUROC is 0.625 and 0.544. These development results do not change the frozen input versions or test plan.

After the operator approved up to **$2** for development Jev scoring, both runs finished under 2-million-input-token guards. All 1,076 primary arms and 60 repeat arms returned `ok` with one version, `jev-1.14.0`; 2,831,945 input tokens were recorded, about **$0.119** at TypeSafe's published $0.042 per million input tokens. Every repeated request matched its original bytes and the largest absolute repeat-score change was 0.04. There were no oversized requests or trace cuts. The account's actual charge has not been verified.

The development resource guide used 499 visible-pass checkpoints with 96 hidden failures. Pooled task-grouped out-of-fold AUROC was 0.766 for cheap features, 0.760 for cheap plus Jev code answers, and 0.748 for cheap plus code and thinking. The full-minus-cheap gain was −0.0175 versus the prespecified +0.03 effort rule. The core held-out Jev comparison stays in the test plan; optional extras are deprioritized. The fitted six-router file records exact weights and operating points; its SHA-256 is `0d825d734d02d45960b31aa74a702ba78d8694f0fdef5c9a6d441dfa93c05faf`.

## Azure cost and cleanup

- The development GPU app existed from 2026-10-23 02:20:19 UTC to 05:40:50 UTC, 3.342 hours according to the Azure activity log. At the West US 3 retail configuration rate of about $3.2004/hour, its compute estimate is **$10.70**, well below the approved $50 development-only limit. The actual Azure bill may lag and has not been confirmed.
- The app deletion succeeded, the resource group `rg-q8b-dev-20261022` returned `false` to `az group exists`, and the deletion watchdog was stopped. No Azure GPU app remains.
- The full test is a **separate future spend**. Scaling 505 development attempts to 325 held-out tasks × five attempts projects about 10.3 GPU hours and $33 of active compute; 20% runtime slack is about 12.4 hours and $40, before startup or incidental charges. Set a new limit and deletion watchdog before deploying any test GPU.

## Remaining sequence and boundaries

1. Verify that the new router config, October 23 plan amendment, and this handoff are committed and tagged `q8b-protocol-freeze-v1` **before any test task is generated**. Push only when requested.
2. After a new test GPU dollar-limit approval, generate 1,625 held-out attempts under a new run ID. Stop vLLM before local hidden grading. Then score test trajectories with Jev under its own dollar limit and with both local Pinocchio input versions; run the frozen test analysis. No hidden test input or label may reach the generator or either judge, and test labels must not choose features or thresholds.
3. The old raw 1.7B `pilot-v1` and `main-test-v1` trajectories are absent from this clone, so the planned Jev drift replay cannot run here. Until they are available and pass that check, report any 1.7B-versus-8B comparison as descriptive and possibly confounded by judge drift. Do not claim an inferential generator-size effect.

Run data remains ignored under `results/`. No new aggregate result or trace export has been committed, and no existing `docs/results/` file was changed.
