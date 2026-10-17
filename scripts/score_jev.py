"""Score the checkpoints of a run with Jev, in both evidence arms.

    uv run python scripts/score_jev.py --run-id pilot-v1 --repeat 30

Outputs go next to the run in results/runs/<run-id>/: jev_scores.jsonl (one
record per checkpoint and arm), jev_ledger.jsonl (one row per HTTP attempt),
jev_repeat.jsonl (the repeat sample: the same requests sent again, for the
stability gate) and jev_meta.json (the scoring protocol and sessions).

The scorer reads trajectories only, never hidden labels. A rerun skips
checkpoints whose arms all have a final record; a checkpoint with a failed
arm (protocol_error, request_error) is scored again in every arm, and
analyses take the last record per (checkpoint, arm). The run stops if the
scoring protocol (rubric hash, evidence version, byte budget, requested
model) differs from the one stored, if Jev returns another model version,
or if the input-token guard is reached. The git tree must be clean, as for
generation runs.
"""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from system1.config import RESULTS, ROOT, load_prices
from system1.eval.ledger import CostLedger, read_jsonl
from system1.features.evidence import ARMS, EVIDENCE_VERSION
from system1.features.jev_scoring import JevScorer, ModelVersionChanged, ScoreStore, load_rubric
from system1.loop.runner import complete_executions, to_scoring_checkpoint
from system1.routers.jev import BYTE_BUDGET, DEFAULT_MODEL, JevClient

SCORES, LEDGER, REPEAT, META = "jev_scores.jsonl", "jev_ledger.jsonl", "jev_repeat.jsonl", "jev_meta.json"
FINAL = {"ok", "no_questions", "evidence_too_large", "bad_checkpoint"}
REPEAT_SEED = 20261016


def git_state() -> tuple[str, bool]:
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True).stdout
    return commit, bool(status.strip())


def protocol(rubric, client: JevClient) -> dict:
    return {"rubric_version": rubric.version, "rubric_sha256": rubric.sha256, "evidence_version": EVIDENCE_VERSION,
            "byte_budget": client.byte_budget, "model_requested": client.model, "arms": list(ARMS)}


def done_checkpoints(store: ScoreStore) -> set[str]:
    """Checkpoints whose every arm has a final last record."""
    rows, bad = store.read()
    if bad:
        raise RuntimeError(f"{len(bad)} damaged lines in {store.path}")
    last = {(r["checkpoint_id"], r["arm"]): r["status"] for r in rows}
    ids = {cid for cid, _ in last}
    return {cid for cid in ids if all(last.get((cid, arm)) in FINAL for arm in ARMS)}


def used_input_tokens(ledger: CostLedger) -> int:
    rows, _ = ledger.read()
    return sum(r.get("input_tokens") or 0 for r in rows)


def score_run(run_dir: Path, client: JevClient, *, repeat: int = 0, max_input_tokens: int = 4_000_000,
              limit: int = 0, commit: str = "", dirty: bool = False, log=print) -> int:
    rows, bad = read_jsonl(run_dir / "trajectories.jsonl")
    if bad:
        log(f"{len(bad)} damaged lines in trajectories.jsonl")
        return 2
    cps = complete_executions(rows)
    if limit:
        cps = cps[:limit]
    rubric = load_rubric()
    proto = protocol(rubric, client)
    meta_path = run_dir / META
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None
    if meta and meta["protocol"] != proto:
        diff = sorted(k for k in set(meta["protocol"]) | set(proto) if meta["protocol"].get(k) != proto.get(k))
        log(f"{run_dir.name} was scored with another protocol (differs in: {', '.join(diff)})")
        return 2
    meta = meta or {"run_id": run_dir.name, "protocol": proto, "model_version": None, "sessions": []}
    session = {"started": datetime.now(timezone.utc).isoformat(), "git_commit": commit, "git_dirty": dirty,
               "outcome": "interrupted"}
    meta["sessions"].append(session)
    meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")

    ledger = client.ledger
    store = ScoreStore(run_dir / SCORES)
    scorer = JevScorer(client, rubric, store, run_id=run_dir.name, expected_model_version=meta["model_version"])
    done = done_checkpoints(store)
    jobs = [r for r in cps if r["checkpoint_id"] not in done]
    log(f"{len(jobs)} checkpoints to score ({len(done)} already done)")
    try:
        for i, rec in enumerate(jobs):
            if used_input_tokens(ledger) >= max_input_tokens:
                session["outcome"] = "token_guard"
                log(f"STOP: input-token guard ({max_input_tokens}) reached")
                return 1
            out = scorer.score_arms(to_scoring_checkpoint(rec))
            meta["model_version"] = scorer.model_version
            if (i + 1) % 50 == 0 or i + 1 == len(jobs):
                log(f"[{i + 1}/{len(jobs)}] " + ", ".join(f"{r.arm} {r.status}" for r in out))
        # The repeat sample: the same evidence again, same model version (stability gate).
        if repeat:
            rstore = ScoreStore(run_dir / REPEAT)
            rrows, _ = rstore.read()
            have = {r["checkpoint_id"] for r in rrows}
            pick = random.Random(REPEAT_SEED).sample(cps, min(repeat, len(cps)))
            rscorer = JevScorer(client, rubric, rstore, run_id=run_dir.name, expected_model_version=scorer.model_version)
            todo = [r for r in pick if r["checkpoint_id"] not in have]
            log(f"repeat sample: {len(todo)} checkpoints to score again ({len(have)} already done)")
            for rec in todo:
                if used_input_tokens(ledger) >= max_input_tokens:
                    session["outcome"] = "token_guard"
                    log(f"STOP: input-token guard ({max_input_tokens}) reached")
                    return 1
                rscorer.score_arms(to_scoring_checkpoint(rec))
        session["outcome"] = "finished"
    except ModelVersionChanged as e:
        session["outcome"] = "model_changed"
        log(f"STOP: {e}")
        return 1
    finally:
        session["ended"] = datetime.now(timezone.utc).isoformat()
        session["input_tokens_total"] = used_input_tokens(ledger)
        meta_path.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    left = [r for r in cps if r["checkpoint_id"] not in done_checkpoints(store)]
    log(f"done; {len(left)} checkpoints without a final record in every arm; "
        f"input tokens in the ledger {used_input_tokens(ledger)}")
    return 1 if left else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--repeat", type=int, default=0, help="checkpoints scored a second time (stability gate)")
    ap.add_argument("--max-input-tokens", type=int, default=4_000_000, help="stop before more input tokens than this")
    ap.add_argument("--limit", type=int, default=0, help="first N checkpoints only (0 = all)")
    ap.add_argument("--allow-dirty", action="store_true", help="smoke runs only")
    args = ap.parse_args()
    commit, dirty = git_state()
    if dirty and not args.allow_dirty:
        print("The git tree has changes. Commit them first, or use --allow-dirty for a smoke run.")
        return 2
    run_dir = RESULTS / "runs" / args.run_id
    if not (run_dir / "trajectories.jsonl").exists():
        print(f"no trajectories.jsonl in {run_dir}")
        return 2
    with JevClient(model=DEFAULT_MODEL, ledger=CostLedger(run_dir / LEDGER), prices=load_prices(),
                   byte_budget=BYTE_BUDGET) as client:
        return score_run(run_dir, client, repeat=args.repeat, max_input_tokens=args.max_input_tokens,
                         limit=args.limit, commit=commit, dirty=dirty)


if __name__ == "__main__":
    sys.exit(main())
