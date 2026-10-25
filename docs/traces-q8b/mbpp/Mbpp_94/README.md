# Mbpp/94

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 856 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1483 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1481 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1147 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1745 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Given a list of tuples, write a function that returns the first value of the tuple with the smallest second value.
assert index_minimum([('Rash', 143), ('Manjeet', 200), ('Varsha', 100)]) == 'Varsha'
"""
```

## Visible tests

```python
assert index_minimum([('Rash', 143), ('Manjeet', 200), ('Varsha', 100)]) == 'Varsha'
```
