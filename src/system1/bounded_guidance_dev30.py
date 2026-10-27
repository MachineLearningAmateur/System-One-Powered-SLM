"""Label-independent selection and immutable settings for the 30-task dev pilot."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from system1.bounded_guidance import (DEV30_PLANNER_INSTRUCTIONS, PLAN_MAX_CHARS,
                                      PLAN_MAX_OUTPUT_TOKENS, PLAN_MAX_WORDS)
from system1.config import ROOT
from system1.eval.exclusions import EXCLUSIONS_PATH, load_exclusions
from system1.eval.split import SPLIT_PATH, load_split
from system1.frontier.client import MODEL as FRONTIER_MODEL, PROVIDER, REASONING
from system1.loop.generate import (CODE_TOKENS, MAX_MODEL_LEN, MODEL as WORKER_MODEL,
                                   REVISION, SAMPLING, THINK_CAP, TOP_LOGPROBS)
from system1.loop.tasks import VISIBLE_TESTS_PATH, load_tasks

MANIFEST_PATH = ROOT / "configs" / "bounded_guidance_dev30_v1.json"
SELECTION_SALT = "bounded-guidance-dev30-v1"
DEBUG_TASKS = ("HumanEval/2", "HumanEval/4", "HumanEval/5", "HumanEval/59",
               "Mbpp/2", "Mbpp/4")
QUOTAS = {"humaneval+": 9, "mbpp+": 21}
MAX_PAIRS = 30
MAX_WORKER_HTTP = 180
MAX_FRONTIER_REQUESTS = 30
MAX_WALL_SECONDS = 5400
WATCHDOG_SECONDS = 7200
FRONTIER_LIMIT_USD = 0.60
TOTAL_CEILING_USD = 10.00
GPU_RATE_USD_PER_HOUR = 3.2004
MAX_CONSECUTIVE_INVALID = 3
AZURE_SUBSCRIPTION_ID = "a1c817da-8cb1-4f20-bc7a-bca1b22e1a9b"
AZURE_RESOURCE_GROUP = "rg-bg-dev30-20261027"
AZURE_APP_NAME = "bg-dev30-vllm-1027"
AZURE_ENV_NAME = "bg-dev30-env-1027"
VLLM_IMAGE = ("docker.io/vllm/vllm-openai:v0.30.0@"
              "sha256:5f5e535216848d0c52159c8c13a0af04be5f6fe1a84e79914300610796f76d40")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def select_tasks() -> list[str]:
    """Hash only frozen development IDs; never read runs, labels, or grades."""
    split, excluded, tasks = load_split(), load_exclusions()["tasks"], load_tasks()
    selected: list[str] = []
    for benchmark, count in QUOTAS.items():
        pool = [tid for tid in split["benchmarks"][benchmark]["dev"]
                if tid in tasks and tid not in excluded and tid not in DEBUG_TASKS]
        pool.sort(key=lambda tid: (hashlib.sha256(f"{SELECTION_SALT}:{tid}".encode()).hexdigest(), tid))
        if len(pool) < count:
            raise ValueError(f"insufficient eligible development tasks for {benchmark}")
        selected.extend(pool[:count])
    if len(selected) != MAX_PAIRS or len(set(selected)) != MAX_PAIRS:
        raise ValueError("development selection is not 30 distinct tasks")
    return selected


def expected_manifest() -> dict:
    return {
        "version": "bounded-guidance-dev30-v1",
        "purpose": "fixed 30-task development pilot; paired intention-to-treat",
        "split": "dev",
        "selection_salt": SELECTION_SALT,
        "benchmarks": QUOTAS,
        "excluded_integration_debug_tasks": list(DEBUG_TASKS),
        "source_sha256": {
            "split_v1": sha256_file(SPLIT_PATH),
            "grading_exclusions_v1": sha256_file(EXCLUSIONS_PATH),
            "visible_tests_v2": sha256_file(VISIBLE_TESTS_PATH),
        },
        "tasks": select_tasks(),
        "protocol": {
            "shared_drafts_per_task": 1,
            "control_continuations_per_task": 1,
            "guided_continuations_per_task": 1,
            "fresh_plans_per_task": 1,
            "planner_prompt": "successful-planner-preflight-v1b-20261027",
            "planner_instruction_sha256": hashlib.sha256(DEV30_PLANNER_INSTRUCTIONS.encode()).hexdigest(),
            "plan_max_words": PLAN_MAX_WORDS,
            "plan_max_unicode_chars": PLAN_MAX_CHARS,
            "plan_max_completion_tokens_including_reasoning": PLAN_MAX_OUTPUT_TOKENS,
            "planner_model": FRONTIER_MODEL,
            "planner_provider": PROVIDER,
            "planner_reasoning": REASONING,
            "worker_model": WORKER_MODEL,
            "worker_revision": REVISION,
            "worker_sampling": SAMPLING,
            "worker_think_cap": THINK_CAP,
            "worker_answer_cap": CODE_TOKENS,
            "worker_max_model_len": MAX_MODEL_LEN,
            "worker_top_logprobs": TOP_LOGPROBS,
            "jev_enabled": False,
            "invalid_plan_fallback": "charge plan and run ordinary guided continuation; retain treatment unit",
            "invalid_plan_streak_stop": MAX_CONSECUTIVE_INVALID,
            "no_retries_or_task_replacement": True,
            "stopping_rules": [
                "stop before the next task after three consecutive completed invalid plans",
                "stop before a task if six Qwen HTTP slots or one frontier slot are unavailable",
                "stop before a planner request whose conservative reservation exceeds $0.60",
                "stop after an actual planner charge exceeds $0.60 or usage is unresolved",
                "stop on provider, configuration, logging, or integrity error",
                "stop new tasks at 90 minutes; kill the process at 90 minutes",
                "delete the GPU app immediately on completion or failure",
                "independent Azure deletion watchdog fires within two hours of provisioning start",
            ],
        },
        "limits": {
            "max_worker_http_requests": MAX_WORKER_HTTP,
            "max_frontier_requests": MAX_FRONTIER_REQUESTS,
            "max_harness_wall_seconds": MAX_WALL_SECONDS,
            "watchdog_from_provisioning_seconds": WATCHDOG_SECONDS,
            "frontier_spend_guard_usd": FRONTIER_LIMIT_USD,
            "proposed_total_spending_ceiling_usd": TOTAL_CEILING_USD,
            "gpu_rate_usd_per_hour_assumption": GPU_RATE_USD_PER_HOUR,
        },
        "deployment": {
            "subscription_id": AZURE_SUBSCRIPTION_ID,
            "resource_group": AZURE_RESOURCE_GROUP,
            "container_app": AZURE_APP_NAME,
            "environment": AZURE_ENV_NAME,
            "region": "westus3",
            "max_gpu_replicas": 1,
            "vllm_image": VLLM_IMAGE,
        },
    }


def load_manifest(path: Path = MANIFEST_PATH) -> tuple[dict, str]:
    raw = path.read_bytes()
    doc = json.loads(raw)
    if doc != expected_manifest():
        raise ValueError("dev30 task selection or frozen protocol does not match the saved manifest")
    return doc, hashlib.sha256(raw).hexdigest()
