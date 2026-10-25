# Mbpp/172

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2198 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2319 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1790 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2369 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2613 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to count the number of occurence of the string 'std' in a given string.
assert count_occurance("letstdlenstdporstd") == 3
"""
```

## Visible tests

```python
assert count_occurance("letstdlenstdporstd") == 3
```
