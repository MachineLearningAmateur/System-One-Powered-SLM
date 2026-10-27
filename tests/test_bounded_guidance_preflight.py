"""Offline checks for the proposed single-call planner preflight."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from system1.bounded_guidance import InvalidPlan, PLAN_MAX_CHARS, PLAN_MAX_WORDS, validate_plan
from system1.config import RESULTS
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import preflight_bounded_guidance_planner as preflight


def test_prompt_change_preserves_checkpoint_and_frozen_acceptance():
    source = {"messages": [{"role": "user", "content":
              "Old 120-word instructions.\n\nTask and visible examples:\nTask\nFirst draft: X\nVisible-test result: Y"}],
              "max_tokens": 512}
    amended = preflight.replace_instructions(source)
    assert amended is not source
    assert source["messages"][0]["content"].startswith("Old 120-word")
    assert amended["messages"][0]["content"].endswith(
        "Task and visible examples:\nTask\nFirst draft: X\nVisible-test result: Y")
    assert "100 whitespace-separated words and 900 characters" in amended["messages"][0]["content"]
    assert "no backticks, code fences" in amended["messages"][0]["content"]
    assert "If no clear defect is evident, say so" in amended["messages"][0]["content"]
    assert "do not invent a defect or change" in amended["messages"][0]["content"]
    assert amended["max_tokens"] == 512
    assert (PLAN_MAX_WORDS, PLAN_MAX_CHARS) == (120, 900)
    with pytest.raises(InvalidPlan, match="fixed bound"):
        validate_plan("word " * 121)
    with pytest.raises(InvalidPlan, match="code fence"):
        validate_plan("Use a ```python block")


def test_pinned_saved_response_and_request_are_replayable_offline():
    run = RESULTS / "runs" / preflight.SOURCE_RUN_ID
    if not (run / "frontier_exchanges.jsonl").exists():
        pytest.skip("operator's ignored run artifact is not available in this checkout")
    original = preflight.source_request()
    amended = preflight.preflight_request()
    assert amended["messages"][0]["content"].split(preflight.ANCHOR, 1)[1] == (
        original["messages"][0]["content"].split(preflight.ANCHOR, 1)[1])
    assert amended["model"] == original["model"]
    assert amended["max_tokens"] == original["max_tokens"]
    assert preflight.reservation_usd(amended) < preflight.PREFLIGHT_MAX_USD
    exchange = json.loads((run / "frontier_exchanges.jsonl").read_text().splitlines()[0])
    choice = exchange["response_body"]["choices"][0]
    content = choice["message"]["content"]
    assert choice["finish_reason"] == "stop"
    assert len(content.strip()) == 785
    assert len(content.strip().split()) == 142
    assert "```" in content
    with pytest.raises(InvalidPlan, match="fixed bound"):
        validate_plan(content)


@pytest.mark.parametrize("content,finish,expected_failed", [
    ("No clear defect is evident. Check edge cases before changing the draft.", "stop", []),
    ("word " * 121 + "```python", "stop", ["at_most_120_words", "no_code_fence"]),
    ("x" * 901, "stop", ["at_most_900_characters"]),
    ("", "stop", ["nonempty_visible_text"]),
    ("Check one edge case.", "length", ["finish_reason_stop"]),
])
def test_every_acceptance_rule_is_recorded_without_editing_text(content, finish, expected_failed):
    reply = SimpleNamespace(content=content, finish_reason=finish, call_id="local-only",
                            model_returned="mock", provider_returned="mock",
                            input_tokens=2, output_tokens=3,
                            usd_reported=0.0, usd_computed=0.0)
    result = preflight.assess_reply(reply, {"reasoning_tokens": 0})
    assert result["visible_content"] == content
    assert result["validation_reasons"] == expected_failed
    assert result["delivery_status"] == ("invalid" if expected_failed else "delivered")
    assert all(result["validation_rules"][name] is False for name in expected_failed)


def test_offline_prepare_never_calls_adviser(monkeypatch, tmp_path):
    if not (RESULTS / "runs" / preflight.SOURCE_RUN_ID / "frontier_exchanges.jsonl").exists():
        pytest.skip("operator's ignored run artifact is not available in this checkout")

    class ForbiddenAdviser:
        def __init__(self, *args, **kwargs):
            raise AssertionError("offline preparation must not construct an API client")

    monkeypatch.setattr(preflight, "BoundedAdviser", ForbiddenAdviser)
    target = tmp_path / "prepared.json"
    monkeypatch.setattr(sys, "argv", ["preflight", "--prepare", "--output", str(target)])
    preflight.main()
    prepared = json.loads(target.read_text())
    assert prepared["reserved_usd_at_current_pinned_prices"] < 0.03
    assert prepared["delivery_max_words"] == 120
    assert prepared["delivery_max_chars"] == 900


def test_real_mode_requires_separate_approval_before_creating_run(monkeypatch, tmp_path, capsys):
    if not (RESULTS / "runs" / preflight.SOURCE_RUN_ID / "frontier_exchanges.jsonl").exists():
        pytest.skip("operator's ignored run artifact is not available in this checkout")
    run_id = f"forbidden-{tmp_path.name}"
    monkeypatch.setattr(sys, "argv", ["preflight", "--real", "--run-id", run_id,
                                      "--max-requests", "1", "--limit-usd", "0.03"])
    with pytest.raises(SystemExit) as error:
        preflight.main()
    assert error.value.code == 2
    assert "separate approval" in capsys.readouterr().err
    assert not (RESULTS / "runs" / run_id).exists()
