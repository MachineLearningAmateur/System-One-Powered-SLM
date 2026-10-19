# Mbpp/253

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1534 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 916 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 895 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 693 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1938 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function that returns the number of integer elements in a given list.
assert count_integer([1,2,'abc',1.2]) == 2
"""
```

## Visible tests

```python
assert count_integer([1,2,'abc',1.2]) == 2
```
