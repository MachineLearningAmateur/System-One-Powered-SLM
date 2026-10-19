# Mbpp/808

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 425 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 583 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 482 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 766 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 553 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check if the given tuples contain the k or not.
assert check_K((10, 4, 5, 6, 8), 6) == True
"""
```

## Visible tests

```python
assert check_K((10, 4, 5, 6, 8), 6) == True
```
