# HumanEval/7

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 960 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 703 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1068 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 822 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 851 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """
```

## Visible tests

```python
assert filter_by_substring([], 'a') == []
assert filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a') == ['abc', 'bacd', 'array']
```
