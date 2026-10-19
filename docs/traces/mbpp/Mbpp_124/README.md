# Mbpp/124

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 1285 / 8192 / 2194 | 1 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 2851 / 2925 / 8192 | 1 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 2078 / 650 / 1847 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 1550 / 1165 / 3190 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 7905 / 1570 / 1455 | 0 |

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
