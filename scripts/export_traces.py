"""Export the small model's test-run thinking traces for review (October 18, after the analysis).

    uv run python scripts/export_traces.py --run-id main-test-v1 [--force]

Writes docs/traces/:
  * README.md, an index of every task with links and a hidden-test indicator per task;
  * <benchmark>/<task>/README.md, one page per task: the prompt the model saw, the visible tests
    and a table of its attempts with the hidden-test result of each final code;
  * <benchmark>/<task>/attempt_<n>.md, one page per attempt: for each round the thinking, the code,
    the visible-test report and the hidden-test result (one page per attempt keeps each page small
    enough to render);
  * <run-id>_traces.jsonl.gz, the same fields in machine-readable form.
Hidden-test results come from load_labelled (the protocol grading session; Amendment A2 applies),
added on the user's request after the analysis. Jev and Pinocchio scores and logprob arrays are
not exported. Tasks excluded from the analysis are kept and marked as not graded.
Refuses to overwrite an existing export unless --force is given.
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
from system1.eval.labels import load_labelled

OUT = ROOT / "docs" / "traces"
FIELDS = ("checkpoint_id", "task_id", "benchmark", "attempt", "round", "thinking", "answer", "code",
          "visible_pass", "visible_report")
GEN = ("prompt_tokens", "thinking_tokens", "answer_tokens", "cap_hit", "think_closed")
ALL_PASS, SOME_FAIL, ALL_FAIL, NOT_GRADED = "🟢", "🟡", "🔴", "⚪"


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


def hidden_text(r: dict) -> str:
    h = r["hidden_passed"]
    return "not graded (A2)" if h is None else ("✅ pass" if h else "❌ fail")


def attempt_flag(rounds: list[dict]) -> str:
    """The final code's hidden result; the routing case (visible pass, hidden fail) is marked."""
    last = rounds[-1]
    if last["hidden_passed"] is None:
        return "not graded (A2)"
    if last["hidden_passed"]:
        return "✅ pass"
    return "❌ fail ⚠️ visible pass" if last["visible_pass"] else "❌ fail"


def task_page(task_id: str, attempts: dict[int, list[dict]], excluded: bool) -> str:
    first = next(iter(attempts.values()))[0]
    out = [f"# {task_id}", "", f"Benchmark: {first['benchmark']}. Run: `{first['run_id']}`. "
           f"Back to the [index](../../README.md).", ""]
    if excluded:
        out += ["> **Excluded from every analysis (Amendment A2):** the EvalPlus 0.3.1 oracle of this task "
                "cannot pass any solution, so no code of this task was graded. The traces are kept for "
                "completeness.", ""]
    out += ["## Attempts", "", "\"Hidden tests\" is the result of the attempt's final code on the full EvalPlus "
            "suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden "
            "tests: the case the routers try to catch.", "",
            "| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |",
            "| --- | --- | --- | --- | --- | --- |"]
    for a, rounds in attempts.items():
        toks = " / ".join(str(r["generation"]["thinking_tokens"]) for r in rounds)
        caps = sum(r["generation"]["cap_hit"] for r in rounds)
        out.append(f"| [Attempt {a}](attempt_{a}.md) | {len(rounds)} | {attempt_end(rounds)} | "
                   f"{attempt_flag(rounds)} | {toks} | {caps} |")
    out += ["", "## Prompt shown to the model (round 1)", "", fence(first["task_shown"], "python"), "",
            "## Visible tests", "", fence("\n".join(map(str, first["visible_tests"])), "python"), ""]
    return "\n".join(out)


def attempt_page(task_id: str, a: int, rounds: list[dict]) -> str:
    out = [f"# {task_id}, attempt {a}", "", f"{len(rounds)} round{'s' if len(rounds) > 1 else ''}; "
           f"{attempt_end(rounds)}; final code on the hidden tests: {attempt_flag(rounds)}. "
           "Back to the [task](README.md). The prompt and the visible tests are on the task page; from "
           "round 2, the model also got its previous code and its visible-test report (never its previous "
           "thinking, and never any hidden-test result).", ""]
    for r in rounds:
        g = r["generation"]
        out += [f"## Round {r['round']} (`{r['checkpoint_id']}`)", "",
                f"Visible tests: **{'pass' if r['visible_pass'] else 'fail'}**. Hidden tests: **{hidden_text(r)}**. "
                f"Thinking tokens: {g['thinking_tokens']}{' (hit the 8,192-token cap)' if g['cap_hit'] else ''}. "
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
    sys.stdout.reconfigure(encoding="utf-8")  # the summary line prints the indicator emoji
    if OUT.exists():
        if not args.force:
            raise SystemExit(f"STOP: {OUT} exists; use --force to write it again")
        for p in OUT.iterdir():  # empty the folder, keep it (it may be a shell's working directory)
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    run_dir = RESULTS / "runs" / args.run_id
    excluded = set(load_exclusions()["tasks"])
    rows = [json.loads(line) for line in (run_dir / "trajectories.jsonl").open(encoding="utf-8")]
    if len({r["checkpoint_id"] for r in rows}) != len(rows):
        raise SystemExit("STOP: duplicate checkpoint ids")
    hidden = {c["checkpoint_id"]: c["hidden"]["passed"] for c in load_labelled(run_dir, report={})}
    missing = [r["checkpoint_id"] for r in rows if r["task_id"] not in excluded and r["checkpoint_id"] not in hidden]
    if missing:
        raise SystemExit(f"STOP: {len(missing)} kept checkpoints have no hidden label, e.g. {missing[:3]}")
    for r in rows:
        r["hidden_passed"] = hidden.get(r["checkpoint_id"])
    by_task = defaultdict(list)
    for r in rows:
        by_task[r["task_id"]].append(r)

    lines, counts = [], defaultdict(int)
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
        finals = [rounds[-1] for rounds in attempts.values()]
        caps = sum(r["generation"]["cap_hit"] for r in rs)
        if t in excluded:
            mark, fails, vp_fail = NOT_GRADED, "—", "—"
        else:
            n_fail = sum(not f["hidden_passed"] for f in finals)
            n_vp_fail = sum(f["visible_pass"] and not f["hidden_passed"] for f in finals)
            mark = ALL_PASS if n_fail == 0 else (ALL_FAIL if n_fail == len(finals) else SOME_FAIL)
            fails, vp_fail = f"{n_fail} / {len(finals)}", (f"**{n_vp_fail}** ⚠️" if n_vp_fail else "0")
        counts[(bench, mark)] += 1
        lines.append(f"| {mark} | [{t}]({bench}/{slug(t)}/README.md) | {rs[0]['benchmark']} | {fails} | {vp_fail} "
                     f"| {len(rs)} | {caps} |")

    def tally(b: str | None) -> str:
        n = lambda m: sum(v for (bb, mm), v in counts.items() if mm == m and (b is None or bb == b))
        return f"{n(ALL_PASS)} {ALL_PASS} / {n(SOME_FAIL)} {SOME_FAIL} / {n(ALL_FAIL)} {ALL_FAIL}"

    index = ["# Thinking traces of the test run", "",
             f"Every checkpoint of run `{args.run_id}`: {len(by_task)} test tasks, {len(rows):,} checkpoints. "
             "Each task page shows the prompt the small model (Qwen3-1.7B) saw and the visible tests, and links to "
             "one page per attempt with the thinking, the code, the visible-test report and the hidden-test result "
             "of each round. Jev and Pinocchio scores are not included. Made by `scripts/export_traces.py`; "
             f"machine-readable copy: [{args.run_id}_traces.jsonl.gz]({args.run_id}_traces.jsonl.gz). "
             "Back to the [README](../../README.md).", "",
             "## How to read the indicator", "",
             "The indicator shows how the small model did **alone, without frontier help**: the final code of each "
             "attempt (after up to 3 rounds) on the full hidden EvalPlus suite.", "",
             f"- {ALL_PASS} every attempt's final code passes the hidden tests",
             f"- {SOME_FAIL} some attempts fail the hidden tests",
             f"- {ALL_FAIL} every attempt fails the hidden tests",
             f"- {NOT_GRADED} not graded (HumanEval/32, excluded by Amendment A2)",
             "- ⚠️ in \"Visible pass, hidden fail\": attempts whose code passed the visible tests but fails the "
             "hidden tests. These are the cases the routers try to catch.", "",
             f"Tasks: HumanEval+ {tally('humaneval')}; MBPP+ {tally('mbpp')}; both {tally(None)}.", "",
             "| | Task | Benchmark | Attempts that fail hidden tests | Visible pass, hidden fail | Checkpoints | Cap hits |",
             "| --- | --- | --- | --- | --- | --- | --- |"] + lines
    (OUT / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8", newline="\n")
    with gzip.open(OUT / f"{args.run_id}_traces.jsonl.gz", "wt", encoding="utf-8") as f:
        for r in sorted(rows, key=lambda r: r["checkpoint_id"]):
            f.write(json.dumps({**{k: r[k] for k in FIELDS}, **{k: r["generation"][k] for k in GEN},
                                "hidden_passed": r["hidden_passed"], "excluded_a2": r["task_id"] in excluded}) + "\n")
    sizes.sort(reverse=True)
    print(f"written {len(by_task)} task pages and {len(sizes)} attempt pages to {OUT}; largest "
          f"{sizes[0][0] / 1e3:.0f} KB ({sizes[0][1]}), median {sizes[len(sizes) // 2][0] / 1e3:.0f} KB")
    print("tasks:", "HumanEval+", tally("humaneval"), "| MBPP+", tally("mbpp"), "| both", tally(None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
