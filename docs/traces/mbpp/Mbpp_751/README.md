# Mbpp/751

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 1679 / 7525 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 1416 / 3255 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 3008 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 4995 / 7855 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 1844 / 5004 / 5231 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check if the given array represents min heap or not. 
assert check_min_heap([1, 2, 3, 4, 5, 6]) == True
"""
```

## Visible tests

```python
assert check_min_heap([1, 2, 3, 4, 5, 6]) == True
```
