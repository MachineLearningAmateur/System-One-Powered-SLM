# HumanEval/145

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 7955 | 2 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 6046 / 8192 | 2 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python

def order_by_points(nums):
    """
    Write a function which sorts the given list of integers
    in ascending order according to the sum of their digits.
    Note: if there are several items with similar sum of their digits,
    order them based on their index in original list.

    For example:
    >>> order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
    >>> order_by_points([]) == []
    """
```

## Visible tests

```python
assert order_by_points([1, 11, -1, -11, -12]) == [-1, -11, 1, -12, 11]
assert order_by_points([]) == []
```
