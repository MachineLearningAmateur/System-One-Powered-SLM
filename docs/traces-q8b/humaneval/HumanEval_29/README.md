# HumanEval/29

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1007 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 991 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1105 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1076 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 782 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of strings only for ones that start with a given prefix.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """
```

## Visible tests

```python
assert filter_by_prefix([], 'a') == []
assert filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a') == ['abc', 'array']
```
