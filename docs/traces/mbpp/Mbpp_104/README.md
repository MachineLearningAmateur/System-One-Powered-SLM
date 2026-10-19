# Mbpp/104

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 1331 / 4246 / 3470 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | 3442 / 3112 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1946 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1104 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 908 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort each sublist of strings in a given list of lists.
assert sort_sublists((["green", "orange"], ["black", "white"], ["white", "black", "orange"]))==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
"""
```

## Visible tests

```python
assert sort_sublists((["green", "orange"], ["black", "white"], ["white", "black", "orange"]))==[['green', 'orange'], ['black', 'white'], ['black', 'orange', 'white']]
```
