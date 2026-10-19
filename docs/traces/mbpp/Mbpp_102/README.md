# Mbpp/102

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | 2404 / 2796 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 890 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | 893 / 1774 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 906 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 1274 / 1397 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert a snake case string to camel case string.
assert snake_to_camel('python_program')=='PythonProgram'
"""
```

## Visible tests

```python
assert snake_to_camel('python_program')=='PythonProgram'
```
