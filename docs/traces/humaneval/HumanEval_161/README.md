# HumanEval/161

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 1459 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1578 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 1500 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1536 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 2164 | 0 |

## Prompt shown to the model (round 1)

```python

def solve(s):
    """You are given a string s.
    if s[i] is a letter, reverse its case from lower to upper or vise versa, 
    otherwise keep it as it is.
    If the string contains no letters, reverse the string.
    The function should return the resulted string.
    Examples
    solve("1234") = "4321"
    solve("ab") = "AB"
    solve("#a@C") = "#A@c"
    """

Visible tests:
assert solve('AsDf') == 'aSdF'
assert solve('1234') == '4321'
assert solve('ab') == 'AB'
```

## Visible tests

```python
assert solve('AsDf') == 'aSdF'
assert solve('1234') == '4321'
assert solve('ab') == 'AB'
```
