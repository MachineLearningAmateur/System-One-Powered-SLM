# HumanEval/53

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 404 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 650 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 342 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 420 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 564 | 0 |

## Prompt shown to the model (round 1)

```python


def add(x: int, y: int):
    """Add two numbers x and y
    >>> add(2, 3)
    5
    >>> add(5, 7)
    12
    """
```

## Visible tests

```python
assert add(2, 3) == 5
assert add(5, 7) == 12
```
