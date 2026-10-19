# Mbpp/722

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2759 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2421 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 3445 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 2313 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | 921 / 2488 | 0 |

## Prompt shown to the model (round 1)

```python
"""
The input is given as - a dictionary with a student name as a key and a tuple of float (student_height, student_weight) as a value, - minimal height, - minimal weight. Write a function to filter students that have height and weight above the minimum.
assert filter_data({'Cierra Vega': (6.2, 70), 'Alden Cantrell': (5.9, 65), 'Kierra Gentry': (6.0, 68), 'Pierre Cox': (5.8, 66)},6.0,70)=={'Cierra Vega': (6.2, 70)}
"""
```

## Visible tests

```python
assert filter_data({'Cierra Vega': (6.2, 70), 'Alden Cantrell': (5.9, 65), 'Kierra Gentry': (6.0, 68), 'Pierre Cox': (5.8, 66)},6.0,70)=={'Cierra Vega': (6.2, 70)}
```
