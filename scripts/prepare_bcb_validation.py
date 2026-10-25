"""Build the BigCodeBench validation manifest from the pinned v0.1.4 parquet.

Run with a Python environment containing pyarrow:
    python scripts/prepare_bcb_validation.py manifest
After the protocol freeze, on the grading machine only:
    python scripts/prepare_bcb_validation.py hidden

The manifest contains prompts and visible docstring examples only. The hidden
file stays ignored under results/datasets/ and must never reach the generator
or Jev. Neither command overwrites an existing output.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import sys
import warnings
from pathlib import Path

import pyarrow.parquet as pq

from system1.config import ROOT
from system1.loop.tasks import docstring_tests

SOURCE = ROOT / "results/datasets/bigcodebench-v014.parquet"
SOURCE_SHA256 = "d9a4965821c9507ebdfb551c288656b2d5fe553234f5183044333ca8a4018267"
SOURCE_REVISION = "b74c0d0bf70d2c0bc459be537895cca163007f1a"
MANIFEST = ROOT / "configs/bcb_jev_only_tasks_v1.json"
HIDDEN = ROOT / "results/datasets/bcb_jev_only_hidden_v1.json"

# Restrict to tasks whose declared libraries work in the existing networkless
# Python sandbox. This rule only reads public prompt metadata, not test cases.
EXCLUDED_MODULES = frozenset({
    "os", "pathlib", "shutil", "glob", "tempfile", "subprocess", "socket", "sqlite3",
    "zipfile", "tarfile", "shelve", "dbm", "pickle", "csv", "urllib", "smtplib",
    "ftplib", "http", "imaplib", "poplib", "ssl", "webbrowser", "turtle",
})


def selected_rows() -> list[dict]:
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise SystemExit("BigCodeBench parquet hash differs from the pinned source")
    rows = pq.read_table(SOURCE).to_pylist()
    selected = []
    for row in rows:
        libs = ast.literal_eval(row["libs"])
        if not all(lib.split(".")[0] in sys.stdlib_module_names
                   and lib.split(".")[0] not in EXCLUDED_MODULES for lib in libs):
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", SyntaxWarning)
                visible = docstring_tests(row["complete_prompt"], row["entry_point"])
        except (ValueError, SyntaxError):
            continue
        if visible:
            selected.append({**row, "visible": visible})
    if len(selected) != 75:
        raise SystemExit(f"selection changed: got {len(selected)} tasks, expected 75")
    return selected


def write_new(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"created {path.relative_to(ROOT)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["manifest", "hidden"])
    args = ap.parse_args()
    rows = selected_rows()
    if args.kind == "manifest":
        tasks = {r["task_id"]: {"benchmark": "bigcodebench", "prompt": r["complete_prompt"],
                                "entry_point": r["entry_point"], "visible_tests": r["visible"],
                                "visible_source": "docstring", "shown_tests": "",
                                "canonical_fails_visible": False} for r in rows}
        write_new(MANIFEST, {"version": "bcb-jev-only-v1", "dataset_revision": SOURCE_REVISION,
                             "source_sha256": SOURCE_SHA256, "tasks": tasks})
    else:
        if not MANIFEST.exists():
            raise SystemExit("manifest must exist before extracting hidden tests")
        ids = set(json.loads(MANIFEST.read_text(encoding="utf-8"))["tasks"])
        if ids != {r["task_id"] for r in rows}:
            raise SystemExit("manifest task IDs differ from pinned selection")
        # Kept out of git and only mounted into the networkless grading sandbox.
        write_new(HIDDEN, {"version": "bcb-jev-only-v1", "dataset_revision": SOURCE_REVISION,
                           "source_sha256": SOURCE_SHA256,
                           "tasks": {r["task_id"]: {"test": r["test"],
                                                   "canonical_code": r["complete_prompt"] + r["canonical_solution"]}
                                     for r in rows}})


if __name__ == "__main__":
    main()
