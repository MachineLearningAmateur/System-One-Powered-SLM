# Mbpp/394

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 956 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 531 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 494 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 714 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 544 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check if given tuple contains no duplicates.
assert check_distinct((1, 4, 5, 6, 1, 4)) == False
"""
```

## Visible tests

```python
assert check_distinct((1, 4, 5, 6, 1, 4)) == False
```
