# Mbpp/71

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 7527 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 7063 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 7468 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 6053 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 7318 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a list of elements.
assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]
"""
```

## Visible tests

```python
assert comb_sort([5, 15, 37, 25, 79]) == [5, 15, 25, 37, 79]
```
