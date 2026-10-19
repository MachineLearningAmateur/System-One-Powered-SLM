# Mbpp/608

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | ✅ pass | 5859 / 301 / 551 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 7714 / 518 | 1 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 5598 / 925 / 617 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 5332 / 309 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find nth bell number.
assert bell_Number(2) == 2
"""
```

## Visible tests

```python
assert bell_Number(2) == 2
```
