# Mbpp/723

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1379 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1329 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1133 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1050 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1097 | 0 |

## Prompt shown to the model (round 1)

```python
"""
The input is defined as two lists of the same length. Write a function to count indices where the lists have the same values.
assert count_same_pair([1, 2, 3, 4, 5, 6, 7, 8],[2, 2, 3, 1, 2, 6, 7, 9])==4
"""
```

## Visible tests

```python
assert count_same_pair([1, 2, 3, 4, 5, 6, 7, 8],[2, 2, 3, 1, 2, 6, 7, 9])==4
```
