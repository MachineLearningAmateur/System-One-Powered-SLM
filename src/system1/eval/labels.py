"""Hidden-test labels of a run, joined to its checkpoints.

scripts/grade_hidden.py writes results/runs/<run-id>/hidden_labels.jsonl, one
row per complete checkpoint, tagged with its grading session, and the session
file grade_sessions/<session>.json. Analyses read checkpoints only through
load_labelled(). It never falls back to another label source, and it stops on:
damaged trajectory lines, a checkpoint without a label, a duplicate label, a
label for other code, labels from more than one session or without their
session file, a non-protocol session (unless allowed), or an invalid label
(unless allowed).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from system1.eval.ledger import read_jsonl
from system1.loop.runner import complete_executions

LABELS_FILE = "hidden_labels.jsonl"
META_FILE = "grade_meta.json"
SESSIONS_DIR = "grade_sessions"


class LabelError(RuntimeError):
    pass


def code_sha(code: str | None) -> str | None:
    return None if code is None else hashlib.sha256(code.encode("utf-8")).hexdigest()


def load_labelled(run_dir: Path, allow_invalid: bool = False, allow_nonprotocol: bool = False,
                  report: dict | None = None) -> list[dict]:
    """Complete checkpoints with a "hidden" field {"passed", "base", "plus", "status", "n_valid_votes"}.

    `report`, if given, receives what the caller must state: the grading
    session, executions left out as incomplete or replaced, and invalid labels
    left out (only with allow_invalid)."""
    rows, bad = read_jsonl(run_dir / "trajectories.jsonl")
    if bad:
        raise LabelError(f"{len(bad)} damaged lines in trajectories.jsonl")
    dropped: list[dict] = []
    cps = complete_executions(rows, dropped=dropped)
    labels, bad = read_jsonl(run_dir / LABELS_FILE)
    if bad:
        raise LabelError(f"{len(bad)} damaged lines in {LABELS_FILE}")
    sessions = {lab.get("grade_session") for lab in labels}
    if len(sessions) != 1 or None in sessions:
        raise LabelError(f"labels must come from one grading session, found {sorted(map(str, sessions))}")
    session = sessions.pop()
    meta_path = run_dir / SESSIONS_DIR / f"{session}.json"
    if not meta_path.exists():
        raise LabelError(f"no session file for grading session {session}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if not meta.get("protocol") and not allow_nonprotocol:
        raise LabelError(f"grading session {session} is not protocol (vLLM running or git tree changed)")

    by_key: dict[tuple[str, str], dict] = {}
    for lab in labels:
        key = (lab["exec_id"], lab["checkpoint_id"])
        if key in by_key:
            raise LabelError(f"duplicate label for {key}")
        by_key[key] = lab
    out, invalid = [], []
    for r in cps:
        lab = by_key.get((r["exec_id"], r["checkpoint_id"]))
        if lab is None:
            raise LabelError(f"no label for {r['checkpoint_id']} ({r['exec_id'][:8]})")
        if lab["code_sha256"] != code_sha(r["code"]):
            raise LabelError(f"label of {r['checkpoint_id']} is for other code")
        if lab["status"] == "invalid":
            if not allow_invalid:
                raise LabelError(f"invalid label for {r['checkpoint_id']}")
            invalid.append(r["checkpoint_id"])
            continue
        out.append({**r, "hidden": {k: lab[k] for k in ("passed", "base", "plus", "status", "n_valid_votes")}})
    if report is not None:
        report.update({"grade_session": session, "protocol": bool(meta.get("protocol")),
                       "dropped_executions": dropped, "invalid_labels": invalid})
    return out
