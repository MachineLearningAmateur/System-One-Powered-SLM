# Mbpp/623

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1742 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 835 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 881 / 388 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 780 / 511 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1045 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to compute the n-th power of each number in a list.
assert nth_nums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],2)==[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
"""
```

## Visible tests

```python
assert nth_nums([1, 2, 3, 4, 5, 6, 7, 8, 9, 10],2)==[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```
