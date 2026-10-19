# HumanEval/31

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2097 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2244 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1664 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2248 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2653 | 0 |

## Prompt shown to the model (round 1)

```python


def is_prime(n):
    """Return true if a given number is prime, and false otherwise.
    >>> is_prime(6)
    False
    >>> is_prime(101)
    True
    >>> is_prime(11)
    True
    >>> is_prime(13441)
    True
    >>> is_prime(61)
    True
    >>> is_prime(4)
    False
    >>> is_prime(1)
    False
    """
```

## Visible tests

```python
assert is_prime(6) == False
assert is_prime(101) == True
assert is_prime(11) == True
assert is_prime(13441) == True
assert is_prime(61) == True
assert is_prime(4) == False
assert is_prime(1) == False
```
