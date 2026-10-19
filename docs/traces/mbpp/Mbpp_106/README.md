# Mbpp/106

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ✅ pass | 976 / 502 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 1478 / 6536 / 488 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 387 | 0 |
| [Attempt 3](attempt_3.md) | 3 | visible pass | ✅ pass | 1022 / 5281 / 558 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 604 / 387 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to append the given list to the given tuples.
assert add_lists([5, 6, 7], (9, 10)) == (9, 10, 5, 6, 7)
"""
```

## Visible tests

```python
assert add_lists([5, 6, 7], (9, 10)) == (9, 10, 5, 6, 7)
```
