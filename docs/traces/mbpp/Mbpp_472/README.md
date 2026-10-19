# Mbpp/472

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1294 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3269 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1509 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1476 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1467 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to check whether the given list contains consecutive numbers or not.
assert check_Consecutive([1,2,3,4,5]) == True
"""
```

## Visible tests

```python
assert check_Consecutive([1,2,3,4,5]) == True
```
