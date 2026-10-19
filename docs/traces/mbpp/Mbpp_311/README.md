# Mbpp/311

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 3363 | 2 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 3657 / 6942 | 1 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to set the left most unset bit.
assert set_left_most_unset_bit(10) == 14
"""
```

## Visible tests

```python
assert set_left_most_unset_bit(10) == 14
```
