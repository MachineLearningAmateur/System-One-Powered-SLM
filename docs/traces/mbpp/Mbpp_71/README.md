# Mbpp/71

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 4365 / 8192 | 2 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 2643 / 8192 / 8192 | 2 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 4868 / 8192 / 4166 | 1 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 8192 / 8192 | 2 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a list of elements.
assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]
"""
```

## Visible tests

```python
assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]
```
