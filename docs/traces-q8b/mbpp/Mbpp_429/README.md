# Mbpp/429

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1180 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1069 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 980 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1093 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2282 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to extract the elementwise and tuples from the given two tuples.
assert and_tuples((10, 4, 6, 9), (5, 2, 3, 3)) == (0, 0, 2, 1)
"""
```

## Visible tests

```python
assert and_tuples((10, 4, 6, 9), (5, 2, 3, 3)) == (0, 0, 2, 1)
```
