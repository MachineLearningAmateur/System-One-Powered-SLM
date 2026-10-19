# Mbpp/282, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/282/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 620. Answer tokens: 67.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called sub_list that subtracts two lists element-wise. The assert statement given is that sub_list([1,2,3], [4,5,6]) equals [-3,-3,-3]. So, the function should take two lists as input and return a new list where each element is the difference between the corresponding elements of the input lists.

First, I need to think about how to subtract each element. For example, the first element is 1 - 4 = -3, then 2-5=-3, and 3-6=-3. So the result is a list of those differences.

The function should probably iterate over each pair of elements from the two lists. But wait, what if the lists are of different lengths? Well, the problem statement doesn't mention handling that. So I assume that the input lists are of the same length. Otherwise, the function might not work correctly. But the assert statement given has the same length, so maybe the problem expects that the input lists are of equal length.

So the approach is: for each index i, take list1[i] - list2[i], collect all those results into a new list.

So the code would be something like:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

Wait, yes. Because zip pairs the elements from both lists. But wait, if the lists are not the same length, zip would stop at the shorter one. But the problem says to subtract element-wise, so perhaps the function should assume that the lists are of the same length. But the assert statement shows that the two lists are of the same length. So the code should work as is.

Testing with the given example: sub_list([1,2,3], [4,5,6]) would produce [-3,-3,-3], which matches the assert.

So the code is straightforward. The function uses a list comprehension with zip.

But I need to make sure that the function is correctly implemented. Also, the imports? Well, there are no imports needed here. The code is just a function.

So the complete code would be:

def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

Then, the assert statement would check that.

But wait, what if the lists are empty? Well, the problem doesn't mention that, so perhaps the function is expected to handle that. But the assert given has three elements, so maybe the function is intended for lists of the same length.

So the code should be correct. Let me test it.

Testing the example:

sub_list([1,2,3], [4,5,6]) → [1-4, 2-5, 3-6] → [-3, -3, -3], which matches the assert.

Yes, that's correct.

So the code is as written.
```

</details>

**Code that ran:**

```python
def sub_list(list1, list2):
    return [a - b for a, b in zip(list1, list2)]

# Test case
assert sub_list([1, 2, 3], [4, 5, 6]) == [-3, -3, -3]
```

**Visible-test report:**

```text
PASS    assert sub_list([1, 2, 3],[4,5,6])==[-3,-3,-3]
1 of 1 visible tests passed
```
