# Mbpp/280

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1215 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 817 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1432 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1130 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1278 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in an array and element and returns a tuple containing a boolean that indicates if the element is in the array and the index position of the element (or -1 if the element is not found).
assert sequential_search([11,23,58,31,56,77,43,12,65,19],31) == (True, 3)
"""
```

## Visible tests

```python
assert sequential_search([11,23,58,31,56,77,43,12,65,19],31) == (True, 3)
```
