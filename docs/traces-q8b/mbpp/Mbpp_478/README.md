# Mbpp/478

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ✅ pass | 2032 / 1434 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 1785 / 4070 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ✅ pass | 1982 / 2304 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | ✅ pass | 2199 / 1701 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 5848 / 2170 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove lowercase substrings from a given string.
assert remove_lowercase("PYTHon")==('PYTH')
"""
```

## Visible tests

```python
assert remove_lowercase("PYTHon")==('PYTH')
```
