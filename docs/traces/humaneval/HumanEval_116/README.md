# HumanEval/116

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ✅ pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ✅ pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ✅ pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ✅ pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ✅ pass | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python

def sort_array(arr):
    """
    In this Kata, you have to sort an array of non-negative integers according to
    number of ones in their binary representation in ascending order.
    For similar number of ones, sort based on decimal value.

    It must be implemented like this:
    >>> sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
    >>> sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
    >>> sort_array([1, 0, 2, 3, 4]) [0, 1, 2, 3, 4]
    """
```

## Visible tests

```python
assert sort_array([1, 5, 2, 3, 4]) == [1, 2, 3, 4, 5]
assert sort_array([-2, -3, -4, -5, -6]) == [-6, -5, -4, -3, -2]
```
