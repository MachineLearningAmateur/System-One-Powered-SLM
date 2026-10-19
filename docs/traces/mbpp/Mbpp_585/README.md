# Mbpp/585

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1251 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1604 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 932 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1137 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1252 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the n most expensive items in a given dataset.
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}],1)==[{'name': 'Item-2', 'price': 555.22}]
"""
```

## Visible tests

```python
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}],1)==[{'name': 'Item-2', 'price': 555.22}]
```
