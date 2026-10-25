# Mbpp/733, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1505. Answer tokens: 106.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

The array is sorted, so maybe binary search would be efficient here. But the standard binary search finds any occurrence, not necessarily the first one. So I need to modify the binary search to find the first occurrence.

Let me think about the steps. Let's say the target is 5 in the example array [2,5,5,5,6,...]. The first occurrence is at index 1. How can I adjust the binary search to find that?

So, during the binary search, when the middle element equals the target, I need to check if it's the first occurrence. That is, if the element before mid is not equal to the target, then mid is the first occurrence. But if there's an element before, and it's equal, then I need to search the left half.

Alternatively, I can adjust the binary search to keep moving left even when the target is found, until I find the first occurrence.

Let me outline the steps for the modified binary search:

Initialize low as 0 and high as len(arr) - 1. The result is initialized as -1 (in case the target isn't found).

While low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        result = mid
        high = mid - 1  # continue searching left to find earlier occurrences
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

At the end, return result if it's not -1, else -1 (or maybe the problem expects to return -1 if not found? The example given doesn't have that case, but the problem says "given number in a sorted array", so perhaps the function is supposed to return the index if found, else maybe -1? But the assert statement in the example shows that the function returns 1 when the number is present. So perhaps the function is supposed to return the first occurrence index, and if not found, maybe return -1. But the problem says "given number in a sorted array"—so perhaps the input is guaranteed to have the number? Or maybe the function should handle cases where it's not present.

But the problem's assert statement is for when the number is present. So the function needs to handle both cases. But the problem says to return the index of the first occurrence, so if the number isn't present, perhaps return -1. But the problem's sample input is for when it is present.

So, the approach is to use a modified binary search that finds the first occurrence.

Let me test this logic with the example. For the array [2,5,5,5,6,6,8,9,9,9], target is 5.

Initial low=0, high=9. mid is (0+9)//2=4. arr[4] is 6 which is larger than 5. So high becomes 3.

Next iteration: low=0, high=3. mid=1. arr[1] is 5. So set result=1 and set high=0. Now, low is 0, high is 0. mid is 0. arr[0] is 2 <5, so low becomes 1. Now low > high, loop ends. Return result=1. Which matches the sample. So that works.

Another example: if the array is [5,5,5], target is 5. The first occurrence is 0. Let's see. Initial low=0, high=2. mid=1. arr[1] is 5, set result=1, high=0. Now mid is (0+0)/2=0. arr[0] is 5. set result=0, high=-1. Loop ends. So returns 0. Correct.

Another case: if the array is [5], target is 5. returns 0.

Another case: if the array is [2,3,4,5,5,5,6], target 5. The first occurrence is 3. Let's see:

low=0, high=6. mid=3. arr[3] is 5. set result=3, high=2. Now loop ends. So returns 3. Correct.

So this logic works. So the code can be written as follows:

The function will take the array and target. Initialize low, high, result. Then perform the binary search as described.

Now, code:

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

Wait, but what if the target is not present? Then the function returns -1. Which is correct.

Testing the sample input:

arr = [2,5,5,5,6,6,8,9,9,9], target=5. The function returns 1. Which matches the assert.

So that's correct.

But wait, what about when the array is empty? Well, the problem says it's a sorted array, but perhaps the function should handle that. But the sample input is valid, so the code should handle that.

So the code seems correct.

Now, the code needs to be written. The function is called find_first_occurrence, and the code should be in a Python code block with any necessary imports. But since the code doesn't require any imports, the code is as above.

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

But wait, the problem says to write the function. So the code is as above. Let me check the sample input:

Testing the sample input:

arr = [2,5,5,5,6,6,8,9,9,9], target=5. The function returns 1. Which is correct.

Another test case: if the array is [5,5,5], target is 5, returns 0. Correct.

Another case: if the array is [1,2,3,4,5], target 3, returns 2. Correct.

Another case: target not present, returns -1. So that's handled.

So this should be correct.
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
