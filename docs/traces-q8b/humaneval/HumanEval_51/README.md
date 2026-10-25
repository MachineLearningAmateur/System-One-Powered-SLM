# HumanEval/51

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1287 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 966 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1688 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1344 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1346 | 0 |

## Prompt shown to the model (round 1)

```python


def remove_vowels(text):
    """
    remove_vowels is a function that takes string and returns string without vowels.
    >>> remove_vowels('')
    ''
    >>> remove_vowels("abcdef\nghijklm")
    'bcdf\nghjklm'
    >>> remove_vowels('abcdef')
    'bcdf'
    >>> remove_vowels('aaaaa')
    ''
    >>> remove_vowels('aaBAA')
    'B'
    >>> remove_vowels('zbcd')
    'zbcd'
    """
```

## Visible tests

```python
assert remove_vowels('') == ''
assert remove_vowels("abcdef\nghijklm") == 'bcdf\nghjklm'
assert remove_vowels('abcdef') == 'bcdf'
assert remove_vowels('aaaaa') == ''
assert remove_vowels('aaBAA') == 'B'
assert remove_vowels('zbcd') == 'zbcd'
```
