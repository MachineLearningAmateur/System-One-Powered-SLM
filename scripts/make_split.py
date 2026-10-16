"""Make the frozen 40/60 development/test split (run once, before the pilot).

    uv run python scripts/make_split.py            # writes configs/split_v1.json
    uv run python scripts/make_split.py --force    # only to rebuild on purpose

It refuses to overwrite an existing split, because the split is frozen.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date

import evalplus
from evalplus.data import get_human_eval_plus, get_human_eval_plus_hash, get_mbpp_plus, get_mbpp_plus_hash
from evalplus.data.humaneval import HUMANEVAL_PLUS_VERSION
from evalplus.data.mbpp import MBPP_PLUS_VERSION

from system1.eval.split import SPLIT_PATH, file_sha256, load_split, make_split


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite an existing split")
    args = parser.parse_args()
    if SPLIT_PATH.exists() and not args.force:
        print(f"{SPLIT_PATH} exists and is frozen; use --force only to rebuild it on purpose.")
        return 1

    he, mb = get_human_eval_plus(), get_mbpp_plus()
    split = make_split({"humaneval+": list(he), "mbpp+": list(mb)})
    split["created"] = date.today().isoformat()
    split["source"] = {
        "evalplus": getattr(evalplus, "__version__", "unknown"),
        "humaneval+": {"version": HUMANEVAL_PLUS_VERSION, "hash": get_human_eval_plus_hash()},
        "mbpp+": {"version": MBPP_PLUS_VERSION, "hash": get_mbpp_plus_hash()},
    }
    SPLIT_PATH.write_text(json.dumps(split, indent=1) + "\n", encoding="utf-8", newline="\n")
    load_split(SPLIT_PATH)  # checks the written file

    for bench, part in split["benchmarks"].items():
        print(f"{bench:11s} {part['n_tasks']:4d} tasks -> dev {len(part['dev']):4d}, test {len(part['test']):4d}")
    print(f"written {SPLIT_PATH}  sha256 {file_sha256(SPLIT_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
