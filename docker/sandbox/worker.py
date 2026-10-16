"""Hidden-test grader worker. Runs inside the network-less `sandbox` container only.

It holds the EvalPlus datasets and ground truth, so it never runs the visible
tests (those run in disposable containers, see visible_runner.py) and it runs
only after generation: scripts/grade_hidden.py drives it.

Protocol: one JSON request per line on stdin, one JSON reply per line on
stdout. Every reply has "ok": true/false.

  {"op": "ping"}
  {"op": "load", "datasets": ["humaneval"|"mbpp", ...]}
  {"op": "hidden", "dataset": str, "task_id": str, "code": str}
      -> EvalPlus check_correctness on base and plus inputs, plus the memory
         facts of the call (see op_hidden)
  {"op": "canonical", "dataset": str, "task_id": str, "extra": str}
      -> the same check on the task's own reference solution (+ `extra` code,
         for the allocation canary); used to calibrate the grader
  {"op": "reference", "dataset": ..., "task_id": str, "n": int}
      -> the first n original inputs and their ground-truth outputs, as repr()

Ground truth: `python worker.py --precompute` once with a writable EvalPlus
cache; later runs mount the cache read-only and only load it.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

import evalplus.eval as _evalplus_eval
from evalplus.data import get_human_eval_plus, get_human_eval_plus_hash, get_mbpp_plus, get_mbpp_plus_hash
from evalplus.evaluate import MBPP_OUTPUT_NOT_NONE_TASKS, PASS, check_correctness, get_groundtruth

_unsafe_execute = _evalplus_eval.unsafe_execute


def _unsafe_execute_without_proto(*args, **kwargs):
    """EvalPlus runs model code in a forked child; close the protocol copy there first."""
    if _PROTO_FD is not None:
        try:
            os.close(_PROTO_FD)
        except OSError:
            pass
    return _unsafe_execute(*args, **kwargs)


_evalplus_eval.unsafe_execute = _unsafe_execute_without_proto  # untrusted_check looks it up by name

WORKER_VERSION = "grader-v3"
# Address space a graded child may add to what the worker already maps. EvalPlus
# applies EVALPLUS_MAX_MEMORY_BYTES as an absolute RLIMIT_AS/RLIMIT_DATA in a
# child forked from this worker, so the absolute value is set per call.
CANDIDATE_BUDGET_BYTES = 4 * 1024**3
MEMORY_EVENTS = "/sys/fs/cgroup/memory.events"
_DATA: dict = {}
_PROTO_FD: int | None = None  # closed in children, so model code cannot forge replies


def load(dataset: str) -> tuple[dict, dict]:
    if dataset not in _DATA:
        if dataset == "humaneval":
            problems = get_human_eval_plus()
            gt = get_groundtruth(problems, get_human_eval_plus_hash(), [])
        elif dataset == "mbpp":
            problems = get_mbpp_plus()
            gt = get_groundtruth(problems, get_mbpp_plus_hash(), MBPP_OUTPUT_NOT_NONE_TASKS)
        else:
            raise ValueError(f"unknown dataset {dataset!r}")
        _DATA[dataset] = (problems, gt)
    return _DATA[dataset]


def _vm_size_bytes() -> int:
    with open("/proc/self/statm", encoding="ascii") as f:
        return int(f.read().split()[0]) * os.sysconf("SC_PAGE_SIZE")


def _memory_events() -> dict[str, int]:
    with open(MEMORY_EVENTS, encoding="ascii") as f:
        return {k: int(v) for k, v in (line.split() for line in f if line.strip())}


def _grade(dataset: str, task_id: str, code: str) -> dict:
    problems, gt = load(dataset)
    vm = _vm_size_bytes()
    os.environ["EVALPLUS_MAX_MEMORY_BYTES"] = str(vm + CANDIDATE_BUDGET_BYTES)
    effective = _evalplus_eval.query_maximum_memory_bytes()  # after EvalPlus's own clamp
    mem0 = _memory_events()
    res = check_correctness(dataset, 0, problems[task_id], code, gt[task_id], fast_check=True)
    mem1 = _memory_events()
    base, plus = res["base"][0], res["plus"][0]
    # A child killed by the container's memory limit is reported by EvalPlus as
    # "timeout"; such a grade is invalid, not a failure.
    oom = mem1.get("oom_kill", 0) > mem0.get("oom_kill", 0)
    return {"ok": True, "base": base, "plus": plus, "passed": base == PASS and plus == PASS,
            "valid": not oom, "oom_kill": oom, "vm_size": vm, "memory_limit": effective}


def op_hidden(req: dict) -> dict:
    return _grade(req["dataset"], req["task_id"], req["code"])


def op_canonical(req: dict) -> dict:
    problems, _ = load(req["dataset"])
    p = problems[req["task_id"]]
    return _grade(req["dataset"], req["task_id"], p["prompt"] + p["canonical_solution"] + req.get("extra", ""))


def op_reference(req: dict) -> dict:
    problems, gt = load(req["dataset"])
    p, n = problems[req["task_id"]], int(req.get("n", 3))
    pairs = [{"args": repr(list(args)), "output": repr(out)}
             for args, out in zip(p["base_input"][:n], gt[req["task_id"]]["base"][:n])]
    return {"ok": True, "entry_point": p["entry_point"], "pairs": pairs}


def op_ping(req: dict) -> dict:
    import evalplus
    from evalplus.config import DEFAULT_GT_TIME_LIMIT_FACTOR, DEFAULT_MIN_TIME_LIMIT
    _memory_events()  # the cgroup counters must be readable, or grades cannot be checked
    settings = {"evalplus": evalplus.__version__, "min_time_limit": DEFAULT_MIN_TIME_LIMIT,
                "gt_time_limit_factor": DEFAULT_GT_TIME_LIMIT_FACTOR, "fast_check": True,
                "timeout_per_task": os.getenv("EVALPLUS_TIMEOUT_PER_TASK", 60),
                "candidate_budget_bytes": CANDIDATE_BUDGET_BYTES}
    return {"ok": True, "pid": os.getpid(), "version": WORKER_VERSION, "datasets": sorted(_DATA),
            "settings": settings}


def op_load(req: dict) -> dict:
    for ds in req.get("datasets", ["humaneval", "mbpp"]):
        load(ds)
    return {"ok": True, "vm_size": _vm_size_bytes(), "datasets": sorted(_DATA)}


OPS = {"ping": op_ping, "load": op_load, "hidden": op_hidden, "canonical": op_canonical, "reference": op_reference}


def serve() -> None:
    # Replies go to a private copy of the original stdout. File descriptor 1 is
    # pointed at stderr, so prints from EvalPlus or from model code (also
    # os.write(1, ...) in child processes) cannot corrupt the protocol.
    global _PROTO_FD
    _PROTO_FD = os.dup(1)
    proto = os.fdopen(_PROTO_FD, "w", buffering=1)
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            reply = OPS[req["op"]](req)
        except Exception as e:  # noqa: BLE001 - the worker must keep serving
            reply = {"ok": False, "error": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-1500:]}
        proto.write(json.dumps(reply) + "\n")
        proto.flush()


if __name__ == "__main__":
    if "--precompute" in sys.argv:
        for ds in ("humaneval", "mbpp"):
            problems, _ = load(ds)
            print(f"{ds}: ground truth ready for {len(problems)} tasks", flush=True)
    else:
        serve()
