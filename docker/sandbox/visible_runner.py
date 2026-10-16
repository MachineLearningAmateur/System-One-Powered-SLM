"""Visible-test runner. One disposable container runs one check, as PID 1.

The host (src/system1/loop/sandbox.py, VisibleRunner) starts

    docker run -i --network none --read-only --memory 2g ... <image id> python /opt/sandbox/visible_runner.py

writes one JSON request to stdin and reads one JSON line from stdout:

    request: {"code": str, "tests": [test, ...], "timeout": float}
        test = {"kind": "assert", "source": "assert f(1) == 2"}
             | {"kind": "compare", "call": "f(1)", "expected": "2"}
    reply:   {"ok": true, "runner": RUNNER_VERSION, "execution": {...}, "results": [...], "elapsed_s": float}
        execution = {"status": ok|error|timeout|oom|crash, "stage": None|"load"|"test",
                     "error_type": str|None, "message": str|None}
        result    = {"status": pass|fail|error|timeout|oom|crash|not_run, "error_type", "message"}

Rules (frozen with the protocol):
  - One total deadline, started just before the fork, covers loading the code
    and all tests. Events from the child never extend it.
  - A load that fails or does not finish: every test is "not_run" and the
    execution carries the reason (stage "load").
  - A test that does not finish: earlier results are kept, that test gets the
    reason, later tests are "not_run" (stage "test").
  - "oom" only when the container's own memory limit was reached
    (memory.events "oom" rose); another death is "crash".
This container holds no hidden tests and no reference solutions. When PID 1
exits, the kernel kills every process left in the container, so descendants
of the candidate need no cleanup here; the host removes the container.
Known limit: the candidate and the test code share one Python process, so
code could change the harness. We do not claim security against hostile code.
"""

from __future__ import annotations

import json
import math
import os
import select
import signal
import sys
import time

RUNNER_VERSION = "visible-runner-v1"
MESSAGE_MAX_CHARS = 500
READ_MAX_BYTES = 1 << 20  # events are small; this bounds a flood
MEMORY_EVENTS = "/sys/fs/cgroup/memory.events"


def _msg(e: BaseException) -> str:
    return str(e)[:MESSAGE_MAX_CHARS]


def _close(a, b) -> bool:
    """Equality with a small float tolerance, recursively (for 'compare' tests)."""
    if isinstance(a, float) or isinstance(b, float):
        try:
            return math.isclose(float(a), float(b), rel_tol=1e-6, abs_tol=1e-9)
        except (TypeError, ValueError):
            return False
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)) and type(a) is type(b):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    return a == b


def _test_namespace(ns: dict) -> dict:
    # The visible MBPP asserts use math.isclose; the model sees that in its
    # prompt, so the test (not the solution) gets `math`.
    return {"math": math, **ns}


def _run_test(t: dict, ns: dict) -> dict:
    try:
        if t["kind"] == "assert":
            exec(compile(t["source"], "<test>", "exec"), _test_namespace(ns))
            return {"status": "pass", "error_type": None, "message": None}
        got = eval(compile(t["call"], "<test>", "eval"), _test_namespace(ns))
        want = eval(compile(t["expected"], "<expected>", "eval"), {})
        if _close(got, want):
            return {"status": "pass", "error_type": None, "message": None}
        return {"status": "fail", "error_type": "AssertionError",
                "message": f"expected {t['expected']}, got {got!r}"[:MESSAGE_MAX_CHARS]}
    except AssertionError as e:
        return {"status": "fail", "error_type": "AssertionError", "message": _msg(e) or "assertion failed"}
    except BaseException as e:  # noqa: BLE001 - report any failure of the candidate
        return {"status": "error", "error_type": type(e).__name__, "message": _msg(e)}


def _child(code: str, tests: list, w: int) -> None:
    """Run the candidate; never returns. Output goes to /dev/null, events to fd w."""
    null = os.open(os.devnull, os.O_RDWR)
    for fd in (0, 1, 2):
        os.dup2(null, fd)
    os.chdir("/tmp")

    def emit(ev: dict) -> None:
        os.write(w, (json.dumps(ev) + "\n").encode())  # < PIPE_BUF: messages are bounded, ASCII-escaped

    emit({"ev": "load_start"})
    ns: dict = {}
    try:
        exec(compile(code, "<solution>", "exec"), ns)
    except BaseException as e:  # noqa: BLE001
        emit({"ev": "load_error", "error_type": type(e).__name__, "message": _msg(e)})
        os._exit(0)
    emit({"ev": "load_done"})
    for i, t in enumerate(tests):
        emit({"ev": "test_start", "i": i})
        emit({"ev": "test_result", "i": i, **_run_test(t, ns)})
    emit({"ev": "done"})
    os._exit(0)


def _memory_events() -> dict[str, int]:
    with open(MEMORY_EVENTS, encoding="ascii") as f:
        return {k: int(v) for k, v in (line.split() for line in f if line.strip())}


def _drain(fd: int, buf: bytearray, total: list[int]) -> bool:
    """Read what is there without blocking. False at EOF."""
    while total[0] < READ_MAX_BYTES:
        try:
            chunk = os.read(fd, 65536)
        except BlockingIOError:
            return True
        if not chunk:
            return False
        buf.extend(chunk)
        total[0] += len(chunk)
    return True


def _events(buf: bytes) -> list[dict]:
    out = []
    for line in buf.split(b"\n"):
        if not line:
            continue
        try:
            ev = json.loads(line)
        except ValueError:
            continue  # a broken or partial line is ignored, never trusted
        if isinstance(ev, dict):
            out.append(ev)
    return out


def check(code: str, tests: list, timeout: float) -> dict:
    mem0 = _memory_events()
    r, w = os.pipe()
    t0 = time.monotonic()
    deadline = t0 + timeout
    pid = os.fork()
    if pid == 0:
        os.close(r)
        try:
            _child(code, tests, w)
        finally:
            os._exit(0)
    os.close(w)
    os.set_blocking(r, False)
    buf, total, killed, status = bytearray(), [0], False, 0
    open_ = True
    while True:
        done_pid, status = os.waitpid(pid, os.WNOHANG)
        if done_pid:
            break
        left = deadline - time.monotonic()
        if left <= 0:
            os.kill(pid, signal.SIGKILL)
            killed = True
            _, status = os.waitpid(pid, 0)
            break
        if open_:
            ready, _, _ = select.select([r], [], [], min(left, 0.05))
            if ready:
                open_ = _drain(r, buf, total)
        else:
            time.sleep(min(left, 0.01))
    _drain(r, buf, total)  # what is already buffered; a descendant may keep the pipe open
    elapsed = time.monotonic() - t0
    oom = _memory_events().get("oom", 0) > mem0.get("oom", 0)
    return {"execution_raw": _summarise(_events(bytes(buf)), len(tests), killed, oom, status, timeout),
            "elapsed_s": round(elapsed, 3)}


def _summarise(events: list[dict], n: int, killed: bool, oom: bool, status: int, timeout: float) -> dict:
    results: list[dict | None] = [None] * n
    loaded, load_error, finished, running = False, None, False, None
    for ev in events:
        kind = ev.get("ev")
        if kind == "load_done":
            loaded = True
        elif kind == "load_error":
            load_error = ev
        elif kind == "test_start" and isinstance(ev.get("i"), int) and 0 <= ev["i"] < n:
            running = ev["i"]
        elif kind == "test_result" and isinstance(ev.get("i"), int) and 0 <= ev["i"] < n:
            results[ev["i"]] = {"status": ev.get("status"), "error_type": ev.get("error_type"),
                                "message": ev.get("message")}
            running = None
        elif kind == "done":
            finished = True

    if load_error is not None:
        execution = {"status": "error", "stage": "load", "error_type": load_error.get("error_type"),
                     "message": load_error.get("message")}
    elif finished and all(r is not None for r in results):
        execution = {"status": "ok", "stage": None, "error_type": None, "message": None}
    else:
        stage = "test" if loaded else "load"
        if killed:
            execution = {"status": "timeout", "stage": stage, "error_type": "Timeout",
                         "message": f"no result within {timeout:g} s"}
        elif oom:
            execution = {"status": "oom", "stage": stage, "error_type": "OutOfMemory",
                         "message": "the memory limit was reached"}
        else:
            how = (f"signal {os.WTERMSIG(status)}" if os.WIFSIGNALED(status)
                   else f"exit code {os.WEXITSTATUS(status)} before all results")
            execution = {"status": "crash", "stage": stage, "error_type": "Crash", "message": f"the process ended ({how})"}
        if stage == "test" and running is not None and results[running] is None:
            results[running] = {"status": execution["status"], "error_type": execution["error_type"],
                                "message": execution["message"]}
    not_run = {"status": "not_run", "error_type": None, "message": None}
    return {"execution": execution, "results": [r if r is not None else dict(not_run) for r in results]}


def main() -> int:
    out = sys.stdout
    try:
        if os.getpid() != 1:
            raise RuntimeError("the runner must be PID 1 of its own container")
        req = json.loads(sys.stdin.buffer.read().decode("utf-8"))
        res = check(req["code"], req["tests"], float(req.get("timeout", 10.0)))
        reply = {"ok": True, "runner": RUNNER_VERSION, **res.pop("execution_raw"), **res}
        code = 0
    except Exception as e:  # noqa: BLE001 - a harness failure, reported to the host
        reply = {"ok": False, "runner": RUNNER_VERSION, "error": f"{type(e).__name__}: {e}"}
        code = 2
    out.write(json.dumps(reply) + "\n")
    out.flush()
    return code


if __name__ == "__main__":
    sys.exit(main())
