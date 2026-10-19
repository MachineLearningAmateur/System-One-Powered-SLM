# Mbpp/137

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 1559 / 767 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2372 | 0 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | ❌ fail ⚠️ visible pass | 3349 / 2549 / 585 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 1823 / 725 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2586 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the ratio of zeroes to non-zeroes in an array of integers.
assert math.isclose(zero_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8]), 0.181818, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(zero_count([0, 1, 2, -1, -5, 6, 0, -3, -2, 3, 4, 6, 8]), 0.181818, rel_tol=0.001)
```
