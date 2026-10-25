# Mbpp/3

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2130 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1794 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1824 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2923 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1528 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to identify non-prime numbers.
assert is_not_prime(2) == False
"""
```

## Visible tests

```python
assert is_not_prime(2) == False
```
