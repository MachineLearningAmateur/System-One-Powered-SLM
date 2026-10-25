# Mbpp/733

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1391 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1407 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1281 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1505 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1346 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the index of the first occurrence of a given number in a sorted array.
assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
"""
```

## Visible tests

```python
assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
```
