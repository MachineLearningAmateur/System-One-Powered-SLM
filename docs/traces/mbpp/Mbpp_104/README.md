# Mbpp/104

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 1331 / 4246 / 3470 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 3442 / 3112 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1946 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1104 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 908 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort each sublist of strings in a given list of lists.
assert sort_sublists((["green", "orange"], ["black", "white"], ["white", "black", "orange"]))==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
"""
```

## Visible tests

```python
assert sort_sublists((["green", "orange"], ["black", "white"], ["white", "black", "orange"]))==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
```
