"""Fixed 40/60 development/test split by task, stratified by benchmark.

The split is made once by scripts/make_split.py, written to
configs/split_v1.json and frozen before the pilot. The file, not this code,
is the source of truth: load_split() checks it and every later step reads it.
The pilot and all protocol decisions use development tasks only; test tasks
get no generation until the protocol is frozen.
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

from system1.config import CONFIGS

DEV_SHARE = 0.4
SEED = 20261016
SPLIT_PATH = CONFIGS / "split_v1.json"


def _task_key(task_id: str) -> tuple[str, int]:
    prefix, _, number = task_id.partition("/")
    return prefix, int(number)


def make_split(task_ids: dict[str, list[str]], dev_share: float = DEV_SHARE, seed: int = SEED) -> dict:
    """Shuffle each benchmark's tasks with its own seeded generator and take dev_share as development.

    The result does not depend on the order of the input ids.
    """
    out: dict = {"seed": seed, "dev_share": dev_share, "benchmarks": {}}
    for bench in sorted(task_ids):
        ids = sorted(set(task_ids[bench]), key=_task_key)
        rng = random.Random(f"{seed}:{bench}")
        shuffled = ids[:]
        rng.shuffle(shuffled)
        n_dev = round(dev_share * len(ids))
        out["benchmarks"][bench] = {
            "n_tasks": len(ids),
            "dev": sorted(shuffled[:n_dev], key=_task_key),
            "test": sorted(shuffled[n_dev:], key=_task_key),
        }
    return out


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_split(path: Path = SPLIT_PATH) -> dict:
    """Load the frozen split and check that it is consistent."""
    with open(path, encoding="utf-8") as f:
        split = json.load(f)
    seen: set[str] = set()
    for bench, part in split["benchmarks"].items():
        dev, test = set(part["dev"]), set(part["test"])
        if dev & test:
            raise ValueError(f"{bench}: {len(dev & test)} tasks are in both dev and test")
        if len(dev) + len(test) != part["n_tasks"] or len(dev) != len(part["dev"]) or len(test) != len(part["test"]):
            raise ValueError(f"{bench}: task counts do not add up")
        if seen & (dev | test):
            raise ValueError(f"{bench}: task ids repeat across benchmarks")
        seen |= dev | test
    return split


def split_of(split: dict, task_id: str) -> str:
    """'dev' or 'test' for a task id; KeyError if the task is not in the split."""
    for part in split["benchmarks"].values():
        if task_id in part["dev"]:
            return "dev"
        if task_id in part["test"]:
            return "test"
    raise KeyError(task_id)
