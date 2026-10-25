# Mbpp/472

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 3753 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2619 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 3984 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2811 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 5320 | 0 |

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
