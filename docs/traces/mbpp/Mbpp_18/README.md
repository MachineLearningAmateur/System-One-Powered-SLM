# Mbpp/18

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1273 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1653 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1402 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1177 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 981 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove characters from the first string which are present in the second string.
assert remove_dirty_chars("probasscurve", "pros") == 'bacuve'
"""
```

## Visible tests

```python
assert remove_dirty_chars("probasscurve", "pros") == 'bacuve'
```
