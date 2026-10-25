# Mbpp/792

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1257 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2138 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1483 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2879 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1123 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to count the number of lists in a given number of lists.
assert count_list([[1, 3], [5, 7], [9, 11], [13, 15, 17]]) == 4
"""
```

## Visible tests

```python
assert count_list([[1, 3], [5, 7], [9, 11], [13, 15, 17]]) == 4
```
