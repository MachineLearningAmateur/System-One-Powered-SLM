# Mbpp/463

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 6385 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 5887 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 5957 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 5881 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 6439 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the maximum product subarray of the given array.
assert max_subarray_product([1, -2, -3, 0, 7, -8, -2]) == 112
"""
```

## Visible tests

```python
assert max_subarray_product([1, -2, -3, 0, 7, -8, -2]) == 112
```
