# Mbpp/300

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1841 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1500 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1768 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1240 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2044 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the count of all binary sequences of length 2n such that sum of first n bits is same as sum of last n bits.
assert math.isclose(count_binary_seq(1), 2.0, rel_tol=0.001)
"""
```

## Visible tests

```python
assert math.isclose(count_binary_seq(1), 2.0, rel_tol=0.001)
```
