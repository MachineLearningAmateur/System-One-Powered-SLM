# Mbpp/91

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1011 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 923 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1060 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 646 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 865 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check if a string is present as a substring in a given list of string values.
assert find_substring(["red", "black", "white", "green", "orange"],"ack")==True
"""
```

## Visible tests

```python
assert find_substring(["red", "black", "white", "green", "orange"],"ack")==True
```
