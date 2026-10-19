# HumanEval/14

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 750 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 882 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 938 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 760 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 761 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def all_prefixes(string: str) -> List[str]:
    """ Return list of all prefixes from shortest to longest of the input string
    >>> all_prefixes('abc')
    ['a', 'ab', 'abc']
    """
```

## Visible tests

```python
assert all_prefixes('abc') == ['a', 'ab', 'abc']
```
