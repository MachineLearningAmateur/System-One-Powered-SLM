# Mbpp/421

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 922 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 1394 / 447 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 622 / 828 | 0 |
| [Attempt 3](attempt_3.md) | 2 | visible pass | 2669 / 614 | 0 |
| [Attempt 4](attempt_4.md) | 3 | visible pass | 2234 / 2360 / 2297 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to concatenate each element of tuple by the delimiter.
assert concatenate_tuple(("ID", "is", 4, "UTS") ) == 'ID-is-4-UTS'
"""
```

## Visible tests

```python
assert concatenate_tuple(("ID", "is", 4, "UTS") ) == 'ID-is-4-UTS'
```
