# Mbpp/468

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 6035 | 1 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 3 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 8192 / 7007 | 2 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the maximum product formed by multiplying numbers of an increasing subsequence of that array.
assert max_product([3, 100, 4, 5, 150, 6]) == 3000
"""
```

## Visible tests

```python
assert max_product([3, 100, 4, 5, 150, 6]) == 3000
```
