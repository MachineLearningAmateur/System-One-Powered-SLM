# Mbpp/77

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3629 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3808 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2467 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2149 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3519 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find whether a number is divisible by 11.
assert is_Diff (12345) == False
"""
```

## Visible tests

```python
assert is_Diff (12345) == False
```
