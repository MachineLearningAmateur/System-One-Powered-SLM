# Mbpp/720

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1060 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 6854 / 2276 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1011 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1793 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 1666 / 1007 | 0 |

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
