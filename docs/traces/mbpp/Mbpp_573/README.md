# Mbpp/573

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1384 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1876 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2038 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1415 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1472 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to calculate the product of the unique numbers in a given list.
assert unique_product([10, 20, 30, 40, 20, 50, 60, 40]) ==  720000000
"""
```

## Visible tests

```python
assert unique_product([10, 20, 30, 40, 20, 50, 60, 40]) ==  720000000
```
