# Mbpp/223, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/223/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1721. Answer tokens: 61.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_majority that checks if a given element is the majority element in a sorted array. The majority element is one that appears more than n/2 times. The function takes in the array, its length n, and the element to check. Let me think about how to approach this.

Since the array is sorted, all instances of the element will be consecutive. That makes things easier. So, for example, if the array is [1,2,3,3,3,3,10], the element 3 appears 4 times. The length n is 7, so n/2 is 3.5. Since 4 is more than 3.5, it's a majority.

So the plan is: find the first and last occurrence of the element in the array. Then calculate the count based on those positions. If the count is more than n/2, return True; else False.

How to find the first and last occurrence? Well, since the array is sorted, I can use binary search for that. Let me think about implementing two helper functions: one to find the leftmost occurrence and another for the rightmost.

Alternatively, maybe I can use the bisect module in Python. The bisect module has bisect_left and bisect_right functions. For example, bisect_left returns the insertion point for the element, which would be the index of the first occurrence if the element exists. And bisect_right returns the insertion point after the last occurrence. So the count would be bisect_right - bisect_left. If that count is greater than n//2, then return True.

Wait, but the array is sorted, but maybe there are multiple elements. Let me test this approach with the sample input.

Sample input: [1,2,3,3,3,3,10], n=7, element 3. Let's compute bisect_left and bisect_right. 

bisect_left would find the index of the first 3, which is 2. bisect_right would find the index after the last 3, which is 6. So the count is 6-2=4. Which is 4>7/2 (3.5) → yes. So returns True. Which matches the sample.

Another example: if the element is not present, then bisect_left and bisect_right would return the same index, so count is zero. So returns False.

So the steps are:

1. Use bisect_left to find the first occurrence index.
2. Use bisect_right to find the last occurrence index.
3. The count is right - left.
4. Check if count > n//2. If yes, return True else False.

But wait, since n is the length of the array, and the array is sorted, but maybe the element is not present. So for example, if the element is not present, then bisect_left and bisect_right would give the same index, so count is zero. So the code would return False.

So the code can be written using the bisect module. Let me think about the code structure.

First, import bisect.

Then, the function is_majority(arr, n, element):

But wait, the array is passed as a parameter. Let me check the parameters. The function is supposed to take in a sorted array, its length (n), and an element. So the code would be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

Wait, but what if the element is not present? For example, if the array is [1,2,3,4,5], and element is 6. Then left and right would be 5, so count is 0. Which is correct.

But what if the array is [3,3,3], n=3, element is 3. Then count is 3, which is 3>1.5 → yes. So returns True.

But wait, the function is called with n as the length. So the code is correct.

But wait, in the sample input, the array is [1,2,3,3,3,3,10], n is 7. So the code would compute count as 4, which is 4>3.5 → True. Which is correct.

So this approach seems correct.

But what about when the array is empty? Well, the problem says that n is the length, so if n is zero, but the function is called, but the problem probably expects that n is at least 1. But the code would handle it.

But the problem says that the array is sorted. So the code is okay.

So the code would be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

Wait, but in Python, the bisect module's functions take the array and the value. So in the code, arr is the array. So the code is correct.

But let me test the sample input. For the sample input:

arr = [1,2,3,3,3,3,10], n=7, element=3.

bisect_left(arr, 3) returns 2. bisect_right returns 6. 6-2=4. 4 > 7//2 → 3.5 → 4>3.5 → True. So returns True. Which is correct.

Another test case: if the array is [3,3,3], n=3, element 3. count is 3. 3>1.5 → True.

Another case: [3,3,3,3], n=4. 4>2 → yes. So returns True.

What if the array is [1,2,3,4], element 3. count is 1. 1>2 → no. So returns False.

So this code should work.

But wait, what if the array is [1,1,1,1,2], n=5, element 1. count is 4. 4>2.5 → yes. So returns True.

Yes. So the code seems correct.

So the code is as above. But the problem says that the function is called with the array, n, and element. So the code is correct.

But in the problem statement, the first assertion is is_majority([1,2,3,3,3,3,10], 7, 3) == True. Which the code would return True.

So the code should be correct.

So the code would need to import bisect, and then use the functions.

So the complete code would be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

But wait, the function parameters are (arr, n, element). But in Python, the array is passed as a list, and n is the length. But the code uses the entire array, so the code is correct.

But what if the array is not sorted? Well, the problem says that the array is sorted, so the code can assume that.

So this should work.

Another test case: arr = [1,1,2,2,2], n=5, element 2. bisect_left returns 2, bisect_right returns 5. count is 3, which is 3>2.5 → True. So returns True.

Yes.

Another test case: arr = [1,2,3,4,5], element 3. count is 1. 1>2.5? No. So returns False.

So the code is correct.

Therefore, the code should work.
```

</details>

**Code that ran:**

```python
import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2
```

**Visible-test report:**

```text
PASS    assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
1 of 1 visible tests passed
```
