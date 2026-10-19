# Mbpp/61

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2659 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 3007 / 1739 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 5933 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 6256 / 1848 / 999 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to count the number of substrings with the sum of digits equal to their length.
assert count_Substrings('112112') == 6
"""
```

## Visible tests

```python
assert count_Substrings('112112') == 6
```
