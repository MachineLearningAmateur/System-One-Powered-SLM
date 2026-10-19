# Mbpp/799

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 5146 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 6880 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3648 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3936 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to that rotate left bits by d bits a given number. We assume that the number is 32 bit.
assert left_rotate(16,2) == 64
"""
```

## Visible tests

```python
assert left_rotate(16,2) == 64
```
