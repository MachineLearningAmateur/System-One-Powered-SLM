# Mbpp/450, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/450/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 713. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called extract_string that takes a list of strings and a size, and returns a list of the strings that have exactly that size. Let me think about how to approach this.

So the example given is extract_string(['Python', 'list', 'exercises', 'practice', 'solution'], 8) should return ['practice', 'solution']. Let me check the lengths. 'practice' is 8 letters? Let me count: p-r-a-c-t-i-c-e, that's 8. Yes. 'solution' is s-o-l-u-t-i-o-n, 8 letters. So the function needs to filter the list to include only those strings with length equal to the given size.

So the steps are: iterate over each string in the input list, check if the length of the string is equal to the specified size. If yes, include it in the result list.

So the function would look something like:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

Wait, but what about the order? The example shows that the output is in the same order as the input. Since the list comprehension processes the input list in order, the output will maintain the original order. So that's correct.

Let me test with the example. The input list is ['Python', 'list', 'exercises', 'practice', 'solution']. Let's check each length:

'Python' is 6 letters. 'list' is 4. 'exercises' is 9. 'practice' is 8. 'solution' is 8. So the output should be ['practice', 'solution'], which matches the assertion.

So the code seems correct. But wait, what if there are multiple strings with the same length? Like if two strings have length 8, they should both be included. The list comprehension handles that.

What about edge cases? Like empty list, or size zero? Well, the problem says 'given list of string values' so maybe the input is valid. But the function should handle any size, even zero. For example, if size is zero, it would return empty list unless there's a string with zero length (empty string). But the problem's example uses 8, so maybe the function is intended to work for any size.

So the code should be straightforward. Let me write the function.

Now, the user wants the code in a code block, including any imports. But this code doesn't need any imports. So the code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

Then, the assertion given in the problem should work. Let me check. The sample input is the list and 8, and the output is the two strings. So yes.

Wait, but the function is supposed to be called extract_string, and the parameters are the list and the size. So the code is correct.

So the complete code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

Then, the assertion would be:

assert extract_string(['Python', 'list', 'exercises', 'practice', 'solution'], 8) == ['practice', 'solution']

But the user wants the code to include the function and any imports. Since there are no imports needed, the code is as above.

So that's the solution.
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
