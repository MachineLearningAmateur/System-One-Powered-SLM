# Mbpp/116

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 620 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 489 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 897 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 620 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 972 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert a given tuple of positive integers into a single integer.
assert tuple_to_int((1,2,3))==123
"""
```

## Visible tests

```python
assert tuple_to_int((1,2,3))==123
```
