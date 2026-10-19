# Mbpp/102, attempt 1

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/102/a1/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 890. Answer tokens: 44.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that converts a snake case string to camel case. Let's think about how snake case and camel case differ. 

Snake case uses underscores to separate words, like 'python_program'. Camel case joins them without underscores, so 'PythonProgram'. 

So the task is to replace the underscores with uppercase letters, but only once per word. Wait, but how do I handle multiple underscores? Like 'hello_worlds' should become 'HelloWorlds'. 

Hmm, the approach could be to split the string by underscores, then capitalize the first letter of each part, and join them. But wait, the first part should be lowercase. For example, if the input is 'python_program', splitting by '_' gives ['python', 'program'], then capitalize each part. So 'PythonProgram' which is correct.

But what about if the input is empty? Well, the assert example shows 'python_program' so maybe the function should handle empty strings as well. But maybe the problem assumes that the input is a valid snake case string, but the function should handle empty strings.

So the steps would be:

1. Split the input string into parts using '_' as the delimiter.
2. Iterate over each part, capitalize the first letter, and make the rest lowercase.
3. Join the parts together.

Wait, but splitting on underscores would split the string into parts. For example, 'hello_worlds' becomes ['hello', 'worlds'], then each part is capitalized. So 'HelloWorlds'.

But how to handle the first part? For example, if the input is 'hello_world', then splitting gives ['hello', 'world'], which becomes 'HelloWorld'.

So the code could be something like:

def snake_to_camel(s):
    parts = s.split('_')
    return ''.join([part.capitalize() for part in parts])

Wait, but what about if the input is empty? Well, split on empty string would return [''], and then capitalize would make it ' '. Wait, no. Wait, if the input is empty, then s.split('_') would return [''], and then part.capitalize() would be ''. So the function would return an empty string, which is correct.

Testing the example given: 'python_program' → split into ['python', 'program'], capitalize each part → 'PythonProgram' which is correct.

Another test case: 'hello_worlds' → ['hello', 'worlds'] → 'HelloWorlds'.

Another case: 'a_b_c' → 'Abc'.

What about 'a_b_c_d' → 'Abcd'.

So this seems to work.

But wait, what if the input is 'a_b_c' with multiple underscores? The code would split into parts and capitalize each. So yes.

So the code would be:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

But wait, the split method splits on every occurrence of the separator. So for example, 'hello__world' would split into ['hello', '', 'world'], then capitalize each part. The empty string would become '', so the result would be 'HelloWorld'. Which is correct.

Yes, that's correct. So the code should work.

Now, the assert statement is given as assert snake_to_camel('python_program') == 'PythonProgram'. So the code should pass that.

So the complete code would be:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

But wait, what about if the input is 'hello_world'? Split into ['hello', 'world'], then capitalize each part. So 'HelloWorld' which is correct.

Yes.

So the code is correct. Now, I need to write it in a code block with the imports. But since there are no imports needed, the code is just the function.

So the final code is:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

But wait, the problem says to include any imports. But in this case, there are no imports needed. So the code is as above.

Testing the example:

snake_to_camel('python_program') → split into ['python', 'program'], capitalize each part → 'PythonProgram' which is correct.

Yes. So this should work.
```

</details>

**Code that ran:**

```python
def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

# Test case
assert snake_to_camel('python_program') == 'PythonProgram'
```

**Visible-test report:**

```text
PASS    assert snake_to_camel('python_program')=='PythonProgram'
1 of 1 visible tests passed
```
