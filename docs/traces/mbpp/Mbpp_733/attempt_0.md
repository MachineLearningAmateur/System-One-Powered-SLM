# Mbpp/733, attempt 0

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/733/a0/r1`)

Visible tests: **pass**. Thinking tokens: 1665. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let me think about how to approach this.

Since the array is sorted, I can use binary search because that's efficient for such cases. But wait, binary search is usually for finding the presence of an element. But here, I need the first occurrence. So maybe I can modify the binary search to track the first occurrence.

Let me recall the binary search steps. The standard binary search finds the leftmost element where the target is present. So maybe I can adjust the binary search to find the first occurrence.

Let me think about the steps. Let's say the array is [2,5,5,5,6,6,8,9,9,9], and the target is 5. The first occurrence is at index 1.

So the idea is to find the first index where the element is equal to the target. How to do that with binary search.

The standard binary search can be modified. Let's think of the steps:

Initialize low and high as 0 and len(arr)-1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target: then we need to check if this is the first occurrence. So, we can record the index and then search the left half to see if there's an earlier occurrence. Because if there's an earlier occurrence, it would be in the left half.

   elif arr[mid] < target: search the right half.

   else: search the left half.

Wait, but when we find arr[mid] equals the target, we need to check if there's a previous occurrence. So, for example, if the target is in the array, then the first occurrence is somewhere in the left part of the array. So, in the binary search, when we find a match, we move the high to mid-1 to check the left side. But how do we track the first occurrence?

Alternatively, maybe we can use a modified binary search that keeps track of the first occurrence.

Let me think of the steps:

Initialize low = 0, high = len(arr) - 1.

result = -1

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

       result = mid

       high = mid - 1  # look for earlier occurrences

   elif arr[mid] < target:

       low = mid + 1

   else:

       high = mid - 1

At the end, return result if it's not -1, else return -1.

Wait, but this would work. Let me test with the example.

In the example, the array is [2,5,5,5,6,6,8,9,9,9], target is 5.

Let's simulate the steps:

low=0, high=9. mid=4 (since (0+9)//2=4). arr[4] is 6. Which is larger than 5. So high = 3.

Now, low=0, high=3. mid=1. arr[1] is 5. So result is 1. Then high = 0.

Now, low=0, high=0. mid=0. arr[0] is 2, which is less than 5. So low = 1. Now low > high, loop ends. So result is 1. Correct.

Another test case: if the target is not present, like 10. Then the loop ends with result -1.

Another test case: array [5,5,5], target 5. The first occurrence is 0. Let's see.

low=0, high=2. mid=1. arr[1] is 5. result=1, high=0. Now mid=0. arr[0] is 5. result=0, high=-1. Loop ends. So returns 0. Correct.

So this approach seems to work.

So the function would be:

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

But wait, what if the array is empty? Well, the problem says that the array is sorted, but maybe the function should handle empty arrays. But the assert given in the problem is for a non-empty array. However, the code would return -1 for empty arrays, which is correct.

But the problem says the array is sorted, but maybe the input is not sorted? But the problem says the function is for a sorted array. So the code is correct.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is just the function.

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

Then, the assert statement would be:

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1

So the code should be correct.

Wait, but what if the array has multiple occurrences, but the first occurrence is not found? Like, if the array is [5,5,5], and target is 5. The code returns 0, which is correct.

Another case: array [1,2,3,3,3,4], target 3. The first occurrence is at index 2. Let's see.

low=0, high=5. mid=2. arr[2] is 3. result=2, high=1. Now low=0, high=1. mid=0. arr[0] is 1 < 3. low=1. Now mid=1. arr[1] is 2 <3. low=2. Now low=2, high=1. loop ends. So result is 2. Correct.

Yes, this seems to work.

So the code is correct. Now, the code needs to be written in Python, with the correct syntax. Also, the function is called find_first_occurrence, and the parameters are arr and target.

So the complete code would be:

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

But wait, the code needs to have the imports? Well, the code doesn't need any imports. So the code is correct.

So the final code is as above.
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
