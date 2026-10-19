# Mbpp/754

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2161 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2116 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2279 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2086 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2433 | 0 |

## Prompt shown to the model (round 1)

```python
"""
We say that an element is common for lists l1, l2, l3 if it appears in all three lists under the same index. Write a function to find common elements from three lists. The function should return a list.
assert extract_index_list([1, 1, 3, 4, 5, 6, 7],[0, 1, 2, 3, 4, 5, 7],[0, 1, 2, 3, 4, 5, 7])==[1, 7]
"""
```

## Visible tests

```python
assert extract_index_list([1, 1, 3, 4, 5, 6, 7],[0, 1, 2, 3, 4, 5, 7],[0, 1, 2, 3, 4, 5, 7])==[1, 7]
```
