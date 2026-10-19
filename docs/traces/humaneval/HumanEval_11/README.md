# HumanEval/11

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1285 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1114 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1108 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1468 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1634 | 0 |

## Prompt shown to the model (round 1)

```python
from typing import List


def string_xor(a: str, b: str) -> str:
    """ Input are two strings a and b consisting only of 1s and 0s.
    Perform binary XOR on these inputs and return result also as a string.
    >>> string_xor('010', '110')
    '100'
    """
```

## Visible tests

```python
assert string_xor('010', '110') == '100'
```
