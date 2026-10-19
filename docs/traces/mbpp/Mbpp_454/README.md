# Mbpp/454

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 602 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 493 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 505 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 553 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 458 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that matches a word containing 'z'.
assert text_match_wordz("pythonz.")==True
"""
```

## Visible tests

```python
assert text_match_wordz("pythonz.")==True
```
