# Mbpp/619

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2207 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2513 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1816 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2260 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3150 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to move all the numbers to the end of the given string.
assert move_num('I1love143you55three3000thousand') == 'Iloveyouthreethousand1143553000'
"""
```

## Visible tests

```python
assert move_num('I1love143you55three3000thousand') == 'Iloveyouthreethousand1143553000'
```
