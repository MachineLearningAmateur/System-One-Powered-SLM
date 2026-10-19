# Mbpp/633

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 4816 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | 1722 / 698 / 3573 | 0 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | 3568 / 3555 / 497 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 1012 / 2917 / 418 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3633 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the sum of xor of all pairs of numbers in the given list.
assert pair_xor_Sum([5,9,7,6],4) == 47
"""
```

## Visible tests

```python
assert pair_xor_Sum([5,9,7,6],4) == 47
```
