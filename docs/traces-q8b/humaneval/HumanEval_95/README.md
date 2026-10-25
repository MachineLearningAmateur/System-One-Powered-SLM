# HumanEval/95

Benchmark: humaneval+. Run: `q8b-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 3044 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 2674 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 2244 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ✅ pass | 2858 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 2828 | 0 |

## Prompt shown to the model (round 1)

```python

def check_dict_case(dict):
    """
    Given a dictionary, return True if all keys are strings in lower 
    case or all keys are strings in upper case, else return False.
    The function should return False is the given dictionary is empty.
    Examples:
    check_dict_case({"a":"apple", "b":"banana"}) should return True.
    check_dict_case({"a":"apple", "A":"banana", "B":"banana"}) should return False.
    check_dict_case({"a":"apple", 8:"banana", "a":"apple"}) should return False.
    check_dict_case({"Name":"John", "Age":"36", "City":"Houston"}) should return False.
    check_dict_case({"STATE":"NC", "ZIP":"12345" }) should return True.
    """

Visible tests:
assert check_dict_case({'p': 'pineapple', 'b': 'banana'}) == True
assert check_dict_case({'p': 'pineapple', 'b': 'banana'}) == True
assert check_dict_case({'p': 'pineapple', 'A': 'banana', 'B': 'banana'}) == False
```

## Visible tests

```python
assert check_dict_case({'p': 'pineapple', 'b': 'banana'}) == True
assert check_dict_case({'p': 'pineapple', 'b': 'banana'}) == True
assert check_dict_case({'p': 'pineapple', 'A': 'banana', 'B': 'banana'}) == False
```
