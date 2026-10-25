# Mbpp/450, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/450/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1030. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called extract_string that takes a list of strings and a size, and returns the strings from the list that have exactly that size. The example given is when the list is ['Python', 'list', 'exercises', 'practice', 'solution'] and the size is 8, the output should be ['practice', 'solution'].

First, I should think about how to approach this. The function needs to iterate through each string in the input list and check if its length equals the specified size. Then collect those strings into a new list.

So the steps are:

1. Define the function with parameters: the list of strings and the size.
2. Initialize an empty list to store the results.
3. Loop through each string in the input list.
4. For each string, check if len(string) == size.
5. If yes, append it to the result list.
6. Return the result list.

Wait, but what about cases where the size is zero? Well, the problem probably assumes that the size is a positive integer, but since the example uses 8, maybe we don't need to handle that. But the function should handle any valid input as per the problem's constraints.

Now, the example given: the input list has 'practice' which is 8 letters (p-r-a-c-t-i-c-e: 8?), let me count. 'practice' is p (1), r(2), a(3), c(4), t(5), i(6), c(7), e(8). Yes, 8 letters. Similarly 'solution' is s-o-l-u-t-i-o-n: 8 letters. So the function correctly returns those two.

So the code would be something like:

def extract_string(strings, size):
    result = []
    for s in strings:
        if len(s) == size:
            result.append(s)
    return result

Wait, but the assert statement in the problem uses the list and 8. Let me test this code with that example.

The list is ['Python', 'list', 'exercises', 'practice', 'solution'].

Check each string:

'Python' has length 6. 'list' is 4. 'exercises' is 9 letters. 'practice' is 8, 'solution' is 8. So the result is ['practice', 'solution'], which matches the example.

So that's correct. But wait, the problem says "extract specified size of strings". So the function is supposed to return the strings that have exactly that length. So the code seems correct.

But what about the parameters? The function parameters are the list and the size. So the code is correct.

Now, the problem says to write the function and include any imports. But in this case, no imports are needed. So the code would be as above.

But the user wants the code in a code block, including any imports. So the code would be:

def extract_string(strings, size):
    result = []
    for s in strings:
        if len(s) == size:
            result.append(s)
    return result

But wait, maybe using list comprehensions would be more concise. Like:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

Yes, that's even better. So the code can be written in one line with a list comprehension.

So the function is straightforward. Let me check the example again. The sample input is the list and 8. The code would return the list of strings with length 8. Which works.

So the code should be correct. Now, the user wants the code in a code block. So the complete code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

But wait, the problem says to write the function. So that's the code. But the user also wants the assert statement. Wait, the problem says to write the function, but the example includes an assert. However, the user's instruction says to write the function, and the code should include any imports. So the code should have the function, and the assert is just an example. But the user probably wants the code that includes the function, and perhaps the assert is part of the test case. However, the problem says to write the function, so the code should include the function. The user's example shows the assert, but the code to be written is the function. So the code should be the function, and the assert is part of the test case. But the user's problem says to write the function, so the code should be the function. But the user's instruction says to write the code that includes any imports. But in this case, no imports are needed.

So the code is as above. So the answer is the function as written. Let me check again.

Yes. So the code is correct. Let me write that.
```

</details>

**Code that ran:**

```python
def extract_string(strings, size):
    return [s for s in strings if len(s) == size]
```

**Visible-test report:**

```text
PASS    assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'] ,8)==['practice', 'solution']
1 of 1 visible tests passed
```
