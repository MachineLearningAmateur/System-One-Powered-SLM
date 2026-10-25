# Mbpp/100

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1947 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1615 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1733 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1854 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1925 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the next smallest palindrome of a specified integer, returned as an integer.
assert next_smallest_palindrome(99)==101
"""
```

## Visible tests

```python
assert next_smallest_palindrome(99)==101
```
