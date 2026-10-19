# Instructions for coding agents

This repository holds a finished, preregistered study (see [README.md](README.md)). Agents may reuse its
pipeline to collect new data, but must not change what the finished study reports. Read this file before
you run or change anything.

## Rules that always apply

1. **Never change the finished study.** Do not edit the committed `configs/` files, the frozen routers
   (`configs/routers_v1.json`, `routers_v2.json`, `routers_transfer_v1.json`), the tag `protocol-freeze-v1`,
   or the existing files in `docs/results/`. New result files may go into `docs/results/` only under new,
   unique names. New data collection goes on its own git branch, with new run ids and new config files.
2. **Never overwrite old run data,** even though it is not in git: the folders in `results/runs/`, their
   score and label files, and the analysis outputs in `results/`. Write new data to new run ids and new
   file names.
3. **Secrets.** API keys live only in `.env` on the operator's own machine (copy `.env.example`). Never
   print a key, never commit it, and never copy it to a remote or rented machine. Check a key only by its
   length. Before every commit, scan the staged changes without printing them, for example
   `git diff --cached | grep -cE "sk-or-v1|sk-ant-|TYPESAFE_API_KEY=.|OPENROUTER_API_KEY=."` (a count of 0
   is clean; on a match, find the file with `grep -l`, not by printing lines).
4. **Billed calls need the operator's approval first,** with a dollar limit: Jev (`scripts/score_jev.py`),
   the frontier model (`scripts/run_frontier.py`) and any rented GPU. Give the expected cost before you ask,
   and set a per-run guard (`score_jev.py --max-input-tokens`). A token guard is not a dollar cap: the last
   call can go past it.
5. **Untrusted code runs only in the sandbox.** Code written by a generator or a frontier model for a
   benchmark task runs only in the evaluation sandbox (`docker/sandbox/`, no network), never on the host.
   The repository's own scripts and tests run on the host as usual.
6. **Hidden tests stay hidden.** Grading (`scripts/grade_hidden.py`) runs only after generation, with vLLM
   stopped. Never show hidden-test inputs, grades or labels to a generator or a judge, and never use test
   labels to choose a model, a threshold or a feature.
7. **Run data stays out of git.** `results/` is git-ignored. Only aggregate results and the trace export
   made by `scripts/export_traces.py` go into git, and only when the operator asks.
8. **Freeze before test data.** Before you generate on any test task, the hypotheses, the analysis plan
   and the frozen routers must be committed and the commit tagged. Record every later change as a dated
   amendment.
9. **Do not restart a job that the system stopped** unless the operator asks. Report what happened.
10. **Commit and push only when the operator asks.** One approval does not cover later commits. A
    runbook step that says "commit" means "commit after the operator approves".

## Tasks with their own runbook

- **Collect data with a different (for example 7–8B) generator:**
  [docs/new-generator-runbook.md](docs/new-generator-runbook.md).
- **Check whether Jev changed since earlier scoring:** `scripts/analysis/jev_drift_check.py` (see its
  docstring; the scoring step is billed).
- **Export traces for review:** `uv run python scripts/export_traces.py --run-id <run-id>` (see its
  docstring; it refuses to overwrite an export unless `--force` is given).

## Useful facts

- Environment: `uv sync` (add `uv sync --group pinocchio` for Pinocchio). Unit tests: `uv run pytest`.
- Every script states its usage in its docstring; read it before you run the script.
- A generation run's fingerprint (`run_meta.json`) includes the git commit. Protocol runs need a clean
  tree, and **a generation run continues after an interruption only on the same commit**: do not commit
  between the sessions of one run. (Jev scoring records the commit per session but does not compare it.)
- `--allow-dirty` lets a smoke run start with uncommitted changes; the run is marked non-protocol only
  when the tree really has changes. Give smoke runs their own run ids and never analyze them.
- The full protocol, glossary and reproduction table: [docs/review-guide.md](docs/review-guide.md).
