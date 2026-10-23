# Runbook: collect data with a different generator (for example a 7–8B thinking model)

This runbook is for an agent or a person who reuses the pipeline of the finished study with a larger
small model. Read [AGENTS.md](../AGENTS.md) first; its rules apply to every step here. Every "commit" or
"push" below needs the operator's approval at that time.

**Research question this data serves.** In the finished study (Qwen3-1.7B), Jev's answers about the
model's *thinking* did not add signal beyond its answers about the *code* (H2: ΔAUROC −0.012), and the same
code question asked with the thinking ranked failures slightly worse. Does that change when a larger model
of the same family does the thinking?

**What the design can and cannot show.** This is a *same-family replication under two generator
checkpoints, with fixed generation limits* (8,192-token thinking cap, 16,384-token context). It is not a
pure test of model size: the checkpoint, the hardware and the concurrency change, and each generator has
its own visible-pass population. The "with vs without thinking" comparison measures the whole trace-call
package (the thinking plus 6 more questions in the same request), not the thinking alone. The fixed cap
also means the study does not measure either model's unrestricted reasoning.

## Order of work

| Step | What | Billed? |
| --- | --- | --- |
| 1–3 | Choose the model, make the branch, one-time setup | GPU rental, if any |
| 4 | Write and commit plan part A (dev procedure, drift-check rule) | no |
| 5 | Jev drift check on the old 1.7B runs | yes, a few cents |
| 6–7 | Smoke run, dev pilot, grading, scoring, dev results, headroom gate | Jev |
| 8 | Fit the routers, write plan part B (test hypotheses), commit, **tag** | no |
| 9 | Test run, grading, scoring | Jev |
| 10 | Analysis and comparison with the 1.7B study | no |

Never generate on a test task before step 8 is complete.

## 1. Choose the generator

Use **`Qwen/Qwen3-8B`** unless the operator decides otherwise. It belongs to the same family as
Qwen3-1.7B: the same `<think>` … `</think>` format, the same `enable_thinking=True` switch and the same
recommended thinking-mode sampling (temperature 0.6, top-p 0.95, top-k 20). Its default
`max_position_embeddings` is 40,960 (native context 32,768); both are above this study's 16,384-token
server limit. Do not assume that the chat template is identical: the run fingerprint stores a hash of the
template, so compare it with the 1.7B run after the smoke run and report any difference.

Another family (for example DeepSeek-R1-Distill-Qwen-7B) also changes the template, the stop rules and the
sampling; `src/system1/loop/generate.py` then needs more changes. Do not use a quantized model (AWQ, GPTQ,
4-bit) unless the operator agrees. Record the choice and its reason in the plan.

## 2. Hardware and where each step runs

| Step | Needs | Where |
| --- | --- | --- |
| Generation (vLLM) | NVIDIA GPU and Docker with GPU support. Qwen3-8B (8.2B parameters) needs about 16.4 GB for bf16 weights plus the KV cache. **Estimate, not a measurement:** a 24 GB card (L4, A10G, RTX 3090/4090) should work at `--concurrency 2`, and 40–48 GB (L40S, A6000) at the original 3. The smoke run (step 6) must confirm it: memory, KV-cache preemptions and speed. The study's RTX 3070 (8 GB) cannot run it. | local or rented GPU machine |
| Visible checks, hidden grading | Docker; about 10 GB RAM for the grader | the generation machine (no API keys needed) |
| Jev scoring, drift check | `TYPESAFE_API_KEY` | **the operator's own machine only** |
| Pinocchio scoring | CPU, about 2 s per checkpoint | either machine (no key needed) |

On a rented machine, run generation and grading there, then copy the new `results/runs/<run-id>/` folders
to the operator's machine for Jev scoring. Never copy `.env` to the rented machine.

## 3. Branch, code changes and one-time setup

```bash
git checkout -b gen-qwen3-8b
```

**Code changes** (commit them in one commit after the operator approves; protocol runs need a clean tree):

1. Find the model revision. Do not guess a hash:
   ```bash
   uv run python -c "from huggingface_hub import model_info; print(model_info('Qwen/Qwen3-8B').sha)"
   ```
2. `src/system1/loop/generate.py`: set `MODEL = "Qwen/Qwen3-8B"` and `REVISION = "<sha>"`. Keep
   `MAX_MODEL_LEN`, `THINK_CAP`, `CODE_TOKENS`, `TOP_LOGPROBS`, `SAMPLING` and `SEED_TAG`, so the runs pair
   with the 1.7B runs by task and attempt index.
3. `docker-compose.yml`, service `vllm`: set `--model=Qwen/Qwen3-8B` and `--revision=<sha>`. Keep
   `--dtype=bfloat16`, `--max-model-len=16384`, `--max-logprobs=20` and `--seed=0`. `scripts/run_loop.py`
   checks model, revision, context length, dtype and seed against `EXPECTED_SERVER` and refuses a mismatch.
   It does **not** check `--max-logprobs`; keep it at 20 yourself (the code needs the top-5 logprobs). Change
   `--gpu-memory-utilization` only if the GPU needs it, and record the value.
4. `scripts/run_loop.py`: set `FREEZE_TAG = "q8b-protocol-freeze-v1"`. The branch descends from
   `protocol-freeze-v1`, so without this change the test gate would not protect the new study. The gate
   checks only that the tag is in the history; it does not check what the tagged commit contains.
5. `scripts/freeze_routers.py`: add `"q8b-v1": ROUTERS_V1 + ["pinocchio"]` to `ROUTERS`. Keep Pinocchio:
   `scripts/test_analysis.py` needs the Pinocchio router and both Pinocchio input versions.
6. `scripts/analysis/trace_effect.py` reads the runs `pilot-v1` and `pilot-v1b` directly and has no
   argument parser. Add one with a repeatable option, and fall back to the old runs only when none is given:
   ```python
   ap = argparse.ArgumentParser()
   ap.add_argument("--run-id", action="append")
   args = ap.parse_args()
   run_ids = args.run_id or ["pilot-v1", "pilot-v1b"]
   ```
   Do not give the append option a default list: the old runs would be added to the new ones. Note that
   this script prints raw answer values (so `on_task` and `stated_fix_matches_change` show below 0.5 when
   they separate in the "false is bad" direction), while `test_analysis.py` orients them as 1 − p. Compare
   like with like.
7. `scripts/export_traces.py`: set `OUT = ROOT / "docs" / "traces-q8b"`, so a later export never touches
   the 1.7B export in `docs/traces/`.
8. Run `uv run pytest`. If a test pins the 1.7B model name, change only that expectation and say why in
   the commit message.

**One-time setup** (from the repository root):

1. `uv sync` and `uv sync --group pinocchio`. Put `.env` on the operator's machine only.
2. Generator weights into the shared cache (vLLM runs with `HF_HUB_OFFLINE=1`):
   ```bash
   uv run python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-8B', revision='<sha>', cache_dir='hf_cache/hub')"
   ```
3. Pinocchio weights at the pinned revisions. `scripts/score_pinocchio.py` loads them with
   `local_files_only=True` from the default Hugging Face cache, on the machine that scores:
   ```bash
   uv run --group pinocchio python -c "from huggingface_hub import snapshot_download; from system1.features import pinocchio_input as PI; [snapshot_download(r, revision=v) for r, v in ((PI.BASE_REPO, PI.BASE_REVISION), (PI.ADAPTER_REPO, PI.ADAPTER_REVISION))]"
   ```
4. EvalPlus data. The setup container has no network. Load the datasets once on the host, which
   downloads them to the EvalPlus user cache (by default `~/.cache/evalplus/`):
   ```bash
   uv run python -c "from evalplus.data import get_human_eval_plus, get_mbpp_plus; get_human_eval_plus(); get_mbpp_plus()"
   ```
   Copy `HumanEvalPlus-v0.1.10.jsonl` and `MbppPlus-v0.2.0.jsonl` into `data/evalplus_cache/evalplus/`.
   Check that these versions match the ones recorded in `configs/split_v1.json` (`source`: HumanEval+
   v0.1.10, hash `916d9bfe…`; MBPP+ v0.2.0, hash `92743def…`). The recorded MD5s use CRLF
   JSONL line endings; the official downloads available on October 22 use LF. Converting only the record
   separators to CRLF reproduces both recorded hashes, and all JSON records parse identically. Verify
   this equivalence without changing either dataset file or the frozen split. Do **not** run
   `scripts/make_split.py`; the split is frozen.
5. Build the sandbox and compute the ground truth:
   ```bash
   docker compose build sandbox
   docker compose --profile setup run --rm sandbox-setup
   ```

## 4. Plan part A (before any new data)

Write `docs/q8b-plan.md` with:

- the generator, its revision, the GPU, `--concurrency` and `--gpu-memory-utilization`;
- the dev design (step 7) and the headroom rule (step 7.6);
- the **drift-check rule** (step 5): sample size and design, the comparisons, the tolerances, and what
  happens if the check fails.

Commit it (after approval). Parts that come later are amendments with a date.

## 5. Jev drift check (the 1.7B scores are from October 16–17, 2026)

The scorer enforces one Jev version inside a run, not across runs. Before the new scores are compared with
the old ones, check that Jev still gives the same answers to the same bytes. The check sends no new
evidence; it repeats old requests.

```bash
uv run python scripts/analysis/jev_drift_check.py prepare --source-run main-test-v1 --n 200 --out jev-drift-main-test-v1-a
uv run python scripts/analysis/jev_drift_check.py prepare --source-run pilot-v1 --n 100 --out jev-drift-pilot-v1-a
uv run python scripts/score_jev.py --run-id jev-drift-main-test-v1-a      # billed: 400 calls
uv run python scripts/score_jev.py --run-id jev-drift-pilot-v1-a          # billed: 200 calls
uv run python scripts/analysis/jev_drift_check.py compare --source-run main-test-v1 --drift-run jev-drift-main-test-v1-a
uv run python scripts/analysis/jev_drift_check.py compare --source-run pilot-v1 --drift-run jev-drift-pilot-v1-a
```

- `prepare` draws a seeded sample stratified by round and thinking length, never by outcome, into a new
  run folder; the old run is only read. `compare` stops if any request's bytes differ from the stored hash.
- Report the returned versions, and per arm and question the signed mean change, the mean and largest
  absolute change and the rank correlation. The tolerances are the ones frozen in part A. Note that the
  1.7B study saw repeat changes of at most 0.05 with identical bytes; that is an observed maximum, not a
  validated equivalence margin.
- **If the check passes:** use the historical 1.7B scores, and write in the report "no drift found in this
  sample", not "no drift". **If it fails:** stop and ask the operator. The options are full re-scoring of
  the 1.7B runs into new folders (billed, with new 1.7B comparison routers fit on the re-scored dev data),
  or a report that states the comparison is confounded by judge drift.
- Every new scoring run must return the same Jev version as the drift check. If it does not, stop.

## 6. Smoke run

```bash
docker compose stop sandbox            # the hidden grader must not run during generation
docker compose up -d vllm
curl -s http://localhost:8000/v1/models   # repeat until it lists Qwen/Qwen3-8B
uv run python scripts/run_loop.py --run-id q8b-smoke --split dev --limit 5 --concurrency 2 --allow-dirty
```

Give the smoke run its own id and never analyze it. Check in `results/runs/q8b-smoke/`: every checkpoint
has code, `think_closed` is mostly true, the cap-hit rate, KV-cache preemptions and the template hash in
`run_meta.json`, and the seconds per attempt (to estimate the full runs and the GPU cost).

## 7. Dev pilot (the same design as the finished study)

1. Generation. Use the same `--concurrency` in every run of this study (it is part of the fingerprint),
   and **do not commit between the sessions of one run**: the fingerprint includes the git commit, so a run
   continues after an interruption only on the same commit.
   ```bash
   uv run python scripts/run_loop.py --run-id q8b-pilot-v1 --split dev --attempts 1 --concurrency 2
   uv run python scripts/run_loop.py --run-id q8b-pilot-v1b --split dev --first-attempt 1 --attempts 5 \
       --tasks-file configs/pilot_subsample_v1.json --concurrency 2
   ```
   The second run makes attempts 1–4 on the fixed 72-task subsample, so those tasks have 5 attempts.
2. Grading (vLLM stopped):
   ```bash
   docker compose stop vllm && docker compose up -d sandbox
   uv run python scripts/grade_hidden.py --run-id q8b-pilot-v1
   uv run python scripts/grade_hidden.py --run-id q8b-pilot-v1b
   ```
3. Jev cost estimate, then approval. Estimate from the observed request sizes of the new runs and the price
   in `configs/prices.yaml`: about 2 calls per checkpoint, plus the repeat sample. Set
   `--max-input-tokens` for each run inside the approved amount.
4. Jev scoring (operator's machine):
   ```bash
   uv run python scripts/score_jev.py --run-id q8b-pilot-v1 --repeat 30 --max-input-tokens <guard>
   uv run python scripts/score_jev.py --run-id q8b-pilot-v1b --max-input-tokens <guard>
   uv run python scripts/jev_gates.py --run-id q8b-pilot-v1 --run-id q8b-pilot-v1b
   ```
   A finished scoring run can still hold records that are not `ok`; the dev analysis needs both arms `ok`.
   Report every other status with its count.
5. Pinocchio scoring, both input versions, both runs:
   ```bash
   uv run --group pinocchio python scripts/score_pinocchio.py --run-id q8b-pilot-v1 --input-version pinocchio-input-v1
   uv run --group pinocchio python scripts/score_pinocchio.py --run-id q8b-pilot-v1 --input-version pinocchio-input-v2
   ```
   and the same two commands for `q8b-pilot-v1b`.
6. **Headroom and class support, before any dev model fitting.** Count, per benchmark, the visible-pass
   checkpoints, the hidden fails among them, and the tasks with at least one visible-pass hidden fail and
   with at least one visible-pass hidden pass.
   - Projection rule (as in the 1.7B pilot): in the 72-task subsample, which has 5 attempts per task, take
     the share of tasks with at least one visible-pass hidden fail, per benchmark, and multiply it by that
     benchmark's number of test tasks (98 HumanEval+, 227 MBPP+), with a Wilson interval on the share.
   - Gate: at least 30 projected test tasks with a visible-pass hidden fail. The task-grouped LR folds also
     need both classes in every fold.
   - If the gate fails, or a fold has one class, **stop and ask the operator.** Do not change the
     benchmark or the cap on your own. Fewer failures mean less precision, not by itself a lower AUROC.
7. Dev results:
   ```bash
   uv run python scripts/resource_guide.py --run-id q8b-pilot-v1 --run-id q8b-pilot-v1b
   uv run python scripts/analysis/trace_effect.py --run-id q8b-pilot-v1 --run-id q8b-pilot-v1b
   ```
   Report the final hidden pass, the counts from step 6, the cap-hit rate, the share of trace-call
   requests whose thinking was cut by the 56,000-byte budget (denominator: all trace-call requests at
   visible-pass checkpoints) with the retained share of the thinking (median and quartiles), and the dev
   AUROCs.

## 8. Freeze (before any test generation)

1. Fit the routers on the new dev runs only:
   ```bash
   uv run python scripts/freeze_routers.py --run-id q8b-pilot-v1 --run-id q8b-pilot-v1b --version q8b-v1
   ```
   This writes `configs/routers_q8b-v1.json` and `results/dev_router_scores_q8b-v1.json`.
2. Add plan part B to `docs/q8b-plan.md`:
   - **The confirmatory family, exactly as `scripts/test_analysis.py` runs it:** two two-sided tests on
     visible-pass test checkpoints, Holm over the two: cheap + code + thinking − cheap, and
     cheap + code + thinking − cheap + code (the H2 contrast). A different family or a one-sided test needs
     a new, separately versioned analysis script, written and committed now.
   - **The cross-generator comparison.** Choose one before the tag:
     (a) descriptive only (default; section 10), or
     (b) an inferential test of the difference between the two H2 gains, with whole tasks resampled jointly
     across both generators and a stated treatment of their different visible-pass populations. Option (b)
     needs its own script now, and a passing drift check does not bound drift's effect on this statistic.
   - The population, the weighting (pooled headline; task-weighted as a sensitivity), Amendment A2 (still
     applies), the missing-score rule, the frozen rubric and byte budget, the trace-cut reporting, the
     support by round and by cap hit, and what happens if a step fails.
3. Commit the router config and the plan together (after approval), then tag that commit:
   `git tag q8b-protocol-freeze-v1`. Push the branch and the tag when the operator asks.

## 9. Test run

```bash
docker compose stop sandbox && docker compose up -d vllm
uv run python scripts/run_loop.py --run-id q8b-test-v1 --split test --attempts 5 --concurrency 2
docker compose stop vllm && docker compose up -d sandbox
uv run python scripts/grade_hidden.py --run-id q8b-test-v1
uv run python scripts/score_jev.py --run-id q8b-test-v1 --max-input-tokens <guard>     # billed, operator's machine
uv run --group pinocchio python scripts/score_pinocchio.py --run-id q8b-test-v1 --input-version pinocchio-input-v1
uv run --group pinocchio python scripts/score_pinocchio.py --run-id q8b-test-v1 --input-version pinocchio-input-v2
```

Do not commit while the test generation run has sessions left. A rerun with the same run id and the same
commit skips finished attempts. Do not restart a run that the system stopped without asking the operator.

## 10. Analysis

1. The planned analysis:
   ```bash
   uv run python scripts/test_analysis.py --run-id q8b-test-v1 --routers q8b-v1
   ```
   It gives the two Holm tests, Table 1, the per-answer audit and the same-question contrast.
2. **Comparison with the 1.7B study** (descriptive unless part B chose option b). Use the same tasks and
   attempt indices. Do not pool the two generators, and do not read a difference in AUROC as an effect of
   size alone: each model has its own visible-pass population. A positive 8B H2 gain next to the negative
   1.7B gain does not by itself show that the two differ. Report side by side, with positive tasks,
   positive checkpoints, prevalence and intervals:
   - the AUROC of each thinking question (`on_task`, `unsupported_claim`, and the round 2–3 questions,
     which apply only to a selected subset of attempts);
   - the same-question contrast (each code question from the history call against the trace call);
   - the H2 contrast;
   - the cap-hit rate, the trace-cut rate and the retained share of the thinking;
   - support by round and by cap hit.
3. Optional replay: the 1.7B study's frontier answers (`frontier-test-v1`) are task-level answers to the
   round-1 prompt, which does not depend on the generator, so they can be reused. Check this in
   `scripts/replay.py` before you rely on it. New frontier calls are billed.

## 11. What to hand back

- The new run folders `results/runs/q8b-*` and `results/runs/jev-drift-*`, copied to the operator (they
  stay out of git).
- New aggregate result files, copied into `docs/results/` under new names when the operator asks.
- Optional: `uv run python scripts/export_traces.py --run-id q8b-test-v1` (writes `docs/traces-q8b/` after
  step 3.7).
- A short report: the drift-check result, the numbers from steps 7.6, 7.7 and section 10, every deviation
  from this runbook, and the costs (GPU hours, Jev and frontier dollars).
