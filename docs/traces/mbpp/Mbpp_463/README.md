# Mbpp/463

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 3867 / 4211 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 7360 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 6109 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

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
