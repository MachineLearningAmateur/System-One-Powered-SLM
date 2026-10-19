# HumanEval/9

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1391 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1671 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1348 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1739 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1171 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List, Tuple


def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of integers, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
```

## Visible tests

```python
assert rolling_max([1, 2, 3, 2, 3, 4, 2]) == [1, 2, 3, 3, 3, 4, 4]
```
