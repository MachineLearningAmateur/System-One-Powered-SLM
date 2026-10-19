# HumanEval/149

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

"Hidden tests" is the result of the attempt's final code on the full EvalPlus suite, without frontier help. ⚠️ marks code that passed the visible tests but fails the hidden tests: the case the routers try to catch.

| Attempt | Rounds | End | Hidden tests (final code) | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | ✅ pass | 7194 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | ✅ pass | 7634 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | ✅ pass | 1587 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | ❌ fail ⚠️ visible pass | 2807 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | ✅ pass | 3495 | 0 |

## Prompt shown to the model (round 1)

```python

def sorted_list_sum(lst):
    """Write a function that accepts a list of strings as a parameter,
    deletes the strings that have odd lengths from it,
    and returns the resulted list with a sorted order,
    The list is always a list of strings and never an array of numbers,
    and it may contain duplicates.
    The order of the list should be ascending by length of each word, and you
    should return the list sorted by that rule.
    If two words have the same length, sort the list alphabetically.
    The function should return a list of strings in sorted order.
    You may assume that all words will have the same length.
    For example:
    assert list_sort(["aa", "a", "aaa"]) => ["aa"]
    assert list_sort(["ab", "a", "aaa", "cd"]) => ["ab", "cd"]
    """

Visible tests:
assert sorted_list_sum(['aa', 'a', 'aaa']) == ['aa']
assert sorted_list_sum(['school', 'AI', 'asdf', 'b']) == ['AI', 'asdf', 'school']
assert sorted_list_sum(['d', 'b', 'c', 'a']) == []
```

## Visible tests

```python
assert sorted_list_sum(['aa', 'a', 'aaa']) == ['aa']
assert sorted_list_sum(['school', 'AI', 'asdf', 'b']) == ['AI', 'asdf', 'school']
assert sorted_list_sum(['d', 'b', 'c', 'a']) == []
```
