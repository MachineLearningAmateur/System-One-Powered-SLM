# Mbpp/724

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1552 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1337 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1375 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1825 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1344 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes base and power as arguments and calculate the sum of all digits of the base to the specified power.
assert power_base_sum(2,100)==115
"""
```

## Visible tests

```python
assert power_base_sum(2,100)==115
```
