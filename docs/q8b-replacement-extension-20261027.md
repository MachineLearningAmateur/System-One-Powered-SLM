# Qwen3-8B task-only replacement extension — prepared October 27, 2026

**Status: offline preparation only. No frontier requests or new grading have run.**
This is an exploratory extension of the already-inspected Qwen3-8B test set,
not an independent confirmation. It preserves the original study, its labels,
and its routers. No frontier outcomes were collected for 8B in that study.
Guidance variants and router development
are paused.

## Frozen population and action

The immutable source is `results/runs/q8b-test-v1/`: 324 graded eligible test
tasks after the original HumanEval/32 exclusion, 5 saved Qwen attempts per
task, 1,620 terminal attempts, 1,580 visible-pass optional decisions, and 40
terminal visible-fail forced escalations. The saved Qwen-only outcome is
1,330/1,620 = 82.10%. The manifest
[`configs/q8b_replacement_extension_v1.json`](../configs/q8b_replacement_extension_v1.json)
pins source-file hashes, the grading session, task IDs, task-only prompt
hashes, policy selections and cost assumptions. Its SHA256, checked after the
final offline edit, must be recorded with the local freeze commit.

For each eligible task, the frontier helper receives exactly
`first_round_messages(task)`—the same task statement and visible examples
used for Qwen's first draft, with the frontier's own chat template. Source
checkpoints were checked against the current task loader: all 1,745 eligible
checkpoint records have matching task text and visible-test lists. This is
semantic prompt compatibility; Qwen's rendered chat-template hash and an
OpenRouter JSON message hash are different representations. Frontier receives
no Qwen code, thinking, hidden labels or grader feedback. The pinned helper is
`anthropic/claude-sonnet-5.5-20260928`, Anthropic provider only, low reasoning,
8,000 total completion-token cap. Two independent task-only samples per task
yield 648 logical requests. Each saved answer is graded under the
existing duplicate-vote sandbox protocol and reused across all 5 attempts and
all policies. No content regeneration, best-of-two choice, or selective sample
collection is permitted.

The primary comparison is the **exact top 25% of visible-pass decisions**:
395 optional selections per policy, plus the same 40 forced escalations.
Thus each routing policy would call the frontier on 435/1,620 attempts
(26.85%) in a deployment replay. Selection uses only the existing frozen
scores and a label-independent tie rule. The four score policies are the
original cheap router, the original fitted `cheap+code+thinking` router, the
history-arm direct `code_likely_fails` answer, and the frozen strong4 mean.
Random uses the existing closed-form 25% expected-selection comparator, with
395 optional calls in expectation; it is not one realized random batch.
Always-small makes zero frontier calls; always-frontier makes 1,620 calls and
does not pay for Qwen. The original frozen 25% thresholds are reported in a
separate deployment sensitivity: their observed optional selections are 383
cheap, 344 fitted and 367 strong4. Direct Jev has no existing frozen
threshold, so no test-set threshold will be invented for it.

Primary effect: fitted minus cheap final pass rate at the equal optional
count. Other policy contrasts are descriptive. Report final pass, rescues,
harms, already-correct escalations, unrescued escalations, optional and forced
call rates, and costs. The paired interval is a 5,000-draw whole-task
bootstrap stratified by benchmark, keeping all five attempts and both
frontier samples of each task together. The observed frontier sample mean
estimates one deployed frontier call; it is not a best-of-two policy. No
router, cutoff, prompt or sample count will be chosen from these outcomes.

## Cost and approval boundary

No Azure GPU, new Qwen, Jev, fitting or benchmark work is involved. There
are 648 frontier logical requests. The old research-plan observation of
651 development requests for about $1.30 suggests roughly **$1.30–$3.00**
for this collection, with uncertain response lengths. The
[current listed model rate](https://openrouter.ai/anthropic/claude-sonnet-5.5)
is $2 per million input tokens and $10 per million output tokens;
the source task prompts average 421.5 UTF-8 bytes and the longest is 1,762.
The 8,000-token cap yields a conservative one-attempt reservation of at most
$0.083924 per prompt. At the five allowed HTTP attempts per logical request,
the largest reservation is $0.41962. If every request hit the full 8,000-token
cap on the first HTTP attempt, the 648 requests would cost about $52.65; the
spend guard will stop much earlier at the approved ceiling.

**Proposed new operator limit: $10 total additional OpenRouter spend** for
this one collection run. The new `--strict-spend` mode reserves all allowed
HTTP attempts before dispatch and treats unknown-cost attempts as potentially
billed. The ledger records reported and computed cost per HTTP attempt. A
provider invoice can still lag or differ, so a guard is an operational bound
on recorded/estimated usage rather than an invoice guarantee. If incomplete
samples or a cost stop occur, preserve them and stop; do not add or replace
samples based on outcomes. Local sandbox grading uses installed resources and
no rented GPU. Its host CPU cost was not measured in the old study and will
be disclosed rather than silently treated as measured zero.

The original Qwen Azure app lifetime was about 9.52 hours at a reported
$3.2004/hour West US 3 retail configuration rate, or about $30.47 modeled.
Deployment costs allocate that full prior app lifetime by generation tokens
across all 1,625 original attempts, retaining the excluded task's share, and
add only each policy's Jev arms and its expected one-call frontier costs.
The old Qwen and Jev charges are not part of the **new $10 approval**. Full
modeled deployment cost is a counterfactual per-policy estimate, not the
charge for collecting all 648 research samples. Visible execution ran during
the Qwen session; separate host CPU time was not logged or priced. Frontier
grading is an offline research step, not a deployment inference charge.

## Execution after separate approval

The operator approval must cover a **local freeze commit** of only the files
in this extension, with no push, and up to $10 of additional frontier spend.
The repository's `AGENTS.md` requires an explicit commit request and a dollar
limit before billed calls. The existing untracked guidance work remains in its
original worktree and is untouched. This separate worktree and branch are
`../System-One-Powered-SLM-q8b-replacement-20261027` and
`q8b-replacement-extension-20261027`. Its ignored `results/runs` and
`data/evalplus_cache` links point to the operator-held local artifacts. A
local ignored `.env` link may be installed only on the operator machine;
credentials are never copied to a remote machine or printed.

From the extension worktree, after the approved freeze commit and a clean
working tree:

```bash
PYTHONPATH=src python scripts/analysis/q8b_replacement_extension.py verify
PYTHONPATH=src python scripts/run_frontier.py \
  --run-id q8b-frontier-replacement-v1 --split test --samples 2 \
  --limit-usd 10 --concurrency 4 --confirm-test \
  --frozen-manifest configs/q8b_replacement_extension_v1.json --strict-spend
docker compose up -d sandbox
PYTHONPATH=src python scripts/grade_hidden.py --run-id q8b-frontier-replacement-v1 --frontier
PYTHONPATH=src python scripts/analysis/q8b_replacement_extension.py analyze \
  --frontier-run q8b-frontier-replacement-v1
```

The collector refuses a different source hash, task/sample grid, prompt or
run ID. The grader must retain the same evaluator code, dataset cache and
sandbox configuration; audit its metadata against the old run before using
the outcomes. `analyze` refuses missing samples, mismatched prompt hashes,
labels for other code, unknown call costs, or changed freeze sources. It
writes ignored `results/q8b-replacement-extension-v1/` tables, a report and
an SVG figure. The old labels and aggregate report remain untouched.

The original EvalPlus base-plus evaluator and HumanEval/32 exclusion remain
unchanged. A hidden failure can reflect an ambiguous prompt, comparison/type
semantics, timeout, or candidate defect. The separate evaluator-derived
development audit documented such caveats; its privileged inputs are not
used in frontier prompts or policy selection. Any grading defect discovered
here would require a separate versioned correction, never a silent relabel.
