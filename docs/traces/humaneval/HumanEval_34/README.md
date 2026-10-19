# HumanEval/34

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1055 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1286 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1389 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1319 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1191 | 0 |

## Prompt shown to the model (round 1)

```python


def unique(l: list):
    """Return sorted unique elements in a list
    >>> unique([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [0, 2, 3, 5, 9, 123]
    """
```

## Visible tests

```python
assert unique([5, 3, 5, 2, 3, 3, 9, 0, 123]) == [0, 2, 3, 5, 9, 123]
```
