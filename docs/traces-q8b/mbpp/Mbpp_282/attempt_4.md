# Mbpp/282, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/282/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 847. Answer tokens: 32.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called sub_list that subtracts two lists element-wise. Let's see. The assertion given is that when you subtract [4,5,6] from [1,2,3], you get [-3,-3,-3]. So each element in the first list is subtracted by the corresponding element in the second list.

First, I should check that both lists are of the same length. Wait, but the problem statement doesn't mention handling cases where the lists are different lengths. Maybe the function assumes that the input lists are of equal length. But maybe I should handle that? The example given uses lists of same length, but perhaps the function should raise an error if they are not. However, the problem statement doesn't specify that. So maybe I can assume that the lists are of the same length. But maybe I should include a check. Hmm. But the problem says to subtract element-wise, so perhaps the function is expected to work only when the lists are of the same length. So maybe I should proceed under that assumption.

So the approach is: iterate through each pair of elements from the two lists, subtract the second element from the first, and collect the results into a new list.

How to do that in Python. Let's think. For example, for list1 and list2, the result would be [a - b for a, b in zip(list1, list2)].

Wait, zip will pair elements from both lists. So if the lists are of same length, zip will work. So the list comprehension would work.

So the function can be written as:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

Wait, but wait. Wait, the subtraction is list1 elements minus list2 elements. So for each element in list1, subtract the corresponding element in list2. So yes, that's correct.

Testing the sample input: [1,2,3] minus [4,5,6] would be 1-4=-3, 2-5=-3, 3-6=-3. Which matches the assertion.

So that's the code. But what about if the lists are of different lengths? For example, if list1 is longer than list2, zip will stop at the shorter one. But the problem may not require handling that. Since the sample input uses same length lists, perhaps the function is intended to work for same-length lists. So the code is correct.

So the code would be:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

But wait, the problem says to write the function. So the code would be as simple as that. Let me check the assertion. Let's see:

sub_list([1,2,3], [4,5,6]) would produce [1-4, 2-5, 3-6] which is [-3, -3, -3], which matches.

So that's correct. So the code is straightforward. But perhaps I should make sure that the function is named correctly. Also, the problem says to include any imports. But since the code uses zip and list comprehensions, no imports are needed. So the complete code would be:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

But wait, maybe the problem expects the function to handle cases where the lists are not the same length? For example, if one is longer than the other, what should happen? The problem statement does not specify, so perhaps we can assume that the lists are of same length. So the code is correct as is.

So the code is as written. Let me check if there are any other possible issues. For example, if the lists are empty, but the code would return an empty list, which is correct. So the code should work.

So the final code is as above. The function is written, and the assertion passes.
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
