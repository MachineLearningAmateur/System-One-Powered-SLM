# Mbpp/94

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1166 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 1467 / 1285 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1516 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1076 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1324 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Given a list of tuples, write a function that returns the first value of the tuple with the smallest second value.
assert index_minimum([('Rash', 143), ('Manjeet', 200), ('Varsha', 100)]) == 'Varsha'
"""
```

## Visible tests

```python
assert index_minimum([('Rash', 143), ('Manjeet', 200), ('Varsha', 100)]) == 'Varsha'
```
