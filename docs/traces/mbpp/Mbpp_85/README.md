# Mbpp/85

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 578 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 853 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 701 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 639 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1035 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the surface area of a sphere.
assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)
```
