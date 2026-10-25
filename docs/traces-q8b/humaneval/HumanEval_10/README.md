# HumanEval/10

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1845 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 5029 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 6646 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 5618 | 0 |

## Prompt shown to the model (round 1)

```python


def is_palindrome(string: str) -> bool:
    """ Test if given string is a palindrome """
    return string == string[::-1]


def make_palindrome(string: str) -> str:
    """ Find the shortest palindrome that begins with a supplied string.
    Algorithm idea is simple:
    - Find the longest postfix of supplied string that is a palindrome.
    - Append to the end of the string reverse of a string prefix that comes before the palindromic suffix.
    >>> make_palindrome('')
    ''
    >>> make_palindrome('cat')
    'catac'
    >>> make_palindrome('cata')
    'catac'
    """
```

## Visible tests

```python
assert make_palindrome('') == ''
assert make_palindrome('cat') == 'catac'
assert make_palindrome('cata') == 'catac'
```
