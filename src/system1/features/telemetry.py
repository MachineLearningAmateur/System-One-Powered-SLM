"""Cheap features of one checkpoint, computed from the loop's own records.

Two views of the same numbers:
  cheap_features()  everything, for the cheap-feature logistic regression;
  jev_telemetry()   the code-and-test signals only, for Jev's shared base
                    state. Trace statistics stay out of it, because the base
                    state is shared by the arm without the thinking.
"""

from __future__ import annotations

import difflib
import re
from collections import Counter
from typing import Any

# Reflection markers at the start of a paragraph (they mostly follow "\n\n").
MARKER = re.compile(r"(?:^|\n\n)\s*(wait|alternatively|hmm|but wait|actually)\b", re.I)
LOOP_NGRAM = 8  # words
LOOP_MIN_REPEATS = 6
NEAR_COPY = 0.95

JEV_TELEMETRY_KEYS = (
    "visible_pass_fraction", "pass_count_delta", "similarity_to_previous",
    "same_error_as_previous", "same_failing_tests_as_previous", "returns_to_earlier_code",
)


def similarity(a: str | None, b: str | None) -> float | None:
    if a is None or b is None:
        return None
    return round(difflib.SequenceMatcher(None, a, b, autojunk=False).ratio(), 4)


def error_signature(results: list[dict], execution: dict | None = None) -> tuple:
    head = ((execution.get("status"), execution.get("stage"), execution.get("error_type")),) \
        if execution and execution.get("status") != "ok" else ()
    return head + tuple((i, r["status"], r.get("error_type")) for i, r in enumerate(results) if r["status"] != "pass")


def failing_tests(results: list[dict]) -> frozenset[int]:
    return frozenset(i for i, r in enumerate(results) if r["status"] != "pass")


def marker_count(thinking: str) -> int:
    return len(MARKER.findall(thinking))


def loop_flag(thinking: str) -> bool:
    words = thinking.split()
    grams = Counter(tuple(words[i:i + LOOP_NGRAM]) for i in range(len(words) - LOOP_NGRAM + 1))
    return bool(grams) and max(grams.values()) >= LOOP_MIN_REPEATS


def cheap_features(rounds: list[dict]) -> dict[str, Any]:
    """Features of the last round in `rounds`.

    Each round: {"code": str|None, "results": [visible result], "execution": {...},
    "thinking": str, "thinking_tokens": int, "cap_hit": bool, "think_closed": bool,
    "confidence": {"thinking": {...}, "answer": {...}}}
    A test that never ran ("not_run") is not passed, but it is not a failure either.
    """
    cur = rounds[-1]
    prev = rounds[-2] if len(rounds) > 1 else None
    res = cur["results"]
    ex = cur.get("execution") or {}
    n_pass = sum(r["status"] == "pass" for r in res)
    n_not_run = sum(r["status"] == "not_run" for r in res)
    error_types = {r.get("error_type") or r["status"] for r in res if r["status"] not in ("pass", "not_run")}
    if ex.get("status") not in (None, "ok"):
        error_types.add(ex.get("error_type") or ex["status"])
    error_types = sorted(error_types)

    f: dict[str, Any] = {
        "round": len(rounds),
        "n_visible": len(res),
        "visible_pass_count": n_pass,
        "visible_pass_fraction": round(n_pass / len(res), 4) if res else None,
        "visible_pass": bool(res) and n_pass == len(res),
        "visible_not_run_count": n_not_run,
        "execution_status": ex.get("status"),
        "execution_stage": ex.get("stage"),
        "error_types": error_types,
        "code_missing": cur["code"] is None,
        "code_lines": len(cur["code"].splitlines()) if cur["code"] else 0,
        "pass_count_delta": None,
        "similarity_to_previous": None,
        "same_error_as_previous": None,
        "same_failing_tests_as_previous": None,
        "returns_to_earlier_code": None,
        # trace statistics (never in Jev's base state)
        "thinking_tokens": cur["thinking_tokens"],
        "cap_hit": cur["cap_hit"],
        "think_closed": cur["think_closed"],
        "marker_count": marker_count(cur["thinking"]),
        "loop_flag": loop_flag(cur["thinking"]),
    }
    for part in ("thinking", "answer"):
        for k, v in (cur.get("confidence", {}).get(part) or {}).items():
            if k != "n_tokens":
                f[f"{part}_{k}"] = v

    if prev is not None:
        prev_pass = sum(r["status"] == "pass" for r in prev["results"])
        f["pass_count_delta"] = n_pass - prev_pass
        f["similarity_to_previous"] = similarity(cur["code"], prev["code"])
        cur_sig, prev_sig = error_signature(res, ex), error_signature(prev["results"], prev.get("execution"))
        f["same_error_as_previous"] = bool(cur_sig) and cur_sig == prev_sig
        cur_fail = failing_tests(res)
        f["same_failing_tests_as_previous"] = bool(cur_fail) and cur_fail == failing_tests(prev["results"])
        earlier = [r["code"] for r in rounds[:-2]]  # rounds before the previous one
        sims = [similarity(cur["code"], c) for c in earlier]
        sims = [s for s in sims if s is not None]
        f["returns_to_earlier_code"] = bool(sims) and max(sims) >= NEAR_COPY
    return f


def jev_telemetry(features: dict[str, Any]) -> dict[str, Any]:
    return {k: features[k] for k in JEV_TELEMETRY_KEYS}
