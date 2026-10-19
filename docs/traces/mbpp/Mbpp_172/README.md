# Mbpp/172

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1998 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3072 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1753 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 919 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2199 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to count the number of occurence of the string 'std' in a given string.
assert count_occurance("letstdlenstdporstd") == 3
"""
```

## Visible tests

```python
assert count_occurance("letstdlenstdporstd") == 3
```
