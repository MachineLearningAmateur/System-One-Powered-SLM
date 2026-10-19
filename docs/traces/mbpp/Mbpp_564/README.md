# Mbpp/564

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 3916 / 3870 / 2346 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 4221 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 3429 / 2370 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 2895 / 4255 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 5322 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function which takes a list of integers and counts the number of possible unordered pairs where both elements are unequal.
assert count_Pairs([1,2,1],3) == 2
"""
```

## Visible tests

```python
assert count_Pairs([1,2,1],3) == 2
```
