# Mbpp/272

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 761 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1070 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 756 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 809 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1135 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a list of tuples and returns a list containing the rear element of each tuple.
assert rear_extract([(1, 'Rash', 21), (2, 'Varsha', 20), (3, 'Kil', 19)]) == [21, 20, 19]
"""
```

## Visible tests

```python
assert rear_extract([(1, 'Rash', 21), (2, 'Varsha', 20), (3, 'Kil', 19)]) == [21, 20, 19]
```
