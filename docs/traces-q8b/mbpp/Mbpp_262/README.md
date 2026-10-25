# Mbpp/262

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1020 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1084 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1919 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1315 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 936 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a list and an integer L and splits the given list into two parts where the length of the first part of the list is L, and returns the resulting lists in a tuple.
assert split_two_parts([1,1,2,3,4,4,5,1],3)==([1, 1, 2], [3, 4, 4, 5, 1])
"""
```

## Visible tests

```python
assert split_two_parts([1,1,2,3,4,4,5,1],3)==([1, 1, 2], [3, 4, 4, 5, 1])
```
