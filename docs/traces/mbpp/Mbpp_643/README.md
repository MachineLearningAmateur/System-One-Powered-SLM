# Mbpp/643

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2437 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3101 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2925 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 4273 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2508 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function that checks if a strings contains 'z', except at the start and end of the word.
assert text_match_wordz_middle("pythonzabc.")==True
"""
```

## Visible tests

```python
assert text_match_wordz_middle("pythonzabc.")==True
```
