# Mbpp/787

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1280 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 4281 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 1328 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2135 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 6359 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that matches a string that has an a followed by three 'b'.
assert not text_match_three("ac")
"""
```

## Visible tests

```python
assert not text_match_three("ac")
```
