# Mbpp/733, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1391. Answer tokens: 106.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

The array is sorted, so maybe binary search would be efficient here. But the standard binary search finds any occurrence, not necessarily the first one. So I need to adjust the binary search to find the first occurrence.

Let me recall: for finding the first occurrence, when the middle element is equal to the target, I shouldn't just return immediately. Instead, I should check if there's a possibility of an earlier occurrence. So maybe I should continue searching the left half even after finding a match.

Let me outline the steps. The idea is to perform a binary search where, when the target is found, we keep moving left to see if there's an earlier occurrence.

Initialize low as 0 and high as len(arr) - 1. The result is initialized to -1 (in case the target isn't found).

While low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        result = mid
        high = mid - 1  # continue searching left
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

At the end, return result if it's not -1, else maybe return -1? But according to the problem statement, the function is supposed to find the first occurrence. So if the target isn't present, perhaps return -1. But the problem's example uses a case where the target is present, so maybe the function is expected to return the index if found, else maybe not. But the problem's assert statement shows that the function returns 1 for the given input.

Wait, the problem says "given number in a sorted array". So the function should return the first occurrence if present, else maybe -1? Well, the problem's example doesn't cover that, but the function should handle that.

So the approach is to use modified binary search to find the first occurrence.

Let me test this logic with the sample input. The sample input is [2,5,5,5,6,6,8,9,9,9], looking for 5. The first occurrence is at index 1.

Let me simulate the steps.

Initial low=0, high=9. mid = 4. arr[4] is 6, which is greater than 5. So high becomes 3.

Next iteration: low=0, high=3. mid is (0+3)//2 = 1. arr[1] is 5. So we set result=1 and set high=0.

Now, low=0, high=0. mid is 0. arr[0] is 2, less than 5. So low becomes 1. Now low > high, loop ends. The result is 1. Which matches the sample.

So this logic works for the sample.

Another test case: if the array is [5,5,5], target 5. The first occurrence is 0. Let's see.

low=0, high=2. mid=1. arr[1] is 5. set result=1, high=0. Now mid is (0+0)//2=0. arr[0] is 5. set result=0, high=-1. loop ends. returns 0. Correct.

Another case: if the array is [5], target 5. returns 0. Correct.

What if the target is not present? Like [2,4,6], target 5. Then the function returns -1. Which is correct.

So the code should be structured as follows:

Define the function find_first_occurrence(arr, target):

Initialize low = 0, high = len(arr) - 1, result = -1.

While low <= high:

   mid = (low + high) // 2

   if arr[mid] == target:

       result = mid

       high = mid - 1

   elif arr[mid] < target:

       low = mid + 1

   else:

       high = mid - 1

Return result.

Wait, but in Python, when the array is empty, len(arr) is 0, so high is -1. But the loop condition is low <= high, which would not run. So returns -1, which is correct.

So this code should handle all cases.

Now, let's code this.

But need to make sure that the function is called correctly. Let me write the code.

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

Testing this with the sample input:

arr = [2,5,5,5,6,6,8,9,9,9], target 5. The function returns 1. Which matches the assert.

Another test case: arr = [5,5,5], target 5: returns 0.

Another case: arr = [5], returns 0.

If target is not present, returns -1.

Yes, this should work.

Now, the problem says to write the function. The code should be in a Python code block. Also, the assert statement is given, so the code should pass that.

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

But wait, the problem says to write the function. So the code is as above.

Now, the user wants the code in a code block. So the answer is the code as written.

But the problem says to include any imports. But in this case, no imports are needed. So the code is as above.

So the final code is as written.
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
