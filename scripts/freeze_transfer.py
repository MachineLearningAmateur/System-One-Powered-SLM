"""Freeze the Amendment A1.1 transfer routers (configs/amendment_a1.json, "transfer").

    uv run python scripts/freeze_transfer.py

For each benchmark and each of the four LR feature sets, one predict-v2 model (standardize on
the fitted rows, L2 LR, C = 1) fit on that benchmark's development visible-pass rows only
(pilot-v1, pilot-v1b). Development data only: no test row is read. configs/routers_v2.json is
not changed. Refuses to overwrite configs/routers_transfer_v1.json.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np

from system1.config import CONFIGS, ROOT
from system1.eval import predict as P

sys.path.insert(0, str(ROOT / "scripts"))
from replay import load_rg  # noqa: E402

RUNS = ["pilot-v1", "pilot-v1b"]
OUT = CONFIGS / "routers_transfer_v1.json"


def main() -> int:
    a1 = json.loads((CONFIGS / "amendment_a1.json").read_text(encoding="utf-8"))["transfer"]
    if OUT.exists():
        print(f"STOP: {OUT} exists; it is frozen")
        return 2
    rg = load_rg()
    data = [d for d in rg.load(RUNS, split="dev") if d["cp"]["visible_pass"]]
    models: dict[str, dict] = {}
    for bench in ("humaneval+", "mbpp+"):
        rows = [d for d in data if d["cp"]["benchmark"] == bench]
        y = np.array([0 if d["cp"]["hidden"]["passed"] else 1 for d in rows])
        tasks = {d["cp"]["task_id"] for d in rows}
        models[bench] = {"n_rows": len(rows), "positives": int(y.sum()), "tasks": len(tasks),
                         "positive_tasks": len({d["cp"]["task_id"] for d, v in zip(rows, y) if v}), "models": {}}
        for fs in a1["feature_sets"]:
            X, cols = rg.design(rows, fs, visible_pass_only=True)
            models[bench]["models"][fs] = {"kind": "lr", "feature_set": fs, **P.fit_final(X, y, cols)}
        print(f"{bench}: {len(rows)} dev VP rows, {int(y.sum())} hidden fail from "
              f"{models[bench]['positive_tasks']} tasks, {len(tasks)} tasks")
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    out = {"version": "routers-transfer-v1", "amendment": "A1.1", "created": datetime.now(timezone.utc).isoformat(),
           "git_commit": commit, "runs": RUNS, "pipeline": P.PIPELINE_VERSION, "C": P.C,
           "fit_rows": a1["fit_rows"], "test_rows_read": False, "by_source": models}
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"written {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
