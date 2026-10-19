# HumanEval/1

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ✅ pass | 8192 / 8192 | 2 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | ✅ pass | 8192 / 8192 | 2 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python
from typing import List


def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
```

## Visible tests

```python
assert separate_paren_groups('( ) (( )) (( )( ))') == ['()', '(())', '(()())']
```
