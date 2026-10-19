# Mbpp/592

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 3859 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1556 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 1837 / 2559 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 1473 / 2130 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1403 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the sum of the product of consecutive binomial co-efficients.
assert sum_Of_product(3) == 15
"""
```

## Visible tests

```python
assert sum_Of_product(3) == 15
```
