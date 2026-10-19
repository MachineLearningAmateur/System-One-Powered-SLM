# HumanEval/158

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 8063 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2879 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 7830 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 7434 | 0 |

## Prompt shown to the model (round 1)

```python

def find_max(words):
    """Write a function that accepts a list of strings.
    The list contains different words. Return the word with maximum number
    of unique characters. If multiple strings have maximum number of unique
    characters, return the one which comes first in lexicographical order.

    find_max(["name", "of", "string"]) == "string"
    find_max(["name", "enam", "game"]) == "enam"
    find_max(["aaaaaaa", "bb" ,"cc"]) == ""aaaaaaa"
    """

Visible tests:
assert find_max(['name', 'of', 'string']) == 'string'
assert find_max(['name', 'enam', 'game']) == 'enam'
assert find_max(['aaaaaaa', 'bb', 'cc']) == 'aaaaaaa'
```

## Visible tests

```python
assert find_max(['name', 'of', 'string']) == 'string'
assert find_max(['name', 'enam', 'game']) == 'enam'
assert find_max(['aaaaaaa', 'bb', 'cc']) == 'aaaaaaa'
```
