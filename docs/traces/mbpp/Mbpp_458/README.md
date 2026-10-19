# Mbpp/458

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 326 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 477 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 441 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 368 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 406 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the area of a rectangle.
assert rectangle_area(10,20)==200
"""
```

## Visible tests

```python
assert rectangle_area(10,20)==200
```
