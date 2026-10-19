# Mbpp/103

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2821 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2769 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 3040 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 3839 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the Eulerian number a(n, m).
assert eulerian_num(3, 1) == 4
"""
```

## Visible tests

```python
assert eulerian_num(3, 1) == 4
```
