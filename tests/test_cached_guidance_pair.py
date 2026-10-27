"""Offline checks for the one cached-plan engineering pair."""

import asyncio
import json
import sys
from argparse import Namespace
from pathlib import Path

import httpx
import pytest

from system1.eval.ledger import CostLedger

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import run_cached_guidance_pair as cached


def test_prepared_continuations_share_base_and_keep_exact_plan_isolated():
    packet = cached.prepare_packet()
    task, first, plan, provenance = cached.verified_sources()
    control = packet["messages"]["control"][0]["content"]
    guidance = packet["messages"]["guidance"][0]["content"]
    suffix = "\nAdvice from a separate assistant (check it; it may be wrong):\n" + plan + "\n"
    assert guidance == control + suffix
    assert plan not in control
    assert packet["source"] == provenance
    assert packet["cached_shared_checkpoint"] == first
    assert packet["source"]["source_checkpoint_id"] == "HumanEval/59/a0/shared/r1"
    assert packet["source"]["source_checkpoint_code_sha256"] == first["code_sha256"]
    assert packet["source"]["plan_sha256"] == cached.PLAN_SHA256
    assert packet["worker"]["effective_think_caps"] == {"control": 8192, "guidance": 8192}
    assert packet["worker"]["answer_cap"] == 2048
    assert packet["worker"]["seed"] == packet["first_phase_http_requests"]["control"]["seed"]
    assert packet["worker"]["seed"] == packet["first_phase_http_requests"]["guidance"]["seed"]
    assert packet["first_phase_http_requests"]["control"]["max_tokens"] == 8192
    assert packet["first_phase_http_requests"]["guidance"]["max_tokens"] == 8192
    assert plan not in packet["first_phase_http_requests"]["control"]["prompt"]
    assert plan in packet["first_phase_http_requests"]["guidance"]["prompt"]
    assert packet["max_worker_http_requests"] == 4
    assert packet["incremental_frontier_requests"] == 0


def test_raw_worker_exchange_logging_and_four_call_guard(tmp_path):
    async def scenario():
        calls = []

        def handle(request):
            calls.append(request)
            return httpx.Response(200, json={"choices": [{"text": "mock"}],
                                             "usage": {"prompt_tokens": 1, "completion_tokens": 1}})

        async with httpx.AsyncClient(transport=httpx.MockTransport(handle)) as http:
            log = CostLedger(tmp_path / "exchanges.jsonl")
            budget = cached.CallBudget(4)
            client = cached.RecordingClient(http, "control", log, budget)
            for _ in range(4):
                await client.post("https://example.invalid/v1/completions", json={"model": "mock"}, timeout=1)
            with pytest.raises(RuntimeError, match="four-call"):
                await client.post("https://example.invalid/v1/completions", json={"model": "mock"}, timeout=1)
            rows, damaged = log.read()
            assert not damaged and len(rows) == len(calls) == budget.used == 4
            assert all(row["request_body"]["model"] == "mock" for row in rows)
            assert all(row["response_body"]["choices"][0]["text"] == "mock" for row in rows)

    asyncio.run(scenario())


def test_paid_mode_fails_before_server_without_new_approval(monkeypatch):
    async def scenario():
        packet = cached.prepare_packet()
        monkeypatch.setattr(cached, "remote_vllm_server_identity",
                            lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("must not query server")))
        with pytest.raises(SystemExit, match="separately approved"):
            await cached._run_real(Namespace(operator_approved=False,
                max_worker_http_requests=4, max_frontier_requests=0, max_wall_seconds=900,
                run_id="never-created", server_url="https://example.invalid",
                remote_manifest="missing", watchdog_manifest="missing"), packet)

    asyncio.run(scenario())
