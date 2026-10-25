# Mbpp/255

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1424 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1204 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1522 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1224 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1216 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a list and length n, and generates all combinations (with repetition) of the elements of the list and returns a list with a tuple for each combination.
assert combinations_colors( ["Red","Green","Blue"],1)==[('Red',), ('Green',), ('Blue',)]
"""
```

## Visible tests

```python
assert combinations_colors( ["Red","Green","Blue"],1)==[('Red',), ('Green',), ('Blue',)]
```
