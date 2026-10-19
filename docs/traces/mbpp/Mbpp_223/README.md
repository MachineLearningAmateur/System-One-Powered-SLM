# Mbpp/223

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 6114 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 5303 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 5546 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 5860 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that takes in a sorted array, its length (n), and an element and returns whether the element is the majority element in the given sorted array. (The majority element is the element that occurs more than n/2 times.)
assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
"""
```

## Visible tests

```python
assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
```
