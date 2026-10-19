# Mbpp/586

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1532 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1688 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2029 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1512 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1683 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to split a list at the nth eelment and add the first part to the end.
assert split_Arr([12,10,5,6,52,36],2) == [5,6,52,36,12,10]
"""
```

## Visible tests

```python
assert split_Arr([12,10,5,6,52,36],2) == [5,6,52,36,12,10]
```
