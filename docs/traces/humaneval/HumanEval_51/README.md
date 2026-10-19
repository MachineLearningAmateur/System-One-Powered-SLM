# HumanEval/51

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1507 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1680 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 759 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1293 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1316 | 0 |

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
