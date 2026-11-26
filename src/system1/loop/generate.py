"""Small-model generation through vLLM with an explicit thinking cap.

Two phases on the plain completions endpoint, with the chat template rendered
here so the token limits are exact:
  1. thinking: up to the cap, stopped at "</think>";
  2. answer: "</think>" is closed (also after a cap hit) and the code follows.
`--max-model-len` alone would not cap the thinking. Cap hits and a missing
"</think>" are recorded, never hidden.

Logprobs: the top-5 alternatives per token give DeepConf-style confidence
summaries (token confidence = minus the mean of the top-k logprobs). A reply
whose logprobs do not match its token count is an error, never filled in.

Every HTTP call is reported through `on_call` as soon as it ends (also when it
fails), so the cost ledger keeps calls whose checkpoint never finishes.

Qwen3.5: its chat template opens a <think> block itself (Qwen3 did not), so
the reply starts inside the thinking. The rendered prompt tells which case applies.
A hosted backend (DeepInfra) can ask for retries of transient HTTP errors; each
try is a separate ledger call.

DeepInfra (checked 2026-11-26) differs from vLLM in two ways. (1) Its replies
have no stop_reason field. The last entry of logprobs.tokens then tells the
cause: "</think>" is the stop string, "<|im_end|>" or "<|endoftext|>" is the
end of the reply. Any other last token is an error, never a guess. (2) It
returns at most the top-1 alternative per token (plus the sampled token), for
any requested count. The DeepInfra backend therefore asks for 1 and uses top-1
confidence (conf_k=1); the top-5 DeepConf values of the vLLM studies do not
exist for it.
"""

from __future__ import annotations

import asyncio
import hashlib
import math
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable

import httpx
import numpy as np

from system1.config import ROOT

MODEL = "Qwen/Qwen3.5-9B"
REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"  # tokenizer and template; DeepInfra does not pin weights
VLLM_URL = "http://localhost:8000/v1/completions"
DEEPINFRA_URL = "https://api.deepinfra.com/v1/openai/completions"
RETRY_STATUS = {408, 429, 500, 502, 503, 504}
END_TOKENS = {"<|im_end|>", "<|endoftext|>"}  # the reply ended by itself (no stop string)
MAX_MODEL_LEN = 16_384
THINK_CAP = 8_192
CODE_TOKENS = 2_048
TOP_LOGPROBS = 5
CONF_WINDOW = 1_024
# Qwen's recommended thinking-mode sampling (no greedy decoding).
SAMPLING = {"temperature": 0.6, "top_p": 0.95, "top_k": 20}
# Seeds come from (SEED_TAG, task, attempt, round), not from the run id. The
# same seed does NOT reproduce a trajectory: vLLM batching changes the bf16
# numerics, and in the pilot the 8K and 12K runs diverged after 78-1,766
# characters of thinking (33 of 33 tasks). Two runs are paired by task and
# attempt index only; replay always uses the logged trajectories.
SEED_TAG = "s1-seed-v1"


def load_tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(MODEL, revision=REVISION, cache_dir=ROOT / "hf_cache" / "hub",
                                         local_files_only=True)


def render_prompt(tokenizer, messages: list[dict]) -> str:
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)


def template_opens_think(prompt: str) -> bool:
    """True when the rendered prompt itself ends inside an open <think> block (Qwen3.5)."""
    return prompt.rstrip().endswith("<think>")


def request_seed(*parts: Any) -> int:
    return int(hashlib.sha256(":".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def token_confidence(top: dict[str, float], k: int = TOP_LOGPROBS) -> float:
    """DeepConf token confidence: minus the mean of the k largest logprobs. vLLM can add the
    sampled token as an extra entry when it is outside the top k, so only the k largest count."""
    if not top:
        return 0.0
    return -float(np.mean(sorted(top.values(), reverse=True)[:k]))


def infer_stop_reason(choice: dict) -> str | None:
    """stop_reason for a backend that omits it, from the last returned token (see the module text)."""
    tokens = (choice.get("logprobs") or {}).get("tokens") or []
    last = tokens[-1] if tokens else None
    if last == "</think>":
        return "</think>"
    if last in END_TOKENS:
        return None
    raise ValueError(f"cannot tell why the reply stopped: last token {last!r}")


def confidence_summary(top_logprobs: list[dict[str, float]], token_logprobs: list[float],
                       window: int = CONF_WINDOW, k: int = TOP_LOGPROBS) -> dict[str, float | int | None]:
    """Prespecified summaries; None when there are no tokens."""
    n = len(token_logprobs)
    if n == 0:
        return {"n_tokens": 0, "mean_logprob": None, "mean_conf": None, "tail_conf": None,
                "lowest_group_conf": None, "bottom10_group_conf": None}
    conf = np.array([token_confidence(t, k) for t in top_logprobs], dtype=float)
    lp = np.array(token_logprobs, dtype=float)
    w = min(window, n)
    groups = np.convolve(conf, np.ones(w) / w, mode="valid")  # sliding-window mean confidence
    k = max(1, math.ceil(0.1 * len(groups)))
    return {
        "n_tokens": n,
        "mean_logprob": round(float(lp.mean()), 4),
        "mean_conf": round(float(conf.mean()), 4),
        "tail_conf": round(float(conf[-w:].mean()), 4),
        "lowest_group_conf": round(float(groups.min()), 4),
        "bottom10_group_conf": round(float(np.sort(groups)[:k].mean()), 4),
    }


CODE_BLOCK = re.compile(r"```[ \t]*(?:python3?|py)?[ \t]*\r?\n(.*?)```", re.S | re.I)


def extract_code(answer: str, entry_point: str | None = None) -> tuple[str | None, str, int]:
    """(code, rule, number of blocks). Models often add a test block after the
    solution, so the preference is: the last block that defines the entry point,
    then the last block with any definition, then the last block."""
    blocks = [b.strip() for b in CODE_BLOCK.findall(answer) if b.strip()]
    if not blocks:
        return None, "none", 0
    if entry_point:
        defining = [b for b in blocks if re.search(rf"^\s*(async\s+)?def\s+{re.escape(entry_point)}\s*\(", b, re.M)]
        if defining:
            return defining[-1] + "\n", "defines_entry_point", len(blocks)
    with_def = [b for b in blocks if re.search(r"^\s*(def|class)\s", b, re.M)]
    if with_def:
        return with_def[-1] + "\n", "any_definition", len(blocks)
    return blocks[-1] + "\n", "last_block", len(blocks)


def prompt_imports(task_prompt: str) -> list[str]:
    """Import lines the task stub gives before its first definition (HumanEval stubs)."""
    out = []
    for line in task_prompt.splitlines():
        if line.startswith(("def ", "class ")):
            break
        if line.startswith(("import ", "from ")):
            out.append(line.rstrip())
    return out


def add_missing_imports(code: str, imports: list[str]) -> tuple[str, list[str]]:
    """Prepend stub imports the code does not repeat (e.g. `from typing import List`)."""
    missing = [i for i in imports if i not in code]
    return ("\n".join(missing) + "\n\n" + code if missing else code), missing


@dataclass
class Generation:
    prompt_sha256: str
    prompt_tokens: int
    thinking: str
    answer: str
    code: str | None
    imports_added: list[str]
    thinking_tokens: int
    answer_tokens: int
    effective_cap: int
    cap_hit: bool
    think_closed: bool
    latency_ms: float
    seed: int
    confidence: dict[str, dict] = field(default_factory=dict)  # "thinking" / "answer" summaries
    arrays: dict[str, np.ndarray] = field(default_factory=dict)  # per-token logprob and confidence
    thinking_skipped: bool = False  # the model answered without any <think> block
    no_code_reason: str | None = None  # no_close | no_block | answer_cut | None
    code_rule: str = "none"  # which extraction rule picked the code
    n_code_blocks: int = 0
    phase1_finish: str | None = None  # finish_reason / stop_reason of the thinking phase
    answer_finish: str | None = None
    phases: list[dict] = field(default_factory=list)  # per HTTP call, for the cost ledger


def _finite(x: Any) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)


def _logprob_parts(choice: dict, usage: dict | None, *,
                   allow_terminal_token_without_logprob: bool = False) -> tuple[list[dict], list[float]]:
    """Return finite logprobs, allowing a local backend's counted stop token if requested."""
    lp = choice.get("logprobs") or {}
    top, tok = lp.get("top_logprobs"), lp.get("token_logprobs")
    n = (usage or {}).get("completion_tokens")
    terminal_token_counted = (allow_terminal_token_without_logprob
                              and choice.get("finish_reason") == "stop"
                              and isinstance(n, int) and not isinstance(n, bool)
                              and tok is not None and n == len(tok) + 1)
    if top is None or tok is None or len(top) != len(tok) or n is None or not (len(tok) == n or terminal_token_counted):
        raise ValueError(f"logprobs do not match the token count: top {None if top is None else len(top)}, "
                         f"tokens {None if tok is None else len(tok)}, usage {n}")
    for x, t in zip(tok, top):
        if not _finite(x) or not t or not all(_finite(v) for v in t.values()):
            raise ValueError("missing or non-finite logprob in the reply")
    return top, tok


CallHook = Callable[[dict], None]


class Generator:
    def __init__(self, client: httpx.AsyncClient, tokenizer, url: str = VLLM_URL, think_cap: int = THINK_CAP,
                 code_tokens: int = CODE_TOKENS, max_model_len: int = MAX_MODEL_LEN,
                 allow_terminal_token_without_logprob: bool = False, max_retries: int = 0,
                 retry_base_s: float = 2.0, top_logprobs: int = TOP_LOGPROBS,
                 infer_missing_stop_reason: bool = False):
        self.client = client
        self.tokenizer = tokenizer
        self.url = url
        self.think_cap = think_cap
        self.code_tokens = code_tokens
        self.max_model_len = max_model_len
        self.allow_terminal_token_without_logprob = allow_terminal_token_without_logprob
        self.max_retries = max_retries
        self.retry_base_s = retry_base_s
        self.tokens_used = {"input": 0, "output": 0}  # all replies with usage, for a billed backend's guard
        self.top_logprobs = top_logprobs  # requested alternatives per token, and the confidence k
        self.infer_missing_stop_reason = infer_missing_stop_reason

    async def _complete(self, prompt: str, max_tokens: int, seed: int, stop: list[str] | None,
                        phase: str, on_call: CallHook | None,
                        opened: bool = False) -> tuple[dict, list[dict], list[float]]:
        """One call, with up to max_retries more tries after a transient HTTP error."""
        for n in range(self.max_retries + 1):
            try:
                return await self._complete_once(prompt, max_tokens, seed, stop, phase, on_call, opened)
            except (httpx.HTTPStatusError, httpx.TransportError) as e:
                status = e.response.status_code if isinstance(e, httpx.HTTPStatusError) else None
                if n == self.max_retries or (status is not None and status not in RETRY_STATUS):
                    raise
                await asyncio.sleep(self.retry_base_s * 2 ** n)
        raise AssertionError("unreachable")

    async def _complete_once(self, prompt: str, max_tokens: int, seed: int, stop: list[str] | None,
                             phase: str, on_call: CallHook | None,
                             opened: bool) -> tuple[dict, list[dict], list[float]]:
        """One HTTP call. It is reported to on_call when it ends, before any later step."""
        body = {"model": MODEL, "prompt": prompt, "max_tokens": max_tokens, "seed": seed,
                "logprobs": self.top_logprobs, **SAMPLING}
        if stop:
            body["stop"] = stop
        t0 = time.perf_counter()
        call = {"phase": phase, "input_tokens": None, "output_tokens": None, "reasoning_tokens": None,
                "status": "ok"}
        try:
            r = await self.client.post(self.url, json=body, timeout=1800.0)
            r.raise_for_status()
            d = r.json()
            usage = d.get("usage") or {}
            call["input_tokens"], call["output_tokens"] = usage.get("prompt_tokens"), usage.get("completion_tokens")
            for k, v in (("input", call["input_tokens"]), ("output", call["output_tokens"])):
                if isinstance(v, int) and not isinstance(v, bool):
                    self.tokens_used[k] += v
            c = d["choices"][0]
            # Same rule as generate(): phase-1 text without <think> (and no cap hit) is a direct answer.
            is_thinking = phase == "thinking" and (opened or c.get("text", "").lstrip().startswith("<think>")
                                                   or c.get("finish_reason") == "length")
            call["reasoning_tokens"] = call["output_tokens"] if is_thinking else 0
            top, tok = _logprob_parts(c, usage, allow_terminal_token_without_logprob=
                                      self.allow_terminal_token_without_logprob)
            if any(len(t) > self.top_logprobs + 1 for t in top):
                raise ValueError("the reply has more logprob alternatives than requested")
            if self.infer_missing_stop_reason and c.get("finish_reason") == "stop" and "stop_reason" not in c:
                c["stop_reason"] = infer_stop_reason(c)
                c["stop_reason_inferred"] = True
            return d, top, tok
        except httpx.HTTPStatusError as e:
            call["status"] = f"http:{e.response.status_code}"
            raise
        except BaseException as e:  # also cancellation (Ctrl+C): never logged as "ok"
            call["status"] = "cancelled" if isinstance(e, asyncio.CancelledError) else f"error:{type(e).__name__}"
            raise
        finally:
            call["latency_ms"] = round((time.perf_counter() - t0) * 1000, 1)
            if on_call is not None:
                on_call(call)

    async def generate(self, messages: list[dict], task_prompt: str, entry_point: str | None,
                       *seed_parts: Any, on_call: CallHook | None = None) -> Generation:
        prompt = render_prompt(self.tokenizer, messages)
        n_prompt = len(self.tokenizer(prompt)["input_ids"])
        cap = min(self.think_cap, self.max_model_len - n_prompt - self.code_tokens - 16)
        if cap <= 0:
            raise ValueError(f"prompt of {n_prompt} tokens leaves no room for thinking")
        seed = request_seed(*seed_parts)
        opened = template_opens_think(prompt)
        t0 = time.perf_counter()
        phases: list[dict] = []

        def hook(call: dict) -> None:
            phases.append(call)
            if on_call is not None:
                on_call(call)

        d1, top1, lp1 = await self._complete(prompt, cap, seed, ["</think>"], "thinking", hook, opened)
        c1 = d1["choices"][0]
        think_text = c1["text"]
        finish1 = c1.get("finish_reason")
        if finish1 == "stop" and "stop_reason" not in c1:
            raise ValueError("the backend reply has no stop_reason: '</think>' and the end of the reply "
                             "cannot be told apart")
        cap_hit = finish1 == "length"
        stopped_on_close = finish1 == "stop" and c1.get("stop_reason") == "</think>"
        # Qwen3's template opens no <think> block, so its text that does not start with
        # one is a direct answer without thinking. Qwen3.5's template opens the block.
        skipped = not opened and not think_text.lstrip().startswith("<think>")

        answer, top2, lp2, answer_finish, think_closed = "", [], [], None, False
        if skipped and not cap_hit:
            answer, think_text, top2, lp2, top1, lp1 = think_text, "", top1, lp1, [], []
            answer_finish = finish1
        elif cap_hit or stopped_on_close:
            prefix = prompt + think_text + ("\n</think>\n\n" if cap_hit else "</think>\n\n")
            d2, top2, lp2 = await self._complete(prefix, self.code_tokens, seed + 1, None, "answer", hook, False)
            c2 = d2["choices"][0]
            answer = c2["text"]
            answer_finish = c2.get("finish_reason")
            think_closed = True

        latency_ms = (time.perf_counter() - t0) * 1000
        thinking = think_text.replace("<think>", "", 1).strip()
        code, rule, n_blocks = extract_code(answer, entry_point)
        no_code_reason = None
        if code is None:
            if not (think_closed or skipped):
                no_code_reason = "no_close"  # ended inside its thinking: no code is taken from it
            elif answer_finish == "length":
                no_code_reason = "answer_cut"
            else:
                no_code_reason = "no_block"
        added: list[str] = []
        if code is not None:
            code, added = add_missing_imports(code, prompt_imports(task_prompt))

        k = self.top_logprobs
        conf1, conf2 = (np.array([token_confidence(t, k) for t in tp], dtype=np.float16) for tp in (top1, top2))
        return Generation(
            prompt_sha256=hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            prompt_tokens=n_prompt, thinking=thinking, answer=answer, code=code, imports_added=added,
            thinking_tokens=len(lp1), answer_tokens=len(lp2), effective_cap=cap, cap_hit=cap_hit,
            think_closed=think_closed, latency_ms=latency_ms, seed=seed,
            confidence={"thinking": confidence_summary(top1, lp1, k=k), "answer": confidence_summary(top2, lp2, k=k)},
            arrays={"thinking_logprob": np.array(lp1, dtype=np.float16),
                    "thinking_conf": conf1,
                    "answer_logprob": np.array(lp2, dtype=np.float16),
                    "answer_conf": conf2},
            thinking_skipped=skipped and not cap_hit, no_code_reason=no_code_reason, code_rule=rule,
            n_code_blocks=n_blocks, phase1_finish=f"{finish1}:{c1.get('stop_reason')}", answer_finish=answer_finish,
            phases=phases,
        )
