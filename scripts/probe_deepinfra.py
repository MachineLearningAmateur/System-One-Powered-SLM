"""Check that DeepInfra's text-completions endpoint can serve the Qwen3.5-9B worker.

Billed, but tiny: two calls with at most 256 + 128 output tokens on a toy
prompt (no benchmark task). At the listed USD 0.10 / 0.15 per million
input / output tokens, the cost is far below USD 0.001. The script refuses to
call unless --confirm-billed is given.

It checks what Generator (src/system1/loop/generate.py) needs from a backend:
a raw prompt, top_k, seed, a "</think>" stop string, finish_reason and
stop_reason, and top-5 logprobs whose count matches usage.completion_tokens.
It writes the raw replies to a new file under results/probes/ (git-ignored)
and prints a summary. The API key is read from .env (DEEPINFRA_API_KEY) and is
never printed or written.

    uv run python scripts/probe_deepinfra.py --confirm-billed
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

import httpx

from system1.config import RESULTS

URL = "https://api.deepinfra.com/v1/openai/completions"
MODEL = "Qwen/Qwen3.5-9B"
SAMPLING = {"temperature": 0.6, "top_p": 0.95, "top_k": 20}
# The Qwen3.5 chat template opens "<think>\n" itself when thinking is on.
PROMPT = ("<|im_start|>user\nWrite a Python function add(a, b) that returns a + b. "
          "Think briefly.<|im_end|>\n<|im_start|>assistant\n<think>\n")


def call(client: httpx.AsyncClient | httpx.Client, prompt: str, max_tokens: int, seed: int,
         stop: list[str] | None) -> tuple[dict, float]:
    body = {"model": MODEL, "prompt": prompt, "max_tokens": max_tokens, "seed": seed, "logprobs": 5, **SAMPLING}
    if stop:
        body["stop"] = stop
    t0 = time.perf_counter()
    r = client.post(URL, json=body, timeout=300.0)
    ms = round((time.perf_counter() - t0) * 1000, 1)
    if r.status_code != 200:
        print(f"HTTP {r.status_code}: {r.text[:500]}")
        sys.exit(1)
    return r.json(), ms


def summary(d: dict, ms: float) -> dict:
    c = (d.get("choices") or [{}])[0]
    lp = c.get("logprobs") or {}
    top, tok = lp.get("top_logprobs"), lp.get("token_logprobs")
    usage = d.get("usage") or {}
    return {
        "latency_ms": ms, "reply_keys": sorted(d), "model": d.get("model"), "choice_keys": sorted(c),
        "finish_reason": c.get("finish_reason"), "stop_reason": c.get("stop_reason"),
        "logprob_keys": sorted(lp), "n_token_logprobs": None if tok is None else len(tok),
        "n_top_logprobs": None if top is None else len(top),
        "top_k_per_token": sorted({len(t) for t in top if t}) if top else None,
        "usage": usage, "text_head": (c.get("text") or "")[:200], "text_tail": (c.get("text") or "")[-120:],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--confirm-billed", action="store_true", help="make the two billed calls")
    args = ap.parse_args()
    key = os.environ.get("DEEPINFRA_API_KEY", "")
    print(f"DEEPINFRA_API_KEY length: {len(key)}")
    if not key:
        print("Add DEEPINFRA_API_KEY to .env first.")
        sys.exit(1)
    if not args.confirm_billed:
        print("Billed probe (< USD 0.001). Run again with --confirm-billed.")
        sys.exit(1)
    out = RESULTS / "probes" / f"deepinfra-q9b-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(headers={"Authorization": f"Bearer {key}"}) as client:
        d1, ms1 = call(client, PROMPT, 256, 1234, ["</think>"])
        think = d1["choices"][0].get("text", "")
        cap_hit = d1["choices"][0].get("finish_reason") == "length"
        prefix = PROMPT + think + ("\n</think>\n\n" if cap_hit else "</think>\n\n")
        d2, ms2 = call(client, prefix, 128, 1235, None)
    res = {"url": URL, "model": MODEL, "sampling": SAMPLING, "thinking": summary(d1, ms1),
           "answer": summary(d2, ms2), "raw": {"thinking": d1, "answer": d2}}
    out.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(json.dumps({k: res[k] for k in ("thinking", "answer")}, indent=1))
    print(f"raw replies: {out}")


if __name__ == "__main__":
    main()
