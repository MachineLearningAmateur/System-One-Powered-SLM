# Mbpp/632

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 737 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1155 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1156 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 997 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 991 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to move all zeroes to the end of the given list.
assert move_zero([1,0,2,0,3,4]) == [1,2,3,4,0,0]
"""
```

## Visible tests

```python
assert move_zero([1,0,2,0,3,4]) == [1,2,3,4,0,0]
```
