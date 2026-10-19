# Mbpp/162

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 3770 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1718 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1253 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3023 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3439 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to calculate the sum (n - 2*i) from i=0 to n // 2, for instance n + (n-2) + (n-4)... (until n-x =< 0).
assert sum_series(6) == 12
"""
```

## Visible tests

```python
assert sum_series(6) == 12
```
