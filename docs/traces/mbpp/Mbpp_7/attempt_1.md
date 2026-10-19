# Mbpp/7, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/7/a1/r1`)

Visible tests: **pass**. Thinking tokens: 743. Answer tokens: 55.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that finds all words in a string which are at least 4 characters long. The assert statement given is for testing, so I should make sure my function passes that test.

First, I need to think about how to split the string into words. In Python, the split() method can be used, but by default it splits on whitespace. However, the problem says "words", so maybe I should split on whitespace and then check each word's length.

Wait, but the example given is 'Please move back to stream'. The words are 'Please', 'move', 'back', 'stream'. The assert checks that the set of these words is correct. So the function should return a set of words that are 4 characters or longer.

So the steps are:

1. Split the input string into words. Using split() would split on any whitespace, which is correct here.
2. Iterate over each word in the list.
3. Check if the length of the word is >=4.
4. Collect those words into a set.
5. Return the set.

But wait, the assert statement uses set() on the result. So the function should return a set, and the assert checks that the set contains the correct words.

So the function could be something like:

def find_char_long(s):
    words = s.split()
    return {word for word in words if len(word) >=4}

Wait, but in Python, the set comprehension is written with curly braces. So that's correct.

Testing the example: 'Please move back to stream' → split into the four words. Each has lengths: 'Please' is 6, 'move' is 4, 'back' is 4, 'stream' is 6. So the set would be {'Please', 'move', 'back', 'stream'}, which matches the assert.

But wait, the assert is set(find_char_long(...)) == set(...). So the function returns a set, and the assert checks that the set is correct.

So the code should be:

def find_char_long(s):
    return {word for word in s.split() if len(word) >=4}

But I need to make sure that the split() is done correctly. What if there are multiple spaces between words? Like 'hello   world'? The split() method would split into ['hello', 'world'], which is correct. So the split() is okay.

So the code should be as simple as that. Let me test the example.

Testing the example input:

s = 'Please move back to stream'

split into ['Please', 'move', 'back', 'stream']

each word's length: 6,4,4,6. So the set is {'Please', 'move', 'back', 'stream'}, which matches the assert.

So the code should work.

But wait, what about words with leading or trailing spaces? Like '  hello  ' → split into ['hello'], which is correct. But the problem says "words", so perhaps the split() is okay.

So the code is correct. The imports? None needed, since it's just using built-in functions.

So the final code is:

def find_char_long(s):
    return {word for word in s.split() if len(word) >=4}

Then, the assert statement would be:

assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])

But the function returns a set, and the assert checks that the set is equal to the expected set.

So the code should be correct.
```

</details>

**Code that ran:**

```python
def find_char_long(s):
    return {word for word in s.split() if len(word) >= 4}

assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
```

**Visible-test report:**

```text
PASS    assert set(find_char_long('Please move back to stream')) == set(['Please', 'move', 'back', 'stream'])
1 of 1 visible tests passed
```
