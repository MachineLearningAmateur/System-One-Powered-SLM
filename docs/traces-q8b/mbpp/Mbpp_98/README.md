# Mbpp/98

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3656 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1617 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 3674 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 3895 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3551 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to multiply all the numbers in a list and divide with the length of the list.
assert math.isclose(multiply_num((8, 2, 3, -1, 7)), -67.2, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(multiply_num((8, 2, 3, -1, 7)), -67.2, rel_tol=0.001)
```
