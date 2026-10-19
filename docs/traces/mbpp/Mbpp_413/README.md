# Mbpp/413

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1493 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 804 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1965 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1151 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1363 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to extract the nth element from a given list of tuples.
assert extract_nth_element([('Greyson Fulton', 98, 99), ('Brady Kent', 97, 96), ('Wyatt Knott', 91, 94), ('Beau Turnbull', 94, 98)] ,0)==['Greyson Fulton', 'Brady Kent', 'Wyatt Knott', 'Beau Turnbull']
"""
```

## Visible tests

```python
assert extract_nth_element([('Greyson Fulton', 98, 99), ('Brady Kent', 97, 96), ('Wyatt Knott', 91, 94), ('Beau Turnbull', 94, 98)] ,0)==['Greyson Fulton', 'Brady Kent', 'Wyatt Knott', 'Beau Turnbull']
```
