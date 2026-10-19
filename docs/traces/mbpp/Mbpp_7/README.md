# Mbpp/7

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 953 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 743 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 848 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1296 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 799 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find all words which are at least 4 characters long in a string.
assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
"""
```

## Visible tests

```python
assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
```
