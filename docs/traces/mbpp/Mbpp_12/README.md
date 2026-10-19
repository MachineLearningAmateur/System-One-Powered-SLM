# Mbpp/12

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 2039 / 7343 / 5015 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2005 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 953 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1488 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1459 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a given matrix in ascending order according to the sum of its rows.
assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]])==[[1, 1, 1], [1, 2, 3], [2, 4, 5]]
"""
```

## Visible tests

```python
assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]])==[[1, 1, 1], [1, 2, 3], [2, 4, 5]]
```
