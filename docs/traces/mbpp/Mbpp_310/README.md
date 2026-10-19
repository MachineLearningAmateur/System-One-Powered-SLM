# Mbpp/310

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 1492 / 2337 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | 563 / 6559 / 3322 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 1526 / 1917 / 5064 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 695 / 3153 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 628 / 4270 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert a given string to a tuple of characters.
assert string_to_tuple("python 3.0")==('p', 'y', 't', 'h', 'o', 'n', '3', '.', '0')
"""
```

## Visible tests

```python
assert string_to_tuple("python 3.0")==('p', 'y', 't', 'h', 'o', 'n', '3', '.', '0')
```
