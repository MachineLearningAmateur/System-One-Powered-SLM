# Mbpp/388

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2976 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3429 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2918 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3138 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 4401 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the highest power of 2 that is less than or equal to n.
assert highest_Power_of_2(10) == 8
"""
```

## Visible tests

```python
assert highest_Power_of_2(10) == 8
```
