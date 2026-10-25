# Mbpp/564

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 6070 / 3704 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 6080 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 5801 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 7832 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 3627 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function which takes a list of integers and counts the number of possible unordered pairs where both elements are unequal.
assert count_Pairs([1,2,1],3) == 2
"""
```

## Visible tests

```python
assert count_Pairs([1,2,1],3) == 2
```
