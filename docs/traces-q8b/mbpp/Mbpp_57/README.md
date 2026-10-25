# Mbpp/57

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2201 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2136 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 866 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2335 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2009 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the largest number that can be formed with the given list of digits.
assert find_Max_Num([1,2,3]) == 321
"""
```

## Visible tests

```python
assert find_Max_Num([1,2,3]) == 321
```
