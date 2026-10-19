# HumanEval/128

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1848 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1492 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2862 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1782 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1581 | 0 |

## Prompt shown to the model (round 1)

```python

def prod_signs(arr):
    """
    You are given an array arr of integers and you need to return
    sum of magnitudes of integers multiplied by product of all signs
    of each number in the array, represented by 1, -1 or 0.
    Note: return None for empty arr.

    Example:
    >>> prod_signs([1, 2, 2, -4]) == -9
    >>> prod_signs([0, 1]) == 0
    >>> prod_signs([]) == None
    """
```

## Visible tests

```python
assert prod_signs([1, 2, 2, -4]) == -9
assert prod_signs([0, 1]) == 0
assert prod_signs([]) == None
```
