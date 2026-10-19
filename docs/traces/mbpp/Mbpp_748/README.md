# Mbpp/748

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 4887 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 6124 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 6102 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 5067 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 7697 / 4922 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to put spaces between words starting with capital letters in a given string.
assert capital_words_spaces("Python") == 'Python'
"""
```

## Visible tests

```python
assert capital_words_spaces("Python") == 'Python'
```
