# Mbpp/573

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1564 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1681 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1761 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1546 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2942 | 0 |

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
