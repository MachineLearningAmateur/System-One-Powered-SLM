# BigCodeBench Jev-only validation: Azure region amendment

**Dated October 26, 2026, before any v2 task generation.** This supplements
the [v1 plan](bcb-jev-only-validation-plan.md) and the
[visible-reference amendment](bcb-jev-only-validation-amendment-2026-10-25.md).

Azure deleted the stopped v1 GPU app, but its West US 3 managed environment
remained `ScheduledForDelete`. The subscription's regional managed-environment
cap of one therefore blocked creation of a new West US 3 environment. No
candidate hidden grade or Jev call had occurred, and the 45 v2 tasks were
untouched by generation.

Run `bcb-jev-only-test-v2` in **East US** on the same
`Consumption-GPU-NC24-A100` type, with one replica, 8 vCPUs, 56 GiB, the
same pinned vLLM image and Qwen3-8B revision, and the same local networkless
sandbox. Azure's retail meters for the A100 GPU, active vCPU, and active
memory in East US equal those used for the West US 3 cost estimate:
$0.000529 per GPU-second, $0.000024 per vCPU-second, and $0.000003 per
GiB-second (about $3.20 per active hour for this app). The v2 group's
separate watchdog deadline remains in force. The combined approval remains
$40 Azure and $1 Jev, including the aborted v1 deployment.

The 45-task manifest, five attempts, Jev-only and cheap scores, thresholds,
primary test, and all grading separation rules are unchanged. Freeze this
amendment in a new commit and tag `bcb-jev-only-freeze-v3` before generation.
The v2 run uses that tag. Continue to verify complete deletion of the old
West US 3 resource group, and delete and verify the East US group after the
v2 generation ends.
