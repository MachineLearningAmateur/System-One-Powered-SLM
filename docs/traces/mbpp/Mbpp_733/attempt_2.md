# Mbpp/733, attempt 2

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/733/a2/r1`)

Visible tests: **pass**. Thinking tokens: 1544. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

Since the array is sorted, I can use binary search because that's efficient for such cases. But wait, the array is sorted, so maybe a linear search would work too, but for large arrays, binary search is better. However, the problem says the array is sorted, so binary search is the way to go here.

Wait, but the problem says the array is sorted. So the first occurrence of the number is the first time it appears. So for example, in the sample input [2,5,5,5,6,6,8,9,9,9], the first occurrence of 5 is at index 1.

So how to find that with binary search.

The standard binary search approach for finding the first occurrence. Let me think. The usual binary search finds the position where the target is found, but if there are duplicates, we need to find the first occurrence.

So here's the idea: during the binary search, when we find the target, we need to check if the current element is the target. If it is, then we check if the left side is also the same. Wait, but how to proceed.

Alternatively, maybe we can modify the binary search to track the first occurrence.

Let me think of the steps:

Initialize low = 0, high = len(arr) - 1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

      record the index, then search to the left to find the first occurrence.

      So, set high = mid - 1.

   elif arr[mid] < target:

      low = mid + 1

   else:

      high = mid - 1

Wait, but when we find arr[mid] == target, we need to check if there's a previous occurrence. So, for example, in the sample input, when we find the first 5 at index 1, then we need to check the left side. So, the approach is to find the first occurrence by moving the high to mid-1 once we find the target.

But how to track the index. Let me think.

Let me think of the steps:

Initialize low = 0, high = len(arr) - 1.

Initialize result = -1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

      result = mid

      high = mid - 1  # because there might be more occurrences to the left

   elif arr[mid] < target:

      low = mid + 1

   else:

      high = mid - 1

At the end, return result.

Yes, this should work. Because when we find the target, we set the result to mid and then search the left half to see if there's an earlier occurrence. So for example, in the sample input, when the first 5 is found at index 1, the code sets result to 1, then searches the left half (from 0 to 0). Then mid is 0, arr[0] is 2, which is less than 5, so low becomes 1. Then the loop ends. So the result is 1, which is correct.

Another example: if the array is [5,5,5], then the first occurrence is 0. Let's see:

low=0, high=2.

mid=1, arr[1] is 5. result=1, high=0.

Now low is 0, high is 0. mid=0. arr[0] is 5. result=0, high=-1. Loop ends. So returns 0.

Another example: array [5,5,6,6,6], target 5. The first occurrence is 0. The code would find it.

So this approach seems correct.

So the code would be:

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

Wait, but what if the target is not present in the array? Then the result remains -1, which is correct.

But the problem says that the array is sorted, but the function is supposed to return the index of the first occurrence. So if the target is not present, the function returns -1. But the assert statement in the problem says that the function is called with the given array and 5, which is present. So the code should handle that.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is just the function.

But wait, the problem says to write the code in one code block. So the code would be:

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

Then, the assert statement would be:

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1

But the code needs to be in a code block. So the complete code would include the function and the assert statement.

But the problem says to write the code in one code block. So the code would be:

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

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1

But wait, the function is called with the array and target. The code should be correct.

So that's the code. Let me check for possible errors.

What if the array is empty? Well, the code would return -1, which is correct.

Another test case: if the array is [5], then returns 0. If the array is [5, 5], returns 0. If the array is [5, 6, 7], returns 0.

Yes.

So the code should be correct.
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

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
```

**Visible-test report:**

```text
PASS    assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
1 of 1 visible tests passed
```
