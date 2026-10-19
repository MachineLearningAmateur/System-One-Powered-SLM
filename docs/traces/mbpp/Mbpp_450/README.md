# Mbpp/450

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1095 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 923 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1862 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 7346 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2652 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to extract specified size of strings from a given list of string values.
assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,8)==['practice', 'solution']
"""
```

## Visible tests

```python
assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,8)==['practice', 'solution']
```
