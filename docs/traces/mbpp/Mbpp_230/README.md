# Mbpp/230

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1116 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1409 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 772 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 778 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1013 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a string and character, replaces blank spaces in the string with the character, and returns the string.
assert replace_blank("hello people",'@')==("hello@people")
"""
```

## Visible tests

```python
assert replace_blank("hello people",'@')==("hello@people")
```
