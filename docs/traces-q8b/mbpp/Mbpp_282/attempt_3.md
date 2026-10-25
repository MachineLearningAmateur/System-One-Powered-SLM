# Mbpp/282, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/282/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 811. Answer tokens: 32.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called sub_list that subtracts two lists element-wise. Let's see. The assertion given is that when you subtract [4,5,6] from [1,2,3], you get [-3,-3,-3]. So each element in the first list is subtracted by the corresponding element in the second list.

First, I should check that both lists are of the same length. Wait, but the problem statement doesn't mention handling cases where the lists are different lengths. Oh, but the example given has lists of the same length. Maybe the function assumes that the input lists are of equal length. But maybe I should handle that? Wait, the problem says to subtract element-wise, so perhaps the function is expected to work only when the lists are the same length. But maybe the problem expects that the user will pass lists of the same length. So perhaps I don't need to handle that case. But maybe I should? Hmm. Well, the problem's sample input has equal length lists, and the function is supposed to return a list of the same length. So perhaps the function is intended to work only when the lists are of the same length. So I can proceed under that assumption.

So, the approach is: iterate through each pair of elements from the two lists, subtract the second list's element from the first, and collect the results into a new list.

How to do that in Python. Let's think. For example, for list1 and list2, the result is [a - b for a, b in zip(list1, list2)].

Wait, yes. Because zip will pair the elements from both lists. So if list1 is [1,2,3] and list2 is [4,5,6], then zip gives (1,4), (2,5), (3,6). Then for each pair, subtract the second element from the first. So 1-4 is -3, etc. So the list comprehension would work.

So the function can be written as:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

Wait, but wait. Wait, the problem says subtract two lists element-wise. So the function is supposed to subtract list2 from list1. So the result is list1[i] - list2[i] for each i. So yes, that's exactly what the list comprehension does.

Testing the sample input: sub_list([1,2,3], [4,5,6]) would give [1-4, 2-5, 3-6] which is [-3, -3, -3], which matches the assertion.

So that's the code. But what about if the lists are of different lengths? Well, zip stops at the shorter one. But the problem's example uses same-length lists. So perhaps the function is intended to work only when the lists are of the same length. So the code is correct.

So the code would be:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

But wait, the problem says to write the function. So that's the code. Let me check if there are any edge cases. For example, empty lists? Well, if both are empty, returns an empty list. But the problem's sample input is non-empty. But the function would handle that.

So the code should be correct. Now, the assertion given is that sub_list([1,2,3],[4,5,6]) returns [-3,-3,-3]. Let me test that. The code would generate [1-4, 2-5, 3-6] which is [-3, -3, -3]. So yes.

So the code is correct. Therefore, the Python code is as written.
```

</details>

**Code that ran:**

```python
def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]
```

**Visible-test report:**

```text
PASS    assert sub_list([1, 2, 3],[4,5,6])==[-3,-3,-3]
1 of 1 visible tests passed
```
