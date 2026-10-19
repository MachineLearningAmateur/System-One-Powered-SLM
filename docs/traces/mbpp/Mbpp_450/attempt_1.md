# Mbpp/450, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/450/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 923. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to write a Python function that extracts strings of a specified size from a given list. The example given is that when the function is called with the list ['Python', 'list', 'exercises', 'practice', 'solution'] and size 8, it returns ['practice', 'solution']. 

Let me think about what's going on here. The input list has strings of different lengths. The task is to extract strings of exactly the specified size. But wait, the example shows that for size 8, the output is 'practice' and 'solution'. Let me check their lengths. 

'practice' is 8 characters long. 'solution' is also 8. So the function needs to take a list of strings and a size, and return those strings that are exactly of that size. But wait, the example shows that the input list has strings of varying lengths. So the function should filter the list to include only those strings that have exactly the specified size.

So the steps would be:

1. The function takes two parameters: the list of strings and the size.
2. Iterate through each string in the list.
3. Check if the length of the string equals the given size.
4. Collect those strings into a new list.
5. Return that new list.

Wait, but in the example, the input list has 'practice' and 'solution' which are 8 characters each. So the function is supposed to return those two. But how does the function know which ones to pick? Because the original list has other strings like 'Python' (6 letters), 'list' (4), etc. So the function should filter the list to include only those strings that are exactly of the given size.

So the function would be something like:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

But wait, the example shows that the input list is ['Python', 'list', 'exercises', 'practice', 'solution'] and the size is 8. So the code would check each string's length. Let's see:

- 'Python' is 6, so no.
- 'list' is 4, no.
- 'exercises' is 9 letters. Wait, 'exercises' is e-x-e-r-c-i-s-e-s? Let me count: e(1), x(2), e(3), r(4), c(5), i(6), s(7), e(8), s(9). Oh right, that's 9 letters. So the size is 8, so 'exercises' is 9, so it's excluded. Then 'practice' is 8, and 'solution' is 8. So the output is those two. So the code would work.

So the function is straightforward. The code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

But wait, the problem says to write a correct Python solution. Are there any edge cases? For example, if the list is empty, or if the size is zero. But the problem doesn't mention handling those, so perhaps the function is supposed to handle those cases as per Python's behavior. But the example given is for size 8, which is valid.

So the code would be as simple as that. Let me check the assert statement. The assert is that extract_string(['Python', 'list', 'exercises', 'practice', 'solution'], 8) == ['practice', 'solution'].

Yes, because the code would filter the list to include only the strings of length 8. So the code should work.

But wait, what if the size is not present in the list? For example, if the list has strings of length 5, and the size is 8, then the output is an empty list. But the problem doesn't specify handling that, so the function is correct as is.

So the code is correct. The imports are not needed here, since it's a simple list comprehension. So the code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

But the problem says to include any imports. But in this case, there are no imports needed. So the code is as above.

So the final code would be that function. Let me write it in the code block.
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
