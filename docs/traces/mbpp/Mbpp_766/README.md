# Mbpp/766

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1050 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 863 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1115 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 675 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 907 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to return a list of all pairs of consecutive items in a given list.
assert pair_wise([1,1,2,3,3,4,4,5])==[(1, 1), (1, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5)]
"""
```

## Visible tests

```python
assert pair_wise([1,1,2,3,3,4,4,5])==[(1, 1), (1, 2), (2, 3), (3, 3), (3, 4), (4, 4), (4, 5)]
```
