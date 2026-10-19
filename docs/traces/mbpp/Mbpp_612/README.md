# Mbpp/612

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 967 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 876 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 769 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 923 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 712 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function which takes a list of lists, where each sublist has two elements, and returns a list of two lists where the first list has the first element of each sublist and the second one has the second.
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
"""
```

## Visible tests

```python
assert merge([['x', 'y'], ['a', 'b'], ['m', 'n']]) == [['x', 'a', 'm'], ['y', 'b', 'n']]
```
