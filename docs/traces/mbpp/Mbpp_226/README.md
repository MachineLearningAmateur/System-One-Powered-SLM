# Mbpp/226

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 698 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 556 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 656 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 774 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 795 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to remove the characters which have odd index values of a given string.
assert odd_values_string('abcdef') == 'ace'
"""
```

## Visible tests

```python
assert odd_values_string('abcdef') == 'ace'
```
