# Mbpp/141

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 6746 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 5362 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 7820 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 6330 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a list of elements.
assert pancake_sort([15, 79, 25, 38, 69]) == [15, 25, 38, 69, 79]
"""
```

## Visible tests

```python
assert pancake_sort([15, 79, 25, 38, 69]) == [15, 25, 38, 69, 79]
```
