# Mbpp/805

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1781 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1533 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1141 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2926 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1891 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that returns the list in a list of lists whose sum of elements is the highest.
assert max_sum_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[10, 11, 12]
"""
```

## Visible tests

```python
assert max_sum_list([[1,2,3], [4,5,6], [10,11,12], [7,8,9]])==[10, 11, 12]
```
