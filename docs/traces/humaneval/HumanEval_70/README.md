# HumanEval/70

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 3040 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 4257 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 4154 | 0 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 2904 / 4085 / 3377 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 3325 | 0 |

## Prompt shown to the model (round 1)

```python

def strange_sort_list(lst):
    '''
    Given list of integers, return list in strange order.
    Strange sorting, is when you start with the minimum value,
    then maximum of the remaining integers, then minimum and so on.

    Examples:
    strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
    strange_sort_list([5, 5, 5, 5]) == [5, 5, 5, 5]
    strange_sort_list([]) == []
    '''

Visible tests:
assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
assert strange_sort_list([5, 6, 7, 8, 9]) == [5, 9, 6, 8, 7]
assert strange_sort_list([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]
```

## Visible tests

```python
assert strange_sort_list([1, 2, 3, 4]) == [1, 4, 2, 3]
assert strange_sort_list([5, 6, 7, 8, 9]) == [5, 9, 6, 8, 7]
assert strange_sort_list([1, 2, 3, 4, 5]) == [1, 5, 2, 4, 3]
```
