# Mbpp/305

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | ❌ fail | 3200 / 4286 / 4058 | 0 |
| [Attempt 1](attempt_1.md) | 3 | visible pass | ✅ pass | 2708 / 4314 / 3193 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 1344 / 2849 / 3403 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | ❌ fail | 3210 / 6137 / 4717 | 0 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | ❌ fail | 2558 / 7563 / 3741 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to return two words from a list of words starting with letter 'p'.
assert start_withp(["Python PHP", "Java JavaScript", "c c++"])==('Python', 'PHP')
"""
```

## Visible tests

```python
assert start_withp(["Python PHP", "Java JavaScript", "c c++"])==('Python', 'PHP')
```
