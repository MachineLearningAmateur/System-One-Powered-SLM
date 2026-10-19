# Mbpp/123

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 5650 / 8192 / 8192 | 2 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 7735 / 791 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 6359 / 8192 / 7593 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 4973 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sum all amicable numbers from 1 to a specified number.
assert amicable_numbers_sum(999)==504
"""
```

## Visible tests

```python
assert amicable_numbers_sum(999)==504
```
