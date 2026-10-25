# HumanEval/18

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2215 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2280 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2250 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3201 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2671 | 0 |

## Prompt shown to the model (round 1)

```python


def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given substring can be found in the original string. Count overlaping cases.
    >>> how_many_times('', 'a')
    0
    >>> how_many_times('aaa', 'a')
    3
    >>> how_many_times('aaaa', 'aa')
    3
    """
```

## Visible tests

```python
assert how_many_times('', 'a') == 0
assert how_many_times('aaa', 'a') == 3
assert how_many_times('aaaa', 'aa') == 3
```
