# HumanEval/29

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 772 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 919 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 628 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 830 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 587 | 0 |

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
