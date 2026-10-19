# Mbpp/773, attempt 3

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/773/a3/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 1138. Answer tokens: 51.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that finds the occurrence and position of a substring within a string. The function should return None if there's no match. The example given is that for the string 'python programming, python language' and the substring 'python', the function should return ('python', 0, 6). Let me think about how to approach this.

First, I need to understand what the function is supposed to do. The function takes two arguments: the main string and the substring to find. The return value is a tuple containing the substring, the starting index, and the length of the substring. Wait, in the example, the starting index is 0 and the length is 6. Wait, the substring 'python' is 6 characters long. So the output is ('python', 0, 6). So the function needs to return the substring, the starting index, and the length of the substring. But wait, the example shows that the starting index is 0, and the length is 6. So the function is supposed to return the substring, the start index, and the length. But how does that fit into the problem?

Wait, the problem says to find the occurrence and position of the substrings. So the position is the starting index. So the function needs to find the first occurrence of the substring in the main string, and return the substring, the starting index, and the length of the substring. But if there are multiple occurrences, maybe the first one? Or maybe the first occurrence? The example shows that the first occurrence is at index 0. But maybe the function is supposed to return the first occurrence.

So the plan is: find the first occurrence of the substring in the main string. If found, return the substring, start index, and length. Otherwise, return None.

But how to find the first occurrence in Python. The string method 'find()' returns the first occurrence's index. So for example, 'python'.find('python') returns 0. Then, the length is len('python') which is 6. So the function can be written as:

def occurance_substring(main_str, sub_str):
    index = main_str.find(sub_str)
    if index != -1:
        return (sub_str, index, len(sub_str))
    else:
        return None

Wait, but the example given is that the function returns ('python', 0, 6). Let's check. The main_str is 'python programming, python language'. The first occurrence of 'python' is at index 0. So the code would return (sub_str, index, len(sub_str)), which is correct.

But what if the substring is not present? Then return None. So the code seems straightforward.

But wait, what if the substring is empty? Well, according to the problem statement, the function is supposed to return None if there's no match. But the substring is empty, then the find method would return -1, but the code would return None. But the problem says that the function is supposed to return None if there's no match. So that's handled.

But the problem says that the function is to return the occurrence and position. So the code seems correct.

But let me check the example again. The example input is 'python programming, python language' and the substring 'python'. The first occurrence is at index 0. So the code returns (sub_str, 0, 6). Which matches the example.

So the code would be:

def occurance_substring(main_str, sub_str):
    index = main_str.find(sub_str)
    if index != -1:
        return (sub_str, index, len(sub_str))
    else:
        return None

But wait, what if the substring is not found? For example, if the main_str is 'abc' and sub_str is 'xyz', then return None.

But the problem says to return None if there is no match. So that's correct.

Now, the assert statement in the problem says that occurance_substring('python programming, python language','python')==('python', 0, 6). So the code should pass that.

But let me test the code with that example. The main_str is 'python programming, python language'. The sub_str is 'python'. The find method returns 0, so the code returns (sub_str, 0, 6). Which matches the example.

So the code seems correct.

But what about cases where the substring is not present? For example, if the main_str is 'abc', and the sub_str is 'bcd', then the code returns None. Which is correct.

So the code is correct.

Now, the problem says to write the code with the correct imports. But the code doesn't need any imports. The find method is part of the string class. So no imports are needed.

So the complete code is:

def occurance_substring(main_str, sub_str):
    index = main_str.find(sub_str)
    if index != -1:
        return (sub_str, index, len(sub_str))
    else:
        return None

But wait, the problem says to return None if there is no match. So the code is correct.

But the assert statement in the problem is written as:

assert occurance_substring('python programming, python language','python')==('python', 0, 6)

Which would check that the function returns the correct tuple.

So the code is correct.

So the final code is as above.
```

</details>

**Code that ran:**

```python
def occurance_substring(main_str, sub_str):
    index = main_str.find(sub_str)
    if index != -1:
        return (sub_str, index, len(sub_str))
    else:
        return None
```

**Visible-test report:**

```text
PASS    assert occurance_substring('python programming, python language','python')==('python', 0, 6)
1 of 1 visible tests passed
```
