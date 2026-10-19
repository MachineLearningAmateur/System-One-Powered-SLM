# Mbpp/390

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1367 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 997 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1081 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 847 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 782 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to apply a given format string to all of the elements in a list.
assert add_string([1,2,3,4],'temp{0}')==['temp1', 'temp2', 'temp3', 'temp4']
"""
```

## Visible tests

```python
assert add_string([1,2,3,4],'temp{0}')==['temp1', 'temp2', 'temp3', 'temp4']
```
