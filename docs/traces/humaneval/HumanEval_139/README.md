# HumanEval/139

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2070 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2079 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2431 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2185 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3174 | 0 |

## Prompt shown to the model (round 1)

```python

def special_factorial(n):
    """The Brazilian factorial is defined as:
    brazilian_factorial(n) = n! * (n-1)! * (n-2)! * ... * 1!
    where n > 0

    For example:
    >>> special_factorial(4)
    288

    The function will receive an integer as input and should return the special
    factorial of this integer.
    """
```

## Visible tests

```python
assert special_factorial(4) == 288
```
