# Mbpp/223, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/223/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1351. Answer tokens: 61.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_majority that checks if a given element is the majority element in a sorted array. The majority element is one that appears more than n/2 times. Let me think about how to approach this.

Since the array is sorted, all instances of the element will be consecutive. That makes things easier. So, for example, if the array is [1,2,3,3,3,3,10], the element 3 appears 4 times. The length n is 7, so n/2 is 3.5. Since 4 > 3.5, it's a majority.

So the steps I need to take are: find the count of the element in the array and check if it's more than n/2.

But how to find the count efficiently? Since the array is sorted, I can use binary search to find the first and last occurrence of the element. Then the count is last - first + 1.

Wait, right. For example, in the sample array, the first occurrence of 3 is at index 2, last at index 5. So 5-2+1 = 4. Which is correct.

So the plan is:

1. Find the first position where the element appears.
2. Find the last position where the element appears.
3. Calculate the count as last - first + 1.
4. Check if count > n/2.

But how to implement the binary search for first and last occurrence?

Alternatively, since the array is sorted, maybe we can use the bisect module. The bisect_left function gives the insertion point for the element, which is the first occurrence. Then bisect_right gives the insertion point after the last occurrence. So the count is bisect_right - bisect_left.

Yes. For example, in the sample array, bisect_left for 3 would be 2, bisect_right would be 6. So 6-2 = 4, which is correct. So the count is bisect_right - bisect_left.

So the steps would be:

- Use bisect_left to find the left index.
- Use bisect_right to find the right index.
- Compute count = right - left.
- Check if count > n//2 (since n is the length, and the majority requires more than n/2, which is equivalent to count > n//2 when n is even or odd? Let me think. For example, if n is 7, n//2 is 3. So count needs to be >3.5, which is 4. So for integer division, if count > n//2, then it's correct. Because for even n, say n=4, n//2 is 2. So count needs to be >2, which is 3 or more. So yes, the condition is count > n//2.

So the code would be:

Import bisect.

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n//2

Wait, but what if the element is not present in the array? Then left and right would be the same, and count is zero. So the function returns False, which is correct.

Testing the sample input: [1,2,3,3,3,3,10], n=7, element 3. bisect_left gives 2, bisect_right gives 6. count is 4. 4 > 7//2 (3) → 4>3 → True. Which matches the sample.

Another test case: if the array is [1,1,2,2,2], n=5. element 2. bisect_left is 2, bisect_right is 5. count is 3. 3>5//2 → 3>2 → True. Correct.

Another case: [1,2,3], element 1. count is 1. 1>3//2 → 1>1 → False. Correct.

So this approach should work.

Now, the code needs to import bisect. So the code would be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

Wait, but what if the array is empty? Well, the problem says n is the length. So for n=0, but the function is called with n=0, but the code would return count (0) > 0//2 → 0>0 → False. Which is correct.

But the problem says that the array is sorted. So the code should handle that.

So the code seems correct. Let me check the sample input. The sample input is [1,2,3,3,3,3,10], n=7, element 3. The code returns True. Which is correct.

So the code should work. Now, the function is called is_majority, and the parameters are arr, n, element. So the code is as above.

But wait, in Python, the bisect module's functions take the list and the value. So the code is correct.

So the complete code would be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

But wait, the problem says that the array is sorted. So the code can assume that arr is sorted. So no need to check that.

So that's the code. Let me check the sample assertion. The sample input is [1,2,3,3,3,3,10], n=7, element 3. The code returns True. Which is correct.

Another test case: [1,1,1,1,2], n=5, element 1. count is 4. 4>2 → True. So correct.

Another case: [1,2,3], element 2. count is 1. 1>1 → False. Correct.

So this code should work.
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
