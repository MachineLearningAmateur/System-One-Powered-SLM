# Mbpp/270

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1028 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1314 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 999 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1144 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1600 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the sum of even numbers at even positions of a list.
assert sum_even_and_even_index([5, 6, 12, 1, 18, 8]) == 30
"""
```

## Visible tests

```python
assert sum_even_and_even_index([5, 6, 12, 1, 18, 8]) == 30
```
