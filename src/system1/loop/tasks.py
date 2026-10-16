"""Tasks, visible tests and prompts for the write -> test -> revise loop.

Rule: the visible tests are exactly the examples the model sees.
  - MBPP+: the one `assert` line inside the task prompt.
  - HumanEval+: the `>>>` examples in the docstring; for a task without a
    usable example, the first three original HumanEval inputs with their
    ground-truth outputs, shown to the model as an explicit test list.
The visible tests are built once by scripts/make_visible_tests.py and frozen
in configs/visible_tests_v2.json. The hidden EvalPlus tests never reach the
model or Jev; they only produce the label.
"""

from __future__ import annotations

import ast
import doctest
import json
import re
from dataclasses import dataclass
from pathlib import Path

from system1.config import CONFIGS

VISIBLE_TESTS_PATH = CONFIGS / "visible_tests_v2.json"
# Tasks whose own reference solution fails a visible example because the
# HumanEval docstring itself is wrong. Kept (it is what the model sees) and
# flagged with canonical_fails_visible, so analyses can stratify them.
KNOWN_BAD_DOCSTRINGS = {"HumanEval/47", "HumanEval/116"}
DATASET = {"humaneval+": "humaneval", "mbpp+": "mbpp"}  # benchmark -> EvalPlus dataset name

INSTRUCTION = (
    "Write a correct Python solution for the task below. "
    "Reply with the complete code in one ```python code block, including any imports it needs."
)


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    benchmark: str  # humaneval+ | mbpp+
    prompt: str  # the task as EvalPlus gives it
    entry_point: str
    visible_tests: tuple[dict, ...]  # {"kind": "assert"|"compare", ...}
    visible_source: str  # prompt_assert | docstring | base_input
    shown_tests: str  # extra test list appended to the prompt ("" if the prompt already shows them)
    canonical_fails_visible: bool = False  # the reference solution fails a visible example

    @property
    def dataset(self) -> str:
        return DATASET[self.benchmark]


def _clean_want(want: str) -> str:
    """Doctest 'want' text without a closing docstring line swallowed after it."""
    kept = []
    for line in want.splitlines():
        if line.strip().startswith(('"""', "'''")):
            break
        kept.append(line)
    return "\n".join(kept).strip()


def docstring_tests(prompt: str, entry_point: str) -> list[dict]:
    """Usable `>>>` examples.

    `>>> f(x)` + an output line -> compare test (an empty output means None).
    `>>> f(x) == y` with no output line -> the line itself is the check, so it
    becomes an assert test. Anything else (invalid Python, or an expression
    that is not a call, such as `f(x) [0, 1]`) is skipped.
    """
    tests = []
    for ex in doctest.DocTestParser().get_examples(prompt):
        call = ex.source.strip()
        if entry_point not in call:
            continue
        try:
            node = ast.parse(call, mode="eval").body
        except SyntaxError:
            continue
        want = _clean_want(ex.want)
        if not want and isinstance(node, ast.Compare):
            tests.append({"kind": "assert", "source": f"assert {call}"})
            continue
        if not isinstance(node, ast.Call):  # e.g. `f(x) [0, 1]`: a garbled example, not a call
            continue
        want = want or "None"
        try:
            ast.literal_eval(want)
        except (ValueError, SyntaxError):
            continue
        tests.append({"kind": "compare", "call": call, "expected": want})
    return tests


def prompt_assert_tests(prompt: str) -> list[dict]:
    return [{"kind": "assert", "source": line.strip()} for line in prompt.splitlines()
            if re.match(r"^\s*assert\s", line)]


def reference_tests(entry_point: str, pairs: list[dict]) -> list[dict]:
    """Compare tests from (args, output) repr pairs; pairs that are not Python literals are skipped."""
    tests = []
    for pair in pairs:
        try:
            args = ast.literal_eval(pair["args"])
            ast.literal_eval(pair["output"])
        except (ValueError, SyntaxError):
            continue
        call = f"{entry_point}({', '.join(repr(a) for a in args)})"
        tests.append({"kind": "compare", "call": call, "expected": pair["output"]})
    return tests


def render_test(t: dict) -> str:
    return t["source"] if t["kind"] == "assert" else f"assert {t['call']} == {t['expected']}"


def load_tasks(path: Path = VISIBLE_TESTS_PATH) -> dict[str, TaskSpec]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return {tid: TaskSpec(task_id=tid, benchmark=t["benchmark"], prompt=t["prompt"], entry_point=t["entry_point"],
                          visible_tests=tuple(t["visible_tests"]), visible_source=t["visible_source"],
                          shown_tests=t["shown_tests"],
                          canonical_fails_visible=t.get("canonical_fails_visible", False))
            for tid, t in raw["tasks"].items()}


def first_round_messages(task: TaskSpec) -> list[dict]:
    body = f"{INSTRUCTION}\n\n{task.prompt.rstrip()}\n"
    if task.shown_tests:
        body += f"\nYour code must pass these tests:\n{task.shown_tests}\n"
    return [{"role": "user", "content": body}]


def revise_messages(task: TaskSpec, prev_code: str, report: str) -> list[dict]:
    """Next round: only the previous code and its test output are carried, not the thinking."""
    body = f"{INSTRUCTION}\n\n{task.prompt.rstrip()}\n"
    if task.shown_tests:
        body += f"\nYour code must pass these tests:\n{task.shown_tests}\n"
    body += (f"\nYour previous code:\n```python\n{prev_code.rstrip()}\n```\n"
             f"\nIt failed the visible tests:\n{report.rstrip()}\n"
             "\nFix the code. Reply with the complete corrected code in one ```python code block.")
    return [{"role": "user", "content": body}]


LOAD_LINES = {
    "error": "The code did not load: {error_type}: {message}",
    "timeout": "The code did not finish loading: {message}",
    "oom": "The code did not finish loading: it reached the memory limit",
    "crash": "The code did not finish loading: {message}",
    "no_code": "No code to test: {message}",
}


def format_test_report(tests: tuple[dict, ...], results: list[dict], execution: dict | None = None) -> str:
    """The visible-test output the model and Jev see. A load failure is one line at
    the top; tests that never ran are listed as NOT_RUN."""
    lines = []
    if execution and execution.get("stage") in ("load", "extract"):
        lines.append(LOAD_LINES[execution["status"]].format(**execution))
    for t, r in zip(tests, results):
        line = f"{r['status'].upper():7s} {render_test(t)}"
        if r["status"] != "pass" and r.get("message"):
            line += f"\n        {r['error_type']}: {r['message']}" if r.get("error_type") else f"\n        {r['message']}"
        lines.append(line)
    n_pass = sum(r["status"] == "pass" for r in results)
    lines.append(f"{n_pass} of {len(results)} visible tests passed")
    return "\n".join(lines)
