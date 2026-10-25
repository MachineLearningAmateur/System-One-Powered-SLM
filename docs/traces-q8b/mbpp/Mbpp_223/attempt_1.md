# Mbpp/223, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/223/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1626. Answer tokens: 61.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_majority that checks if a given element is the majority element in a sorted array. The majority element is one that appears more than n/2 times. The function takes in the array, its length n, and the element to check. Let me think about how to approach this.

Since the array is sorted, all instances of the element will be consecutive. That makes things easier. So, for example, if the array is [1,2,3,3,3,3,10], the element 3 appears 4 times. The length n is 7, so n/2 is 3.5. Since 4 > 3.5, it's a majority.

So the plan is: find the first and last occurrence of the target element. Then calculate the count based on those positions. If the count is more than n/2, return True.

How to find the first and last occurrence? Well, since the array is sorted, I can use binary search for that. Let me think about implementing two helper functions: one to find the leftmost occurrence and another for the rightmost.

Alternatively, maybe I can use the bisect module in Python. The bisect module has bisect_left and bisect_right functions. For example, bisect_left returns the insertion point for the element, which would be the index of the first occurrence if the element exists. Similarly, bisect_right returns the insertion point after the last occurrence. So the count would be bisect_right - bisect_left. If that count is greater than n//2, then return True.

Wait, but the array is sorted, so maybe even better. Let me think. For example, if the element is present, then the first occurrence is at index left, and the last occurrence is at index right-1. The total count is right - left. So if that count is greater than n//2, then return True.

So the steps are:

1. Use bisect_left to find the first occurrence of the element. Let's call this left.
2. Use bisect_right to find the first occurrence of the element after the last occurrence. Let's call this right.
3. The count is right - left.
4. If count > n//2, return True. Else, False.

But wait, what if the element is not present in the array? Then bisect_left and bisect_right would return the same index, so right - left would be zero. Which would correctly return False.

So this approach should work.

Now, I need to import bisect. Let me check the example given. The sample input is [1,2,3,3,3,3,10], n=7, element 3. The bisect_left would return index 2 (since the first 3 is at index 2). bisect_right would return index 6 (since the last 3 is at index 5, and bisect_right returns insertion point after that). So right - left is 6-2=4. n is 7, n//2 is 3. 4>3, so True. Which matches the sample.

Another example: if the array is [1,1,2,2,2], n=5. The majority is 2. Let's see: bisect_left for 2 is 2, bisect_right is 5. 5-2=3, which is more than 5//2=2. So returns True.

Another case: if the array is [1,1,2,3], n=4. The element 1 occurs 2 times. n//2 is 2. So 2 is not more than 2. So returns False.

So the approach seems solid.

Now, the code. Let's structure it.

Import bisect.

Function is_majority(arr, n, element):

   left = bisect.bisect_left(arr, element)
   right = bisect.bisect_right(arr, element)
   count = right - left
   return count > n//2

Wait, but what if the array is empty? Well, the problem says n is the length, so n is at least 1? Well, the function parameters are given as n, so maybe the code can assume that n is valid. But the code should handle cases where the element is not present.

But in the code, if the element is not present, then left and right would be the same, so count is zero. Which would return False, which is correct.

So the code should be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

Wait, but the function parameters are arr, n, element. But in the sample input, the array is [1,2,3,3,3,3,10], n is 7. So the code should work.

Testing the sample input:

arr = [1,2,3,3,3,3,10], element 3. bisect_left returns 2, bisect_right returns 6. count is 4. 4 > 7//2 (3.5?), wait, in Python, 7//2 is 3. So 4>3 is True. So returns True. Which is correct.

Another test case: if n is even. Let's say n=4, and element occurs 2 times. Then 2 is not more than 4//2=2. So returns False.

But what if the element occurs exactly n/2 times? For example, n=4, count is 2. Then 2 is not more than 2, so returns False. Which is correct.

So the code should work.

But wait, the problem says the array is sorted. So the code can assume that the array is sorted. So the bisect functions will work.

So the code is correct. Now, the code needs to be written with the correct parameters. Also, the function is called is_majority, and the parameters are arr, n, element. So the code should be as written.

But wait, in Python, the function parameters are arr, n, element. But the problem says that the array is sorted. So the code is correct.

So the code should be:

import bisect

def is_majority(arr, n, element):
    left = bisect.bisect_left(arr, element)
    right = bisect.bisect_right(arr, element)
    count = right - left
    return count > n // 2

But wait, the problem says that the array is sorted. So the code is correct. Let me check the sample input. The sample input is [1,2,3,3,3,3,10], n=7, element 3. The code returns 4>3 (since 7//2 is 3), which is True. Correct.

Another test case: if the array is [3,3,3], n=3, element 3. count is 3. 3>1.5? 3>1 (since 3//2 is 1). So returns True. Correct.

Another test case: [3,3,3,3], n=4, element 3. count is 4, 4>2. So returns True.

Another test case: [1,2,3,4], n=4, element 2. count is 1. 1>2? No. So returns False.

So the code should work.

Therefore, the code is correct.
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
