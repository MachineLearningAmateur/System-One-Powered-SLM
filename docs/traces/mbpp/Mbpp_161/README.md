# Mbpp/161

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1169 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1261 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1078 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1260 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2274 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove all elements from a given list present in another list.
assert remove_elements([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 4, 6, 8]) == [1, 3, 5, 7, 9, 10]
"""
```

## Visible tests

```python
assert remove_elements([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2, 4, 6, 8]) == [1, 3, 5, 7, 9, 10]
```
