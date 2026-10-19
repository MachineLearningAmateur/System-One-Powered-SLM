# Mbpp/108

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1380 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1599 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1617 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2988 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1179 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to merge three lists into a single sorted list.
assert merge_sorted_list([25, 24, 15, 4, 5, 29, 110],[19, 20, 11, 56, 25, 233, 154],[24, 26, 54, 48])==[4, 5, 11, 15, 19, 20, 24, 24, 25, 25, 26, 29, 48, 54, 56, 110, 154, 233]
"""
```

## Visible tests

```python
assert merge_sorted_list([25, 24, 15, 4, 5, 29, 110],[19, 20, 11, 56, 25, 233, 154],[24, 26, 54, 48])==[4, 5, 11, 15, 19, 20, 24, 24, 25, 25, 26, 29, 48, 54, 56, 110, 154, 233]
```
