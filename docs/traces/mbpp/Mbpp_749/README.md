# Mbpp/749

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 2256 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1664 | 0 |
| [Attempt 2](attempt_2.md) | 2 | visible pass | ✅ pass | 1598 / 1164 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1615 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2122 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a given list of strings of numbers numerically. 
assert sort_numeric_strings( ['4','12','45','7','0','100','200','-12','-500'])==[-500, -12, 0, 4, 7, 12, 45, 100, 200]
"""
```

## Visible tests

```python
assert sort_numeric_strings( ['4','12','45','7','0','100','200','-12','-500'])==[-500, -12, 0, 4, 7, 12, 45, 100, 200]
```
