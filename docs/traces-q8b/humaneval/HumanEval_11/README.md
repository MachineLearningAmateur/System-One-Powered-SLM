# HumanEval/11

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3541 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 3559 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2927 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3476 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2877 | 0 |

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
