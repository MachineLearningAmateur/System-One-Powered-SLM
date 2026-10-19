# Mbpp/280, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/280/a1/r1`)

Visible tests: **pass**. Thinking tokens: 817. Answer tokens: 59.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that performs a sequential search on an array. The function should return a tuple with a boolean and the index of the element if it's found, else -1. Let me think about how to approach this.

First, the function signature. Let's say the function is called sequential_search, and it takes three parameters: the array, the element, and maybe return the tuple. Wait, the problem says the function takes in an array and an element. So the function would be something like:

def sequential_search(arr, element):

Wait, but the assert statement shows that the first argument is the array, and the second is the element. So the function should take the array and the element as parameters.

So the function needs to check if the element is present in the array. Then return True/False and the index.

Now, how to implement sequential search. The straightforward way is to iterate through each element in the array, check if it's equal to the target element. Once found, return the index. If none found, return -1.

So, the steps:

Initialize a variable to track whether the element is found. Let's say found = False. Then, loop through each index in the array. For each element, if it's equal to the target, set found to True and break the loop. Then, return (found, index) if found, else (-1, -1) ?

Wait, but the problem says if the element is not found, return -1. So, the index is -1 in that case.

So, in code:

def sequential_search(arr, element):
    found = False
    index = -1
    for i in range(len(arr)):
        if arr[i] == element:
            found = True
            index = i
            break
    return (found, index)

Wait, but what if the array is empty? Well, the problem doesn't mention handling that, so maybe we can assume the array is non-empty. But in Python, if the array is empty, then len(arr) is 0, and the loop doesn't run. So index remains -1, and found is False. Which is correct.

Testing the example given: [11,23,58,31,56,77,43,12,65,19], element 31. The index is 3, so the function returns (True, 3). Which matches the assert.

But wait, what if the element is not present? Like, if the array is [1,2,3], and the element is 4. Then the function returns (False, -1). Which is correct.

So that's the code. Now, the imports? Well, the code doesn't need any imports, since it's just a function. So the code would be:

def sequential_search(arr, element):
    found = False
    index = -1
    for i in range(len(arr)):
        if arr[i] == element:
            found = True
            index = i
            break
    return (found, index)

Wait, but what if the array is empty? Well, the code would return (False, -1), which is correct.

Testing the assert statement: sequential_search([11,23,58,31,56,77,43,12,65,19],31) should return (True, 3). Which it does.

So that's the solution. I think that's correct. Let me check for possible errors.

Another test case: if the element is the first element. Like [5, 10, 15], element 5. Then index is 0. Correct.

Another case: element not present. Like [1,2,3], element 4. Returns (False, -1). Correct.

Yes, this should work.
```

</details>

**Code that ran:**

```python
def sequential_search(arr, element):
    found = False
    index = -1
    for i in range(len(arr)):
        if arr[i] == element:
            found = True
            index = i
            break
    return (found, index)
```

**Visible-test report:**

```text
PASS    assert sequential_search([11,23,58,31,56,77,43,12,65,19],31) == (True, 3)
1 of 1 visible tests passed
```
