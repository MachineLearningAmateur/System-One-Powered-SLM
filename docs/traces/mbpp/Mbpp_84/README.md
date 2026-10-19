# Mbpp/84

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 4011 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 6346 / 8192 | 2 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 5909 | 2 |
| [Attempt 3](attempt_3.md) | 3 | visible pass | 8192 / 8192 / 3162 | 2 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 5630 / 6385 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the nth number in the newman conway sequence.
assert sequence(10) == 6
"""
```

## Visible tests

```python
assert sequence(10) == 6
```
