# Cached accepted-plan engineering integration check

**Status:** prepared offline; no GPU, Qwen, Jev, or frontier request has been
made for this check. It requires a new operator spending approval. The prior
$0.003146 planner charge belongs to the completed preflight and is not an
incremental charge for this pair. This is an **engineering integration check
using a cached accepted plan**, not an independent effectiveness result or a
member of the primary research-pilot estimate.

## Frozen inputs and planned requests

The label-independent task is `HumanEval/59`, attempt 0. The shared first draft
and visible-test report are copied from checkpoint
`HumanEval/59/a0/shared/r1` in `bg-v1a-integration-dev-20261027`:

- Draft code SHA-256: `3b41d61a6ca18613bf69ce21fe37ac3a8b251742d7d6f8ac8e17db44650011d1`.
- Visible-report SHA-256: `76326ca2bcd8c914646a5a538c62feb0d324a847debe1c3bfca5687ae5b5d738`.
- The accepted preflight plan is the exact saved response from call
  `5b76a3eef8ad495b9806d402b6a31ee0` in
  `bg-v1b-planner-preflight-20261027`; its SHA-256 is
  `8dada55126c03965446ce27d754dad6f237e83c22300ceee5d54b83d258c7fe2`.
  It passed all unchanged delivery rules with finish reason `stop`.

`scripts/run_cached_guidance_pair.py` rechecks all joins, hashes, source
messages, and the accepted verdict before preparing or running. The ignored
offline packet is `results/bg-cached-plan-pair-prepared-v1-20261027.json`.
It contains both full continuation messages and both first-phase Qwen HTTP
requests. The answer-phase request depends on the returned thinking text and
will be saved at execution. The guided message equals the control message plus
the saved plan under the existing advice heading. No part of that plan is in
the control message. Neither branch regenerates the draft.

Both branches use pinned `Qwen/Qwen3-8B` revision
`b968826d9c46dd6066d109eabc6255188de91218`, temperature 0.6, top-p 0.95,
top-k 20, seed `2180677079`, maximum 8,192 thinking tokens and 2,048 answer
tokens, and the same visible sandbox. The offline tokenizer counted 373 prompt
tokens in control and 530 in guidance; both effective thinking caps remain
8,192. There are **two Qwen generations, at most four Qwen HTTP phases, zero
frontier calls, zero Jev calls, and one control/guidance pair**. No retries,
replacement task, or follow-on pair are allowed.

## Incremental cost and new proposed approval

The previous paired run's two continuations used about **36.5 seconds** of
Qwen HTTP time combined. The new guided prompt is longer, so roughly **40–60
seconds** of active generation is a planning estimate, not a guarantee. The
previous full GPU app lifetime was about **10 minutes**, dominated by startup.
A comparable app lifetime here would model to about **$0.53** at the West US 3
rate of **$3.2004/hour** for one A100 replica, 8 vCPUs, and 56 GiB. Microsoft
bills the running replica's GPU, active vCPU, and active memory by seconds; the
rate estimate uses the current [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices)
meters. Azure's actual invoice may arrive later.

**Proposed new maximum approval: $3 total incremental spend.** Start an
independent deletion watchdog before provisioning and set its deadline no more
than **40 minutes** from the start of provisioning. At the recorded rate, 40
minutes of one replica models to **$2.1336**, leaving about **$0.8664** within
the proposed limit for incidental charges and deletion lag. This is an
operational backstop, not a guaranteed invoice cap. Allow at most one replica,
delete the GPU app immediately after completion or failure, then delete the
isolated resource group and verify `az group exists` returns `false` in the
correct subscription. Do not stop the watchdog until that confirmation.

The prior planner request's **$0.003146** is reported separately and never
charged to this new pair. In the full record, report actual recorded Azure
charges when available and distinguish them from modeled GPU cost.

## Execution shape after a separate approval

The prepared code is uncommitted. `AGENTS.md` requires a clean committed tree
for the real run and forbids committing without an operator request. Commit
only the reviewed config, harness, tests, and this document locally after that
authorization; do not push. Use a new isolated resource group, one pinned vLLM
replica, an Azure-derived remote manifest, the networkless local sandbox, and
the independent watchdog. The harness command is:

```bash
uv run python scripts/run_cached_guidance_pair.py \
  --real --operator-approved \
  --run-id <new-engineering-run-id> \
  --prepared-file results/bg-cached-plan-pair-prepared-v1-20261027.json \
  --max-worker-http-requests 4 --max-frontier-requests 0 \
  --max-wall-seconds 900 --approved-gpu-usd 3.00 \
  --server-url <approved-vllm-url> \
  --remote-manifest <azure-derived-manifest.json> \
  --watchdog-manifest <active-watchdog.json>
```

Wrap this command in a 900-second process timeout that requests GPU app and
resource-group deletion in `finally`, even if the pair fails. Keep the
watchdog as independent protection. Save the one pair's `run_meta.json`,
`prepared_packet.json`, `worker_exchanges.jsonl` (raw credential-free Qwen
requests and responses), `worker_calls.jsonl` (usage), `checkpoints.jsonl`,
and `pairs.jsonl`. Grade the two final codes only after vLLM is stopped, using
`scripts/grade_bounded_guidance.py --real`; never expose hidden grades to
Qwen. Record the Azure invoice separately from any modeled app-lifetime cost.
Stop after this one pair regardless of outcomes. No full pilot is authorized.
