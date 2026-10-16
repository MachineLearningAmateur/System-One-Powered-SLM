"""The write -> test -> revise loop for one attempt, with durable checkpoint records.

Fixed loop (docs/research-plan.md, Benchmarks): after each test run the
policy may escalate or continue. Here the loop always continues, so that every
checkpoint is logged; escalation policies are replayed offline. If the
visible tests pass, the candidate is accepted and the attempt ends. If they
fail and rounds remain, the model revises. After round 3 the last candidate
is returned. Missing code counts as a failed checkpoint and is recorded.

Harness failures are different: a vLLM error or a sandbox error is written to
failures.jsonl (and the ledger), and the attempt stops with AttemptFailed. The
model never sees harness error text, and a resumed run reruns the attempt.

The hidden EvalPlus label is not computed here. scripts/grade_hidden.py grades
every complete checkpoint after generation (vLLM stopped) and writes
hidden_labels.jsonl; analyses join it with system1.eval.labels.load_labelled().
Every HTTP call to vLLM is written to the cost ledger when it ends.
"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx
import numpy as np

from system1.eval.ledger import CostLedger, LedgerRow
from system1.features.evidence import Checkpoint
from system1.features.telemetry import cheap_features, jev_telemetry
from system1.loop.generate import MODEL, SEED_TAG, Generator
from system1.loop.sandbox import SandboxError, VisibleRunner
from system1.loop.tasks import TaskSpec, first_round_messages, format_test_report, render_test, revise_messages

MAX_ROUNDS = 3
VISIBLE_TIMEOUT_S = 10.0  # one total deadline: loading the code and all visible tests
NO_CODE_MESSAGE = {
    "no_block": "the answer contains no ```python code block",
    "answer_cut": "the answer was cut off before its code block closed",
    "no_close": "the response ended inside its thinking, without an answer",
}


class AttemptFailed(RuntimeError):
    """A harness failure (not a model failure) stopped the attempt; it is rerun on resume."""


@dataclass
class RunContext:
    run_id: str
    split: str  # dev | test
    generator: Generator
    visible: VisibleRunner  # one disposable container per visible check
    store: CostLedger  # trajectory records (JSONL), one per checkpoint
    ledger: CostLedger  # cost ledger
    failures: CostLedger  # harness failures (JSONL)
    logprob_dir: Path


def shown_task(task: TaskSpec) -> str:
    """The task as the model and Jev see it."""
    return task.prompt.rstrip() + (f"\n\nVisible tests:\n{task.shown_tests}" if task.shown_tests else "")


def _fail(ctx: RunContext, task: TaskSpec, attempt: int, rnd: int, exec_id: str, stage: str, e: BaseException) -> None:
    """Record a harness failure. Generation calls are already in the ledger (one row per HTTP call)."""
    err = f"{type(e).__name__}: {e}"[:500]
    ctx.failures.append_obj({"run_id": ctx.run_id, "exec_id": exec_id, "task_id": task.task_id,
                             "attempt": attempt, "round": rnd, "stage": stage, "error": err})
    if stage == "sandbox":
        ctx.ledger.append(LedgerRow(component="sandbox", model=MODEL, provider="sandbox", task_id=task.task_id,
                                    attempt=attempt, step=rnd, call_id=f"{exec_id}:r{rnd}",
                                    status=f"sandbox:{type(e).__name__}"))


def _ledger_hook(ctx: RunContext, task: TaskSpec, attempt: int, rnd: int, exec_id: str):
    """Writes one ledger row per HTTP call to vLLM, when the call ends."""
    n = 0

    def hook(call: dict) -> None:
        nonlocal n
        ctx.ledger.append(LedgerRow(
            component="small_model", model=MODEL, provider="local-vllm", task_id=task.task_id,
            attempt=attempt, step=rnd, arm=call["phase"], call_id=f"{exec_id}:r{rnd}", http_attempt=n,
            input_tokens=call["input_tokens"], output_tokens=call["output_tokens"],
            reasoning_tokens=call["reasoning_tokens"],
            latency_ms=call["latency_ms"], status=call["status"],
            # The GPU serves several attempts at once, so this is wall time
            # per call, not exclusive GPU time; cost views use tokens and run time.
            gpu_seconds=None,
        ))
        n += 1
    return hook


async def run_attempt(ctx: RunContext, task: TaskSpec, attempt: int) -> list[dict[str, Any]]:
    # One id per execution of an attempt: if a run stops mid-attempt and is
    # resumed, the incomplete copy can be told apart and dropped.
    exec_id = uuid.uuid4().hex
    rounds: list[dict] = []
    records: list[dict] = []
    messages = first_round_messages(task)
    for rnd in range(1, MAX_ROUNDS + 1):
        try:
            g = await ctx.generator.generate(messages, task.prompt, task.entry_point,
                                             SEED_TAG, task.task_id, attempt, rnd,
                                             on_call=_ledger_hook(ctx, task, attempt, rnd, exec_id))
        except (httpx.HTTPError, ValueError, KeyError) as e:
            _fail(ctx, task, attempt, rnd, exec_id, "generate", e)
            raise AttemptFailed(f"generation failed: {e}") from e

        if g.code is None:
            execution = {"status": "no_code", "stage": "extract", "error_type": "NoCode",
                         "message": NO_CODE_MESSAGE[g.no_code_reason or "no_block"]}
            results = [{"status": "not_run", "error_type": None, "message": None} for _ in task.visible_tests]
            runner_version = None
        else:
            try:
                v = await asyncio.to_thread(ctx.visible.run, g.code, list(task.visible_tests), VISIBLE_TIMEOUT_S)
            except SandboxError as e:
                _fail(ctx, task, attempt, rnd, exec_id, "sandbox", e)
                raise AttemptFailed(f"sandbox failed: {e}") from e
            execution, results, runner_version = v["execution"], v["results"], v.get("runner")

        report = format_test_report(task.visible_tests, results, execution)
        rounds.append({"code": g.code, "results": results, "execution": execution, "report": report,
                       "thinking": g.thinking, "thinking_tokens": g.thinking_tokens, "cap_hit": g.cap_hit,
                       "think_closed": g.think_closed, "confidence": g.confidence})
        feats = cheap_features(rounds)
        prev = rounds[-2] if rnd > 1 else None
        cp_id = f"{task.task_id}/a{attempt}/r{rnd}"

        arrays_path = ctx.logprob_dir / f"{cp_id.replace('/', '_')}_{exec_id[:8]}.npz"
        arrays_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(arrays_path, **g.arrays)

        rec = {
            "run_id": ctx.run_id, "exec_id": exec_id, "checkpoint_id": cp_id, "task_id": task.task_id,
            "benchmark": task.benchmark, "split": ctx.split, "attempt": attempt, "round": rnd,
            "task_shown": shown_task(task), "visible_source": task.visible_source,
            "canonical_fails_visible": task.canonical_fails_visible,
            "visible_tests": [render_test(t) for t in task.visible_tests],
            "prompt_sha256": g.prompt_sha256, "seed": g.seed,
            "thinking": g.thinking, "answer": g.answer, "code": g.code, "imports_added": g.imports_added,
            "code_rule": g.code_rule, "n_code_blocks": g.n_code_blocks, "no_code_reason": g.no_code_reason,
            "visible_execution": execution, "visible_results": results, "visible_report": report,
            "visible_pass": feats["visible_pass"], "visible_runner": runner_version,
            "prev_code": (prev["code"] or "") if prev else None,
            "prev_report": prev["report"] if prev else None,
            "generation": {"prompt_tokens": g.prompt_tokens, "thinking_tokens": g.thinking_tokens,
                           "answer_tokens": g.answer_tokens, "effective_cap": g.effective_cap,
                           "cap_hit": g.cap_hit, "think_closed": g.think_closed,
                           "thinking_skipped": g.thinking_skipped, "phase1_finish": g.phase1_finish,
                           "answer_finish": g.answer_finish, "latency_ms": round(g.latency_ms, 1)},
            "confidence": g.confidence, "features": feats, "jev_telemetry": jev_telemetry(feats),
            "logprob_arrays": str(arrays_path.relative_to(ctx.logprob_dir.parent)),
        }
        ctx.store.append_obj(rec)
        records.append(rec)

        if feats["visible_pass"] or rnd == MAX_ROUNDS:
            break
        messages = revise_messages(task, g.code or "(no code was produced)", report)
    return records


def to_scoring_checkpoint(rec: dict[str, Any]) -> Checkpoint:
    """The Jev evidence for one stored checkpoint (no hidden label in it)."""
    return Checkpoint(
        task_id=rec["task_id"], benchmark=rec["benchmark"], attempt=rec["attempt"], round=rec["round"],
        task_prompt=rec["task_shown"], code=rec["code"] or "", visible_test_output=rec["visible_report"],
        visible_pass=rec["visible_pass"], thinking=rec["thinking"], telemetry=rec["jev_telemetry"],
        prev_code=rec["prev_code"], prev_test_output=rec["prev_report"],
    )


def execution_is_complete(recs: list[dict], max_rounds: int = MAX_ROUNDS) -> bool:
    """One task/attempt, rounds exactly 1..n, no visible pass before round n, and the
    last round ends the loop (a visible pass, or round max_rounds)."""
    if not recs or len({(r["task_id"], r["attempt"]) for r in recs}) != 1:
        return False
    if [r["round"] for r in recs] != list(range(1, len(recs) + 1)) or len(recs) > max_rounds:
        return False
    if any(r["visible_pass"] for r in recs[:-1]):
        return False
    return bool(recs[-1]["visible_pass"]) or len(recs) == max_rounds


def complete_executions(rows: list[dict], max_rounds: int = MAX_ROUNDS,
                        dropped: list[dict] | None = None) -> list[dict]:
    """Rows of complete executions only, one execution per (task, attempt): the one
    written last. Analyses must use this. Executions that are not complete, and
    complete ones replaced by a later copy, go to `dropped` (their costs stay in the ledger)."""
    by_exec: dict[str, list[dict]] = {}
    for r in rows:
        by_exec.setdefault(r["exec_id"], []).append(r)
    chosen: dict[tuple[str, int], tuple[str, list[dict]]] = {}
    for exec_id, recs in by_exec.items():  # file order: a later execution comes later
        recs.sort(key=lambda r: r["round"])
        if not execution_is_complete(recs, max_rounds):
            if dropped is not None:
                dropped.append({"exec_id": exec_id, "reason": "incomplete", "n_rows": len(recs)})
            continue
        key = (recs[0]["task_id"], recs[0]["attempt"])
        if key in chosen and dropped is not None:
            dropped.append({"exec_id": chosen[key][0], "reason": "replaced", "n_rows": len(chosen[key][1])})
        chosen[key] = (exec_id, recs)
    return [r for _, recs in chosen.values() for r in recs]
