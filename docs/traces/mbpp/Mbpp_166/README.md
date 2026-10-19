# Mbpp/166

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1254 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1133 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1139 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 936 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1212 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that counts the number of pairs of integers in a list that xor to an even number.
assert find_even_pair([5, 4, 7, 2, 1]) == 4
"""
```

## Visible tests

```python
assert find_even_pair([5, 4, 7, 2, 1]) == 4
```
