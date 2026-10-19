# HumanEval/47

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 7236 / 5837 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | 5952 / 7093 / 8168 | 0 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | 4199 / 8192 / 7276 | 1 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 3683 / 5086 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python


def median(l: list):
    """Return median of elements in the list l.
    >>> median([3, 1, 2, 4, 5])
    3
    >>> median([-10, 4, 6, 1000, 10, 20])
    15.0
    """
```

## Visible tests

```python
assert median([3, 1, 2, 4, 5]) == 3
assert median([-10, 4, 6, 1000, 10, 20]) == 15.0
```
