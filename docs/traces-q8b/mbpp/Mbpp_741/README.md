# Mbpp/741

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1135 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 4125 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1417 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 931 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1164 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to check whether all the characters are same or not.
assert all_Characters_Same("python") == False
"""
```

## Visible tests

```python
assert all_Characters_Same("python") == False
```
