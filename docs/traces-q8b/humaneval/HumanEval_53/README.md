# HumanEval/53

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 763 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 483 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 517 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 695 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1146 | 0 |

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
