# Mbpp/596

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 628 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 658 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 699 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 562 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 982 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the size in bytes of the given tuple.
assert tuple_size(("A", 1, "B", 2, "C", 3) ) == sys.getsizeof(("A", 1, "B", 2, "C", 3))
"""
```

## Visible tests

```python
assert tuple_size(("A", 1, "B", 2, "C", 3) ) == sys.getsizeof(("A", 1, "B", 2, "C", 3))
```
