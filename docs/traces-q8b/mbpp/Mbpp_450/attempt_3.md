# Mbpp/450, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/450/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 719. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called extract_string that takes a list of strings and a size, and returns a list of the strings that have exactly that size. Let me think about how to approach this.

So the example given is extract_string(['Python', 'list', 'exercises', 'practice', 'solution'], 8) should return ['practice', 'solution']. Let me check the lengths. 'practice' is 8 letters? Let's see: p-r-a-c-t-i-c-e, that's 8. Yes. 'solution' is s-o-l-u-t-i-o-n, 8 letters. The others: 'Python' is 6, 'list' is 4, 'exercises' is 9. So the function needs to filter the list to include only those strings with length equal to the given size.

So the steps are: iterate through each string in the input list, check if its length is equal to the specified size, and collect those strings into a new list.

Now, how to implement this. The function will take two parameters: the list of strings and the size. Then, return a list comprehension that includes each string from the list where len(string) == size.

Wait, but what about cases where the size is zero? Well, the problem probably assumes that the size is a positive integer. But since the example uses 8, maybe the function is intended to handle any integer. But the function should handle any valid input, but perhaps the test cases will cover that.

So the code would be something like:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

Wait, but the assert in the example uses 8 and the list. Let me test that. For the given example, the list is ['Python', 'list', 'exercises', 'practice', 'solution'], and the size is 8. The list comprehension would check each string's length. 'practice' is 8, 'solution' is 8. So the output is those two. Which matches the example.

But wait, the function is supposed to return a list of the strings that have exactly that size. So that's correct.

But what about the order? The original list's order is preserved. The example returns ['practice', 'solution'], which are in the same order as they appear in the input list. So the code is correct.

So the code is straightforward. Now, the problem says to write the function and include any imports. But in this case, there are no imports needed. So the code would be:

def extract_string(strings, size):
    return [s for s in strings if len(s) == size]

But wait, the problem says to write a function that extracts specified size of strings. So that's exactly what this does.

Let me test the sample input. Let's see:

The input list is ['Python', 'list', 'exercises', 'practice', 'solution'], size 8. The function returns the list of strings with length 8. Which are 'practice' and 'solution', so the assert would pass.

So this should be the correct solution. But perhaps I need to handle cases where the size is zero? Well, the problem says "specified size of strings" but the example uses 8. So the function is intended to work for any size. But the code will handle that.

So the code is correct. Therefore, the final code is as written.
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
