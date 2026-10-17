# One-off pilot analyses (October 16, 2026)

These scripts produced the numbers in `docs/findings.md`. They are kept for
reproducibility, not as part of the frozen pipeline. Run them from the
repository root with `uv run python scripts/analysis/<name>.py`. They read
`results/runs/<run-id>/` (git-ignored) and need the hidden labels from
`scripts/grade_hidden.py`.

| Script | What it measured | Calls |
|---|---|---|
| `pilot_gate.py` | Headroom gate: cap hits, hidden pass rate, projected positive test tasks | none |
| `cap_detail.py` | Cap hits by subset; cap hit vs hidden outcome | none |
| `make_cap_tasks.py` | Froze `configs/cap12k_tasks_v1.json` (already run; refuses to overwrite) | none |
| `cap_compare.py` | 8K vs 12K on attempt 0 of the 33 cap-hit dev tasks | none |
| `loop_check.py` | Share of cap-hit traces that end in a verbatim loop | none |
| `jev_check.py` + `jev_check_report.py` | First Jev integration check, 50 checkpoints (evidence-v2, 28,000-byte budget) | billed Jev calls |
| `jev_budget.py` + `jev_budget_report.py` | Full vs cut traces on the 15 cut checkpoints | billed Jev calls |
| `jev_probe.py` | Largest natural requests (55,776 bytes) from the 12K run | billed Jev calls |

The Jev scripts were run once with the user's approval (cap $2; spent about
$0.03 on them). `jev_check.py` refuses to run again on the same output
folder. The evidence version has changed since (evidence-v3, 56,000 bytes),
so a rerun would not reproduce the v2 numbers exactly.
