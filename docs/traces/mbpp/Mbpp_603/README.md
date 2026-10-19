# Mbpp/603

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 3228 / 4083 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 7273 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 3855 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2431 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2631 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to get all lucid numbers smaller than or equal to a given integer.
assert get_ludic(10) == [1, 2, 3, 5, 7]
"""
```

## Visible tests

```python
assert get_ludic(10) == [1, 2, 3, 5, 7]
```
