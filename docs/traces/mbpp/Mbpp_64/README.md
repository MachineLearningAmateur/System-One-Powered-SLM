# Mbpp/64

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 2 | visible pass | ✅ pass | 927 / 624 | 0 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | ❌ fail | 867 / 1354 / 2951 | 0 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | ❌ fail | 804 / 656 / 1640 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 765 | 0 |
| [Attempt 4](attempt_4.md) | 2 | visible pass | ✅ pass | 1049 / 459 | 0 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to sort a list of tuples using the second value of each tuple.
assert subject_marks([('English', 88), ('Science', 90), ('Maths', 97), ('Social sciences', 82)])==[('Social sciences', 82), ('English', 88), ('Science', 90), ('Maths', 97)]
"""
```

## Visible tests

```python
assert subject_marks([('English', 88), ('Science', 90), ('Maths', 97), ('Social sciences', 82)])==[('Social sciences', 82), ('English', 88), ('Science', 90), ('Maths', 97)]
```
