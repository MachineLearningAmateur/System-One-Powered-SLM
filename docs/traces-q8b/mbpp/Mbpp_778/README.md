# Mbpp/778

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1847 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1819 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1923 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1730 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1487 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to pack consecutive duplicates of a given list elements into sublists.
assert pack_consecutive_duplicates([0, 0, 1, 2, 3, 4, 4, 5, 6, 6, 6, 7, 8, 9, 4, 4])==[[0, 0], [1], [2], [3], [4, 4], [5], [6, 6, 6], [7], [8], [9], [4, 4]]
"""
```

## Visible tests

```python
assert pack_consecutive_duplicates([0, 0, 1, 2, 3, 4, 4, 5, 6, 6, 6, 7, 8, 9, 4, 4])==[[0, 0], [1], [2], [3], [4, 4], [5], [6, 6, 6], [7], [8], [9], [4, 4]]
```
