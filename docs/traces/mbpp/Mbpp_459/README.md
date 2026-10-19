# Mbpp/459

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1844 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1384 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1438 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1470 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1303 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to remove uppercase substrings from a given string.
assert remove_uppercase('cAstyoUrFavoRitETVshoWs') == 'cstyoravoitshos'
"""
```

## Visible tests

```python
assert remove_uppercase('cAstyoUrFavoRitETVshoWs') == 'cstyoravoitshos'
```
