# Mbpp/470

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1059 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1863 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 828 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1186 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1162 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the pairwise addition of the neighboring elements of the given tuple.
assert add_pairwise((1, 5, 7, 8, 10)) == (6, 12, 15, 18)
"""
```

## Visible tests

```python
assert add_pairwise((1, 5, 7, 8, 10)) == (6, 12, 15, 18)
```
