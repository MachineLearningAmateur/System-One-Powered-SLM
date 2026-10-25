# Mbpp/585

Benchmark: mbpp+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 899 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 1155 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 946 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 1286 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 868 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the n most expensive items in a given dataset.
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}],1)==[{'name': 'Item-2', 'price': 555.22}]
"""
```

## Visible tests

```python
assert expensive_items([{'name': 'Item-1', 'price': 101.1},{'name': 'Item-2', 'price': 555.22}],1)==[{'name': 'Item-2', 'price': 555.22}]
```
