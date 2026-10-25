# Mbpp/586

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1948 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1511 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2194 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1396 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2156 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to split a list at the nth eelment and add the first part to the end.
assert split_Arr([12,10,5,6,52,36],2) == [5,6,52,36,12,10]
"""
```

## Visible tests

```python
assert split_Arr([12,10,5,6,52,36],2) == [5,6,52,36,12,10]
```
