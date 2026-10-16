"""Score checkpoints with Jev and keep a durable record of every scoring.

One record per (checkpoint, arm). The record links to the cost ledger by
call_id and holds what replay needs: the rubric and evidence versions, the
request hash and size, the budget, the raw answers and the validated
features. A question that does not apply is recorded with its reasons, never
as a probability.

The arms of one checkpoint are built together on one shared base, so a
checkpoint is either scored in every arm or recorded as too large in every
arm. Ownership: like the ledger, one ScoreStore instance owns a file.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from system1.config import CONFIGS
from system1.eval.ledger import CostLedger
from system1.features.evidence import (
    ARMS,
    EVIDENCE_VERSION,
    Checkpoint,
    Evidence,
    EvidenceTooLarge,
    build_arms,
)
from system1.routers.jev import JevClient, JevProtocolError, JevRequestError, request_body

APPLICABLE = "applicable"


class ModelVersionChanged(RuntimeError):
    """Jev returned a different model version in the middle of a run."""


@dataclass(frozen=True)
class Rubric:
    version: str
    sha256: str
    questions: dict[str, dict[str, Any]]

    def api_question(self, qid: str) -> dict[str, Any]:
        q = self.questions[qid]
        out = {"type": "noul", "instructions": q["instructions"]}
        if q.get("criteria"):
            out["criteria"] = {"true": q["criteria"]["true"], "false": q["criteria"]["false"]}
        return out


def load_rubric(path: Path | None = None) -> Rubric:
    with open(path or CONFIGS / "rubric_v2.yaml", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    questions = raw["questions"]
    for qid, q in questions.items():
        crit = q.get("criteria") or {}
        if crit and set(crit) != {"true", "false"}:
            raise ValueError(f"{qid}: criteria keys must be the strings 'true' and 'false' (quote them in YAML)")
        unknown = set(q.get("needs", [])) - {"history", "trace"}
        if unknown:
            raise ValueError(f"{qid}: unknown evidence blocks {sorted(unknown)}")
        bad_rules = set(q.get("not_applicable_when", [])) - {"first_round", "visible_pass"}
        if bad_rules:
            raise ValueError(f"{qid}: unknown applicability rules {sorted(bad_rules)}")
    # The hash covers what changes the requests or the applicability, not the status label.
    hashed = {qid: {k: q.get(k) for k in ("instructions", "criteria", "needs", "not_applicable_when")}
              for qid, q in questions.items()}
    canonical = json.dumps({"version": raw["version"], "questions": hashed}, sort_keys=True, ensure_ascii=False)
    return Rubric(raw["version"], hashlib.sha256(canonical.encode("utf-8")).hexdigest(), questions)


def applicability(rubric: Rubric, cp: Checkpoint, arm: str) -> dict[str, str]:
    """APPLICABLE, or "na:" + every reason the question is not asked (checkpoint reasons first)."""
    blocks = ARMS[arm]
    out = {}
    for qid, q in rubric.questions.items():
        needs = set(q.get("needs", []))
        rules = set(q.get("not_applicable_when", []))
        reasons = []
        if "first_round" in rules and cp.first_round:
            reasons.append("first_round")
        if "visible_pass" in rules and cp.visible_pass:
            reasons.append("visible_pass")
        if "trace" in needs and not cp.has_trace:
            reasons.append("trace_missing")
        missing = needs - blocks
        if missing:
            reasons.append("arm_lacks_" + "_".join(sorted(missing)))
        out[qid] = "na:" + ",".join(reasons) if reasons else APPLICABLE
    return out


@dataclass
class ScoringRecord:
    run_id: str
    checkpoint_id: str
    task_id: str
    benchmark: str
    attempt: int
    round: int
    arm: str
    visible_pass: bool
    first_round: bool
    rubric_version: str
    rubric_sha256: str
    evidence_version: str
    byte_budget: int | None
    # ok | no_questions | evidence_too_large | bad_checkpoint | protocol_error
    # | request_error | model_changed | skipped
    status: str
    applicability: dict[str, str]
    features: dict[str, float | None]
    model_requested: str
    model_returned: str | None = None
    call_id: str | None = None
    request_sha256: str | None = None
    request_bytes: int | None = None
    unfitted_bytes: int | None = None
    base_trimmed: bool | None = None
    telemetry_sanitized: list[str] | None = None
    trace_original_chars: int | None = None
    trace_retained_chars: int | None = None
    trace_truncated: bool | None = None
    raw_answers: dict[str, Any] | None = None
    error: str | None = None
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ScoreStore:
    def __init__(self, path: Path | str):
        # Reuse the ledger's append and damaged-tail handling for JSONL files.
        self._file = CostLedger(path)
        self.path = self._file.path

    def append(self, record: ScoringRecord) -> None:
        self._file.append_obj(asdict(record))

    def read(self) -> tuple[list[dict], list[tuple[int, str]]]:
        return self._file.read()

    def last_model_version(self, run_id: str) -> str | None:
        rows, _ = self.read()
        versions = [r["model_returned"] for r in rows
                    if r.get("run_id") == run_id and r.get("status") == "ok" and r.get("model_returned")]
        return versions[-1] if versions else None


class JevScorer:
    def __init__(self, client: JevClient, rubric: Rubric, store: ScoreStore, run_id: str,
                 expected_model_version: str | None = None):
        self.client = client
        self.rubric = rubric
        self.store = store
        self.run_id = run_id
        # A resumed run keeps checking against the version it started with.
        self.model_version = expected_model_version or store.last_model_version(run_id)

    def _record(self, cp: Checkpoint, arm: str, app: dict[str, str]) -> ScoringRecord:
        return ScoringRecord(
            run_id=self.run_id, checkpoint_id=cp.checkpoint_id, task_id=cp.task_id,
            benchmark=cp.benchmark, attempt=cp.attempt, round=cp.round, arm=arm,
            visible_pass=cp.visible_pass, first_round=cp.first_round,
            rubric_version=self.rubric.version, rubric_sha256=self.rubric.sha256,
            evidence_version=EVIDENCE_VERSION, byte_budget=self.client.byte_budget,
            status="ok", applicability=app, features={q: None for q in app},
            model_requested=self.client.model,
        )

    def score(self, cp: Checkpoint, arm: str) -> ScoringRecord:
        return self.score_arms(cp, (arm,))[0]

    def score_arms(self, cp: Checkpoint, arms: tuple[str, ...] = tuple(ARMS)) -> list[ScoringRecord]:
        """Score the arms of one checkpoint together (interleaved, one shared base)."""
        records: dict[str, ScoringRecord] = {}
        questions: dict[str, dict] = {}
        for arm in arms:
            app = applicability(self.rubric, cp, arm)
            records[arm] = self._record(cp, arm, app)
            qids = [q for q, s in app.items() if s == APPLICABLE]
            if qids:
                questions[arm] = {q: self.rubric.api_question(q) for q in qids}
            else:
                records[arm].status = "no_questions"

        evidence: dict[str, Evidence] = {}
        if questions:
            try:
                evidence = build_arms(cp, questions, model=self.client.model, budget=self.client.byte_budget)
            except EvidenceTooLarge as e:
                for arm in questions:  # every arm with questions, so the pair stays paired
                    records[arm].status, records[arm].error = "evidence_too_large", str(e)
                    records[arm].unfitted_bytes = e.unfitted_bytes
            except (ValueError, TypeError) as e:  # e.g. telemetry that is not JSON
                for arm in questions:
                    records[arm].status, records[arm].error = "bad_checkpoint", f"{type(e).__name__}: {e}"

        changed: str | None = None
        for arm in arms:
            rec = records[arm]
            if arm in evidence:
                if changed:  # do not pay for more calls once the version changed
                    rec.status, rec.error = "skipped", "model version changed in an earlier arm"
                else:
                    changed = self._call(cp, arm, rec, questions[arm], evidence[arm])
            self.store.append(rec)
        if changed:
            raise ModelVersionChanged(changed)
        return [records[arm] for arm in arms]

    def _call(self, cp: Checkpoint, arm: str, rec: ScoringRecord, questions: dict, ev: Evidence) -> str | None:
        """Ask Jev for one arm and fill the record. Returns a message if the model version changed."""
        rec.request_bytes = ev.payload_bytes
        rec.request_sha256 = hashlib.sha256(request_body(self.client.model, ev.state, questions)).hexdigest()
        rec.unfitted_bytes = ev.unfitted_bytes
        rec.base_trimmed = ev.base_trimmed
        rec.telemetry_sanitized = ev.telemetry_sanitized
        rec.trace_original_chars = ev.trace_original_chars
        rec.trace_retained_chars = ev.trace_retained_chars
        rec.trace_truncated = ev.trace_truncated
        try:
            r = self.client.ask(ev.state, questions, task_id=cp.task_id, attempt=cp.attempt,
                                step=cp.round, arm=arm)
        except JevProtocolError as e:
            rec.status, rec.error = "protocol_error", str(e)
            return None
        except JevRequestError as e:
            rec.status, rec.error = "request_error", str(e)
            return None

        rec.call_id = r.call_id
        rec.model_returned = r.model_returned
        rec.request_sha256 = r.request_sha256  # identical by construction; this is the sent copy
        rec.raw_answers = r.answers
        for q in questions:
            rec.features[q] = r.probability(q)

        if self.model_version is None:
            self.model_version = r.model_returned
        elif r.model_returned != self.model_version:
            rec.status = "model_changed"  # answers kept for audit; analyses use status == "ok"
            return (f"run {self.run_id}: model changed from {self.model_version} to {r.model_returned} "
                    f"at {cp.checkpoint_id} {arm}; stop and rescore")
        return None
