# Mbpp/436

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 582 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 904 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 623 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 524 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 422 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to return the negative numbers in a list.
assert neg_nos([-1,4,5,-6]) == [-1,-6]
"""
```

## Visible tests

```python
assert neg_nos([-1,4,5,-6]) == [-1,-6]
```
