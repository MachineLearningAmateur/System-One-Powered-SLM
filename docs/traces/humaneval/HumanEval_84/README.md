# HumanEval/84

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3142 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 4333 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ✅ pass | 8192 / 2228 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1994 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 8192 / 5903 | 1 |

## Prompt shown to the model (round 1)

```python

def solve(N):
    """Given a positive integer N, return the total sum of its digits in binary.
    
    Example
        For N = 1000, the sum of digits will be 1 the output should be "1".
        For N = 150, the sum of digits will be 6 the output should be "110".
        For N = 147, the sum of digits will be 12 the output should be "1100".
    
    Variables:
        @N integer
             Constraints: 0 ≤ N ≤ 10000.
    Output:
         a string of binary number
    """

Visible tests:
assert solve(1000) == '1'
assert solve(150) == '110'
assert solve(147) == '1100'
```

## Visible tests

```python
assert solve(1000) == '1'
assert solve(150) == '110'
assert solve(147) == '1100'
```
