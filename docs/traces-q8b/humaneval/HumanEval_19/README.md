# HumanEval/19

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1996 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3665 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2293 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2115 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1708 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """
```

## Visible tests

```python
assert sort_numbers('three one five') == 'one three five'
```
