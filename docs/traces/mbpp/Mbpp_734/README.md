# Mbpp/734

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | 8192 / 658 / 963 | 1 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | 8192 / 4334 / 729 | 1 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 7160 / 356 / 502 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 4291 / 1133 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 7920 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find sum of products of all possible sublists of a given list. 
assert sum_Of_Subarray_Prod([1,2,3]) == 20
"""
```

## Visible tests

```python
assert sum_Of_Subarray_Prod([1,2,3]) == 20
```
