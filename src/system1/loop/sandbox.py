"""Host-side clients for the sandbox image (docker/sandbox).

VisibleRunner: one disposable container per visible check. No hidden data is
mounted, and when the check ends the container (with every process and file
the candidate made) is removed. The container is started by image ID, not by
tag, and the ID goes into the run's protocol fingerprint.

Sandbox: the hidden-test grader. It keeps one worker process open inside the
`sandbox` compose service through `docker exec -i` and talks JSON lines with
it. A request that gets no reply in time kills the worker; the next request
starts a new one. It runs only after generation (scripts/grade_hidden.py).
"""

from __future__ import annotations

import json
import queue
import subprocess
import threading
import uuid
from pathlib import Path
from typing import Any

DEFAULT_CONTAINER = "system1-sandbox-1"  # docker compose: <project>-<service>-1
WORKER_CMD = ["python", "/opt/sandbox/worker.py"]
VISIBLE_IMAGE = "system1-sandbox:v2"
VISIBLE_CMD = ["python", "/opt/sandbox/visible_runner.py"]
# Limits of one visible check (part of the protocol fingerprint).
VISIBLE_DOCKER_FLAGS = (
    "--network", "none", "--read-only", "--tmpfs", "/tmp:size=64m,mode=1777",
    "--memory", "2g", "--memory-swap", "2g", "--pids-limit", "128", "--cpus", "2",
    "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--user", "10001",
    "--cgroupns", "private", "-e", "TMPDIR=/tmp",
)
VISIBLE_GRACE_S = 60.0  # infrastructure allowance (container start and stop), not candidate time
RESULT_STATUSES = {"pass", "fail", "error", "timeout", "oom", "crash", "not_run"}


class SandboxError(RuntimeError):
    pass


def image_id(image: str) -> str:
    r = subprocess.run(["docker", "image", "inspect", "-f", "{{.Id}}", image],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not r.stdout.strip():
        raise SandboxError(f"image {image} not found: {r.stderr.strip()[:200]}")
    return r.stdout.strip()


class VisibleRunner:
    def __init__(self, image: str = VISIBLE_IMAGE, max_concurrent: int = 4, grace_s: float = VISIBLE_GRACE_S):
        self.image = image
        self.image_id = image_id(image)
        self.max_concurrent = max_concurrent
        self.grace_s = grace_s
        self._slots = threading.BoundedSemaphore(max_concurrent)
        self.broken: str | None = None  # set when a container could not be removed

    def protocol(self) -> dict[str, Any]:
        return {"visible_image": self.image, "visible_image_id": self.image_id,
                "visible_docker_flags": list(VISIBLE_DOCKER_FLAGS), "visible_concurrency": self.max_concurrent}

    def run(self, code: str, tests: list[dict], timeout: float = 10.0) -> dict[str, Any]:
        """{"execution": {...}, "results": [...], "runner": str, "elapsed_s": float}; SandboxError on harness failure."""
        with self._slots:
            if self.broken:  # checked inside the slot: no check starts after a failed cleanup
                raise SandboxError(f"visible runner stopped: {self.broken}")
            return self._run(code, tests, timeout)

    def _run(self, code: str, tests: list[dict], timeout: float) -> dict[str, Any]:
        name = f"s1v-{uuid.uuid4().hex[:16]}"
        cmd = ["docker", "run", "-i", "--name", name, *VISIBLE_DOCKER_FLAGS, self.image_id, *VISIBLE_CMD]
        req = json.dumps({"code": code, "tests": tests, "timeout": timeout}).encode("utf-8")
        try:
            try:
                p = subprocess.run(cmd, input=req, capture_output=True, timeout=timeout + self.grace_s)
            except subprocess.TimeoutExpired as e:
                raise SandboxError(f"visible check gave no reply within {timeout + self.grace_s:.0f} s") from e
            reply = self._parse(p.stdout, len(tests)) if p.returncode == 0 else None
            if reply is None:
                raise SandboxError(f"visible check failed (exit {p.returncode}, {self._diagnose(name)}): "
                                   f"{p.stderr.decode('utf-8', 'replace').strip()[-300:]}")
        finally:
            removed = self._remove(name)
        if not removed:  # the result is not used: a container may still hold resources
            raise SandboxError(f"visible runner stopped: {self.broken}")
        return reply

    @staticmethod
    def _parse(stdout: bytes, n_tests: int) -> dict[str, Any] | None:
        lines = [x for x in stdout.decode("utf-8", "replace").splitlines() if x.strip()]
        if len(lines) != 1:
            return None
        try:
            reply = json.loads(lines[0])
        except ValueError:
            return None
        if not isinstance(reply, dict) or reply.get("ok") is not True:
            return None
        results, execution = reply.get("results"), reply.get("execution")
        if not isinstance(results, list) or len(results) != n_tests or not isinstance(execution, dict):
            return None
        if any(not isinstance(r, dict) or r.get("status") not in RESULT_STATUSES for r in results):
            return None
        return {"execution": execution, "results": results, "runner": reply.get("runner"),
                "elapsed_s": reply.get("elapsed_s")}

    @staticmethod
    def _diagnose(name: str) -> str:
        r = subprocess.run(["docker", "inspect", "-f", "exit={{.State.ExitCode}} oom={{.State.OOMKilled}}", name],
                           capture_output=True, text=True, timeout=60)
        return r.stdout.strip() or "no container state"

    def _remove(self, name: str) -> bool:
        try:
            r = subprocess.run(["docker", "rm", "-f", name], capture_output=True, text=True, timeout=60)
            ok = r.returncode == 0 or "No such container" in r.stderr
        except (subprocess.TimeoutExpired, OSError):
            ok = False
        if not ok:
            self.broken = f"could not remove container {name}"
        return ok


class Sandbox:
    """Client of the grader worker (docker/sandbox/worker.py)."""

    def __init__(self, container: str = DEFAULT_CONTAINER, stderr_log: Path | None = None,
                 cmd: list[str] | None = None):
        self.container = container
        self.cmd = cmd or ["docker", "exec", "-i", container, *WORKER_CMD]
        self.stderr_log = stderr_log
        self._proc: subprocess.Popen | None = None
        self._lines: queue.Queue = queue.Queue()
        self._lock = threading.Lock()
        self.worker_pid: int | None = None  # pid inside the container, for a real kill
        self.worker_version: str | None = None

    def _start(self) -> None:
        err = open(self.stderr_log, "a", encoding="utf-8") if self.stderr_log else subprocess.DEVNULL
        self._proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err,
                                      text=True, encoding="utf-8", bufsize=1)
        self._lines = queue.Queue()
        proc, lines = self._proc, self._lines

        def pump() -> None:
            for line in proc.stdout:
                lines.put(line)
            lines.put(None)  # worker ended

        threading.Thread(target=pump, daemon=True).start()

    def _kill(self) -> None:
        """Stop the worker inside the container (killing only the local `docker exec`
        client would leave it running and holding its memory), then the client."""
        if self.worker_pid is not None:
            subprocess.run(["docker", "exec", self.container, "kill", "-9", str(self.worker_pid)],
                           capture_output=True, timeout=30)
            self.worker_pid = None
        if self._proc is not None:
            try:
                self._proc.kill()
            except OSError:
                pass
            self._proc = None

    def _send(self, req: dict[str, Any], timeout: float) -> dict[str, Any]:
        try:
            self._proc.stdin.write(json.dumps(req) + "\n")
            self._proc.stdin.flush()
            line = self._lines.get(timeout=timeout)
        except queue.Empty:
            self._kill()
            raise SandboxError(f"no reply to {req.get('op')} within {timeout:.0f} s; worker restarted")
        except OSError as e:
            self._kill()
            raise SandboxError(f"worker pipe failed: {e}") from e
        if line is None:
            self._kill()
            raise SandboxError("worker exited")
        try:
            reply = json.loads(line)
        except json.JSONDecodeError as e:
            self._kill()
            raise SandboxError(f"unreadable worker reply: {line[:200]!r}") from e
        if not reply.get("ok"):
            raise SandboxError(reply.get("error", "unknown worker error"))
        return reply

    def request(self, req: dict[str, Any], timeout: float) -> dict[str, Any]:
        with self._lock:
            if self._proc is None or self._proc.poll() is not None:
                self._start()
                hello = self._send({"op": "ping"}, 60.0)
                self.worker_pid, self.worker_version = hello.get("pid"), hello.get("version")
            return self._send(req, timeout)

    def ping(self, timeout: float = 60.0) -> dict[str, Any]:
        return self.request({"op": "ping"}, timeout)

    def load(self, datasets: list[str], timeout: float = 900.0) -> dict[str, Any]:
        return self.request({"op": "load", "datasets": datasets}, timeout)

    def hidden(self, dataset: str, task_id: str, code: str, timeout: float = 600.0) -> dict:
        return self.request({"op": "hidden", "dataset": dataset, "task_id": task_id, "code": code}, timeout)

    def canonical(self, dataset: str, task_id: str, extra: str = "", timeout: float = 600.0) -> dict:
        return self.request({"op": "canonical", "dataset": dataset, "task_id": task_id, "extra": extra}, timeout)

    def reference(self, dataset: str, task_id: str, n: int = 3, timeout: float = 600.0) -> dict:
        return self.request({"op": "reference", "dataset": dataset, "task_id": task_id, "n": n}, timeout)

    def close(self) -> None:
        with self._lock:
            if self._proc is not None and self._proc.stdin:
                try:
                    self._proc.stdin.close()
                except OSError:
                    pass
            self._kill()
