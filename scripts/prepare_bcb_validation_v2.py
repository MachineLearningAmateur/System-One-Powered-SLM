"""Build the amended BigCodeBench manifest using reference-visible calibration.

    uv run python scripts/prepare_bcb_validation_v2.py manifest
    # Only after generation completes and vLLM stops:
    uv run python scripts/prepare_bcb_validation_v2.py hidden

The manifest step executes public reference code only in the disposable,
networkless visible sandbox. It reads no hidden test, candidate grade, or
model output. It never overwrites the v1 manifest or run data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor

from system1.config import ROOT
from system1.loop.sandbox import VisibleRunner

from prepare_bcb_validation import SOURCE_REVISION, SOURCE_SHA256, selected_rows, write_new

OLD = ROOT / "configs/bcb_jev_only_tasks_v1.json"
NEW = ROOT / "configs/bcb_jev_only_tasks_v2.json"
HIDDEN = ROOT / "results/datasets/bcb_jev_only_hidden_v2.json"
AUDIT = ROOT / "results/bcb_jev_only_reference_visible_v2.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> None:
    old = json.loads(OLD.read_text(encoding="utf-8"))["tasks"]
    source = {r["task_id"]: r for r in selected_rows()}
    runner = VisibleRunner(max_concurrent=4)

    def check(tid):
        row, task = source[tid], old[tid]
        try:
            result = runner.run(row["complete_prompt"] + row["canonical_solution"], task["visible_tests"])
            passed = result["execution"]["status"] == "ok" and all(
                r["status"] == "pass" for r in result["results"])
            return tid, {"reference_visible_pass": passed, "execution": result["execution"]["status"],
                         "result_statuses": [r["status"] for r in result["results"]]}
        except Exception as e:
            return tid, {"reference_visible_pass": False, "execution": "harness_error",
                         "error_type": type(e).__name__}

    with ThreadPoolExecutor(max_workers=4) as pool:
        audit = dict(pool.map(check, old))
    keep = {tid: old[tid] for tid in old if audit[tid]["reference_visible_pass"]}
    if len(keep) != 45:
        raise SystemExit(f"reference-visible selection changed: got {len(keep)}, expected 45")
    write_new(AUDIT, {"version": "bcb-jev-only-reference-visible-v2", "source_manifest_sha256": sha(OLD),
                      "results": audit})
    write_new(NEW, {"version": "bcb-jev-only-v2", "dataset_revision": SOURCE_REVISION,
                    "source_sha256": SOURCE_SHA256, "source_manifest_sha256": sha(OLD),
                    "eligibility": "v1 selector plus public canonical code passes every frozen visible example",
                    "tasks": keep})
    print(f"kept {len(keep)} of {len(old)} tasks")


def hidden() -> None:
    if not NEW.exists():
        raise SystemExit("v2 manifest missing")
    ids = set(json.loads(NEW.read_text(encoding="utf-8"))["tasks"])
    rows = [r for r in selected_rows() if r["task_id"] in ids]
    if len(rows) != len(ids):
        raise SystemExit("v2 manifest IDs differ from source")
    write_new(HIDDEN, {"version": "bcb-jev-only-v2", "dataset_revision": SOURCE_REVISION,
                       "source_sha256": SOURCE_SHA256,
                       "tasks": {r["task_id"]: {"test": r["test"],
                                               "canonical_code": r["complete_prompt"] + r["canonical_solution"]}
                                 for r in rows}})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["manifest", "hidden"])
    args = ap.parse_args()
    manifest() if args.kind == "manifest" else hidden()


if __name__ == "__main__":
    main()
