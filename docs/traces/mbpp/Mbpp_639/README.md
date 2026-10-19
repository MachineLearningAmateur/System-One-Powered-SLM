# Mbpp/639

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2174 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 865 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2303 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1107 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1535 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sum the length of the names of a given list of names after removing the names that start with a lowercase letter.
assert sample_nam(['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'])==16
"""
```

## Visible tests

```python
assert sample_nam(['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'])==16
```
