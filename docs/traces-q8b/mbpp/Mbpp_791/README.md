# Mbpp/791

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 4932 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2904 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 4755 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3689 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3528 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove tuples from the given tuple.
assert remove_nested((1, 5, 7, (4, 6), 10)) == (1, 5, 7, 10)
"""
```

## Visible tests

```python
assert remove_nested((1, 5, 7, (4, 6), 10)) == (1, 5, 7, 10)
```
