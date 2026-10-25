# Mbpp/18

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1570 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2443 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2422 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1032 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1197 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove characters from the first string which are present in the second string.
assert remove_dirty_chars("probasscurve", "pros") == 'bacuve'
"""
```

## Visible tests

```python
assert remove_dirty_chars("probasscurve", "pros") == 'bacuve'
```
