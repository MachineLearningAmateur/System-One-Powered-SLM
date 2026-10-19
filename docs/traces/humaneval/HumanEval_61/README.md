# HumanEval/61

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 981 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 2340 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1114 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1142 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 983 | 0 |

## Prompt shown to the model (round 1)

```python


def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
```

## Visible tests

```python
assert correct_bracketing("(") == False
assert correct_bracketing("()") == True
assert correct_bracketing("(()())") == True
assert correct_bracketing(")(()") == False
```
