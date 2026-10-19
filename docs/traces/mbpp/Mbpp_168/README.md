# Mbpp/168

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 343 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 458 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 612 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 894 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 501 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to count the number of occurrences of a number in a given list.
assert frequency([1,2,3], 4) == 0
"""
```

## Visible tests

```python
assert frequency([1,2,3], 4) == 0
```
