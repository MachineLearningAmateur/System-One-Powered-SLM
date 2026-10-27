# Bounded guidance v1a: invalid advice delivery amendment (2026-10-27)

**Status:** prepared, offline tested, not committed or used for paid inference. This
amends only the planner integration and its accounting. The single shared Qwen
draft, one frontier request, two isolated continuations, frozen development task
pool, and downstream grading remain the same. No Jev routing is added.

## Incident and limits of reconstruction

The stopped `bg-pilot-dev-20261027` run made two Qwen HTTP calls and one
OpenRouter call for `HumanEval/59`, then raised `InvalidPlan: adviser response
exceeded the fixed bound`. It completed zero pairs. The unchanged incident file
records 542 prompt tokens, 286 completion tokens, 0 reported reasoning tokens,
and $0.003944 for the frontier request. The Azure app lived an estimated 577.8
seconds, about $0.5136 at the recorded $3.2004/hour rate; the actual invoice is
unknown. The Azure resource group has since been verified absent. These costs
remain charged to the stopped run.

The exact validator was `validate_plan` in `src/system1/bounded_guidance.py`.
It strips `choices[0].message.content` and rejects if its Python Unicode
character count exceeds **900** or its Python whitespace-delimited word count
exceeds **120**. It also rejects empty text and code fences. The old run saved
neither the HTTP response body nor the rejected text, counts, `finish_reason`,
response ID, or upstream provider. Its `ledger.jsonl` only saved usage and
cost. The observed exception proves that the parser supplied a nonempty string
from `message.content` and at least one of the two bounds fired. The code did
not count usage tokens or the separate `message.reasoning` field as plan text.
The exact response cannot be replayed offline, so the actual text, which bound
fired, and any provider normalization of that content cannot be verified.
Offline regression tests reproduce the same
validator exception with 901 characters and 121 words; they are synthetic
examples, not a reconstruction of the missing response.

The request code used `anthropic/claude-sonnet-5.5-20260928` via OpenRouter,
with `provider={"order":["anthropic"],"allow_fallbacks":false}`,
`reasoning={"effort":"low"}`, and `max_tokens=512`; it did not set temperature.
The ledger returned model name was `anthropic/claude-sonnet-5.5`. It names
OpenRouter as the gateway but did not save the returned upstream provider.
OpenRouter documents `max_tokens` as a deprecated alias for the **completion**
token ceiling, rather than a visible-plan word or character limit. It documents
reasoning separately from message content, and its usage accounting includes
reasoning within completion tokens. Sonnet 5.5 has thinking enabled, with effort
as a control. Thus 512 cannot be interpreted as 512 visible tokens. The old
usage of 286 completion and 0 reported reasoning tokens does not show that the
request exhausted its completion budget. The missing finish reason prevents a
truncation determination.

Sources: [OpenRouter chat completion API](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request),
[OpenRouter reasoning response fields](https://openrouter.ai/blog/announcements/reasoning-tokens-for-thinking-models/),
[OpenRouter completion token accounting](https://openrouter.ai/assets/State-of-AI.pdf),
[Sonnet 5.5 model and provider information](https://openrouter.ai/anthropic/claude-sonnet-5.5/providers).

## Versioned rule, `invalid-advice-v1a-20261027`

For one successful, accounted frontier response, classify empty visible
content, content exceeding 120 words or 900 characters, a code fence, a
`length` finish reason, or a `content_filter` finish reason as **invalid advice
delivery**. Save the raw credential-free request and response, measured visible
lengths, finish reason, reason for invalidity, and usage. Charge the request.
Run the guidance continuation with the ordinary continuation prompt and retain
it as a treatment unit. It receives the same continuation opportunity as the
control, even when the prompts are identical. No regeneration, truncation, or
relaxed acceptance occurs. The intention-to-treat paired analysis includes
these units and reports delivery counts.

The planner prompt now states both existing limits using the validator's
counting convention: at most 120 whitespace-separated words and 900 Unicode
characters after leading and trailing whitespace is trimmed. Neither bound
was increased.

HTTP or transport failure, missing usage, unexpected content shape, unknown or
missing finish reason, completion usage above the requested cap, damaged logs,
spending violations, unmatched records, and other unresolved configuration or
integrity failures still stop the job. The request/response and charge are
written before a response-level hard stop. If **three consecutive completed
pairs** have invalid advice, stop before starting a fourth paid pair. Report
the three outcomes and investigate the integration; any restart needs a new
operator decision. An early-stopped pilot is a feasibility check, not a full
120-pair performance result.

The old stopped run remains untouched and is not resumed under this amendment.
The new run metadata records the amendment version. A real run requires a new
run ID and a clean committed implementation, under `AGENTS.md`; neither a
commit nor any billable action is authorized by this document.

## Offline verification

```bash
uv run pytest -q tests/test_bounded_guidance.py
uv run python scripts/run_bounded_guidance.py --run-id <fresh-mock-id> --mock --mock-advice-case overlength --limit 1
uv run python scripts/grade_bounded_guidance.py --run-id <fresh-mock-id> --mock
uv run python scripts/analyze_bounded_guidance.py --run-id <fresh-mock-id>
```

The mock is expected to show one pair, one invalid delivery, one plan request,
six Qwen HTTP phases, two final labels, and zero charges. It validates pair
completion and accounting, not scientific performance.

## Proposed single real integration pair — **not executed**

After a separate operator approval of the billed check and the new commit,
arm the deletion watchdog **before** creating at most one Azure GPU replica.
Set its UTC deadline no later than 45 minutes after creation. At $3.2004/hour,
45 minutes models to $2.4003 GPU compute. Add a $0.03 frontier ceiling: $2.4303
modeled total, excluding incidental charges and deletion lag. An operator
should approve a **$3 total ceiling** for this one-pair check and verify the
current GPU rate and resource-group deletion afterward.

```bash
nohup uv run python scripts/azure_smoke_watchdog.py \
  --resource-group <integration-only-resource-group> \
  --deadline-utc <UTC-time-within-45-minutes-of-GPU-creation> \
  > results/bounded_guidance_v1a_watchdog.log 2>&1 &
```

Start the watchdog before creating the replica; confirm it remains active.
Only then create the GPU app and run the pair:

```bash
uv run python scripts/run_bounded_guidance.py \
  --run-id <new-v1a-integration-run-id> --real --operator-approved \
  --split dev --attempts 1 --tasks-file configs/bounded_guidance_pilot_v1.json \
  --limit 1 --limit-usd 0.03 --max-frontier-requests 1 \
  --max-worker-http-requests 6 --max-wall-seconds 900 \
  --server-url <approved-vllm-url> --remote-manifest <deployment-manifest.json>
```

`--limit 1` selects the first task in the frozen, label-independent pilot
manifest, `HumanEval/59`, and uses a fresh run ID. One pair means one shared
draft, one frontier request, and one Qwen continuation per arm: **three Qwen
generations**, at most **six Qwen HTTP phases**, and **one** frontier HTTP
request. The frontier reservation is bounded by the existing 512 completion
token cap and the $0.03 pre-call guard, followed by an after-call limit check.
The 900-second harness limit is checked before starting the pair; an in-flight
pair can overrun it, so the external 45-minute deletion watchdog remains
necessary. A complete pair with valid advice or recorded invalid delivery is
an integration success. Relative performance is not an integration criterion.
