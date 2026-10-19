# HumanEval/22

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1477 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1022 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1222 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1564 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 4237 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """
```

## Visible tests

```python
assert filter_integers(['a', 3.14, 5]) == [5]
assert filter_integers([1, 2, 3, 'abc', {}, []]) == [1, 2, 3]
```
