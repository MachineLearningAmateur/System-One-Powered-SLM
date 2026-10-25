# Mbpp/75

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1291 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1853 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1585 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1172 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2405 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find tuples which have all elements divisible by k from the given list of tuples.
assert find_tuples([(6, 24, 12), (7, 9, 6), (12, 18, 21)], 6) == [(6, 24, 12)]
"""
```

## Visible tests

```python
assert find_tuples([(6, 24, 12), (7, 9, 6), (12, 18, 21)], 6) == [(6, 24, 12)]
```
