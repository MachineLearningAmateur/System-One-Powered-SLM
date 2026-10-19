# Mbpp/426

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 771 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 786 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 854 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 637 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 543 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to filter odd numbers.
assert filter_oddnumbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1,3,5,7,9]
"""
```

## Visible tests

```python
assert filter_oddnumbers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])==[1,3,5,7,9]
```
