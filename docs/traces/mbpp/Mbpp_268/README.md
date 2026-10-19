# Mbpp/268

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | ✅ pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 8192 / 663 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 8192 | 1 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 8192 / 6334 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 3922 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the n'th star number.
assert find_star_num(3) == 37
"""
```

## Visible tests

```python
assert find_star_num(3) == 37
```
