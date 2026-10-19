# Mbpp/397

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2198 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 819 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1749 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1847 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2104 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the median of three numbers.
assert median_numbers(25,55,65)==55.0
"""
```

## Visible tests

```python
assert median_numbers(25,55,65)==55.0
```
