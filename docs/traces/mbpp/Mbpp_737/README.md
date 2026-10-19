# Mbpp/737

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | visible pass | ✅ pass | 2268 / 3137 / 2041 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2066 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 8192 | 1 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2954 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to check whether the given string is starting with a vowel or not using regex.
assert check_str("annie")
"""
```

## Visible tests

```python
assert check_str("annie")
```
