# Mbpp/412

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 684 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 453 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 736 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 699 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 625 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to remove odd numbers from a given list.
assert remove_odd([1,2,3]) == [2]
"""
```

## Visible tests

```python
assert remove_odd([1,2,3]) == [2]
```
