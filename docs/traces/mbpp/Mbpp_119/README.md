# Mbpp/119

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 2851 | 2 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 5385 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 7195 | 2 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the element that appears only once in a sorted array.
assert search([1,1,2,2,3]) == 3
"""
```

## Visible tests

```python
assert search([1,1,2,2,3]) == 3
```
