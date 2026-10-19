# HumanEval/125

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 5338 / 3615 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 4445 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2607 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 4960 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3313 | 0 |

## Prompt shown to the model (round 1)

```python

def split_words(txt):
    '''
    Given a string of words, return a list of words split on whitespace, if no whitespaces exists in the text you
    should split on commas ',' if no commas exists you should return the number of lower-case letters with odd order in the
    alphabet, ord('a') = 0, ord('b') = 1, ... ord('z') = 25
    Examples
    split_words("Hello world!") ➞ ["Hello", "world!"]
    split_words("Hello,world!") ➞ ["Hello", "world!"]
    split_words("abcdef") == 3 
    '''

Visible tests:
assert split_words('Hello world!') == ['Hello', 'world!']
assert split_words('Hello,world!') == ['Hello', 'world!']
assert split_words('Hello world,!') == ['Hello', 'world,!']
```

## Visible tests

```python
assert split_words('Hello world!') == ['Hello', 'world!']
assert split_words('Hello,world!') == ['Hello', 'world!']
assert split_words('Hello world,!') == ['Hello', 'world,!']
```
