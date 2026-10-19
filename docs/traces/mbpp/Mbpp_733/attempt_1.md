# Mbpp/733, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1770. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

Since the array is sorted, I can use binary search. The standard binary search approach can be modified to find the first occurrence. Because the array is sorted, once I find the target, I need to check if there are any previous occurrences.

Wait, the usual binary search finds the position where the target is found. But if the array is sorted, and the target is present multiple times, the first occurrence is the leftmost one. So how to find that?

Let me recall. For example, in the array [2,5,5,5,6,6,8,9,9,9], the first occurrence of 5 is at index 1. So the function should return 1.

The standard binary search can be modified to find the first occurrence. Here's an idea: when we find the target in the middle, we check if the left half contains the target. If yes, then we search the left half. Otherwise, search the right half.

Wait, maybe I can adjust the binary search to track the first occurrence. Let me think of the steps.

Initialize low as 0, high as len(arr) - 1. While low <= high:

- mid = (low + high) // 2.

- If arr[mid] == target, then we need to check if there's a previous occurrence. So we set high = mid - 1, and keep track of the index. Once we exit the loop, the index would be the first occurrence.

Wait, but how to handle that. Let me think. Let's say we find the target at mid. Then, we move high to mid - 1 to check if there's a previous occurrence. But if there is, then the first occurrence is somewhere in the left part. So the process would be:

Initialize low = 0, high = len(arr) - 1.

Initialize result = -1.

While low <= high:

   mid = (low + high) // 2.

   if arr[mid] == target:

       result = mid

       high = mid - 1  # search left for possible earlier occurrence.

   elif arr[mid] < target:

       low = mid + 1

   else:

       high = mid - 1

At the end, return result if it's not -1, else return -1.

Wait, but what if the target is not present? Then the result remains -1. But the problem says the array is sorted, so maybe the function is supposed to handle that. But the assert statement given in the problem shows that the function is called with a number that exists in the array. So the function can assume that the target exists.

But the code should handle that. So the function will return the first occurrence.

Let me test this logic with the example.

Example array: [2,5,5,5,6,6,8,9,9,9], target 5.

Let's simulate the binary search.

Initial low=0, high=9. mid=4 (5). arr[4] is 6. Which is greater than 5. So high=3.

Now low=0, high=3. mid=1 (5). arr[1] is 5. So result=1. high=0. Now low=0, high=0. mid=0. arr[0] is 2 <5. So low=1. Now low>high, loop ends. Return result=1. Which is correct.

Another example: if the array is [5,5,5], target 5. The first occurrence is 0. Let's see.

low=0, high=2. mid=1. arr[1]=5. result=1. high=0. Now mid=0. arr[0] is 5. result=0. high=-1. Loop ends. Return 0.

Another case: array [5,5,6,6], target 5. The first occurrence is 0. Let's see:

low=0, high=3. mid=1. arr[1]=5. result=1. high=0. mid=0. arr[0] is 5. result=0. high=-1. So return 0.

Yes, that's correct.

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

Wait, but what if the array is empty? Well, the problem says that the array is sorted, but maybe the function should handle that. But the assert given in the problem shows that the array is non-empty. So perhaps the code is okay.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is just the function.

But the problem says to write the complete code in one code block. So the code would be:

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

But the code should include the imports. However, there are no imports needed here. So the code is as above.

Wait, but in Python, the function is defined, and the code is written. So the complete code would be:

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

But the problem says to write the complete code, including any imports. However, there are no imports needed here. So the code is as above.

So the final code is the function plus the assert statement. But the user may want the code to be in a single code block. So the code is:

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

But the user may want the code to be in a code block. So the code is written as such.

I think that's correct. Let me check for possible errors. For example, if the target is not present, the function returns -1. But the assert in the problem says that the function is called with a number that exists. So the code is correct.

Yes, this should work.
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
