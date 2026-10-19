# Mbpp/82

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 917 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1115 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1079 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 967 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 846 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the volume of a sphere.
assert math.isclose(volume_sphere(10), 4188.790204786391, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(volume_sphere(10), 4188.790204786391, rel_tol=0.001)
```
