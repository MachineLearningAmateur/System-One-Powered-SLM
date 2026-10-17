"""Tasks excluded from hidden grading and from every outcome analysis (Amendment A2).

configs/grading_exclusions_v1.json lists tasks that the pinned grader cannot
grade (see each task's reason and evidence). The split stays unchanged: an
excluded task is still a split task, but scripts/grade_hidden.py gives it no
grade and no label, scripts/run_frontier.py makes no call for it, and
eval.labels.load_labelled() drops all its checkpoints and reports them. One
file and one helper serve all three, so they cannot disagree.
"""

from __future__ import annotations

import json
from pathlib import Path

from system1.config import CONFIGS
from system1.eval.split import file_sha256, load_split

EXCLUSIONS_PATH = CONFIGS / "grading_exclusions_v1.json"


def load_exclusions(path: Path = EXCLUSIONS_PATH) -> dict:
    """{"version", "sha256", "tasks": {task_id: benchmark}}; each task must be in the split as listed."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    split = load_split()
    tasks: dict[str, str] = {}
    for t in doc["tasks"]:
        tid, bench, part = t["task_id"], t["benchmark"], t["split"]
        if tid not in split["benchmarks"][bench][part]:
            raise ValueError(f"excluded task {tid} is not a {bench} {part} task")
        if tid in tasks:
            raise ValueError(f"excluded task {tid} is listed twice")
        tasks[tid] = bench
    return {"version": doc["version"], "sha256": file_sha256(path), "tasks": tasks}


def split_excluded(rows: list[dict], excl: dict) -> tuple[list[dict], list[dict]]:
    """(kept, excluded) rows by task_id."""
    kept = [r for r in rows if r["task_id"] not in excl["tasks"]]
    gone = [r for r in rows if r["task_id"] in excl["tasks"]]
    return kept, gone


def session_record(excl: dict, gone: list[dict], n_before: int) -> dict:
    """What a grading session stores about the exclusions it applied."""
    return {"version": excl["version"], "sha256": excl["sha256"], "tasks": sorted(excl["tasks"]),
            "excluded_checkpoints": sorted(r["checkpoint_id"] for r in gone),
            "n_before": n_before, "n_after": n_before - len(gone)}
