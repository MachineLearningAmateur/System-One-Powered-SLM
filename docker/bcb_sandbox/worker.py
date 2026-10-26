"""Networkless BigCodeBench hidden grader; only aggregate results leave the sandbox."""

from __future__ import annotations

import io
import json
import os
import select
import signal
import sys
import time
import types
import unittest

DATA_PATH = "/bcb/hidden.json"
VERSION = "bcb-grader-v2-assertEquals"
TIMEOUT_S = 30.0
_PROTO_FD: int | None = None


def memory_events() -> dict[str, int]:
    with open("/sys/fs/cgroup/memory.events", encoding="ascii") as f:
        return {k: int(v) for k, v in (line.split() for line in f)}


def child(code: str, test: str, w: int) -> None:
    if _PROTO_FD is not None:
        os.close(_PROTO_FD)
    null = os.open(os.devnull, os.O_RDWR)
    for fd in (0, 1, 2):
        os.dup2(null, fd)
    os.chdir("/tmp")
    try:
        # BigCodeBench v0.1.4 still calls this old unittest spelling in one
        # hidden suite. Python 3.12 removed it; restore its identical alias
        # before either the reference or a candidate is tested.
        unittest.TestCase.assertEquals = unittest.TestCase.assertEqual
        module = types.ModuleType("bcb_candidate")
        ns = module.__dict__
        exec(compile(code, "<candidate>", "exec"), ns)
        exec(compile(test, "<hidden_tests>", "exec"), ns)
        suite = unittest.defaultTestLoader.loadTestsFromModule(module)
        n = suite.countTestCases()
        if not n:
            out = {"valid": False, "passed": False, "n_tests": 0, "reason": "no_tests"}
        else:
            result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
            out = {"valid": True, "passed": result.wasSuccessful(), "n_tests": n,
                   "n_failures": len(result.failures), "n_errors": len(result.errors)}
    except BaseException as e:
        out = {"valid": True, "passed": False, "n_tests": None,
               "reason": "candidate_or_test_error", "error_type": type(e).__name__}
    os.write(w, json.dumps(out).encode("utf-8"))
    os._exit(0)


def grade(code: str, test: str) -> dict:
    before = memory_events()
    r, w = os.pipe()
    pid = os.fork()
    if pid == 0:
        os.close(r)
        child(code, test, w)
    os.close(w)
    deadline = time.monotonic() + TIMEOUT_S
    status = 0
    timed_out = False
    while True:
        done, status = os.waitpid(pid, os.WNOHANG)
        if done:
            break
        if time.monotonic() >= deadline:
            os.kill(pid, signal.SIGKILL)
            os.waitpid(pid, 0)
            timed_out = True
            break
        time.sleep(0.02)
    ready, _, _ = select.select([r], [], [], 0)
    payload = os.read(r, 4096) if ready else b""
    os.close(r)
    oom = memory_events().get("oom_kill", 0) > before.get("oom_kill", 0)
    if oom:
        return {"ok": True, "valid": False, "passed": False, "reason": "oom"}
    if timed_out:
        return {"ok": True, "valid": True, "passed": False, "reason": "timeout"}
    if not payload:
        return {"ok": True, "valid": False, "passed": False, "reason": f"child_exit_{status}"}
    return {"ok": True, **json.loads(payload)}


def main() -> None:
    global _PROTO_FD
    data = json.load(open(DATA_PATH, encoding="utf-8"))["tasks"]
    _PROTO_FD = os.dup(1)
    proto = os.fdopen(_PROTO_FD, "w", buffering=1)
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            op = req["op"]
            if op == "ping":
                out = {"ok": True, "pid": os.getpid(), "version": VERSION,
                       "n_tasks": len(data), "timeout_s": TIMEOUT_S}
            elif op in ("hidden", "canonical"):
                row = data[req["task_id"]]
                code = row["canonical_code"] if op == "canonical" else req["code"]
                out = grade(code, row["test"])
            else:
                out = {"ok": False, "error": "unknown operation"}
        except Exception as e:
            out = {"ok": False, "error": f"{type(e).__name__}: {e}"}
        proto.write(json.dumps(out) + "\n")


if __name__ == "__main__":
    main()
