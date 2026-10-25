# Mbpp/106

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3369 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2385 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1447 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1124 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3218 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to append the given list to the given tuples.
assert add_lists([5, 6, 7], (9, 10)) == (9, 10, 5, 6, 7)
"""
```

## Visible tests

```python
assert add_lists([5, 6, 7], (9, 10)) == (9, 10, 5, 6, 7)
```
