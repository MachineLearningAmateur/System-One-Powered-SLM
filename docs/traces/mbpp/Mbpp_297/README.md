# Mbpp/297

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1260 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1606 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1553 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1257 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 1435 / 640 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to flatten a given nested list structure.
assert flatten_list([0, 10, [20, 30], 40, 50, [60, 70, 80], [90, 100, 110, 120]])==[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
"""
```

## Visible tests

```python
assert flatten_list([0, 10, [20, 30], 40, 50, [60, 70, 80], [90, 100, 110, 120]])==[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
```
