# HumanEval/14

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 750 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 882 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 938 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 760 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 761 | 0 |

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
