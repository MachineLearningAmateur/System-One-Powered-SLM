# Mbpp/733, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1346. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

The array is sorted, so maybe binary search is a good idea here. Because binary search is efficient for sorted arrays. But the standard binary search might not directly give the first occurrence. Hmm.

Right, for the first occurrence, when I find the target, I need to check if there's a previous element that's the same. Or maybe adjust the binary search to keep moving left once the target is found.

Let me think of the steps. Let's say I perform a binary search. When the middle element is equal to the target, I need to check if it's the first occurrence. How?

Maybe, when the middle element is equal to the target, I set the high to mid - 1 to see if there's an earlier occurrence. Then, keep track of the result whenever I find a match. Wait, but how to structure this.

Alternatively, the binary search can be modified to find the leftmost occurrence. Let me think about the conditions.

Let me outline the steps:

Initialize low = 0, high = len(arr) - 1. Initialize result to -1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

       result = mid

       high = mid - 1  # continue searching left to find earlier occurrences

   elif arr[mid] < target:

       low = mid + 1

   else:

       high = mid - 1

At the end, return result if found, else -1.

Wait, that seems like a standard approach for finding the first occurrence. Because whenever we find a match, we record it and search the left half to see if there's an earlier occurrence. So this would eventually find the first occurrence.

Let me test this logic with the sample input.

Sample input: [2,5,5,5,6,6,8,9,9,9], target 5.

Let's simulate the steps.

Initial low=0, high=9. mid is (0+9)//2=4. arr[4] is 6 which is greater than 5. So high becomes 3.

Next iteration: low=0, high=3. mid=1. arr[1] is 5. So set result=1, and set high=0.

Now, low=0, high=0. mid=0. arr[0] is 2 <5. So low becomes 1. Now low > high, loop ends.

Result is 1. Which matches the sample. So that seems correct.

Another test case: if the array is [5,5,5], target 5. The first occurrence is 0. Let's see.

low=0, high=2. mid=1. arr[1] is 5. set result=1, high=0.

Now mid is (0+0)//2=0. arr[0] is 5. set result=0, high=-1. loop ends. returns 0. Correct.

Another case: if the target is not present. Like [2,3,4], target 5. The function returns -1.

So this logic seems to work. So the function can be implemented with this approach.

Now, code-wise, the function will take the array and the target. So:

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

Wait, but what if the array is empty? Well, the problem says it's a sorted array, but perhaps the function should handle empty arrays. But the sample input is non-empty. But the code would return -1 in that case, which is correct.

So the code seems correct. Let me check the sample input again.

The sample input is [2,5,5,5,6,6,8,9,9,9], target 5. The code returns 1, which is correct.

Another test case: if the target is the first element. Like [5,5,5], returns 0. Correct.

Another case: target is the last element. Like [2,3,5], target 5. The code would find mid=1, then check 3 <5, so low becomes 2. Then mid is 2, which is 5. Set result=2, high=1. Loop ends. So returns 2. Correct.

What if the array has multiple occurrences but the target is not present? Like [2,3,4], target 5. Returns -1. Correct.

So the code should work.

Now, the problem says to write the function and include the assert statement. So the code should have the function and the assert.

Wait, the problem says to write a function, and the user will test it with the assert. So the code should have the function and the assert statement.

But the user's instruction says to write the function and include any imports. But the code doesn't need any imports. So the code would be:

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

But wait, the problem says to write a function. So the code is correct. Let me check if the code is correct.

Yes, the code should work. So that's the solution.
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
