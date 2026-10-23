# Qwen3-8B experiment handoff — October 22, 2026

## Later October 22 update

The sections below describe the earlier October 21 Azure attempt. A later Azure smoke run, `q8b-azure-smoke-20261022`, used the pinned public vLLM image on a West US 3 A100 Container App. All five selected development attempts completed, passed their visible checks, and later passed two local hidden grades each after the operator asked for that check. The Azure group was deleted and `az group exists` returned `false`. The grader session is exploratory and non-protocol; details are in `docs/q8b-plan.md`. The operator has now requested the full 8B experiment. A fresh spending approval is required before another GPU deployment or Jev scoring. The original 1.7B raw runs are still unavailable in this clone, so its Jev drift check cannot run here.

## Current state

- Repository: `/Users/aaparvat/System-One-Powered-SLM`, branch `akhil-8b`.
- In the earlier October 21 attempt, no Azure 8B experiment ran. No Azure Container App or GPU replica was deployed during that attempt, and no generation results came from it.
- The temporary Azure resource group `rg-q8b-smoke-20261021` was deleted. A final `az group exists` check returned `false`. The Docker image push was canceled. Nothing from this attempt is left running in Azure.
- The exact Azure charge is **not yet verified**. A Cost Management query returned HTTP 429, another returned `RBACAccessDenied`, and the legacy usage query did not yield a usable result before the session was interrupted. There was no GPU usage. The only plausible charge from the temporary setup is the short-lived Basic Azure Container Registry; the Consumption GPU profile had no app replicas. Azure billing records can arrive later. Do not report `$0` as a confirmed invoice amount.
- Local, ignored exploratory run data remains under `results/runs/`. No commit or push was made.

## Goal and protocol choice

The user wants to repeat James's finished `Qwen3-1.7B` System One experiment with `Qwen/Qwen3-8B`, keeping the same write/test/revise loop and direct TypeSafe Jev route. Qwen3-8B was chosen over SERA-8B for this replication. The intended protocol uses BF16 Qwen3-8B on pinned vLLM, the fixed split and visible tests, an 8,192-token thinking cap, 2,048-token answer cap, and the existing sampling and seed scheme. The first cloud step is only a **five-task development smoke run**, with no Jev, hidden grading, or test-split generation. The previous Azure smoke budget was $5; discuss a fresh limit before any new rented GPU run.

Read `AGENTS.md` and `docs/new-generator-runbook.md` before resuming. The finished 1.7B study, committed `configs/`, existing results, and `protocol-freeze-v1` must stay untouched. New runs need unique IDs. Do not commit or push without an explicit request. Keys remain in the local `.env`; none were copied to Azure.

## Local exploratory results

`docs/q8b-plan.md` records these in more detail:

- `q8b-local-smoke-20261019`: Docker Model Runner with quantized Qwen3-8B GGUF on Apple Silicon completed `HumanEval/2` in one round and passed its visible test. It hit the full thinking cap and took about 16.4 minutes. A separate direct TypeSafe Jev smoke scored the saved trajectory.
- A later local attempt on `HumanEval/4` stopped before a checkpoint because Docker Model Runner returned one fewer logprob than completion tokens. No Jev call was made for that failed attempt.
- `q8b-local-integrated-smoke-retry-20261020`: `HumanEval/4` completed in one round, passed its visible test, and direct TypeSafe Jev scored both arms. These are exploratory, non-protocol results; the GGUF/Metal backend does not establish BF16/vLLM replication.

The EvalPlus source-file hash mismatch was resolved on October 22. The local official downloads use LF line endings; changing only their JSONL record separators to CRLF reproduces both frozen MD5s in `configs/split_v1.json` exactly. All 164 HumanEval+ and 378 MBPP+ JSON records parse identically with either line ending. This is a serialization difference, not a grading-data difference; leave the downloaded files and frozen split unchanged. The old raw 1.7B trajectories are absent from this clone, so the planned direct Jev drift check cannot yet run.

## Code prepared locally

The working tree is dirty. Relevant uncommitted changes include:

- `src/system1/loop/generate.py`, `docker-compose.yml`: Qwen3-8B revision `b968826d9c46dd6066d109eabc6255188de91218`, BF16 vLLM settings, and pinned vLLM `v0.30.0` image digest `sha256:5f5e535216848d0c52159c8c13a0af04be5f6fe1a84e79914300610796f76d40`.
- `scripts/run_loop.py`, `src/system1/loop/monitor.py`: remote vLLM URL/manifest support and checks for the launch flags plus the live `/v1/models` response. For a remote run, derive the manifest from the actual Azure revision and image identity rather than trusting handwritten values.
- `docker/azure-vllm/Dockerfile`: custom non-root vLLM image built locally. It is about 8.7 GB and remains in local Docker cache. Its registry upload was canceled; the Azure registry was deleted.
- `scripts/azure_smoke_watchdog.py`: a deletion watchdog created as a cost guard. It was **not launched** because no GPU app was deployed.
- `scripts/run_local_8b_smoke.py`, `docs/q8b-plan.md`, and other uncommitted 8B-related changes. Inspect `git status --short` and `git diff` before editing; preserve earlier work.

The targeted validation command `uv run pytest -q tests/test_runner.py tests/test_loop.py` passed **47 tests** after the remote-run edits. No remote end-to-end test has passed.

## What happened in the Azure attempt

1. Azure CLI authentication, the `Microsoft.App`/`Microsoft.ContainerRegistry` providers, and A100 Consumption GPU quota were available in West US 3.
2. A temporary resource group, Container Apps environment, A100 Consumption workload profile, and Basic Azure Container Registry were created. **No app or GPU replica was created.**
3. Azure rejected an ACR build with `TasksOperationsNotAllowed` for this subscription.
4. The pinned vLLM image was built locally for `linux/amd64`. Pushing its 8.7 GB image from the Mac to ACR was very slow; the push was still running after at least 21 minutes and was canceled before a final registry digest existed.
5. A direct deployment of the pinned public vLLM image was identified as a possible route that avoids the upload, with non-root execution and writable `/tmp` cache settings. **That route was not tested or deployed.** Verify Azure's container configuration and actual image identity before using it.
6. At the user's request, deletion of the entire temporary resource group was requested and confirmed. Azure took time to remove the environment, but the final existence check returned `false`.

The main avoidable delay was choosing a custom image and ACR upload before trying the pinned public image directly. Azure deletion and repeated sandbox approval prompts added further time. The model itself never ran in Azure.

## Suggested next session

1. Confirm the branch and read this handoff, `AGENTS.md`, `docs/q8b-plan.md`, and the current diff. Do not reuse the deleted Azure resource names as evidence of a running service.
2. If the user asks to resume, agree on a new dollar cap. Prefer testing a **direct public pinned vLLM image** in a zero-replica Azure Container App, with non-root execution and `/tmp` model cache, before creating another registry. Keep the GPU at zero replicas until the deployment and cost guard are ready.
3. Verify the Azure image digest, revision launch arguments, live model identity, and HTTPS endpoint. Start a deletion watchdog with a conservative UTC deadline **before** triggering the first billable GPU replica.
4. Run only five development tasks using a new smoke run ID. Keep visible-test code inside the Docker sandbox on the Mac. Do not call Jev or hidden grading for the smoke.
5. Save logs and the run manifest, then delete the entire temporary Azure group and verify `az group exists` returns `false`.
6. Check Azure Cost Management later for the actual October 21 setup charge. If access remains denied, the account owner needs Cost Management Reader or billing access; do not infer an exact amount from the absence of GPU usage.

Official Azure billing references: [Container Apps billing](https://learn.microsoft.com/azure/container-apps/billing) and [Cost Management data latency](https://learn.microsoft.com/azure/cost-management-billing/costs/understand-cost-mgt-data).
