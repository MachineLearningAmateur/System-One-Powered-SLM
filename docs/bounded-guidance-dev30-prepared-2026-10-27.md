# Fixed 30-task bounded-guidance development pilot: prepared protocol

**Status:** prepared and tested offline, **not committed and not authorized for
paid execution**. This is a new development pilot on
`bounded-guidance-dev30-pilot`, branched from the bounded-guidance implementation.
The previous cached-plan integration pair
must not be repeated or included as an independent effectiveness observation.
The existing finished study, its frozen configs, and its results are untouched.

## Cleanup and authorization reconciliation

The cached integration pair's Azure group `rg-bg-cached-pair-20261027` is
confirmed absent in subscription `a1c817da-8cb1-4f20-bc7a-bca1b22e1a9b`.
The watchdog logged confirmed deletion and exited. Its raw artifacts and ledger
remain in `results/runs/bg-cached-plan-integration-20261027/`.

The operator authorized **up to $10 additional Azure spend** for that one
cached pair and a local commit. The harness deliberately imposed a stricter
**$3 internal GPU guard**. The reported **$0.4846** was a modeled app-lifetime
cost, not an actual Azure invoice charge; the invoice was not yet available.
The earlier planner preflight's recorded **$0.003146** was separate. Neither
approval carries over to this 30-task pilot.

## Frozen candidate design

The new manifest is `configs/bounded_guidance_dev30_v1.json`. Selection uses
only the committed development split and grading-exclusion list. Within each
benchmark, sort eligible task IDs by SHA-256 of
`bounded-guidance-dev30-v1:<task_id>` (task ID as tie-break), then take **9
HumanEval+ and 21 MBPP+**. The integration-debug tasks from bounded guidance
and the older Qwen smoke runs—`HumanEval/2`, `/4`, `/5`, `/59`, `Mbpp/2`, and
`/4`—are excluded. Mock IDs are outside the development pool. No
hidden correctness or observed rescue outcome enters this rule. The manifest
records source file hashes, the 30 ordered IDs, settings, and operational
limits. `load_manifest()` recomputes and checks the entire document before a
real run. The ignored run metadata records its byte hash and the clean git
commit. The prepared manifest hash is printed by:

```bash
uv run python scripts/operate_bounded_guidance_dev30.py --check
```

Each of the 30 distinct tasks gets exactly **one freshly generated shared Qwen
draft**, one visible-test run, **one new frontier plan request**, and one Qwen
continuation in each of control and guidance. The two continuations receive
the same draft, visible evidence, instructions, sampling settings, round seed,
and 8,192 thinking / 2,048 answer token caps. The guidance message alone adds
the accepted plan. Effective thinking caps are checked for equality before
either continuation request. Arm order is determined by task ID and attempt,
without outcomes. Jev remains disabled.

The planner request uses the **exact instruction header from the successful
planner-only preflight**, with each task's new first draft and visible report.
It requests Claude Sonnet 5.5 through OpenRouter's Anthropic-only route, low
reasoning effort, no provider fallback, and at most **512 total completion
tokens including reasoning**. The instruction aims for 100 words and plain
text. The unchanged acceptance validator trims leading/trailing whitespace,
counts Python Unicode characters and whitespace-delimited words, accepts at
most **900 characters and 120 words**, and rejects empty text and code fences.
A `length` or `content_filter` finish is invalid delivery.

An ordinary invalid response is charged and logged, then the guided branch
uses the ordinary continuation prompt. It remains a treatment unit in the
intention-to-treat analysis. No plan regeneration, truncation, outcome-driven
retry, task replacement, resumption of a stopped batch, or prompt tuning is
allowed. Three consecutive completed invalid deliveries stop the batch before
another paid task. Provider, configuration, accounting, score-log, and
integrity failures also stop it. Already completed pairs can be graded after
vLLM is removed; any task with a partial pair, infrastructure failure, or no
start remains explicitly listed with no imputed outcome.

The primary report is the paired pass-rate difference over the **30 frozen
tasks**, if all 30 complete and receive hidden grades. It reports
guidance-only pass, control-only pass, both-pass, both-fail, and a fixed-seed
10,000-resample task bootstrap 95% interval. A stopped batch's estimates are
marked **graded subset only**, not a full-pilot result. It also reports plan
delivery validity, invalid fallbacks, incomplete task states, per-call token
usage, recorded planner charges, modeled Azure cost, and invoice cost only if
available. Hidden grading occurs only after model serving ends, in the
networkless sandbox; no labels enter any prompt or selection step.

## Requests, time, and spending proposal

For a complete run: **90 Qwen generations**, normally two HTTP phases each,
so **180 Qwen HTTP requests maximum**, plus **30 frontier requests maximum**.
There are **zero Jev requests**. A direct Qwen answer can use one HTTP phase,
and an early stop uses fewer requests. There are no retries. The harness
pre-reserves six Qwen phases and one plan request before starting each task;
the raw credential-free Qwen and frontier HTTP exchanges are saved.

The guarded planner ledger has a **$0.60 limit**. It reserves each next request
using the UTF-8 request byte count plus 500 tokens and the 512-token completion
cap, then records provider-reported usage and cost. The planner-only preflight
took 9.725 seconds and recorded $0.003146; 30 calls at that measured cost
would be about $0.094, while larger task prompts may cost more. The $0.60
limit is a stopping guard, not a promise of an exact invoice total.

The previous Qwen3-8B pilot took 4,548.3 seconds for 228 generations.
Scaling that observed rate to 90 generations gives about **30 minutes of
generation**. Thirty plans at the measured preflight latency add about **five
minutes**. The previous Azure setup and model startup took about 13 minutes.
Visible execution and variability add time. A **rough 50–60 minute app life**
models to **$2.67–$3.20** at the current West US 3 one-A100/8-vCPU/56-GiB
assumption of **$3.2004/hour**; with expected planner use, plan on roughly
**$2.8–$3.5 total**. These are extrapolations, not charges. Azure bills
running replicas by GPU/vCPU/memory seconds and may add request or incidental
charges ([Azure billing rules](https://learn.microsoft.com/en-us/azure/container-apps/billing));
the pinned OpenRouter price is $2/M input and $10/M output tokens
([model pricing](https://openrouter.ai/anthropic/claude-sonnet-5.5)). Recheck
rates and quota immediately before a paid run.

**Proposed new total spending ceiling: $10.00.** The harness hard stop is
**90 minutes** from generation start; the outer process kills a still-running
pair at that time and never retries it. Arm an independent **two-hour watchdog
before provisioning**, so startup is included. One replica for two hours
models to **$6.4008**; plus the $0.60 planner guard is **$7.0008**. The
remaining approximately $3 covers billing lag and incidental charges. This is
an operational limit, not a guaranteed invoice cap. Delete the app immediately
after success or failure; request group deletion; retain the watchdog until the
correct subscription reports the group absent. If an app is not confirmed
absent, stop and investigate before grading. No full pilot is authorized yet.

## Operator sequence after a separate approval

`AGENTS.md` forbids commits without an operator request. The files are not yet
committed. Before any generation, obtain approval for the new $10 batch **and
the local freeze commit**, scan staged files for secret patterns, commit only
the prepared protocol/implementation/tests, record the hash, and run from a
clean tree. Do not push unless separately requested. Use one new run ID, for
example `bg-dev30-v1-20261027`; confirm that ID has no existing run folder.

Select the exact subscription, then arm the watchdog **before** creating the
resource group or GPU environment:

```bash
az account set --subscription a1c817da-8cb1-4f20-bc7a-bca1b22e1a9b
uv run python scripts/operate_bounded_guidance_dev30.py \
  --arm-watchdog --operator-approved --approved-total-usd 10 \
  --run-id bg-dev30-v1-20261027
```

Confirm its process is active, then run these commands **once**. The group must
be absent before its creation. The IP substitution changes only ingress access;
the pinned image, command, resource caps, and one-replica maximum remain
unchanged. The app and group names are fixed in the manifest. Do not copy
`.env` or keys to Azure.

```bash
az group create --name rg-bg-dev30-20261027 --location westus3
az containerapp env create --name bg-dev30-env-1027 \
  --resource-group rg-bg-dev30-20261027 --location westus3 \
  --enable-workload-profiles true --logs-destination none
az containerapp env workload-profile add --name bg-dev30-env-1027 \
  --resource-group rg-bg-dev30-20261027 \
  --workload-profile-name gpu-a100 \
  --workload-profile-type Consumption-GPU-NC24-A100
OPERATOR_IP_CIDR="$(curl -fsS https://api.ipify.org)/32"
sed "s/__OPERATOR_PUBLIC_IP_CIDR__/${OPERATOR_IP_CIDR}/" \
  configs/bounded_guidance_dev30_azure_app_v1.yaml \
  > results/bg-dev30-v1-20261027-app.yaml
az containerapp create --name bg-dev30-vllm-1027 \
  --resource-group rg-bg-dev30-20261027 \
  --yaml results/bg-dev30-v1-20261027-app.yaml
```

Capture the actual revision and its credential-free manifest. The real harness
checks live `/v1/models` against the pinned Qwen identity before inference:

```bash
uv run python scripts/operate_bounded_guidance_dev30.py \
  --capture-revision --run-id bg-dev30-v1-20261027
```

After the separate batch approval, this command runs the existing two-arm
harness **once** with all 30 manifest tasks and performs immediate app/group
cleanup even if the harness fails. It accepts neither `--resume` nor a task
limit:

```bash
uv run python scripts/operate_bounded_guidance_dev30.py \
  --real --operator-approved --approved-total-usd 10 \
  --run-id bg-dev30-v1-20261027 \
  --watchdog-manifest results/bg-dev30-v1-20261027-watchdog.json \
  --remote-manifest results/bg-dev30-v1-20261027-remote-manifest.json
```

When the app is confirmed absent, grade completed pairs in the local sandbox,
then produce a new, exclusively created analysis output:

```bash
uv run python scripts/grade_bounded_guidance.py \
  --run-id bg-dev30-v1-20261027 --real
uv run python scripts/analyze_bounded_guidance_dev30.py \
  --run-id bg-dev30-v1-20261027 \
  --output-prefix results/bg-dev30-v1-20261027-analysis-v1
uv run python scripts/operate_bounded_guidance_dev30.py \
  --verify-cleanup --run-id bg-dev30-v1-20261027
```

The final cleanup command succeeds only after `az group exists` returns
`false` in the exact subscription. A `Deleting` state, authentication error,
or failed query is not proof of cleanup. Keep the watchdog if verification
fails. The run data remains ignored under `results/`; publish only a separately
approved aggregate report.
