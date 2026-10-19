# Mbpp/765

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 7799 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 6838 / 6340 | 1 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | 8192 / 8192 / 3964 | 2 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 7070 / 8192 / 8192 | 2 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find nth polite number. geeksforgeeks.org/n-th-polite-number/
assert is_polite(7) == 11
"""
```

## Visible tests

```python
assert is_polite(7) == 11
```
