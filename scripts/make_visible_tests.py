"""Build the frozen visible tests (run once, with the sandbox container running).

    docker compose build sandbox && docker compose up -d sandbox
    uv run python scripts/make_visible_tests.py            # build (refuses to overwrite)
    uv run python scripts/make_visible_tests.py --check    # run the gate again on the frozen file

Writes configs/visible_tests_v2.json and refuses to overwrite it (use --force
only to rebuild on purpose). See src/system1/loop/tasks.py for the rule.

Gate: every task's EvalPlus reference solution must pass its own visible
tests, run exactly as candidates are (VisibleRunner, one disposable
container per check). A failure stops the build, except for the known wrong
HumanEval docstrings (KNOWN_BAD_DOCSTRINGS), which are kept and flagged.
The reference inputs for HumanEval tasks without docstring examples come from
the grader worker (the only place with the ground truth).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date

import evalplus
from evalplus.data import get_human_eval_plus, get_mbpp_plus

from system1.eval.split import file_sha256
from system1.loop.sandbox import Sandbox, VisibleRunner
from system1.loop.tasks import (
    KNOWN_BAD_DOCSTRINGS,
    VISIBLE_TESTS_PATH,
    docstring_tests,
    prompt_assert_tests,
    reference_tests,
    render_test,
)

N_REFERENCE = 3


def gate(tasks: dict, sources: dict, workers: int = 4) -> tuple[list[str], int]:
    """Problems found, and the number of flagged known-bad tasks. Sets canonical_fails_visible."""
    runner = VisibleRunner(max_concurrent=workers)
    with ThreadPoolExecutor(workers) as ex:
        replies = dict(zip(tasks, ex.map(lambda tid: runner.run(sources[tid], tasks[tid]["visible_tests"], 10.0),
                                         tasks)))
    problems, flagged = [], 0
    for tid, t in tasks.items():
        r = replies[tid]
        failed = [render_test(x) + f"  -> {res['status']} {res.get('error_type') or ''} {res.get('message') or ''}"
                  for x, res in zip(t["visible_tests"], r["results"]) if res["status"] != "pass"]
        if r["execution"]["status"] != "ok":
            failed.append(f"execution {r['execution']}")
        t["canonical_fails_visible"] = bool(failed)
        if failed and tid not in KNOWN_BAD_DOCSTRINGS:
            problems.append(f"{tid}: reference solution fails visible tests:\n      " + "\n      ".join(failed))
        elif failed:
            flagged += 1
        elif tid in KNOWN_BAD_DOCSTRINGS:
            problems.append(f"{tid}: listed as a known wrong docstring, but the reference solution passes")
    return problems, flagged


def reference_sources() -> dict[str, str]:
    out = {tid: p["prompt"] + p["canonical_solution"] for tid, p in get_mbpp_plus().items()}
    out.update({tid: p["prompt"] + p["canonical_solution"] for tid, p in get_human_eval_plus().items()})
    return out


def check() -> int:
    frozen = json.loads(VISIBLE_TESTS_PATH.read_text(encoding="utf-8"))["tasks"]
    tasks = {tid: dict(t) for tid, t in frozen.items()}
    problems, flagged = gate(tasks, reference_sources())
    changed = [tid for tid in tasks if tasks[tid]["canonical_fails_visible"] != frozen[tid].get("canonical_fails_visible")]
    print(f"gate on {len(tasks)} tasks: {len(problems)} problems, {flagged} flagged, {len(changed)} flags changed")
    for x in problems + [f"flag changed: {tid}" for tid in changed]:
        print("  " + x)
    return 0 if not problems and not changed else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--check", action="store_true", help="run the gate on the frozen file; write nothing")
    args = ap.parse_args()
    if args.check:
        return check()
    if VISIBLE_TESTS_PATH.exists() and not args.force:
        print(f"{VISIBLE_TESTS_PATH} exists and is frozen; use --force only to rebuild it on purpose.")
        return 1

    sb = Sandbox()
    tasks, counts, problems = {}, Counter(), []
    sources = {}
    for tid, p in get_mbpp_plus().items():
        tests = prompt_assert_tests(p["prompt"])
        if len(tests) != 1:
            problems.append(f"{tid}: {len(tests)} asserts in the prompt")
        tasks[tid] = dict(benchmark="mbpp+", prompt=p["prompt"], entry_point=p["entry_point"],
                          visible_tests=tests, visible_source="prompt_assert", shown_tests="")
        sources[tid] = p["prompt"] + p["canonical_solution"]
        counts["mbpp+/prompt_assert"] += 1

    for tid, p in get_human_eval_plus().items():
        tests = docstring_tests(p["prompt"], p["entry_point"])
        source, shown = "docstring", ""
        if not tests:
            ref = sb.reference("humaneval", tid, N_REFERENCE)
            tests = reference_tests(p["entry_point"], ref["pairs"])
            source, shown = "base_input", "\n".join(render_test(t) for t in tests)
        if not tests:
            problems.append(f"{tid}: no visible test could be built")
        tasks[tid] = dict(benchmark="humaneval+", prompt=p["prompt"], entry_point=p["entry_point"],
                          visible_tests=tests, visible_source=source, shown_tests=shown)
        sources[tid] = p["prompt"] + p["canonical_solution"]
        counts[f"humaneval+/{source}"] += 1

    sb.close()
    # Gate: the reference solution must pass its own visible tests.
    gate_problems, flagged = gate(tasks, sources)
    problems += gate_problems
    if flagged:
        counts["flagged: known wrong docstring"] = flagged

    if problems:
        print("STOP: the visible tests did not pass the gate:\n  " + "\n  ".join(problems))
        return 1
    out = {"created": date.today().isoformat(), "evalplus": getattr(evalplus, "__version__", "unknown"),
           "rule": "visible tests = the examples the model sees; see src/system1/loop/tasks.py",
           "gate": "every reference solution passes its visible tests, except KNOWN_BAD_DOCSTRINGS (flagged)",
           "counts": dict(counts), "tasks": tasks}
    VISIBLE_TESTS_PATH.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    for k, v in sorted(counts.items()):
        print(f"{k:32s} {v}")
    print(f"written {VISIBLE_TESTS_PATH}  sha256 {file_sha256(VISIBLE_TESTS_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
