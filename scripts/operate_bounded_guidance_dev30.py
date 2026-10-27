"""Guard one approved dev30 run after a separate watchdog and GPU app are ready.

Offline preparation (no Azure or model call):
    uv run python scripts/operate_bounded_guidance_dev30.py --check

Real mode needs a NEW operator approval, clean commit, active watchdog started
before provisioning, and a ready one-replica app. This script invokes the
existing two-arm harness once, then requests app/group deletion in finally.
It neither provisions resources nor retries inference.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

from system1.bounded_guidance_dev30 import (AZURE_APP_NAME, AZURE_ENV_NAME,
    AZURE_RESOURCE_GROUP, AZURE_SUBSCRIPTION_ID, FRONTIER_LIMIT_USD,
    GPU_RATE_USD_PER_HOUR, MANIFEST_PATH, MAX_FRONTIER_REQUESTS, MAX_WALL_SECONDS,
    MAX_WORKER_HTTP, TOTAL_CEILING_USD, WATCHDOG_SECONDS, load_manifest)
from system1.bounded_guidance_dev30 import VLLM_IMAGE
from system1.config import RESULTS, ROOT


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def azure_utc(value: str) -> str:
    parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc).isoformat()


def azure_json(*args: str):
    result = subprocess.run(["az", *args, "-o", "json"], capture_output=True, text=True,
                            timeout=45, check=True)
    return json.loads(result.stdout)


def verify_cleanup(run_id: str) -> dict:
    if not run_id:
        raise ValueError("cleanup verification requires the run ID")
    if azure_json("account", "show")["id"] != AZURE_SUBSCRIPTION_ID:
        raise ValueError("wrong Azure subscription; cleanup is unverified")
    result = subprocess.run(["az", "group", "exists", "--name", AZURE_RESOURCE_GROUP],
                            capture_output=True, text=True, timeout=45)
    if result.returncode != 0 or result.stdout.strip().lower() != "false":
        raise RuntimeError("resource group is present or Azure query failed; keep watchdog active")
    record = {"verified_utc": now(), "subscription_id": AZURE_SUBSCRIPTION_ID,
              "resource_group": AZURE_RESOURCE_GROUP, "az_group_exists_stdout": "false",
              "gpu_app_absent": True}
    target = RESULTS / "runs" / run_id / "cleanup_verification.json"
    with target.open("x") as output:
        json.dump(record, output, indent=2)
    return record


def arm_watchdog(run_id: str, approved_total_usd: float) -> dict:
    if not run_id or approved_total_usd is None or not 0 < approved_total_usd <= TOTAL_CEILING_USD:
        raise ValueError("watchdog arming needs a fresh run ID and approved total ceiling")
    if (RESULTS / "runs" / run_id).exists():
        raise ValueError("run ID already exists")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip():
        raise ValueError("watchdog arming needs the clean frozen commit")
    if azure_json("account", "show")["id"] != AZURE_SUBSCRIPTION_ID:
        raise ValueError("wrong Azure subscription")
    exists = subprocess.run(["az", "group", "exists", "--name", AZURE_RESOURCE_GROUP],
                            capture_output=True, text=True, timeout=45)
    if exists.returncode != 0 or exists.stdout.strip().lower() != "false":
        raise ValueError("isolated pilot resource group already exists or query failed")
    start = dt.datetime.now(dt.timezone.utc)
    deadline = start + dt.timedelta(seconds=WATCHDOG_SECONDS)
    if GPU_RATE_USD_PER_HOUR * WATCHDOG_SECONDS / 3600 + FRONTIER_LIMIT_USD >= approved_total_usd:
        raise ValueError("modeled watchdog plus frontier cap reaches approved ceiling")
    log_path = RESULTS / f"{run_id}-watchdog.log"
    manifest_path = RESULTS / f"{run_id}-watchdog.json"
    with log_path.open("x") as log:
        process = subprocess.Popen([
            "uv", "run", "python", "scripts/azure_smoke_watchdog.py",
            "--resource-group", AZURE_RESOURCE_GROUP,
            "--deadline-utc", deadline.isoformat()], cwd=ROOT,
            stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    watcher = {"subscription_id": AZURE_SUBSCRIPTION_ID,
               "resource_group": AZURE_RESOURCE_GROUP,
               "started_utc": start.isoformat(), "deadline_utc": deadline.isoformat(),
               "pid": process.pid, "log": str(log_path)}
    with manifest_path.open("x") as output:
        json.dump(watcher, output, indent=2)
    return {"manifest": str(manifest_path), **watcher}


def capture_revision(run_id: str) -> dict:
    if not run_id or azure_json("account", "show")["id"] != AZURE_SUBSCRIPTION_ID:
        raise ValueError("revision capture needs a run ID in the correct subscription")
    app = azure_json("containerapp", "show", "--name", AZURE_APP_NAME,
                     "--resource-group", AZURE_RESOURCE_GROUP)
    revisions = azure_json("containerapp", "revision", "list", "--name", AZURE_APP_NAME,
                           "--resource-group", AZURE_RESOURCE_GROUP)
    active = [r for r in revisions if r["properties"].get("active")]
    if len(active) != 1:
        raise ValueError("expected exactly one active pinned Azure revision")
    container = app["properties"]["template"]["containers"][0]
    if (container["image"] != VLLM_IMAGE
            or app["properties"]["template"]["scale"]["maxReplicas"] != 1):
        raise ValueError("actual Azure image or replica limit changed")
    flags = dict(part.split("=", 1) for part in container["args"]
                 if part.startswith("--") and "=" in part)
    if (flags.get("--model") != "Qwen/Qwen3-8B"
            or flags.get("--revision") != "b968826d9c46dd6066d109eabc6255188de91218"
            or flags.get("--max-model-len") != "16384"):
        raise ValueError("actual Azure worker model or context configuration changed")
    record = {"azure_revision": active[0]["name"],
              "image_digest": container["image"].rsplit("@", 1)[1],
              "image_reference": container["image"],
              "command": container["command"] + container["args"],
              "resource_group": AZURE_RESOURCE_GROUP,
              "max_replicas": 1,
              "server_url": "https://" + app["properties"]["configuration"]["ingress"]["fqdn"]}
    target = RESULTS / f"{run_id}-remote-manifest.json"
    with target.open("x") as output:
        json.dump(record, output, indent=2)
    return {"manifest": str(target), "server_url": record["server_url"],
            "azure_revision": record["azure_revision"]}


def check_watchdog(path: Path, approved_total_usd: float) -> dict:
    watcher = json.loads(path.read_text())
    started = dt.datetime.fromisoformat(watcher["started_utc"])
    deadline = dt.datetime.fromisoformat(watcher["deadline_utc"])
    if (watcher.get("subscription_id") != AZURE_SUBSCRIPTION_ID
            or watcher.get("resource_group") != AZURE_RESOURCE_GROUP
            or not 0 < (deadline - started).total_seconds() <= WATCHDOG_SECONDS
            or started > dt.datetime.now(dt.timezone.utc)
            or deadline <= dt.datetime.now(dt.timezone.utc)
            or GPU_RATE_USD_PER_HOUR * (deadline - started).total_seconds() / 3600
               + FRONTIER_LIMIT_USD >= approved_total_usd):
        raise ValueError("watchdog identity, deadline, or modeled spending guard is invalid")
    os.kill(int(watcher["pid"]), 0)
    process = subprocess.run(["ps", "-p", str(watcher["pid"]), "-o", "command="],
                             capture_output=True, text=True, timeout=10)
    if (process.returncode != 0 or "azure_smoke_watchdog.py" not in process.stdout
            or AZURE_RESOURCE_GROUP not in process.stdout):
        raise ValueError("independent watchdog process identity does not match")
    return watcher


def _request_delete(args: list[str]) -> dict:
    try:
        response = subprocess.run(["az", *args], capture_output=True, text=True, timeout=120)
        return {"at_utc": now(), "exit_code": response.returncode,
                "stderr_tail": response.stderr[-300:]}
    except BaseException as exc:
        return {"at_utc": now(), "error": type(exc).__name__}


def wait_for_app_absence(seconds: int = 300) -> str | None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        try:
            exists = subprocess.run(["az", "group", "exists", "--name", AZURE_RESOURCE_GROUP],
                                    capture_output=True, text=True, timeout=30)
            if exists.returncode == 0 and exists.stdout.strip().lower() == "false":
                return now()
            if exists.returncode == 0 and exists.stdout.strip().lower() == "true":
                apps = azure_json("containerapp", "list", "--resource-group", AZURE_RESOURCE_GROUP)
                if all(app.get("name") != AZURE_APP_NAME for app in apps):
                    return now()
        except (OSError, subprocess.SubprocessError, ValueError):
            pass
        time.sleep(10)
    return None


def operate(args) -> dict:
    manifest, manifest_hash = load_manifest()
    if (not args.operator_approved or args.approved_total_usd is None
            or not 0 < args.approved_total_usd <= TOTAL_CEILING_USD):
        raise ValueError("dev30 needs a new total-dollar operator approval")
    if not args.run_id or not args.remote_manifest or not args.watchdog_manifest:
        raise ValueError("real mode needs a fresh run id, live server, revision, and watchdog")
    if (RESULTS / "runs" / args.run_id).exists():
        raise ValueError("run ID already exists; no restart or retry")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip():
        raise ValueError("real dev30 needs a clean committed tree")
    watcher = check_watchdog(Path(args.watchdog_manifest), args.approved_total_usd)
    if azure_json("account", "show")["id"] != AZURE_SUBSCRIPTION_ID:
        raise ValueError("wrong Azure subscription")
    ops_path = RESULTS / f"{args.run_id}-operator.json"
    log_path = RESULTS / f"{args.run_id}-driver.log"
    ops = {"version": manifest["version"], "manifest_sha256": manifest_hash,
           "run_id": args.run_id, "subscription_id": AZURE_SUBSCRIPTION_ID,
           "resource_group": AZURE_RESOURCE_GROUP, "app_name": AZURE_APP_NAME,
           "watchdog_started_utc": watcher["started_utc"],
           "watchdog_deadline_utc": watcher["deadline_utc"],
           "app_created_utc": None,
           "approved_total_usd": args.approved_total_usd,
           "modelled_watchdog_plus_frontier_usd":
               GPU_RATE_USD_PER_HOUR * WATCHDOG_SECONDS / 3600 + FRONTIER_LIMIT_USD,
           "driver_started_utc": now(), "driver_log": str(log_path)}
    cmd = ["uv", "run", "python", "scripts/run_bounded_guidance.py", "--real",
           "--operator-approved", "--run-id", args.run_id, "--split", "dev",
           "--attempts", "1", "--tasks-file", str(MANIFEST_PATH.relative_to(ROOT)),
           "--limit-usd", str(FRONTIER_LIMIT_USD),
           "--max-frontier-requests", str(MAX_FRONTIER_REQUESTS),
           "--max-worker-http-requests", str(MAX_WORKER_HTTP),
           "--max-wall-seconds", str(MAX_WALL_SECONDS),
           "--server-url", None, "--remote-manifest", args.remote_manifest]
    with ops_path.open("x") as output:
        json.dump(ops, output, indent=2)
    try:
        app = azure_json("containerapp", "show", "--name", AZURE_APP_NAME,
                         "--resource-group", AZURE_RESOURCE_GROUP)
        ops["app_created_utc"] = azure_utc(app["systemData"]["createdAt"])
        if dt.datetime.fromisoformat(ops["app_created_utc"]) < dt.datetime.fromisoformat(watcher["started_utc"]):
            raise ValueError("watchdog started after app provisioning")
        if (app["properties"]["workloadProfileName"] != "gpu-a100"
                or app["properties"]["template"]["scale"]["maxReplicas"] != 1
                or app["properties"]["template"]["scale"]["minReplicas"] != 0):
            raise ValueError("GPU app profile or replica limit differs from the frozen pilot")
        resources = azure_json("resource", "list", "--resource-group", AZURE_RESOURCE_GROUP)
        if {x["name"] for x in resources} != {AZURE_APP_NAME, AZURE_ENV_NAME}:
            raise ValueError("pilot resource group is not isolated")
        ops["group_isolated"] = True
        remote = json.loads(Path(args.remote_manifest).read_text())
        server_url = remote.get("server_url")
        container = app["properties"]["template"]["containers"][0]
        if (remote.get("azure_revision") not in [x["name"] for x in
                azure_json("containerapp", "revision", "list", "--name", AZURE_APP_NAME,
                           "--resource-group", AZURE_RESOURCE_GROUP)]
                or container["image"] != VLLM_IMAGE
                or remote.get("image_reference") != container["image"]
                or remote.get("command") != container["command"] + container["args"]):
            raise ValueError("remote manifest differs from actual Azure app")
        if (not isinstance(server_url, str) or
                server_url.rstrip("/") != "https://" + app["properties"]["configuration"]["ingress"]["fqdn"] or
                (args.server_url and args.server_url.rstrip("/") != server_url.rstrip("/"))):
            raise ValueError("server URL differs from actual Azure app")
        cmd[cmd.index("--server-url") + 1] = server_url
        remaining = (dt.datetime.fromisoformat(watcher["deadline_utc"])
                     - dt.datetime.now(dt.timezone.utc)).total_seconds() - 300
        if remaining <= 0:
            raise RuntimeError("less than five minutes remain for cleanup")
        with log_path.open("x") as stream:
            process = subprocess.Popen(cmd, cwd=ROOT, stdout=stream,
                                       stderr=subprocess.STDOUT, start_new_session=True)
            ops["driver_pid"] = process.pid
            try:
                ops["driver_exit_code"] = process.wait(timeout=min(MAX_WALL_SECONDS, remaining))
            except subprocess.TimeoutExpired:
                ops["driver_timeout"] = True
                os.killpg(process.pid, signal.SIGKILL)
                ops["driver_exit_code"] = process.wait()
    except BaseException as exc:
        ops["driver_error"] = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        ops["driver_ended_utc"] = now()
        ops["app_delete_request"] = _request_delete([
            "containerapp", "delete", "--name", AZURE_APP_NAME,
            "--resource-group", AZURE_RESOURCE_GROUP, "--yes", "--no-wait"])
        ops["app_delete_requested_utc"] = ops["app_delete_request"]["at_utc"]
        if ops.get("group_isolated"):
            ops["group_delete_request"] = _request_delete([
                "group", "delete", "--name", AZURE_RESOURCE_GROUP, "--yes", "--no-wait"])
        else:
            ops["group_delete_request"] = {"skipped": "resource group isolation not verified"}
        ops["gpu_app_absent_utc"] = wait_for_app_absence()
        run_path = RESULTS / "runs" / args.run_id
        if run_path.exists():
            (run_path / "azure_lifecycle.json").write_text(json.dumps(ops, indent=2))
        else:
            ops["prestart_infrastructure_failure"] = True
            ops["task_accounting"] = [
                {"task_id": tid, "status": "not_started_infrastructure_failure"}
                for tid in manifest["tasks"]]
        ops_path.write_text(json.dumps(ops, indent=2))
    return ops


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--real", action="store_true")
    mode.add_argument("--verify-cleanup", action="store_true")
    mode.add_argument("--arm-watchdog", action="store_true")
    mode.add_argument("--capture-revision", action="store_true")
    ap.add_argument("--operator-approved", action="store_true")
    ap.add_argument("--approved-total-usd", type=float)
    ap.add_argument("--run-id")
    ap.add_argument("--server-url")
    ap.add_argument("--remote-manifest")
    ap.add_argument("--watchdog-manifest")
    args = ap.parse_args()
    if args.arm_watchdog:
        if not args.operator_approved:
            ap.error("arming the paid pilot watchdog needs new operator approval")
        print(json.dumps(arm_watchdog(args.run_id, args.approved_total_usd)))
        return
    if args.capture_revision:
        print(json.dumps(capture_revision(args.run_id)))
        return
    if args.verify_cleanup:
        print(json.dumps(verify_cleanup(args.run_id)))
        return
    manifest, sha = load_manifest()
    if args.check:
        if args.operator_approved or args.run_id or args.server_url:
            ap.error("--check is offline and takes no real-run arguments")
        print(json.dumps({"manifest_sha256": sha, "tasks": len(manifest["tasks"]),
                          "qwen_generations": 90, "max_qwen_http": MAX_WORKER_HTTP,
                          "frontier_requests": MAX_FRONTIER_REQUESTS,
                          "watchdog_seconds": WATCHDOG_SECONDS,
                          "frontier_guard_usd": FRONTIER_LIMIT_USD,
                          "proposed_total_ceiling_usd": TOTAL_CEILING_USD}))
        return
    ops = operate(args)
    print(json.dumps({k: ops.get(k) for k in
                      ("run_id", "driver_exit_code", "driver_timeout", "app_delete_request",
                       "group_delete_request")}))
    if ops.get("driver_exit_code") != 0:
        raise SystemExit("dev30 generation stopped; no automatic retry or replacement")
    if not ops.get("gpu_app_absent_utc"):
        raise SystemExit("GPU app absence remains unverified; keep watchdog active")


if __name__ == "__main__":
    sys.exit(main())
