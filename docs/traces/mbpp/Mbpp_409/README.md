# Mbpp/409

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 985 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 812 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 959 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 829 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 933 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the minimum product from the pairs of tuples within a given list.
assert min_product_tuple([(2, 7), (2, 6), (1, 8), (4, 9)] )==8
"""
```

## Visible tests

```python
assert min_product_tuple([(2, 7), (2, 6), (1, 8), (4, 9)] )==8
```
