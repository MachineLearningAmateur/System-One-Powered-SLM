# Mbpp/123

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 5650 / 8192 / 8192 | 2 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 7735 / 791 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 6359 / 8192 / 7593 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 4973 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sum all amicable numbers from 1 to a specified number.
assert amicable_numbers_sum(999)==504
"""
```

## Visible tests

```python
assert amicable_numbers_sum(999)==504
```
