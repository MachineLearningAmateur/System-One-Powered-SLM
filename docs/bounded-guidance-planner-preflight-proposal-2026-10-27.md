# Planner-only preflight proposal (2026-10-27)

**Status:** prepared offline; the operator subsequently approved exactly one
planner-only request with a $0.03 ceiling. No Qwen or GPU request is approved. The
completed `bg-v1a-integration-dev-20261027` pair remains labeled in its ignored
run directory as **"invalid-advice fallback completed; valid guidance delivery
unverified."** It is not evidence that a valid plan helped Qwen.

## Evidence and minimal change

The saved OpenRouter response is present in the ignored
`results/runs/bg-v1a-integration-dev-20261027/frontier_exchanges.jsonl` file.
Its visible `message.content` is 142 whitespace-separated words and 785
Unicode characters after trimming, and it contains a literal three-backtick
`python` marker. The finish reason is `stop`; the separate reasoning field is
null. The 120-word acceptance limit and the no-code-fence rule both reject it;
the 900-character limit does not. This is a visible-content problem. There is
no evidence that extraction or the 512-token completion ceiling caused this
particular rejection.

The proposed preflight changes only the planner instruction header. It asks
for **at most 100 words** as a drafting target and plain text with no backticks,
numbered lists, or final-answer formatting advice. It explicitly permits
"no clear defect" and forbids inventing a defect or change. The task, saved first
draft, visible-test report, model, Anthropic-only route, low reasoning effort,
and 512-token completion cap remain unchanged. The delivery validator stays
at the frozen **120 words / 900 characters** and still rejects code fences.
Nothing is truncated or retroactively accepted. The production v1a prompt is
unchanged; this proposal is for one isolated integration preflight, not a new
study arm.

## Prepared packet and exact limit

`scripts/preflight_bounded_guidance_planner.py` pins the one saved
`HumanEval/59` checkpoint and verifies the original request hash and joins.
It reads no hidden grades and contains no Azure or Qwen call. Its offline
`--prepare` mode wrote
`results/bg-v1b-planner-preflight-request-approved-20261027.json`. At the repository's
pinned prices, the existing byte-based input reservation plus **512 completion
tokens** is **$0.009412**. The approved preflight has **one**
frontier request, **zero** GPU provisioning, **zero** Qwen requests, **no
retries**, and a **$0.03 frontier guard**. A provider's final reported charge
can exceed a reservation, so the script records and checks it afterward.

The following is the separately approved, clean-commit command for **one**
planner-only request. It is not covered by the earlier $3 pair authorization:

```bash
uv run python scripts/preflight_bounded_guidance_planner.py \
  --real --operator-approved --run-id <new-planner-only-run-id> \
  --max-requests 1 --limit-usd 0.03
```

Save the raw credential-free exchange, finish reason, all acceptance-rule
outcomes, measured lengths, usage, and charge. A failed preflight is recorded
once and stops; another billed attempt needs another decision. If
valid, a separate protocol amendment and approval would still be needed
before any further Qwen or pilot run.
