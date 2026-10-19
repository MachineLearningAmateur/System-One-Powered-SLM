# HumanEval/27

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1019 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1293 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1282 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1796 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1292 | 0 |

## Prompt shown to the model (round 1)

```python


def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """
```

## Visible tests

```python
assert flip_case('Hello') == 'hELLO'
```
