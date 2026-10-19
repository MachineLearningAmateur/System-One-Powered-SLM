# HumanEval/15

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 803 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 892 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 920 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 889 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 968 | 0 |

## Prompt shown to the model (round 1)

```python


def string_sequence(n: int) -> str:
    """ Return a string containing space-delimited numbers starting from 0 upto n inclusive.
    >>> string_sequence(0)
    '0'
    >>> string_sequence(5)
    '0 1 2 3 4 5'
    """
```

## Visible tests

```python
assert string_sequence(0) == '0'
assert string_sequence(5) == '0 1 2 3 4 5'
```
