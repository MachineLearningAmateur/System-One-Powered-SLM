# Mbpp/7

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 953 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 743 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 848 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1296 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 799 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find all words which are at least 4 characters long in a string.
assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
"""
```

## Visible tests

```python
assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
```
