# Mbpp/720

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1240 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 761 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 867 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 768 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 1025 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to add a dictionary to the tuple. The output should be a tuple.
assert add_dict_to_tuple((4, 5, 6), {"MSAM" : 1, "is" : 2, "best" : 3} ) == (4, 5, 6, {'MSAM': 1, 'is': 2, 'best': 3})
"""
```

## Visible tests

```python
assert add_dict_to_tuple((4, 5, 6), {"MSAM" : 1, "is" : 2, "best" : 3} ) == (4, 5, 6, {'MSAM': 1, 'is': 2, 'best': 3})
```
