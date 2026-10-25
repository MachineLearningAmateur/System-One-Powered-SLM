# Mbpp/619

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2554 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2044 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ✅ pass | 3823 / 8192 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3689 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 4213 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to move all the numbers to the end of the given string.
assert move_num('I1love143you55three3000thousand') == 'Iloveyouthreethousand1143553000'
"""
```

## Visible tests

```python
assert move_num('I1love143you55three3000thousand') == 'Iloveyouthreethousand1143553000'
```
