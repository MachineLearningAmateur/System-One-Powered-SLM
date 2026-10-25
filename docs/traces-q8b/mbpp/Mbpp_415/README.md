# Mbpp/415

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 4840 / 325 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 5687 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 7208 / 325 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 6012 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ❌ fail ⚠️ visible pass | 6163 / 796 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find a pair with highest product from a given array of integers.
assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
"""
```

## Visible tests

```python
assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
```
