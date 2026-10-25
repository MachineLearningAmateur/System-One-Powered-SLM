# Mbpp/641

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1094 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1328 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1397 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1590 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1066 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the nth nonagonal number.
assert is_nonagonal(10) == 325
"""
```

## Visible tests

```python
assert is_nonagonal(10) == 325
```
