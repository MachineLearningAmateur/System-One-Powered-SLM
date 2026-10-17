"""Score every complete checkpoint of a run with Pinocchio-0.8B (local, CPU).

    uv run --group pinocchio python scripts/score_pinocchio.py --run-id pilot-v1 --input-version pinocchio-input-v2

The input versions and the frozen setup are defined in
system1.features.pinocchio_input. The base model and the adapter are loaded from
their pinned local snapshots (never a moving Hub name), and the script checks the
package's truncation, the dtype and the placeholder image before it scores; every
record carries these fields. Labels are never read.

Resume: a checkpoint is skipped only if a record with the same execution, the same
rebuilt input and the full pinned setup exists. Records made before the setup was
pinned (the first input-v1 dev scores) are therefore not reused by this script.
Output: results/runs/<run-id>/<file of the input version>. "cpu_seconds" is the
elapsed time of one score on the CPU (not process CPU time; loading excluded).
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from importlib.metadata import version

from system1.config import RESULTS
from system1.eval.ledger import CostLedger, read_jsonl
from system1.features import pinocchio_input as PI
from system1.loop.runner import complete_executions
from system1.loop.tasks import load_tasks


def load_judge():
    """Pinocchio from the pinned snapshots, with the frozen setup checked."""
    import torch
    from huggingface_hub import snapshot_download
    from pinocchio import Pinocchio
    from pinocchio.prompts import TRUNCATION

    base = snapshot_download(PI.BASE_REPO, revision=PI.BASE_REVISION, local_files_only=True)
    adapter = snapshot_download(PI.ADAPTER_REPO, revision=PI.ADAPTER_REVISION, local_files_only=True)
    judge = Pinocchio(adapter=adapter, base_model=base, device_map="cpu")
    actual = {"adapter": PI.ADAPTER_REPO, "adapter_revision": PI.ADAPTER_REVISION, "base_model": PI.BASE_REPO,
              "base_revision": PI.BASE_REVISION, "package": f"pinocchio-uq=={version('pinocchio-uq')}",
              "prompt_variant": PI.PROMPT_VARIANT, "truncation": list(TRUNCATION[PI.PROMPT_VARIANT]),
              "dtype": str(next(judge._model.parameters()).dtype), "placeholder_image": judge._processor is not None,
              "device": str(next(judge._model.parameters()).device)}
    if actual != PI.PINNED:
        raise SystemExit(f"STOP: the loaded Pinocchio setup differs from the frozen one: "
                         f"{ {k: (actual[k], PI.PINNED[k]) for k in actual if actual[k] != PI.PINNED[k]} }")
    return judge, {**actual, "torch": torch.__version__}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--input-version", choices=PI.INPUT_VERSIONS, required=True)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()
    d = RESULTS / "runs" / args.run_id
    rows, bad = read_jsonl(d / "trajectories.jsonl")
    if bad:
        print(f"STOP: {len(bad)} damaged lines in trajectories.jsonl")
        return 2
    cps = complete_executions(rows)
    tasks = load_tasks()
    valid, counts = PI.select_records(PI.read_records(d, args.input_version), cps, tasks, args.input_version,
                                      require_pinned=True)
    todo = [c for c in cps if c["checkpoint_id"] not in valid]
    if args.limit:
        todo = todo[: args.limit]
    print(f"{len(cps)} checkpoints; valid records {counts['used']}, stale {counts['stale']}; {len(todo)} to score",
          flush=True)
    if not todo:
        return 0

    t0 = time.perf_counter()
    judge, setup = load_judge()
    print(f"model loaded in {time.perf_counter() - t0:.1f} s; setup {setup}", flush=True)
    store = CostLedger(d / PI.FILES[args.input_version])
    for i, c in enumerate(todo, 1):
        q, a = PI.build_input(c, tasks, args.input_version)
        t = time.perf_counter()
        # The package refuses an empty answer (input-v2 of a checkpoint without code): no score, recorded
        # as such. Such a checkpoint never passes the visible tests, so no routing decision uses it.
        p = float(judge.score(question=q, answer=a)) if a.strip() else None
        store.append_obj({"checkpoint_id": c["checkpoint_id"], "exec_id": c["exec_id"], "task_id": c["task_id"],
                          "attempt": c["attempt"], "round": c["round"], "p_correct": p,
                          "score": None if p is None else 1.0 - p, "status": "ok" if p is not None else "empty_answer",
                          "cpu_seconds": round(time.perf_counter() - t, 3), "input_version": args.input_version,
                          "input_sha256": PI.input_sha(q, a), **setup, "ts": datetime.now(timezone.utc).isoformat()})
        if i % 50 == 0:
            print(f"  {i}/{len(todo)}", flush=True)
    print(f"done: {len(todo)} scored in {time.perf_counter() - t0:.0f} s", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
