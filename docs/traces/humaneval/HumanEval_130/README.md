# HumanEval/130

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python

def tri(n):
    """Everyone knows Fibonacci sequence, it was studied deeply by mathematicians in 
    the last couple centuries. However, what people don't know is Tribonacci sequence.
    Tribonacci sequence is defined by the recurrence:
    tri(1) = 3
    tri(n) = 1 + n / 2, if n is even.
    tri(n) =  tri(n - 1) + tri(n - 2) + tri(n + 1), if n is odd.
    For example:
    tri(2) = 1 + (2 / 2) = 2
    tri(4) = 3
    tri(3) = tri(2) + tri(1) + tri(4)
           = 2 + 3 + 3 = 8 
    You are given a non-negative integer number n, you have to a return a list of the 
    first n + 1 numbers of the Tribonacci sequence.
    Examples:
    tri(3) = [1, 3, 2, 8]
    """

Visible tests:
assert tri(3) == [1, 3, 2.0, 8.0]
assert tri(4) == [1, 3, 2.0, 8.0, 3.0]
assert tri(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]
```

## Visible tests

```python
assert tri(3) == [1, 3, 2.0, 8.0]
assert tri(4) == [1, 3, 2.0, 8.0, 3.0]
assert tri(5) == [1, 3, 2.0, 8.0, 3.0, 15.0]
```
