# Mbpp/11

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 7169 / 6862 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 5177 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 3056 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3052 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2938 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to remove first and last occurrence of a given character from the string.
assert remove_Occ("hello","l") == "heo"
"""
```

## Visible tests

```python
assert remove_Occ("hello","l") == "heo"
```
