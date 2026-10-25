# Mbpp/139

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1209 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1758 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1747 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3002 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2055 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the circumference of a circle.
assert math.isclose(circle_circumference(10), 62.830000000000005, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(circle_circumference(10), 62.830000000000005, rel_tol=0.001)
```
