# Mbpp/12

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 2039 / 7343 / 5015 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2005 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 953 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1488 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1459 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a given matrix in ascending order according to the sum of its rows.
assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]])==[[1, 1, 1], [1, 2, 3], [2, 4, 5]]
"""
```

## Visible tests

```python
assert sort_matrix([[1, 2, 3], [2, 4, 5], [1, 1, 1]])==[[1, 1, 1], [1, 2, 3], [2, 4, 5]]
```
