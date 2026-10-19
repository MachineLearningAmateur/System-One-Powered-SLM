# Mbpp/116

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 620 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 489 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 897 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 620 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 972 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert a given tuple of positive integers into a single integer.
assert tuple_to_int((1,2,3))==123
"""
```

## Visible tests

```python
assert tuple_to_int((1,2,3))==123
```
