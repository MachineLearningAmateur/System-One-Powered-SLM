# HumanEval/85

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 984 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 924 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 983 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1293 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1265 | 0 |

## Prompt shown to the model (round 1)

```python

def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..


    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """

Visible tests:
assert add([4, 88]) == 88
assert add([4, 5, 6, 7, 2, 122]) == 122
assert add([4, 0, 6, 7]) == 0
```

## Visible tests

```python
assert add([4, 88]) == 88
assert add([4, 5, 6, 7, 2, 122]) == 122
assert add([4, 0, 6, 7]) == 0
```
