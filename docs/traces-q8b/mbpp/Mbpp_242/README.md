# Mbpp/242

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 552 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 591 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 459 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 486 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 497 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to count the total number of characters in a string.
assert count_charac("python programming")==18
"""
```

## Visible tests

```python
assert count_charac("python programming")==18
```
