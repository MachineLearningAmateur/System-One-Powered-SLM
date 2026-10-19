# HumanEval/21

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 710 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1768 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1052 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1686 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1362 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:
    """ Given list of numbers (of at least two elements), apply a linear transform to that list,
    such that the smallest number will become 0 and the largest will become 1
    >>> rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
```

## Visible tests

```python
assert rescale_to_unit([1.0, 2.0, 3.0, 4.0, 5.0]) == [0.0, 0.25, 0.5, 0.75, 1.0]
```
