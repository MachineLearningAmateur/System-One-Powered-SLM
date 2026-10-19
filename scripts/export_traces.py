"""Export the small model's test-run thinking traces for review (October 18, after the analysis).

    uv run python scripts/export_traces.py --run-id main-test-v1

Writes docs/traces/:
  * README.md, an index of every task with links;
  * <benchmark>/<task>/README.md, one page per task: the prompt the model saw, the visible tests
    and a table of its attempts;
  * <benchmark>/<task>/attempt_<n>.md, one page per attempt: for each round the thinking, the code
    and the visible-test report (one page per attempt keeps each page small enough to render);
  * <run-id>_traces.jsonl.gz, the same fields in machine-readable form.
Only what the small model wrote and saw is exported. Hidden-test results, Jev and Pinocchio
scores and logprob arrays are not. Tasks excluded from the analysis (Amendment A2) are kept and
marked. Refuses to overwrite an existing export unless --force is given.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import shutil
import sys
from collections import defaultdict

from system1.config import RESULTS, ROOT
from system1.eval.exclusions import load_exclusions

OUT = ROOT / "docs" / "traces"
FIELDS = ("checkpoint_id", "task_id", "benchmark", "attempt", "round", "thinking", "answer", "code",
          "visible_pass", "visible_report")
GEN = ("prompt_tokens", "thinking_tokens", "answer_tokens", "cap_hit", "think_closed")


def fence(text: str, lang: str = "") -> str:
    """A code fence longer than any backtick run inside the text."""
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    f = "`" * max(3, longest + 1)
    return f"{f}{lang}\n{text.rstrip()}\n{f}"


def slug(task_id: str) -> str:
    return task_id.replace("/", "_")


def attempt_end(rounds: list[dict]) -> str:
    last = rounds[-1]
    return "visible pass" if last["visible_pass"] else f"no visible pass after round {last['round']}"


def task_page(task_id: str, attempts: dict[int, list[dict]], excluded: bool) -> str:
    first = next(iter(attempts.values()))[0]
    out = [f"# {task_id}", "", f"Benchmark: {first['benchmark']}. Run: `{first['run_id']}`. "
           f"Back to the [index](../../README.md).", ""]
    if excluded:
        out += ["> **Excluded from every analysis (Amendment A2):** the EvalPlus 0.3.1 oracle of this task "
                "cannot pass any solution. The traces are kept for completeness.", ""]
    out += ["## Attempts", "", "| Attempt | Rounds | End | Thinking tokens per round | Cap hits |",
            "| --- | --- | --- | --- | --- |"]
    for a, rounds in attempts.items():
        toks = " / ".join(str(r["generation"]["thinking_tokens"]) for r in rounds)
        caps = sum(r["generation"]["cap_hit"] for r in rounds)
        out.append(f"| [Attempt {a}](attempt_{a}.md) | {len(rounds)} | {attempt_end(rounds)} | {toks} | {caps} |")
    out += ["", "## Prompt shown to the model (round 1)", "", fence(first["task_shown"], "python"), "",
            "## Visible tests", "", fence("\n".join(map(str, first["visible_tests"])), "python"), ""]
    return "\n".join(out)


def attempt_page(task_id: str, a: int, rounds: list[dict]) -> str:
    out = [f"# {task_id}, attempt {a}", "", f"{len(rounds)} round{'s' if len(rounds) > 1 else ''}; "
           f"{attempt_end(rounds)}. Back to the [task](README.md). The prompt and the visible tests are on the "
           "task page; from round 2, the model also got its previous code and its visible-test report "
           "(never its previous thinking).", ""]
    for r in rounds:
        g = r["generation"]
        out += [f"## Round {r['round']} (`{r['checkpoint_id']}`)", "",
                f"Visible tests: **{'pass' if r['visible_pass'] else 'fail'}**. Thinking tokens: "
                f"{g['thinking_tokens']}{' (hit the 8,192-token cap)' if g['cap_hit'] else ''}. "
                f"Answer tokens: {g['answer_tokens']}.", "",
                "<details><summary>Thinking</summary>", "", fence(r["thinking"] or "(empty)", "text"), "",
                "</details>", "", "**Code that ran:**", "", fence(r["code"] or "(no code)", "python"), "",
                "**Visible-test report:**", "", fence(r["visible_report"] or "(none)", "text"), ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if OUT.exists():
        if not args.force:
            raise SystemExit(f"STOP: {OUT} exists; use --force to write it again")
        for p in OUT.iterdir():  # empty the folder, keep it (it may be a shell's working directory)
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    excluded = set(load_exclusions()["tasks"])
    rows = [json.loads(line) for line in
            (RESULTS / "runs" / args.run_id / "trajectories.jsonl").open(encoding="utf-8")]
    if len({r["checkpoint_id"] for r in rows}) != len(rows):
        raise SystemExit("STOP: duplicate checkpoint ids")
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task_id"]].append(r)

    index = ["# Thinking traces of the test run", "",
             f"Every checkpoint of run `{args.run_id}`: {len(by_task)} test tasks, {len(rows):,} checkpoints. "
             "Each task page shows the prompt the small model (Qwen3-1.7B) saw and the visible tests, and links to one "
             "page per attempt with the thinking, the code and the visible-test report of each round. Hidden-test results, Jev and Pinocchio "
             "scores are not included. Made by `scripts/export_traces.py`; machine-readable copy: "
             f"[{args.run_id}_traces.jsonl.gz]({args.run_id}_traces.jsonl.gz). Back to the [README](../../README.md).", "",
             "| Task | Benchmark | Attempts | Checkpoints | Attempts with a visible pass | Cap hits |",
             "| --- | --- | --- | --- | --- | --- |"]
    sizes = []
    key = lambda t: (by_task[t][0]["benchmark"], int(t.split("/")[1]))
    for t in sorted(by_task, key=key):
        rs = by_task[t]
        bench = rs[0]["benchmark"].rstrip("+")
        d = OUT / bench / slug(t)
        d.mkdir(parents=True, exist_ok=True)
        attempts = defaultdict(list)
        for r in sorted(rs, key=lambda r: (r["attempt"], r["round"])):
            attempts[r["attempt"]].append(r)
        (d / "README.md").write_text(task_page(t, attempts, t in excluded), encoding="utf-8", newline="\n")
        for a, rounds in attempts.items():
            text = attempt_page(t, a, rounds)
            (d / f"attempt_{a}.md").write_text(text, encoding="utf-8", newline="\n")
            sizes.append((len(text.encode()), f"{t} attempt {a}"))
        vp = sum(rounds[-1]["visible_pass"] for rounds in attempts.values())
        caps = sum(r["generation"]["cap_hit"] for r in rs)
        mark = " (excluded, A2)" if t in excluded else ""
        index.append(f"| [{t}]({bench}/{slug(t)}/README.md){mark} | {rs[0]['benchmark']} | {len(attempts)} "
                     f"| {len(rs)} | {vp} | {caps} |")
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8", newline="\n")
    with gzip.open(OUT / f"{args.run_id}_traces.jsonl.gz", "wt", encoding="utf-8") as f:
        for r in sorted(rows, key=lambda r: r["checkpoint_id"]):
            f.write(json.dumps({**{k: r[k] for k in FIELDS}, **{k: r["generation"][k] for k in GEN},
                                "excluded_a2": r["task_id"] in excluded}) + "\n")
    sizes.sort(reverse=True)
    print(f"written {len(by_task)} task pages and {len(sizes)} attempt pages to {OUT}; largest {sizes[0][0] / 1e3:.0f} KB ({sizes[0][1]}), "
          f"median {sizes[len(sizes) // 2][0] / 1e3:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
