# Mbpp/6

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1513 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1144 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1121 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1057 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1157 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to check whether the two numbers differ at one bit position only or not.
assert differ_At_One_Bit_Pos(13,9) == True
"""
```

## Visible tests

```python
assert differ_At_One_Bit_Pos(13,9) == True
```
