# Mbpp/451

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 647 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3496 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1664 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 675 / 762 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 4160 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove all whitespaces from the given string.
assert remove_whitespaces(' Google    Flutter ') == 'GoogleFlutter'
"""
```

## Visible tests

```python
assert remove_whitespaces(' Google    Flutter ') == 'GoogleFlutter'
```
