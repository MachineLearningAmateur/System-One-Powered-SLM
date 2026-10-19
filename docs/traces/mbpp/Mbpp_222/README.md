# Mbpp/222

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1149 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1439 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1111 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1296 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1423 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check if all the elements in tuple have same data type or not.
assert check_type((5, 6, 7, 3, 5, 6) ) == True
"""
```

## Visible tests

```python
assert check_type((5, 6, 7, 3, 5, 6) ) == True
```
