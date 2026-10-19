# HumanEval/24

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2932 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3055 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 3343 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2513 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3470 | 0 |

## Prompt shown to the model (round 1)

```python


def largest_divisor(n: int) -> int:
    """ For a given number n, find the largest number that divides n evenly, smaller than n
    >>> largest_divisor(15)
    5
    """
```

## Visible tests

```python
assert largest_divisor(15) == 5
```
