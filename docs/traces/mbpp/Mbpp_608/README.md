# Mbpp/608

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | 5859 / 301 / 551 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | 8192 / 7714 / 518 | 1 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 5598 / 925 / 617 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 5332 / 309 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find nth bell number.
assert bell_Number(2) == 2
"""
```

## Visible tests

```python
assert bell_Number(2) == 2
```
