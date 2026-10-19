# Mbpp/607

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2936 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2577 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 8192 / 4154 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3442 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2671 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to search a string for a regex pattern. The function should return the matching subtring, a start index and an end index.
assert find_literals('The quick brown fox jumps over the lazy dog.', 'fox') == ('fox', 16, 19)
"""
```

## Visible tests

```python
assert find_literals('The quick brown fox jumps over the lazy dog.', 'fox') == ('fox', 16, 19)
```
