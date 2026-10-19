# Mbpp/612

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 967 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 876 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 769 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 923 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 712 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function which takes a list of lists, where each sublist has two elements, and returns a list of two lists where the first list has the first element of each sublist and the second one has the second.
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
"""
```

## Visible tests

```python
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
```
