"""Run-level telemetry for the cost views and the throughput report.

  - GPU power: a background thread samples `nvidia-smi` every few seconds into
    power.jsonl; energy_wh() integrates it (electricity-only marginal cost).
  - vLLM counters: a snapshot of the server's /metrics at the start and the
    end of each session (token totals, KV-cache preemptions, request counts);
    the difference is the session's own work.
Both are best effort: a missing tool or server gives None, never a crash,
and the run records that the measurement is missing.
"""

from __future__ import annotations

import json
import subprocess
import threading
import time
from pathlib import Path

import httpx

METRICS_URL = "http://localhost:8000/metrics"
POWER_QUERY = "timestamp,power.draw,utilization.gpu,memory.used"
POWER_INTERVAL_S = 2.0


def vllm_metrics(url: str = METRICS_URL) -> dict[str, float] | None:
    """vLLM counters and gauges summed over labels (histogram buckets left out)."""
    try:
        text = httpx.get(url, timeout=5.0).text
    except httpx.HTTPError:
        return None
    out: dict[str, float] = {}
    for line in text.splitlines():
        if not line.startswith("vllm:") or "_bucket{" in line or "_created" in line:
            continue
        name, _, value = line.rpartition(" ")
        key = name.split("{", 1)[0][len("vllm:"):]
        try:
            out[key] = out.get(key, 0.0) + float(value)
        except ValueError:
            continue
    return out


def metrics_delta(start: dict | None, end: dict | None) -> dict[str, float | None] | None:
    """Counter changes over a session; None for a counter that went down (a server restart)."""
    if start is None or end is None:
        return None
    keys = ("prompt_tokens_total", "generation_tokens_total", "num_preemptions_total",
            "request_success_total", "prefix_cache_queries_total", "prefix_cache_hits_total")
    out: dict[str, float | None] = {}
    for k in keys:
        if k in end:
            d = end[k] - start.get(k, 0.0)
            out[k] = d if d >= 0 else None
    if any(v is None for v in out.values()):
        out["counter_reset"] = True
    return out


VLLM_CONTAINER = "system1-vllm-1"


class ServerMismatch(RuntimeError):
    pass


def vllm_server_identity(expected: dict[str, str], container: str = VLLM_CONTAINER,
                         models_url: str = "http://localhost:8000/v1/models") -> dict:
    """The running generation server: container image ID and launch flags, checked
    against `expected` ({flag: value}, e.g. {"--model": "Qwen/Qwen3-1.7B"}). Fails closed."""
    r = subprocess.run(["docker", "inspect", "-f", "{{.Image}}\n{{json .Config.Cmd}}", container],
                       capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise ServerMismatch(f"cannot inspect the vLLM container {container}: {r.stderr.strip()[:200]}")
    image, cmd_json = r.stdout.strip().split("\n", 1)
    cmd = json.loads(cmd_json) or []
    flags = dict(a.split("=", 1) for a in cmd if a.startswith("--") and "=" in a)
    wrong = {k: (flags.get(k), v) for k, v in expected.items() if flags.get(k) != v}
    if wrong:
        raise ServerMismatch(f"the vLLM server runs with other settings: {wrong}")
    try:
        models = httpx.get(models_url, timeout=10.0).json()["data"]
    except (httpx.HTTPError, KeyError, ValueError) as e:
        raise ServerMismatch(f"the vLLM server does not answer: {e}") from e
    return {"vllm_image_id": image, "vllm_cmd": cmd,
            "vllm_models": sorted((m["id"], m.get("max_model_len")) for m in models)}


def remote_vllm_server_identity(expected: dict[str, str], manifest: dict,
                                models_url: str) -> dict:
    """Check the deployed command and live model before a remote generation run."""
    image = manifest.get("image_digest")
    revision = manifest.get("azure_revision")
    command = manifest.get("command")
    if not isinstance(image, str) or not image.startswith("sha256:") or not revision:
        raise ServerMismatch("remote deployment manifest lacks an image digest or Azure revision")
    if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
        raise ServerMismatch("remote deployment manifest lacks a command list")
    flags = dict(a.split("=", 1) for a in command if a.startswith("--") and "=" in a)
    wrong = {k: (flags.get(k), v) for k, v in expected.items() if flags.get(k) != v}
    if wrong:
        raise ServerMismatch(f"the remote vLLM command has other settings: {wrong}")
    try:
        response = httpx.get(models_url, timeout=30.0)
        response.raise_for_status()
        models = response.json()["data"]
        identities = sorted((m["id"], m.get("max_model_len")) for m in models)
    except (httpx.HTTPError, KeyError, ValueError, TypeError) as e:
        raise ServerMismatch(f"the remote vLLM server does not answer: {e}") from e
    if (expected["--model"], int(expected["--max-model-len"])) not in identities:
        raise ServerMismatch(f"the remote vLLM server reports another model: {identities}")
    return {"vllm_image_id": image, "vllm_cmd": command, "vllm_models": identities,
            "azure_revision": revision, "server_kind": "azure-container-app"}


def gpu_sample() -> dict | None:
    try:
        r = subprocess.run(["nvidia-smi", f"--query-gpu={POWER_QUERY}", "--format=csv,noheader,nounits"],
                           capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if r.returncode != 0 or not r.stdout.strip():
        return None
    parts = [p.strip() for p in r.stdout.strip().splitlines()[0].split(",")]
    try:
        return {"t": time.time(), "power_w": float(parts[1]), "util_pct": float(parts[2]), "mem_mb": float(parts[3])}
    except (IndexError, ValueError):
        return None


class PowerSampler:
    """Samples GPU power into a JSONL file until stop()."""

    def __init__(self, path: Path, interval_s: float = POWER_INTERVAL_S, sample=gpu_sample):
        self.path = path
        self.interval_s = interval_s
        self.sample = sample
        self.samples: list[dict] = []
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def _loop(self) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            while not self._stop.is_set():
                s = self.sample()
                if s is not None:
                    self.samples.append(s)
                    f.write(json.dumps(s) + "\n")
                    f.flush()
                self._stop.wait(self.interval_s)

    def start(self) -> "PowerSampler":
        self._thread.start()
        return self

    def stop(self) -> dict:
        self._stop.set()
        self._thread.join(timeout=30)
        return {"power_samples": len(self.samples), "energy_wh": energy_wh(self.samples),
                "mean_power_w": (round(sum(s["power_w"] for s in self.samples) / len(self.samples), 1)
                                 if self.samples else None)}


def energy_wh(samples: list[dict]) -> float | None:
    """Trapezoid integral of power over time, in watt-hours (GPU board power only)."""
    if len(samples) < 2:
        return None
    joules = sum((b["t"] - a["t"]) * (a["power_w"] + b["power_w"]) / 2 for a, b in zip(samples, samples[1:]))
    return round(joules / 3600, 4)
