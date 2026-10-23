import asyncio
import json

import httpx
import pytest

from system1.eval.ledger import CostLedger
from system1.features.telemetry import JEV_TELEMETRY_KEYS, cheap_features, jev_telemetry, loop_flag, marker_count
from system1.loop.generate import (
    Generator,
    _logprob_parts,
    add_missing_imports,
    confidence_summary,
    extract_code,
    prompt_imports,
    token_confidence,
)
from system1.loop.tasks import (
    KNOWN_BAD_DOCSTRINGS,
    TaskSpec,
    docstring_tests,
    format_test_report,
    load_tasks,
    prompt_assert_tests,
    reference_tests,
    render_test,
    revise_messages,
)

HE_PROMPT = '''from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if any two numbers are closer than threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([], 0.5)
    >>> has_close_elements([1.0], 0.5) == False
    >>> has_close_elements([1.0, 2.0]) [0, 1]
    """
'''


# --- tasks and visible tests -------------------------------------------------

def test_docstring_tests_cover_output_none_comparison_and_invalid_lines():
    tests = docstring_tests(HE_PROMPT, "has_close_elements")
    assert tests == [
        {"kind": "compare", "call": "has_close_elements([1.0, 2.0, 3.0], 0.5)", "expected": "False"},
        {"kind": "compare", "call": "has_close_elements([], 0.5)", "expected": "None"},
        {"kind": "assert", "source": "assert has_close_elements([1.0], 0.5) == False"},  # `== y` line, no output
    ]  # the last line is not valid Python and is skipped


def test_prompt_assert_and_reference_tests():
    assert prompt_assert_tests('"""\nWrite f.\nassert f(1) == 2\n"""\n') == [{"kind": "assert", "source": "assert f(1) == 2"}]
    pairs = [{"args": "[1, 'a']", "output": "[1]"}, {"args": "[float('inf')]", "output": "1"}]
    assert reference_tests("f", pairs) == [{"kind": "compare", "call": "f(1, 'a')", "expected": "[1]"}]


def test_frozen_visible_tests_v2():
    tasks = load_tasks()
    assert len(tasks) == 542 and all(t.visible_tests for t in tasks.values())
    assert all(t.shown_tests for t in tasks.values() if t.visible_source == "base_input")
    assert all(len(t.visible_tests) == 1 for t in tasks.values() if t.benchmark == "mbpp+")
    assert {tid for tid, t in tasks.items() if t.canonical_fails_visible} == KNOWN_BAD_DOCSTRINGS
    for tid in ("HumanEval/108", "HumanEval/128", "HumanEval/145", "HumanEval/156", "HumanEval/162"):
        assert all(x["kind"] == "assert" for x in tasks[tid].visible_tests), tid


def test_report_and_revise_prompt_carry_code_and_output_not_thinking():
    t = ({"kind": "assert", "source": "assert f(1) == 2"},)
    rep = format_test_report(t, [{"status": "fail", "error_type": "AssertionError", "message": "assertion failed"}])
    assert "FAIL" in rep and "0 of 1 visible tests passed" in rep and render_test(t[0]) in rep
    spec = TaskSpec("X/1", "mbpp+", "Write f.", "f", t, "prompt_assert", "")
    msg = revise_messages(spec, "def f(x): return x", rep)[0]["content"]
    assert "def f(x): return x" in msg and rep in msg and "<think>" not in msg


# --- code extraction ---------------------------------------------------------------

def test_extraction_prefers_the_block_that_defines_the_function():
    ans = "```python\ndef f(x):\n    return x\n```\nTests:\n```python\nassert f(1) == 1\n```"
    code, rule, n = extract_code(ans, "f")
    assert code.startswith("def f") and rule == "defines_entry_point" and n == 2
    code, rule, _ = extract_code("```python\ndef g(): pass\n```\n```python\nassert g() is None\n```", "f")
    assert code.startswith("def g") and rule == "any_definition"
    assert extract_code("```python\nx = 1\n```", "f") == ("x = 1\n", "last_block", 1)
    assert extract_code("no code here", "f") == (None, "none", 0)


def test_extraction_accepts_capitalised_and_python3_fences():
    ans = "```Python\ndef f(): return 1\n```\nText\n```python3\ndef f(): return 2\n```"
    assert extract_code(ans, "f")[0] == "def f(): return 2\n"


def test_imports():
    imports = prompt_imports(HE_PROMPT)
    assert imports == ["from typing import List"]
    code, added = add_missing_imports("def has_close_elements(numbers: List[float], t): ...\n", imports)
    assert code.startswith("from typing import List") and added == imports
    assert add_missing_imports("from typing import List\nx = 1\n", imports)[1] == []


def test_confidence_uses_only_the_k_largest():
    assert token_confidence({"a": -0.1, "b": -0.2, "c": -0.3, "d": -0.4, "e": -0.5, "sampled": -9.0}) == pytest.approx(0.3)
    tops = [{"a": -0.1, "b": -2.1}] * 4 + [{"a": -1.0, "b": -3.0}] * 4
    s = confidence_summary(tops, [-0.1] * 8, window=4)
    assert s["n_tokens"] == 8 and s["mean_conf"] == pytest.approx(1.55)
    assert s["lowest_group_conf"] == pytest.approx(1.1) and s["tail_conf"] == pytest.approx(2.0)
    assert confidence_summary([], [])["mean_conf"] is None


def test_local_stop_token_may_be_counted_without_logprobs():
    choice = {"finish_reason": "stop", "logprobs": {
        "token_logprobs": [-0.5], "top_logprobs": [{"x": -0.5}]}}
    usage = {"completion_tokens": 2}
    with pytest.raises(ValueError, match="do not match"):
        _logprob_parts(choice, usage)
    assert _logprob_parts(choice, usage, allow_terminal_token_without_logprob=True) == (
        [{"x": -0.5}], [-0.5])
    choice["finish_reason"] = "length"
    with pytest.raises(ValueError, match="do not match"):
        _logprob_parts(choice, usage, allow_terminal_token_without_logprob=True)


# --- generation ------------------------------------------------------------------

class FakeTokenizer:
    def apply_chat_template(self, messages, **kw):
        assert kw["enable_thinking"] is True
        return "<|user|>" + messages[-1]["content"] + "<|assistant|>"

    def __call__(self, text):
        return {"input_ids": text.split()}


def vllm(responses, seen):
    it = iter(responses)

    def handler(request):
        seen.append(json.loads(request.content))
        text, finish, stop_reason, *bad = next(it)
        n = max(1, len(text.split()))
        n_top = n - 1 if bad else n  # a reply whose logprobs do not match its token count
        body = json.loads(request.content)
        return httpx.Response(200, json={
            "choices": [{"text": text, "finish_reason": finish, "stop_reason": stop_reason,
                         "logprobs": {"token_logprobs": [-0.5] * n, "top_logprobs": [{"x": -0.5, "y": -1.5}] * n_top}}],
            "usage": {"prompt_tokens": len(body["prompt"].split()), "completion_tokens": n}})
    return handler


def generate(responses, think_cap=100, calls=None):
    seen = []

    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(vllm(responses, seen))) as c:
            gen = Generator(c, FakeTokenizer(), url="http://vllm/v1/completions", think_cap=think_cap,
                            code_tokens=50, max_model_len=1000)
            return await gen.generate([{"role": "user", "content": "task"}], HE_PROMPT, "has_close_elements",
                                      "run", "t", 0, 1, on_call=calls.append if calls is not None else None)
    return asyncio.run(go()), seen


SOLUTION = "```python\ndef has_close_elements(n, t):\n    return False\n```"


def test_thinking_closed_normally():
    g, seen = generate([("<think>\nplan the loop", "stop", "</think>"), (SOLUTION, "stop", None)])
    assert len(seen) == 2 and seen[0]["stop"] == ["</think>"] and seen[0]["max_tokens"] == 100
    assert seen[1]["prompt"].endswith("plan the loop</think>\n\n") and seen[1]["max_tokens"] == 50
    assert g.think_closed and not g.cap_hit and g.thinking == "plan the loop"
    assert "def has_close_elements" in g.code and g.imports_added == ["from typing import List"]
    assert g.code_rule == "defines_entry_point" and g.answer_finish == "stop"
    assert [p["phase"] for p in g.phases] == ["thinking", "answer"]


def test_cap_hit_closes_thinking_and_records_it():
    g, seen = generate([("<think>\nwait wait", "length", None), (SOLUTION, "stop", None)])
    assert g.cap_hit and g.think_closed and seen[1]["prompt"].endswith("wait wait\n</think>\n\n")


def test_no_close_gives_no_code_even_if_the_thinking_has_some():
    g, seen = generate([("<think>\nmaybe\n" + SOLUTION, "stop", None)])
    assert len(seen) == 1 and not g.think_closed and g.code is None and g.no_code_reason == "no_close"


def test_answer_without_thinking_is_kept_as_answer():
    g, seen = generate([(SOLUTION, "stop", None)])
    assert len(seen) == 1 and g.thinking_skipped and g.thinking == "" and g.code is not None
    assert g.thinking_tokens == 0 and g.answer_tokens > 0
    assert g.phases[0]["reasoning_tokens"] == 0  # the ledger does not count a direct answer as reasoning


def test_cut_answer_is_recorded():
    g, _ = generate([("<think>\nok", "stop", "</think>"), ("```python\ndef has_close_elements(", "length", None)])
    assert g.code is None and g.no_code_reason == "answer_cut" and g.answer_finish == "length"


def test_every_http_call_is_reported_with_its_usage():
    calls = []
    generate([("<think>\nplan the loop", "stop", "</think>"), (SOLUTION, "stop", None)], calls=calls)
    assert [(c["phase"], c["status"]) for c in calls] == [("thinking", "ok"), ("answer", "ok")]
    assert calls[0]["input_tokens"] == 1 and calls[0]["output_tokens"] == 4  # from the reply's usage
    assert calls[0]["reasoning_tokens"] == 4 and calls[1]["reasoning_tokens"] == 0


def test_logprobs_that_do_not_match_the_tokens_are_an_error_and_still_reported():
    calls = []
    with pytest.raises(ValueError, match="logprobs do not match"):
        generate([("<think>\nplan", "stop", "</think>"), (SOLUTION, "stop", None, "bad")], calls=calls)
    assert [(c["phase"], c["status"]) for c in calls] == [("thinking", "ok"), ("answer", "error:ValueError")]
    assert calls[1]["output_tokens"] is not None  # the work is counted although the reply is rejected


def test_cap_shrinks_for_long_prompts():
    async def go():
        async with httpx.AsyncClient(transport=httpx.MockTransport(vllm([], []))) as c:
            gen = Generator(c, FakeTokenizer(), think_cap=100, code_tokens=50, max_model_len=60)
            return await gen.generate([{"role": "user", "content": "word " * 20}], "", "f", "r", "t", 0, 1)
    with pytest.raises(ValueError):
        asyncio.run(go())


# --- telemetry -------------------------------------------------------------------

def rnd(code, statuses, thinking="plan", tokens=10):
    return {"code": code, "results": [{"status": s, "error_type": None if s == "pass" else "AssertionError"}
                                      for s in statuses],
            "thinking": thinking, "thinking_tokens": tokens, "cap_hit": False, "think_closed": True,
            "confidence": {"thinking": {"n_tokens": 3, "mean_conf": 1.2}, "answer": {"n_tokens": 1, "mean_conf": 0.9}}}


A = "def f(x):\n    return 0\n"
B = "def f(x):\n    if x > 3:\n        return sorted([x, x + 1, x * 2])\n    raise ValueError('no')\n"


def test_cheap_features_across_rounds():
    r1, r2, r3 = rnd(A, ["fail", "pass"]), rnd(B, ["fail", "pass"], thinking="\n\nWait, maybe.\n\nAlternatively x"), \
        rnd(A, ["pass", "pass"])
    f1 = cheap_features([r1])
    assert f1["pass_count_delta"] is None and f1["visible_pass"] is False and f1["thinking_mean_conf"] == 1.2
    f2 = cheap_features([r1, r2])
    assert f2["pass_count_delta"] == 0 and f2["similarity_to_previous"] < 0.95
    assert f2["same_error_as_previous"] and f2["same_failing_tests_as_previous"] and f2["marker_count"] == 2
    assert f2["returns_to_earlier_code"] is False  # nothing before the previous round
    f3 = cheap_features([r1, r2, r3])
    assert f3["visible_pass"] and f3["pass_count_delta"] == 1
    assert f3["returns_to_earlier_code"] is True  # r3 is r1 again, and differs from r2
    assert f3["similarity_to_previous"] < 0.95


def test_jev_telemetry_has_no_trace_statistics():
    f = cheap_features([rnd("a", ["pass"]), rnd("b", ["fail"])])
    t = jev_telemetry(f)
    assert set(t) == set(JEV_TELEMETRY_KEYS)
    assert not any(k.startswith(("thinking", "answer", "marker", "loop", "cap", "think")) for k in t)


def test_marker_and_loop_flag():
    assert marker_count("Plan.\n\nWait, no.\n\nHmm ok") == 2
    assert loop_flag(" ".join(["a b c d e f g h"] * 7)) and not loop_flag("one two three")


