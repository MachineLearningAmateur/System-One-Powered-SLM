# Mbpp/733, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1281. Answer tokens: 106.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. The example given is when the array is [2,5,5,5,6,6,8,9,9,9] and the target is 5, the output should be 1. 

First, I remember that since the array is sorted, we can use binary search to find the first occurrence efficiently. But how exactly?

Wait, the standard binary search finds any occurrence, but here we need the first one. So maybe we need to modify the binary search to find the leftmost occurrence.

Let me think about the approach. Let's consider the binary search steps. When the middle element is equal to the target, we need to check if it's the first occurrence. But how?

Alternatively, we can adjust the binary search to keep moving left when the target is found. For example, when we find a match, we set the high to mid -1 to check if there's an earlier occurrence. Then, after the loop, we check if the low index is the correct one.

Let me outline the steps:

Initialize low = 0, high = len(arr) - 1. Initialize result to -1 (in case the target isn't found).

While low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        result = mid
        high = mid - 1  # keep searching left to find the first occurrence
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

At the end, return result if it's not -1, else -1 (or maybe the problem expects to return -1 if not found? The example given has a valid case.)

Wait, the problem's assert statement checks for the first occurrence. So the function should return the index if found, else maybe -1? But the problem's example doesn't mention that. But the function's specification probably expects that if the number is not present, it returns -1 or something. But the problem's example is for when it is present.

So the code should handle that.

So the approach is to perform a modified binary search where when the target is found, we continue searching the left half to find the earliest occurrence.

Let me test this logic with the example.

Example array: [2,5,5,5,6,6,8,9,9,9], target 5.

Initial low=0, high=9. mid is (0+9)//2=4. arr[4] is 6 which is larger than 5. So high becomes 3.

Next iteration: low=0, high=3. mid=1. arr[1] is 5. So set result=1, and high=0.

Now, low=0, high=0. mid=0. arr[0] is 2 <5. So low becomes 1. Now low > high, loop ends. Return result=1. Which matches the example.

That seems correct.

Another test case: if the array is [5,5,5], target 5. The first occurrence is 0. Let's see:

low=0, high=2. mid=1. arr[1] is 5. set result=1, high=0. Then mid is (0+0)/2=0. arr[0] is 5. set result=0, high=-1. loop ends. return 0. Correct.

Another test case: if the array is [5], target 5. returns 0.

What if the target is not present? Like [2,5,6], target 3. Then the function returns -1.

So the code should handle that.

So the code structure would be:

def find_first_occurrence(arr, target):
    low = 0
    high = len(arr) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid -1
    return result

Wait, but what if the array is empty? Well, the problem says it's a sorted array, but perhaps the function should handle empty arrays. But the assert given has a non-empty array.

But the code would return -1 in that case, which is correct.

So this code should work.

Let me check the example again. The sample input is [2,5,5,5,6,6,8,9,9,9], target 5. The code returns 1. Which is correct.

Another test case: if the target is the first element. Like [5,5,5], returns 0. Correct.

Another case: target is the last element. Like [2,5,6,6,6], target 6. The code would find mid=2 (value 6), set result=2, then search left. Then high becomes 1. Then mid is (0+1)/2=0. arr[0] is 2 <6. low becomes 1. mid=1. arr[1] is 5 <6. low becomes 2. Now low > high. return result 2. Which is correct.

So the code seems to work.

So the code should be written as such. Now, the problem says to write the function and include any imports. But since this is a standard binary search, no imports are needed. So the code is as above.

Now, the assert statement in the problem is given as:

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1

Which the code would pass.

So the code is correct.
```

</details>

**Code that ran:**

```python
def find_first_occurrence(arr, target):
    low = 0
    high = len(arr) - 1
    result = -1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            result = mid
            high = mid - 1
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return result
```

**Visible-test report:**

```text
PASS    assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
1 of 1 visible tests passed
```
