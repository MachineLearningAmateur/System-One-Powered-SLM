# Mbpp/170

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 984 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1061 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 878 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1186 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1194 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the sum of numbers in a list within a range specified by two indices.
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 8, 10) == 29
"""
```

## Visible tests

```python
assert sum_range_list([2,1,5,6,8,3,4,9,10,11,8,12], 8, 10) == 29
```
