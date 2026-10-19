# Mbpp/479

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1358 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 1134 / 1173 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1302 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1757 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 4232 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the first digit of a given number.
assert first_Digit(123) == 1
"""
```

## Visible tests

```python
assert first_Digit(123) == 1
```
