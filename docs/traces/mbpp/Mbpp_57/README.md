# Mbpp/57

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 1904 / 3241 / 3621 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3157 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1172 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2487 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 756 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to find the largest number that can be formed with the given list of digits.
assert find_Max_Num([1,2,3]) == 321
"""
```

## Visible tests

```python
assert find_Max_Num([1,2,3]) == 321
```
