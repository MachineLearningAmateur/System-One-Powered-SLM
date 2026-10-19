# Mbpp/170

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1258 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1141 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1617 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1304 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1120 | 0 |

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
