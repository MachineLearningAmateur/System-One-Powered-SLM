# BigCodeBench Jev-only validation: grading compatibility amendment

**Dated October 26, 2026, after generation and the first reference-calibration
stop, before any candidate hidden grade or Jev call.** This supplements the
[frozen plan](bcb-jev-only-validation-plan.md) and its earlier amendments.
The stopped session and its aggregate calibration log remain in ignored run
data. The operator requested a retry after the cause was identified.

## Cause and scope

All 225 planned attempts on the frozen 45 tasks completed at generation commit
`7253b53` (`bcb-jev-only-freeze-v3`). The first grading session stopped when
the public benchmark reference for `BigCodeBench/394` raised one error in five
hidden tests. No candidate was graded and no Jev call occurred. A diagnostic
inside the networkless grader found that the test calls `assertEquals` on a
`unittest.TestCase`; the grader's Python 3.12.14 has only `assertEqual`.
Restoring the exact alias in a disposable diagnostic made all five reference
tests pass. No hidden input or candidate outcome was used to choose the fix.

## Amended grading procedure

The `bcb-grader-v2-assertEquals` worker defines
`unittest.TestCase.assertEquals = unittest.TestCase.assertEqual` in each
networkless child before executing either reference or candidate code. This
is the only semantic change to hidden execution. Rebuild it as a separate
`system1-bcb-sandbox:v2` image; retain the v1 image and failed session. Use
the frozen manifest and hidden data already associated with
`bcb-jev-only-test-v2`. Recheck **all 45 reference solutions** before any
candidate grade. Stop again if any reference fails; do not drop a task.

The grader must run from a clean commit tagged
`bcb-jev-only-grader-amendment-v1`, descended from the generation commit. It
records both commit hashes, the amendment tag, worker hash, and actual image
ID in its new grading session. Existing candidate grading rules, Jev inputs,
router weights, thresholds, and the analysis plan stay fixed. The original
calibration stop and this after-generation amendment must accompany any
reported result; it is not an unamended preregistered result.

No new Azure generation is needed. If the amended grading succeeds, use the
previously approved **$1 Jev ceiling** for this validation, with the frozen
12-million-input-token guard. No result is published or pushed automatically.
