# Mbpp/773

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1748 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1348 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1830 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1138 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1887 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the occurrence and position of the substrings within a string. Return None if there is no match.
assert occurance_substring('python programming, python language','python')==('python', 0, 6)
"""
```

## Visible tests

```python
assert occurance_substring('python programming, python language','python')==('python', 0, 6)
```
