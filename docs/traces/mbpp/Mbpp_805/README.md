# Mbpp/805

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 642 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1240 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1069 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1056 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 890 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that returns the list in a list of lists whose sum of elements is the highest.
assert max_sum_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[10, 11, 12]
"""
```

## Visible tests

```python
assert max_sum_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[10, 11, 12]
```
