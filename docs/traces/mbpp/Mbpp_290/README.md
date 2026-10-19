# Mbpp/290

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2228 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3786 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2082 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3835 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2835 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the list of maximum length in a list of lists.
assert max_length([[0], [1, 3], [5, 7], [9, 11], [13, 15, 17]])==(3, [13, 15, 17])
"""
```

## Visible tests

```python
assert max_length([[0], [1, 3], [5, 7], [9, 11], [13, 15, 17]])==(3, [13, 15, 17])
```
