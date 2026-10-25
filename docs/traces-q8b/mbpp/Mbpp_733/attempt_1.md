# Mbpp/733, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/733/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1407. Answer tokens: 148.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_first_occurrence that takes a sorted array and a number, and returns the index of the first occurrence of that number. Let's think about how to approach this.

The array is sorted, so maybe binary search would be efficient here. But the standard binary search finds any occurrence, not necessarily the first one. So I need to modify the binary search to find the first occurrence.

Let me recall: For finding the first occurrence, when the middle element is equal to the target, I shouldn't just return immediately. Instead, I should check if there's a possibility of an earlier occurrence. So maybe I should continue searching the left half even after finding a match.

Let me outline the steps. The idea is to perform a binary search where, when the target is found, we keep moving left to see if there's an earlier occurrence.

So here's a plan:

Initialize low as 0 and high as len(arr) - 1. Initialize result as -1 (in case the target isn't found).

While low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        result = mid  # record this position
        high = mid - 1  # continue searching left to find earlier occurrences
    elif arr[mid] < target:
        low = mid + 1
    else:
        high = mid - 1

At the end, return result if it's not -1, else maybe return -1? But according to the problem statement, the function is supposed to find the first occurrence. Wait, the problem says that the array is sorted, but it's possible that the target isn't present. However, the given example has the target present. But the problem says to return the index of the first occurrence. So maybe the function should return -1 if the target isn't present? Or maybe the problem assumes that the target is present? Let me check the example given.

In the example, the input array has 5s, and the function returns 1. So the function is supposed to return the first occurrence. But what if the target isn't present? The problem's assert statement doesn't cover that. However, the problem says to write a function that finds the first occurrence. So perhaps the function should return -1 if the target is not present. But the problem's example doesn't cover that. However, the problem's sample input has the target present. So the function needs to handle both cases.

But the problem's sample input is given, and the function is expected to return 1. So the code should handle the case when the target is present.

So the approach with the modified binary search should work. Let me test this logic with the sample input.

Sample input: [2,5,5,5,6,6,8,9,9,9], target 5.

Let me simulate the binary search steps.

Initial low=0, high=9. mid is (0+9)//2=4. arr[4] is 6, which is larger than 5. So high becomes 3.

Now low=0, high=3. mid is 1. arr[1] is 5. So set result=1, and set high=0 (mid-1=0). Now, low=0, high=0. mid is 0. arr[0] is 2 <5, so low becomes 1. Now low is 1, high is 0. Loop ends. So result is 1. Which matches the sample. So that works.

Another test case: if the array is [5,5,5], target 5. The first occurrence is 0. Let's see. Let's simulate.

low=0, high=2. mid=1. arr[1] is 5. set result=1, high=0. Now low=0, high=0. mid=0. arr[0] is 5. set result=0. high becomes -1. Loop ends. So returns 0. Correct.

Another test case: if the array is [5], target 5. returns 0. Correct.

Another case where the target is not present. For example, array [2,4,6], target 5. The function should return -1.

So the code would return -1 in that case.

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
            high = mid -1
    return result

Wait, but what if the array is empty? Well, the problem says it's a sorted array. But the function should handle that. For example, if the array is empty, returns -1.

But the problem's sample input is not empty. But the code would handle that.

So the code seems correct.

Now, the problem says to write the function, and the assert statement is given. So the code should pass the given assert.

So the code would be:

But wait, the problem says to write a function. So the code should include that function.

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

Then, the assert statement would be:

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1

Which is correct.

So that's the code. Let me check if there are any edge cases.

Another test case: when the first occurrence is at the beginning. Like [5,5,5], returns 0. Correct.

Another case where the target is the first element. Like [5,6,7], target 5. Returns 0.

Another case where the target is not present. Like [2,4,6], target 5. Returns -1.

Yes, the code handles that.

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

assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
```

**Visible-test report:**

```text
PASS    assert find_first_occurrence([2, 5, 5, 5, 6, 6, 8, 9, 9, 9], 5) == 1
1 of 1 visible tests passed
```
