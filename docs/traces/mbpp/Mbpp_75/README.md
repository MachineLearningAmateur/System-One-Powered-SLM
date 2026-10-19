# Mbpp/75

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1102 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1094 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1161 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1471 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1072 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find tuples which have all elements divisible by k from the given list of tuples.
assert find_tuples([(6, 24, 12), (7, 9, 6), (12, 18, 21)], 6) == [(6, 24, 12)]
"""
```

## Visible tests

```python
assert find_tuples([(6, 24, 12), (7, 9, 6), (12, 18, 21)], 6) == [(6, 24, 12)]
```
