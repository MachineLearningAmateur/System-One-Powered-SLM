# Mbpp/271

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 695 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1047 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 950 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 706 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 901 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function that takes in an integer n and finds the sum of the first n even natural numbers that are raised to the fifth power.
assert even_Power_Sum(2) == 1056
"""
```

## Visible tests

```python
assert even_Power_Sum(2) == 1056
```
