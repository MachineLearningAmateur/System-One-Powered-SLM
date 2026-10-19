# HumanEval/103

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ✅ pass | 2811 / 7359 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | ✅ pass | 8192 / 8192 / 2621 | 2 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | ✅ pass | 3541 / 5294 / 5131 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3535 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 2356 / 6955 | 0 |

## Prompt shown to the model (round 1)

```python

def rounded_avg(n, m):
    """You are given two positive integers n and m, and your task is to compute the
    average of the integers from n through m (including n and m). 
    Round the answer to the nearest integer and convert that to binary.
    If n is greater than m, return -1.
    Example:
    rounded_avg(1, 5) => "0b11"
    rounded_avg(7, 5) => -1
    rounded_avg(10, 20) => "0b1111"
    rounded_avg(20, 33) => "0b11010"
    """

Visible tests:
assert rounded_avg(1, 5) == '0b11'
assert rounded_avg(7, 13) == '0b1010'
assert rounded_avg(964, 977) == '0b1111001010'
```

## Visible tests

```python
assert rounded_avg(1, 5) == '0b11'
assert rounded_avg(7, 13) == '0b1010'
assert rounded_avg(964, 977) == '0b1111001010'
```
