# Mbpp/559

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 1307 / 3529 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | 1238 / 6056 / 4473 | 0 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | 2185 / 5529 / 2808 | 0 |
| [Attempt 3](attempt_3.md) | 3 | visible pass | 1533 / 4370 / 5094 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 1531 / 8192 / 2417 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the sum of the largest contiguous sublist in the given list.
assert max_sub_array_sum([-2, -3, 4, -1, -2, 1, 5, -3], 8) == 7
"""
```

## Visible tests

```python
assert max_sub_array_sum([-2, -3, 4, -1, -2, 1, 5, -3], 8) == 7
```
