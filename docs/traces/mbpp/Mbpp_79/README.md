# Mbpp/79

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 1896 | 0 |
| [Attempt 1](attempt_1.md) | 2 | visible pass | ✅ pass | 913 / 597 | 0 |
| [Attempt 2](attempt_2.md) | 3 | visible pass | ✅ pass | 2435 / 3405 / 2400 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 555 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 564 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a python function to check whether the length of the word is odd or not.
assert word_len("Hadoop") == False
"""
```

## Visible tests

```python
assert word_len("Hadoop") == False
```
