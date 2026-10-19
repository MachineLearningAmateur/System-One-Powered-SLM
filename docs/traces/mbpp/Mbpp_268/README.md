# Mbpp/268

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 8192 / 663 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 8192 / 6334 | 1 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3922 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the n'th star number.
assert find_star_num(3) == 37
"""
```

## Visible tests

```python
assert find_star_num(3) == 37
```
