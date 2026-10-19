# Mbpp/733, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1504. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let me think about how to approach this.

Since the array is sorted, I can use binary search because that's efficient for such cases. But wait, binary search is usually for finding the presence of an element. But here, I need the first occurrence. So maybe I can modify the binary search to track the first occurrence.

Alternatively, since the array is sorted, maybe I can use a linear search. But for a sorted array, even linear search would be O(n) time, which is acceptable if the array is small. But for large arrays, binary search is better. However, the problem says the array is sorted, so maybe the solution can be optimized.

Let me think about the binary search approach. Let's consider the standard binary search. The standard binary search finds the index of the element. But for the first occurrence, perhaps I can adjust the search to find the first occurrence.

Let me think about the steps. The array is sorted, so all elements before the first occurrence are less than the target, and elements after are greater. So, during the binary search, I can check if the mid element is equal to the target. If it is, then we need to check if there's a previous occurrence. So maybe we can adjust the search to move left until we find the first occurrence.

Wait, here's an idea. Let's perform a binary search where whenever we find the target, we check if the left side has a previous occurrence. So, for example, in the array [2,5,5,5,6,6,8,9,9,9], the first occurrence of 5 is at index 1.

So, the binary search would proceed as follows:

Initialize low = 0, high = len(arr) - 1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

       we need to check if there's a first occurrence. So, we can record the index and then move the high to mid - 1 to see if there's a previous occurrence.

   elif arr[mid] < target: move low to mid + 1

   else: move high to mid - 1

But how to track the first occurrence. Let's think. When we find the target at mid, we need to check if the left side has any occurrence. So, in the binary search, once we find the target, we can move the high to mid - 1 and check again. But how to track the first occurrence.

Alternatively, during the binary search, when we find the target, we can record the index and then continue searching to the left to see if there's a previous occurrence.

Wait, here's a possible approach. Let's have a variable to store the result. Let's say we start with low = 0, high = len(arr) - 1. Initialize result as -1. Then, while low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

       result = mid

       high = mid - 1  # look for earlier occurrence

   elif arr[mid] < target:

       low = mid + 1

   else:

       high = mid - 1

At the end, return result if it's not -1. But wait, what if the target is not present? Then result remains -1. But in the problem statement, the array is sorted, but the function is supposed to return the index of the first occurrence. So, if the target is not present, maybe the function should return -1 or something else? But the problem says that the function is supposed to find the first occurrence, so perhaps the function should return -1 if not found.

But the given example is for the case where the target exists. So, the code should handle that.

So, the function would be:

def find_first_occurrence(arr, target):

    low = 0

    high = len(arr) - 1

    result = -1

    while low <= high:

        mid = (low + high) // 2

        if arr[mid] == target:

            result = mid

            high = mid - 1  # look for earlier occurrence

        elif arr[mid] < target:

            low = mid + 1

        else:

            high = mid - 1

    return result

Wait, let's test this with the example. The array is [2,5,5,5,6,6,8,9,9,9], target is 5.

Let's simulate the steps.

Initial low=0, high=9. mid is 4. arr[4] is 6. Since 6 > 5, high becomes 3.

Now low=0, high=3. mid is 1. arr[1] is 5. So result is 1. high becomes 0.

Now low=0, high=0. mid is 0. arr[0] is 2 <5. So low becomes 1. Now low>high, loop ends. Return 1. Which is correct.

Another test case: if the array is [5,5,5], target 5. The code would return 0. Correct.

Another case: if the array is [5,5,6], target 5. The code would return 0.

What if the array is [5,5,5,5], target 5. The code would return 0.

What if the array is [5,6,6,6], target 5. The code would return 0.

Yes, this seems to work.

So the code should be as above. Now, the problem says to write the function, and the assert statement. So the code would be:

But wait, the problem says that the function is to find the first occurrence. So, the code is correct.

Now, the code needs to include the imports. But the code is for a function, and no imports are needed. So the code would be:

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

So the code is correct.

But wait, what if the array is empty? Well, the problem says that the array is sorted, but the function is supposed to handle it. But the code would return -1, which is correct.

So, the code should be written as such.
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
