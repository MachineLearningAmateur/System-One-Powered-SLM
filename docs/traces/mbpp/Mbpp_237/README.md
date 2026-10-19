# Mbpp/237

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 4915 / 5982 / 4200 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 3735 / 2881 / 3676 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 5305 / 3843 / 2726 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 3321 / 3893 / 8192 | 1 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 4400 / 2426 / 2281 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a list of tuples and returns a dictionary mapping each unique tuple to the number of times it occurs in the list.
assert check_occurences([(3, 1), (1, 3), (2, 5), (5, 2), (6, 3)] ) == {(1, 3): 2, (2, 5): 2, (3, 6): 1}
"""
```

## Visible tests

```python
assert check_occurences([(3, 1), (1, 3), (2, 5), (5, 2), (6, 3)] ) == {(1, 3): 2, (2, 5): 2, (3, 6): 1}
```
