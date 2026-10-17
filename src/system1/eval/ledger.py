"""Append-only JSONL cost ledger: one row per HTTP attempt or local model call.

Rows are logged for every attempt, including retries, failures and router
calls that say "continue", so router overhead is never left out of the cost.
Unknown usage or cost stays null; it is never recorded as zero. A sum of
usd_computed is therefore not total spend: report the null rows with it and
reconcile against the provider's billing.

Ownership: one shared CostLedger instance per file. Threads in that process
share the instance; other processes write their own files, which are merged
after the run. The lock below protects only threads that share the instance.
"""

from __future__ import annotations

import json
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class LedgerRow:
    component: str  # small_model | router | frontier | labeler
    model: str
    provider: str
    task_id: str | None = None
    attempt: int | None = None  # generation attempt of the small model (0-4)
    step: int | None = None
    arm: str | None = None  # evidence arm, e.g. "base+history+trace"
    call_id: str | None = None  # one logical call; its HTTP retries share it
    http_attempt: int | None = None  # 0 for the first request of a call
    status: str = "ok"  # ok | http:<code> | transport:<error> | protocol:<reason>
    input_tokens: int | None = None
    output_tokens: int | None = None
    reasoning_tokens: int | None = None
    usd_reported: float | None = None
    usd_computed: float | None = None
    latency_ms: float | None = None
    gpu_seconds: float | None = None
    request_bytes: int | None = None
    model_returned: str | None = None
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CostLedger:
    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._close_damaged_tail()

    def _close_damaged_tail(self) -> None:
        """An interrupted earlier write can leave a final line with no newline.
        Terminate it, so that it stays one bad line for audit and the next row
        is not joined to it."""
        if not self.path.exists() or self.path.stat().st_size == 0:
            return
        with open(self.path, "rb+") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                f.write(b"\n")

    def append(self, row: LedgerRow) -> None:
        self.append_obj(asdict(row))

    def append_obj(self, obj: dict) -> None:
        """Append one JSON object as a line (also used by other JSONL stores)."""
        line = json.dumps(obj, ensure_ascii=False)
        with self._lock, open(self.path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def read(self) -> tuple[list[dict], list[tuple[int, str]]]:
        """Return (rows, bad_lines); see read_jsonl."""
        with self._lock:
            return read_jsonl(self.path)


def read_jsonl(path: Path | str) -> tuple[list[dict], list[tuple[int, str]]]:
    """Read a JSONL file without opening it for writing (analysis loaders use this, so a
    read never changes a run's files). Returns (rows, bad_lines); bad lines keep their
    1-based line number for audit; bytes that are not valid UTF-8 are shown with
    replacement characters."""
    rows: list[dict] = []
    bad: list[tuple[int, str]] = []
    path = Path(path)
    if not path.exists():
        return rows, bad
    with open(path, "rb") as f:
        for n, raw in enumerate(f, start=1):
            if not raw.strip():
                continue
            try:
                rows.append(json.loads(raw.decode("utf-8")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                bad.append((n, raw.rstrip(b"\n").decode("utf-8", errors="replace")))
    return rows, bad


def usd_for(prices: dict | None, model: str, input_tokens: int | None, output_tokens: int | None) -> float | None:
    """Dollars from pinned prices; None when a price or the usage is unknown."""
    if input_tokens is None or output_tokens is None:
        return None
    entry = (prices or {}).get("models", {}).get(model)
    if not entry:
        return None
    p_in, p_out = entry.get("usd_per_m_input"), entry.get("usd_per_m_output")
    if p_in is None or p_out is None:
        return None
    return (input_tokens * p_in + output_tokens * p_out) / 1_000_000
