# Mbpp/433

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 955 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1304 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 833 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 874 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 868 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check whether the entered number is greater than the elements of the given array.
assert check_greater([1, 2, 3, 4, 5], 4) == False
"""
```

## Visible tests

```python
assert check_greater([1, 2, 3, 4, 5], 4) == False
```
