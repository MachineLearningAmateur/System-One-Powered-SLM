# Mbpp/430

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | visible pass | 8192 / 8192 / 7902 | 2 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the directrix of a parabola.
assert parabola_directrix(5,3,2)==-198
"""
```

## Visible tests

```python
assert parabola_directrix(5,3,2)==-198
```
