# Mbpp/765

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ✅ pass | 8192 / 2036 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 6918 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 7921 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 3047 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find nth polite number. geeksforgeeks.org/n-th-polite-number/
assert is_polite(7) == 11
"""
```

## Visible tests

```python
assert is_polite(7) == 11
```
