# Mbpp/733, attempt 4

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/733/a4/r1`)

Visible tests: **pass**. Thinking tokens: 2018. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

Since the array is sorted, I can use binary search because that's efficient for such problems. But wait, binary search is usually for finding the presence of an element, but here I need the first occurrence. So maybe I can modify the binary search to track the first occurrence.

Alternatively, since the array is sorted, maybe I can use a linear search. But linear search would be O(n) time, which is not efficient for large arrays. But given that the array is sorted, maybe the problem expects a binary search approach.

Let me think about the binary search approach. The standard binary search finds the first occurrence. Let me recall how that works.

In binary search, when the middle element is equal to the target, we need to check if there's a previous occurrence. So, for example, if the array is [2,5,5,5,6,6,8,9,9,9], and the target is 5, the first occurrence is at index 1.

So the idea is to find the first occurrence. Let's outline the steps:

Initialize low = 0, high = len(arr) - 1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

      record the index, and then search the left half to find the first occurrence.

   elif arr[mid] < target: move low to mid + 1

   else: move high to mid - 1

Wait, but how to handle the case where the target is found. Let's think.

Let me think of the steps. Suppose I have a target, and during the binary search, when I find a mid element equal to the target, I need to check if there's a previous occurrence. So, I can set high = mid - 1, and then once the loop ends, the first occurrence is the last position where the target was found.

Wait, maybe not. Let me think of an example. Let's say the array is [5,5,5], target is 5. The first occurrence is 0. So during the binary search, when the mid is 1, the value is 5. Then, we set high to mid -1 (so high is 0). Then, the loop continues. Then, mid is (0+0)//2 = 0. The value is 5. So we set high to -1. The loop ends. So the first occurrence is at 0.

So maybe the approach is to track the first occurrence. So during the binary search, when we find a mid element equal to the target, we can record the index and then search the left half. But how to do that.

Alternatively, during the binary search, when we find a match, we can check the left side to see if there's a previous occurrence. But how to do that.

Another approach is to use a modified binary search where, when the target is found, we check the left side for the first occurrence. So here's a possible algorithm:

Initialize low = 0, high = len(arr) - 1.

Initialize result = -1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

      result = mid

      high = mid - 1  # look for earlier occurrences

   elif arr[mid] < target:

      low = mid + 1

   else:

      high = mid - 1

At the end, return result.

Yes, this seems right. Because whenever we find a match, we record it and search the left half. So the first occurrence will be found.

Let me test this logic with the example given. The array is [2,5,5,5,6,6,8,9,9,9], target is 5.

Let's simulate the steps.

Initial low=0, high=9. mid=4. arr[4] is 6. Since 6>5, high=3.

Now low=0, high=3. mid=(0+3)//2=1. arr[1] is 5. So result=1. high=0.

Now low=0, high=0. mid=0. arr[0] is 2 <5. So low=1. Now low>high, loop ends. Return result=1. Which is correct.

Another test case: array [5,5,5], target 5. The steps would be:

low=0, high=2. mid=1. arr[1] is 5. result=1, high=0. Now low=0, high=0. mid=0. arr[0] is 5. result=0, high=-1. loop ends. return 0. Correct.

Another test case: array [5,5,6,6,7], target 5. The first occurrence is 0. Let's see:

low=0, high=4. mid=2. arr[2] is 6>5. high=1.

low=0, high=1. mid=0. arr[0] is 5. result=0. high=-1. loop ends. return 0. Correct.

Another case: array [5,5,5,6,6,6], target 5. The first occurrence is 0. The code would return 0.

So this logic seems to work.

So the function would be:

def find_first_occurrence(arr, target):

    low = 0

    high = len(arr) - 1

    result = -1

    while low <= high:

        mid = (low + high) // 2

        if arr[mid] == target:

            result = mid

            high = mid -1

        elif arr[mid] < target:

            low = mid + 1

        else:

            high = mid -1

    return result

But wait, what if the target is not present in the array? Then result remains -1, which is correct.

But the problem says that the array is sorted, so perhaps the function is supposed to handle that. But the problem says that the function is to find the first occurrence, so if the target is not present, it should return -1.

But the assert in the problem says that the function is called with [2,5,5,5,6,6,8,9,9,9], 5, which is present. So the code would return 1.

So this code should work.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is just the function.

But the problem says to write the complete code in one code block, including any imports. So the code would be:

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

Wait, but the code needs to be in a code block. So the code would be:

But the code is written as a function. So the code would be:

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

But the problem says to write the code with any necessary imports. Since there are no imports needed, the code is as above.

But wait, the code needs to be in a code block. So the code would be:

So the final code is:

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

Yes. So that's the code. The code is correct, and the assert statement checks that the function returns 1 for the given input.

I think that's the correct solution.
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
