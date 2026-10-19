# Mbpp/743

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1817 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1664 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2179 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3133 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1603 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to rotate a given list by specified number of items to the right direction. 
assert rotate_right([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],3)==[8, 9, 10, 1, 2, 3, 4, 5, 6, 7]
"""
```

## Visible tests

```python
assert rotate_right([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],3)==[8, 9, 10, 1, 2, 3, 4, 5, 6, 7]
```
