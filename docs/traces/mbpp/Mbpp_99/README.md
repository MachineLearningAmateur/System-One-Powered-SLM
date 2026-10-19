# Mbpp/99

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1227 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 532 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 863 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 711 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 789 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert the given decimal number to its binary equivalent, represented as a string with no leading zeros.
assert decimal_to_binary(8) == '1000'
"""
```

## Visible tests

```python
assert decimal_to_binary(8) == '1000'
```
