# HumanEval/79

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 875 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 994 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1063 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1143 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 937 | 0 |

## Prompt shown to the model (round 1)

```python

def decimal_to_binary(decimal):
    """You will be given a number in decimal form and your task is to convert it to
    binary format. The function should return a string, with each character representing a binary
    number. Each character in the string will be '0' or '1'.

    There will be an extra couple of characters 'db' at the beginning and at the end of the string.
    The extra characters are there to help with the format.

    Examples:
    decimal_to_binary(15)   # returns "db1111db"
    decimal_to_binary(32)   # returns "db100000db"
    """

Visible tests:
assert decimal_to_binary(0) == 'db0db'
assert decimal_to_binary(32) == 'db100000db'
assert decimal_to_binary(103) == 'db1100111db'
```

## Visible tests

```python
assert decimal_to_binary(0) == 'db0db'
assert decimal_to_binary(32) == 'db100000db'
assert decimal_to_binary(103) == 'db1100111db'
```
