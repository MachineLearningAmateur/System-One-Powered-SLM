# Mbpp/410

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 1088 / 1488 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1227 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 1305 / 1977 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 3329 / 2479 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 914 / 2356 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the minimum value in a given heterogeneous list.
assert min_val(['Python', 3, 2, 4, 5, 'version'])==2
"""
```

## Visible tests

```python
assert min_val(['Python', 3, 2, 4, 5, 'version'])==2
```
