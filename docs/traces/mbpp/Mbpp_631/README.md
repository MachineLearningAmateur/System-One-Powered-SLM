# Mbpp/631

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1521 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1792 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1156 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1289 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1350 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to replace whitespaces with an underscore and vice versa in a given string.
assert replace_spaces('Jumanji The Jungle') == 'Jumanji_The_Jungle'
"""
```

## Visible tests

```python
assert replace_spaces('Jumanji The Jungle') == 'Jumanji_The_Jungle'
```
