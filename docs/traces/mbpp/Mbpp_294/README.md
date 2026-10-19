# Mbpp/294

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 1555 / 4413 / 7967 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 1541 / 834 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1767 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 2870 / 1497 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 1085 / 1758 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the maximum value in a given heterogeneous list.
assert max_val(['Python', 3, 2, 4, 5, 'version'])==5
"""
```

## Visible tests

```python
assert max_val(['Python', 3, 2, 4, 5, 'version'])==5
```
