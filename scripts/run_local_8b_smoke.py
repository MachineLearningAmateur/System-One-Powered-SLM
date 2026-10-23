"""Run one development attempt through Docker Model Runner's llama.cpp Metal backend.

This is an exploratory smoke run, not the frozen vLLM protocol. It uses the
study's prompts, generation limits, visible sandbox and durable checkpoint
format. It never generates a test task or invokes hidden grading or Jev.

    uv run python scripts/run_local_8b_smoke.py --run-id q8b-local-smoke-1
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import subprocess
from datetime import datetime, timezone

import httpx

from system1.config import RESULTS
from system1.eval.ledger import CostLedger
from system1.eval.split import SPLIT_PATH, file_sha256, load_split
from system1.loop.generate import (CODE_TOKENS, MAX_MODEL_LEN, MODEL, REVISION,
                                   SAMPLING, THINK_CAP, TOP_LOGPROBS, Generator,
                                   load_tokenizer)
from system1.loop.runner import MAX_ROUNDS, RunContext, run_attempt
from system1.loop.sandbox import VisibleRunner
from system1.loop.tasks import VISIBLE_TESTS_PATH, load_tasks

DMR_MODEL = "huggingface.co/ggml-org/qwen3-8b-gguf:BF16"
DMR_BASE = "http://localhost:12434/engines/v1"


class DMRClient:
    """Translate Docker's OpenAI logprob layout into the vLLM layout."""

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def post(self, url: str, json: dict, timeout: float) -> httpx.Response:
        request = {**json, "model": DMR_MODEL}
        response = await self.client.post(url, json=request, timeout=timeout)
        if response.is_error:
            return response
        data = response.json()
        choice = data["choices"][0]
        content = choice["logprobs"]["content"]
        choice["logprobs"] = {
            "token_logprobs": [entry["logprob"] for entry in content],
            "top_logprobs": [
                {candidate["token"]: candidate["logprob"]
                 for candidate in entry["top_logprobs"]}
                for entry in content
            ],
        }
        # Docker omits stop_reason. A stop response in the thinking phase is
        # treated as the requested </think> stop, as in the vLLM response.
        # This assumption is recorded in the non-protocol run metadata.
        if request.get("stop") and choice.get("finish_reason") == "stop":
            choice["stop_reason"] = request["stop"][0]
        return httpx.Response(response.status_code, json=data, request=response.request)


async def main(args: argparse.Namespace) -> int:
    split = load_split()
    tasks = load_tasks()
    dev_ids = [task_id for bench in ("humaneval+", "mbpp+")
               for task_id in split["benchmarks"][bench]["dev"]]
    task_id = args.task_id or dev_ids[0]
    if task_id not in dev_ids:
        raise SystemExit(f"{task_id} is not a development task")

    output = RESULTS / "runs" / args.run_id
    if output.exists():
        raise SystemExit(f"run directory already exists: {output}")
    tokenizer = load_tokenizer()
    visible = VisibleRunner(max_concurrent=1)
    async with httpx.AsyncClient() as raw_client:
        models = (await raw_client.get(f"{DMR_BASE}/models", timeout=30.0)).json()["data"]
        if DMR_MODEL not in {item["id"] for item in models}:
            raise SystemExit(f"Docker Model Runner does not list {DMR_MODEL}")
        inspected = subprocess.run(["docker", "model", "inspect", DMR_MODEL],
                                   check=True, capture_output=True, text=True)
        model_id = json.loads(inspected.stdout)["id"]
        commit = subprocess.run(["git", "rev-parse", "HEAD"], check=True,
                                capture_output=True, text=True).stdout.strip()
        dirty = bool(subprocess.run(["git", "status", "--porcelain"], check=True,
                                    capture_output=True, text=True).stdout.strip())
        output.mkdir(parents=True)
        metadata = {
            "run_id": args.run_id, "split": "dev", "non_protocol": True,
            "status": "running", "started": datetime.now(timezone.utc).isoformat(),
            "reason": "llama.cpp Metal backend; GGUF checkpoint and stop semantics differ from vLLM",
            "backend": "docker-model-runner/llama.cpp-metal", "backend_model": DMR_MODEL,
            "backend_model_id": model_id, "stop_reason_inferred": True,
            "terminal_token_without_logprob_allowed": True,
            "study_model": MODEL, "study_revision": REVISION,
            "sampling": SAMPLING, "thinking_cap": THINK_CAP,
            "answer_cap": CODE_TOKENS, "max_model_len": MAX_MODEL_LEN,
            "top_logprobs": TOP_LOGPROBS, "max_rounds": MAX_ROUNDS,
            "chat_template_sha256": hashlib.sha256(tokenizer.chat_template.encode()).hexdigest(),
            "split_sha256": file_sha256(SPLIT_PATH),
            "visible_tests_sha256": file_sha256(VISIBLE_TESTS_PATH),
            "git_commit": commit, "git_dirty": dirty,
            "task_id": task_id, "attempt": args.attempt, **visible.protocol(),
        }
        meta_path = output / "run_meta.json"
        meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
        ctx = RunContext(
            run_id=args.run_id, split="dev",
            generator=Generator(DMRClient(raw_client), tokenizer,
                                url=f"{DMR_BASE}/completions",
                                allow_terminal_token_without_logprob=True),
            visible=visible,
            store=CostLedger(output / "trajectories.jsonl"),
            ledger=CostLedger(output / "ledger.jsonl"),
            failures=CostLedger(output / "failures.jsonl"),
            logprob_dir=output / "logprobs",
            provider="local-llamacpp-metal",
        )
        try:
            records = await run_attempt(ctx, tasks[task_id], args.attempt)
        except BaseException as exc:
            metadata.update(status="failed", error=f"{type(exc).__name__}: {exc}")
            raise
        else:
            metadata.update(status="completed", n_checkpoints=len(records),
                            visible_pass=records[-1]["visible_pass"])
            print(f"{task_id} attempt {args.attempt}: {len(records)} rounds; "
                  f"visible pass: {records[-1]['visible_pass']}")
            print(f"thinking tokens by round: "
                  f"{[record['generation']['thinking_tokens'] for record in records]}")
        finally:
            metadata["ended"] = datetime.now(timezone.utc).isoformat()
            meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--task-id", default="", help="development task ID; default: first HumanEval+ dev task")
    parser.add_argument("--attempt", type=int, default=0)
    raise SystemExit(asyncio.run(main(parser.parse_args())))
