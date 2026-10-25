# Mbpp/310

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 2493 / 5505 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 2008 / 5243 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 1159 / 5777 / 3113 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 6358 / 4466 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 2617 / 5259 / 4027 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert a given string to a tuple of characters.
assert string_to_tuple("python 3.0")==('p', 'y', 't', 'h', 'o', 'n', '3', '.', '0')
"""
```

## Visible tests

```python
assert string_to_tuple("python 3.0")==('p', 'y', 't', 'h', 'o', 'n', '3', '.', '0')
```
