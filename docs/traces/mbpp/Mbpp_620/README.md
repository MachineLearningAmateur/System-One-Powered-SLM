# Mbpp/620

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 3239 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 5408 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 4791 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 5974 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the size of the largest subset of a list of numbers so that every pair is divisible.
assert largest_subset([ 1, 3, 6, 13, 17, 18 ]) == 4
"""
```

## Visible tests

```python
assert largest_subset([ 1, 3, 6, 13, 17, 18 ]) == 4
```
