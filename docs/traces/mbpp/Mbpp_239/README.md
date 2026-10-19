# Mbpp/239

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in positive integers m and n and finds the number of possible sequences of length n, such that each element is a positive integer and is greater than or equal to twice the previous element but less than or equal to m.
assert get_total_number_of_sequences(10, 4) == 4
"""
```

## Visible tests

```python
assert get_total_number_of_sequences(10, 4) == 4
```
