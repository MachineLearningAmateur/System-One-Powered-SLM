# HumanEval/91

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 4714 / 6276 / 6611 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 4070 / 6179 / 5984 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 5019 / 4718 / 7075 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 5026 / 8192 | 2 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python

def is_bored(S):
    """
    You'll be given a string of words, and your task is to count the number
    of boredoms. A boredom is a sentence that starts with the word "I".
    Sentences are delimited by '.', '?' or '!'.
   
    For example:
    >>> is_bored("Hello world")
    0
    >>> is_bored("The sky is blue. The sun is shining. I love this weather")
    1
    """
```

## Visible tests

```python
assert is_bored("Hello world") == 0
assert is_bored("The sky is blue. The sun is shining. I love this weather") == 1
```
