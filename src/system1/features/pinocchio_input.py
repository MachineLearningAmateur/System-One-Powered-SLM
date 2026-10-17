"""Pinocchio-0.8B inputs, frozen setup and record selection (scorer, freeze, replay).

Input versions (frozen before any score of that version):
  pinocchio-input-v1  question = the small model's round-1 message (the task and its visible
            tests); answer = the checkpoint's answer text after the thinking. The
            router in routers_v2.json and the Table 1 entry. Frozen October 17.
  pinocchio-input-v2  the same question; answer = exactly the stored `code` of the checkpoint
            (the executed code, including harness-added imports; "" without code).
            An empty answer (no code) gets no score (status "empty_answer"; the package
            refuses empty answers); such a checkpoint never passes the visible tests.
            A dev-informed sensitivity, frozen October 17 after input-v1 was scored
            on dev: the package cuts answers at 800 characters, and in about 30 of
            the 470 visible-pass dev answers the graded code started after the cut.
Both keep the package defaults (prompt "combined", question cut at 1,500 and
answer at 800 characters, as in Pinocchio's training) and no source model or
benchmark. Router score = 1 - p_correct.

A score record is used only if it matches the current execution (exec_id), the
rebuilt input (input_sha256) and, where required, the full frozen setup.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from system1.loop.tasks import first_round_messages

V1, V2 = "pinocchio-input-v1", "pinocchio-input-v2"
INPUT_VERSIONS = (V1, V2)
FILES = {V1: "pinocchio_scores.jsonl", V2: "pinocchio_scores_input-v2.jsonl"}
ADAPTER_REPO, ADAPTER_REVISION = "KevinDavidHayes/pinocchio-0.8b", "a1410d4c3c74b1cb09c9133bb97c683db9726bf2"
BASE_REPO, BASE_REVISION = "Qwen/Qwen3.5-0.8B", "2fc06364715b967f1860aea9cf38778875588b17"
PACKAGE = "pinocchio-uq==0.1.1"
PROMPT_VARIANT = "combined"
TRUNCATION = (1500, 800)  # pinocchio.prompts.TRUNCATION["combined"]; checked at load time
# Fields every record made from now on carries, and that must equal the frozen values.
PINNED = {"adapter": ADAPTER_REPO, "adapter_revision": ADAPTER_REVISION, "base_model": BASE_REPO,
          "base_revision": BASE_REVISION, "package": PACKAGE, "prompt_variant": PROMPT_VARIANT,
          "truncation": list(TRUNCATION), "dtype": "torch.float32", "placeholder_image": True, "device": "cpu"}


def build_input(rec: dict, tasks, version: str) -> tuple[str, str]:
    question = first_round_messages(tasks[rec["task_id"]])[0]["content"]
    if version == V1:
        return question, rec["answer"] or ""
    if version == V2:
        return question, rec["code"] or ""
    raise ValueError(f"unknown Pinocchio input version {version!r}")


def input_sha(question: str, answer: str) -> str:
    return hashlib.sha256(json.dumps([question, answer]).encode()).hexdigest()


class PinocchioRecordError(RuntimeError):
    pass


def select_records(records: list[dict], checkpoints: list[dict], tasks, version: str,
                   require_pinned: bool) -> tuple[dict[str, dict], dict[str, int]]:
    """The one valid score record per checkpoint id: same exec_id, same rebuilt input hash, the
    given input version and, with require_pinned, every PINNED field. Stale records (another
    execution, input or setup) are counted, never used; two valid records for one checkpoint are
    an error. Returns (records by checkpoint id, counts)."""
    want = {c["checkpoint_id"]: (c["exec_id"], input_sha(*build_input(c, tasks, version))) for c in checkpoints}
    out: dict[str, dict] = {}
    counts = {"used": 0, "stale": 0, "other_checkpoints": 0}
    for r in records:
        cid = r["checkpoint_id"]
        if cid not in want:
            counts["other_checkpoints"] += 1
            continue
        ok = (r.get("input_version") == version and (r["exec_id"], r["input_sha256"]) == want[cid]
              and (not require_pinned or all(r.get(k) == v for k, v in PINNED.items())))
        if not ok:
            counts["stale"] += 1
            continue
        if cid in out:
            raise PinocchioRecordError(f"two valid Pinocchio records for {cid}")
        out[cid] = r
    counts["used"] = len(out)
    return out, counts


def read_records(run_dir: Path, version: str) -> list[dict]:
    from system1.eval.ledger import read_jsonl
    path = run_dir / FILES[version]
    if not path.exists():
        return []
    rows, bad = read_jsonl(path)
    if bad:
        raise PinocchioRecordError(f"{len(bad)} damaged lines in {path}")
    return rows
