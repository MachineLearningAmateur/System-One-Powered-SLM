# Mbpp/262

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 908 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1345 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 800 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 720 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 922 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a list and an integer L and splits the given list into two parts where the length of the first part of the list is L, and returns the resulting lists in a tuple.
assert split_two_parts([1,1,2,3,4,4,5,1],3)==([1, 1, 2], [3, 4, 4, 5, 1])
"""
```

## Visible tests

```python
assert split_two_parts([1,1,2,3,4,4,5,1],3)==([1, 1, 2], [3, 4, 4, 5, 1])
```
