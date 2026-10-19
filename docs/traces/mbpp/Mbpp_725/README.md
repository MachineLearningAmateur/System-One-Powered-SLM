# Mbpp/725

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1911 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1513 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1400 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1429 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1593 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to extract values between quotation marks " " of the given string.
assert extract_quotation('Cortex "A53" Based "multi" tasking "Processor"') == ['A53', 'multi', 'Processor']
"""
```

## Visible tests

```python
assert extract_quotation('Cortex "A53" Based "multi" tasking "Processor"') == ['A53', 'multi', 'Processor']
```
