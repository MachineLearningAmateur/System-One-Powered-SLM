# Mbpp/590

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 5737 / 6568 / 8192 | 1 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 7376 / 8192 | 2 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 6442 / 5743 / 7391 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 5414 / 8192 / 7759 | 1 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 6140 / 8177 / 8192 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to convert polar coordinates to rectangular coordinates.
assert polar_rect(3,4)==((5.0, 0.9272952180016122), (-2+2.4492935982947064e-16j))
"""
```

## Visible tests

```python
assert polar_rect(3,4)==((5.0, 0.9272952180016122), (-2+2.4492935982947064e-16j))
```
