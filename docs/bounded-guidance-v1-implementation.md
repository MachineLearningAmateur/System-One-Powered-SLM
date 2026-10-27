# Bounded guidance v1: implementation and operator runbook

**Status:** implemented and mock-tested on `bounded-guidance-v1-implementation`.
`codex_bounded_guidance_plan.md` was not present in the repository or supplied
workspace. The operator accepted the explicit protocol below and approved a
$20 ceiling for the development pilot; no paid inference had run when this
document was frozen.

## Question and unit

The unit is one EvalPlus task and attempt. Qwen3-8B makes one shared first draft;
the networkless visible runner tests that code once. After that observation, a
single pinned frontier call returns a bounded natural-language repair plan. The
control arm sees the shown task, draft, and visible report; the guidance arm sees
the same material plus that plan. Each arm gets **one** Qwen continuation with
the same 8,192 thinking-token cap, 2,048 answer-token cap, sampling settings,
and round-2 seed. The final code from each arm is graded only after generation.
The first visible result does not decide eligibility; visible-pass drafts are
included. No Jev call or routing occurs in Stage 1.

The frontier prompt is in `system1.bounded_guidance.plan_messages`; it sees no
hidden test or grade. A plan is limited to 120 words, 900 characters, 512 output
tokens, and no code fence. Missing, invalid, or overlong advice stops the pair
instead of being substituted with control text. There is no content retry.
The control and guidance continuations have equal **maximum** Qwen generation
budgets. They can use different numbers of actual output tokens. Guidance also
uses a frontier call and extra input tokens; compare those costs explicitly.

The real worker is the pinned `Qwen/Qwen3-8B` revision already in
`system1.loop.generate`. The adviser is the pinned Claude Sonnet 5.5 model and
Anthropic provider path already used by the repository's frontier client. The
real visible runner executes generated code only in the disposable, networkless
Docker sandbox. The mock runner checks a string marker and executes no code.

## Recorded files and analysis

Each new run uses a unique ignored `results/runs/<run-id>/` directory. It writes
`run_meta.json` (protocol, git commit, server and sandbox identities, sessions),
`pairs.jsonl` (shared and arm checkpoints, prompt messages and hashes, code and
hashes, visible results, tokens and latency), `plans.jsonl` (prompt, response,
usage and cost), `worker_calls.jsonl` (each Qwen HTTP phase), `ledger.jsonl`
(each frontier HTTP attempt), and `failures.jsonl`. The grader writes distinct
`bounded_hidden_*` files and refuses to overwrite labels. The analysis joins
labels by pair, arm, checkpoint and code hash. It reports the paired final
pass-rate difference, rescue/harm counts, and a whole-task bootstrap interval.
All attempts of a task stay together. First-draft outcomes and intervention
cost are retained for diagnostics. `bounded_pairs.csv` and
`bounded_analysis.json` are machine-readable analysis outputs.

The implementation uses one continuation per arm, not the older three-round
stop-on-visible-pass repair loop. Thus the estimand is the effect of adding one
short plan to a fixed continuation opportunity. A later Jev allocation study
would need its own protocol and untouched evaluation.

## Zero-cost demonstration (tested)

```bash
uv run python scripts/run_bounded_guidance.py --run-id bg-mock-complete-20261026 --mock
uv run python scripts/grade_bounded_guidance.py --run-id bg-mock-complete-20261026 --mock
uv run python scripts/analyze_bounded_guidance.py --run-id bg-mock-complete-20261026
uv run pytest
```

The shown run id has already been used; substitute a new id to repeat it.
The mock result has 3 pairs (including 1 first-draft visible pass), 3 plan
requests, 3 shared drafts, 3 control continuations, 3 guidance continuations,
and 18 Qwen HTTP phases. Mock hidden grading yields 1/3 control passes and
3/3 guidance passes by construction;
those figures validate the pipeline and are **not research evidence**. The mock
made zero paid requests and ran no generated code on the host.

## Guarded real pilot: below $20 modeled total

The pilot uses **120 tasks** from the frozen EvalPlus development split, one
attempt each. [The new task manifest](../configs/bounded_guidance_pilot_v1.json)
contains 36 HumanEval+ and 84 MBPP+ tasks. It was selected by a fixed SHA-256
ordering within each benchmark, using task IDs only; no outcomes were read.
Its SHA-256 is `8286e4ea01a3ae3128bf91a3d295281525f996a5fdfb3fe1e75131981da7e33c`.
The existing grading exclusion is applied before generation.

The harness rejects a larger real pilot: at most **120 frontier requests**,
**720 Qwen HTTP phases** (3 generations × at most 2 phases × 120 pairs),
**$1.50** frontier spend limit, and **2.5 hours** of harness wall time. The
wall-time ceiling is checked before each pair; one in-flight pair may run past
it. The frontier ledger reserves a conservative input-token estimate plus
512 output tokens before each call. Reported usage is charged after the call.
The real pilot must use the 120-task manifest and one attempt.

Before creating a rented GPU app, arm the existing resource-group deletion
watchdog with a UTC deadline **no more than 3 hours later** and allow **at most
one replica**. Verify deletion afterward. This is the GPU cost backstop: the
harness cannot stop Azure billing after it exits, and a delayed or failed
deletion can exceed the modeled amount. The frontier guard also cannot
guarantee the exact final invoice if a provider bills an unexpectedly large
request. Azure budgets and cost alerts may lag, so do not rely on them as the
only cutoff. This script does not provision or delete compute.

The user set a **$20 total pilot ceiling**. The $1.50 frontier cap and 3-hour
GPU deadline are sublimits inside it. After freezing this protocol on a clean
commit, the command shape is:

```bash
nohup uv run python scripts/azure_smoke_watchdog.py \
  --resource-group <pilot-only-resource-group> \
  --deadline-utc <UTC-time-no-more-than-3-hours-from-now> \
  > results/bounded_guidance_watchdog.log 2>&1 &
```

Arm that watchdog **before** provisioning the one-replica GPU app. Once the
app is live, run:

```bash
uv run python scripts/run_bounded_guidance.py \
  --run-id <new-dev-run-id> --real --operator-approved --split dev \
  --attempts 1 --tasks-file configs/bounded_guidance_pilot_v1.json \
  --limit-usd 1.50 --max-frontier-requests 120 \
  --max-worker-http-requests 720 --max-wall-seconds 9000 \
  --server-url <approved-vllm-url> --remote-manifest <deployment-manifest.json>
```

For local vLLM, omit `--server-url` and `--remote-manifest`. The server identity,
model revision, visible image, git commit, task IDs, and plan bounds are stored
in `run_meta.json`; a resumed run must match exactly and requires explicit
`--resume`. For a test split, the harness also requires a new
`bounded-guidance-v1-freeze` ancestor tag after the hypotheses and analysis
plan have been committed. No such freeze tag is created here.

Then stop vLLM before hidden grading:

```bash
uv run python scripts/grade_bounded_guidance.py --run-id <new-dev-run-id> --real
uv run python scripts/analyze_bounded_guidance.py --run-id <new-dev-run-id>
```

The grade command checks local vLLM and a configured remote model endpoint.
It runs reference calibration, a memory canary, two hidden votes per distinct
code, and a conditional third vote in the networkless grader. Hidden labels
never enter generation or adviser prompts.

## Pre-run cost estimate, not a charge

The saved 217-attempt `q8b-pilot-v1` run made 228 Qwen generations in 4,548.3
session seconds. Scaling that measured rate to this pilot's 360 generations
gives about **2.00 active GPU hours**, or **$6.38** at $3.2004/hour. For the
120 selected saved first drafts, the new adviser prompt's UTF-8-byte
reservation plus the 512-token output cap sums to about **$1.01** at the
repository's pinned $2/million input and $10/million output token prices.
The expected modeled total is therefore about **$7.39** before deployment
overhead. These are extrapolations, not measured charges.

Microsoft's [Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices)
currently returns West US 3 Container Apps meters of $0.000529 per GPU-second,
$0.000024 per vCPU-second, and $0.000003 per GiB-second. For the prior
one-A100, 8-vCPU, 56-GiB configuration, that is **$3.2004/hour**. At a
3-hour deletion deadline, modeled GPU compute is at most **$9.60**;
including the $1.50 frontier limit gives **$11.10**, leaving **$8.90** below
the user's $20 pilot budget for startup, request and incidental charges or
deletion lag. Azure bills per running replica and can charge for requests and
other attached resources; the actual invoice must be reconciled afterward.

The first-draft failure count in the source run was 9/217; the combined
development runs had 24/505 first-draft visible failures. Restricting advice
to those failures would miss the main visible-pass population.
