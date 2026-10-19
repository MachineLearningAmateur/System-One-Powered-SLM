# Mbpp/641

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | 8192 / 6693 / 7072 | 1 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 6921 / 7609 / 5026 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 7992 / 8192 / 8192 | 2 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 4527 / 5526 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the nth nonagonal number.
assert is_nonagonal(10) == 325
"""
```

## Visible tests

```python
assert is_nonagonal(10) == 325
```
