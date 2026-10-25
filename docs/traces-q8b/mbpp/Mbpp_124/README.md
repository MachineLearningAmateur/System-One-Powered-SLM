# Mbpp/124

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 6726 / 8192 / 1385 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 7273 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 8192 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 8017 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to get the angle of a complex number.
assert math.isclose(angle_complex(0,1j), 1.5707963267948966, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(angle_complex(0,1j), 1.5707963267948966, rel_tol=0.001)
```
