# HumanEval/18

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2096 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2360 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2900 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3281 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2310 | 0 |

## Prompt shown to the model (round 1)

```python


def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlaping cases.
    >>> how_many_times('', 'a')
    0
    >>> how_many_times('aaa', 'a')
    3
    >>> how_many_times('aaaa', 'aa')
    3
    """
```

## Visible tests

```python
assert how_many_times('', 'a') == 0
assert how_many_times('aaa', 'a') == 3
assert how_many_times('aaaa', 'aa') == 3
```
