"""Freeze the pilot's five-attempt subsample (run once).

    uv run python scripts/make_pilot_subsample.py

Rule (docs/research-plan.md, Pilot): one third of the development tasks of
each benchmark, drawn with seed SEED (the split seed + 1), written to
configs/pilot_subsample_v1.json. The pilot runs one attempt on every
development task and five attempts on these tasks:

    uv run python scripts/run_loop.py --run-id pilot-v1 --attempts 1
    uv run python scripts/run_loop.py --run-id pilot-v1 --attempts 5 --tasks-file configs/pilot_subsample_v1.json
"""

from __future__ import annotations

import json
import random
import sys
from datetime import date

from system1.config import CONFIGS
from system1.eval.split import SPLIT_PATH, file_sha256, load_split

SUBSAMPLE_PATH = CONFIGS / "pilot_subsample_v1.json"
SEED = 20261017
SHARE = 1 / 3


def draw(split: dict) -> dict[str, list[str]]:
    rng = random.Random(SEED)
    out = {}
    for bench in sorted(split["benchmarks"]):
        dev = split["benchmarks"][bench]["dev"]
        chosen = set(rng.sample(dev, round(len(dev) * SHARE)))
        out[bench] = [t for t in dev if t in chosen]  # split order
    return out


def main() -> int:
    if SUBSAMPLE_PATH.exists():
        print(f"{SUBSAMPLE_PATH} exists and is frozen.")
        return 1
    tasks = draw(load_split())
    out = {"created": date.today().isoformat(), "seed": SEED, "share": "1/3 of dev tasks per benchmark",
           "split_sha256": file_sha256(SPLIT_PATH), "benchmarks": tasks,
           "tasks": [t for b in sorted(tasks) for t in tasks[b]]}
    SUBSAMPLE_PATH.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    print({b: len(v) for b, v in tasks.items()}, f"written {SUBSAMPLE_PATH}  sha256 {file_sha256(SUBSAMPLE_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
