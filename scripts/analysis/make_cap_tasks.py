"""Froze configs/cap12k_tasks_v1.json (dev tasks with >=1 8K cap hit); run once, refuses to overwrite."""
import json
from datetime import date
from pathlib import Path
from system1.eval.labels import load_labelled
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
cps = load_labelled(Path("results/runs/pilot-v1")) + load_labelled(Path("results/runs/pilot-v1b"))
hit = {c["task_id"] for c in cps if c["generation"]["cap_hit"]}
split = load_split()
bench = {b: [t for t in split["benchmarks"][b]["dev"] if t in hit] for b in sorted(split["benchmarks"])}
out = {"created": date.today().isoformat(),
       "rule": "dev tasks with >=1 thinking-cap hit at 8K in runs pilot-v1 and pilot-v1b; rerun attempt 0 at 12K",
       "split_sha256": file_sha256(SPLIT_PATH), "benchmarks": bench,
       "tasks": [t for b in sorted(bench) for t in bench[b]]}
p = Path("configs/cap12k_tasks_v1.json")
assert not p.exists()
p.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
print({b: len(v) for b, v in bench.items()}, len(out["tasks"]))
