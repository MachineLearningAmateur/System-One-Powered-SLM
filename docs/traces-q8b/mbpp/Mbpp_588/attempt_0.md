# Mbpp/588, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/588/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 568. Answer tokens: 19.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called big_diff that takes a list of numbers and returns the difference between the largest and smallest values. Let's see. The example given is big_diff([1,2,3,4]) returns 3. Because 4-1 is 3. Right.

So the steps are: find the maximum in the list, find the minimum, then subtract them. But wait, what if the list is empty? Oh, the problem probably assumes that the list has at least one element. Because otherwise, we can't compute the difference. But the example given has elements, so maybe the function is expected to handle non-empty lists.

So the function can be straightforward. Let's think about how to implement it.

First, I need to import nothing, right? Because the built-in functions for max and min are available. So the function would be:

def big_diff(nums):
    return max(nums) - min(nums)

Wait, but what if the list is empty? Like, if someone passes an empty list, this would throw an error. But the problem's example uses a list with elements, and the assert statement probably expects that the input is valid. So maybe the function is supposed to work for non-empty lists. So the code is simple.

Wait, the problem says "given list"—so perhaps the list is non-empty. So the function can safely use max and min.

So the code is as simple as that. Let me test the example. For [1,2,3,4], max is 4, min is 1. 4-1=3. Which matches the assert. So that's correct.

But what about if the list has only one element? Like [5]. Then max and min are the same, so the difference is 0. That's correct.

So the code should work. So the complete code would be:

def big_diff(nums):
    return max(nums) - min(nums)

But wait, the problem says to write a function. So the code is as above. But the user wants the code in a code block, including any imports. But there are no imports needed here. So the code is as simple as that.

Wait, but the problem says to write a correct Python solution. So maybe there's a case where the list is empty? But the problem's example doesn't cover that. But the function as written would raise a ValueError if the list is empty. However, the problem's assert statement probably expects that the input is valid. So the function is correct as per the problem's requirements.

So the code is correct. Let me check again. The sample input [1,2,3,4] returns 3. Which works. So the code is correct.
```

</details>

**Code that ran:**

```python
def big_diff(nums):
    return max(nums) - min(nums)
```

**Visible-test report:**

```text
PASS    assert big_diff([1,2,3,4]) == 3
1 of 1 visible tests passed
```
