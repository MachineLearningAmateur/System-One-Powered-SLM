# Mbpp/784

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 2791 / 4646 / 3585 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2237 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1637 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1322 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2182 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the product of first even and odd number of a given list.
assert mul_even_odd([1,3,5,7,4,1,6,8])==4
"""
```

## Visible tests

```python
assert mul_even_odd([1,3,5,7,4,1,6,8])==4
```
