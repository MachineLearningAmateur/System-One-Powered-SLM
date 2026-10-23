"""Delete and verify the temporary Azure smoke resource group at a UTC deadline.

Start this as a detached process before sending traffic to the GPU app. The
resource group must contain only disposable smoke-test resources.
"""

from __future__ import annotations

import argparse
import datetime as dt
import subprocess
import time


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--deadline-utc", required=True)
    args = parser.parse_args()
    deadline = dt.datetime.fromisoformat(args.deadline_utc.replace("Z", "+00:00"))
    if deadline.tzinfo is None:
        parser.error("deadline must include a timezone")
    while True:
        remaining = (deadline - dt.datetime.now(dt.timezone.utc)).total_seconds()
        if remaining <= 0:
            break
        time.sleep(min(remaining, 30))
    attempt = 0
    while True:
        attempt += 1
        try:
            result = subprocess.run(
                ["az", "group", "delete", "--name", args.resource_group, "--yes", "--no-wait"],
                capture_output=True, text=True, timeout=120,
            )
            if result.returncode == 0:
                print(f"deletion requested for {args.resource_group}", flush=True)
            else:
                print(f"deletion attempt {attempt} failed: {result.stderr[-500:]}", flush=True)
        except (OSError, subprocess.TimeoutExpired) as exc:
            print(f"deletion attempt {attempt} failed: {type(exc).__name__}", flush=True)

        # A successful --no-wait request does not mean the group is gone.
        for _ in range(6):
            try:
                check = subprocess.run(
                    ["az", "group", "exists", "--name", args.resource_group],
                    capture_output=True, text=True, timeout=30,
                )
                if check.returncode == 0 and check.stdout.strip().lower() == "false":
                    print(f"deletion confirmed for {args.resource_group}", flush=True)
                    return 0
            except (OSError, subprocess.TimeoutExpired):
                pass
            time.sleep(10)
        print(f"{args.resource_group} still exists; retrying deletion", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
