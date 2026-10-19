# HumanEval/23

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 409 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 348 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 410 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 331 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 348 | 0 |

## Prompt shown to the model (round 1)

```python


def strlen(string: str) -> int:
    """ Return length of given string
    >>> strlen('')
    0
    >>> strlen('abc')
    3
    """
```

## Visible tests

```python
assert strlen('') == 0
assert strlen('abc') == 3
```
