# Mbpp/565

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 430 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 593 / 5822 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 815 / 2776 / 5122 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 1254 / 2678 / 3083 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 794 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to split a string into characters.
assert split('python') == ['p','y','t','h','o','n']
"""
```

## Visible tests

```python
assert split('python') == ['p','y','t','h','o','n']
```
