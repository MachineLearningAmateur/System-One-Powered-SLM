# Mbpp/603

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 3735 | 1 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 8192 | 2 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 8192 | 2 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to get all lucid numbers smaller than or equal to a given integer.
assert get_ludic(10) == [1, 2, 3, 5, 7]
"""
```

## Visible tests

```python
assert get_ludic(10) == [1, 2, 3, 5, 7]
```
