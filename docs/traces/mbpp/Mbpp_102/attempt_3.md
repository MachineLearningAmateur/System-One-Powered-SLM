# Mbpp/102, attempt 3

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/102/a3/r1`)

Visible tests: **pass**. Thinking tokens: 906. Answer tokens: 230.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that converts a snake case string to camel case. Let's see. The example given is 'python_program' becoming 'PythonProgram'. So, the function should split the string on underscores and then capitalize each word except the first one. Wait, but the first word is already capitalized. Wait, no. Wait, in the example, the first letter is capitalized. So, the first word is capitalized, and the rest are capitalized as well. So, the approach is to split the string into parts, capitalize each part, and join them without underscores.

So, for example, 'python_program' splits into ['python', 'program'], then capitalize each part. So 'PythonProgram'.

So the steps are: split the input string by underscores, then capitalize each part, then join them.

But how to split? Using the split('_') method. But wait, if there are multiple underscores, like 'hello_world_world', splitting would give ['hello', 'world', 'world'], then capitalize each part. So 'HelloWorldWorld'.

So the function would be something like:

def snake_to_camel(s):
    parts = s.split('_')
    return ''.join([part.capitalize() for part in parts])

Wait, but what about the first part? Because if the original string starts with an underscore, like '_python_program', then splitting would give ['', 'python', 'program'], and capitalizing the first part would make it 'PythonProgram'. But the original string starts with an underscore, but the example given doesn't have that. But the problem says that the input is a snake case string, which typically doesn't start with an underscore. But the function should handle any input, even if it starts with an underscore. So, for example, if the input is '_python_program', the function would split into ['', 'python', 'program'], then capitalize each part. The first part is empty, so capitalize would return the empty string. Then the rest would be 'PythonProgram'. So the result would be 'PythonProgram' as desired. But maybe the function should not capitalize the first part if it's empty. Wait, but in the case of an empty string, the capitalize() method returns the empty string. So that's okay.

But perhaps the function should handle cases where the input is empty or has leading or trailing underscores. But the problem statement says that the input is a snake case string. So maybe the input is valid, but the function should handle all cases.

So the code would be:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

Wait, but what about if the input is empty? Well, the function would return an empty string, which is correct.

Testing the example: 'python_program' becomes 'PythonProgram'.

Another test case: 'hello_world' becomes 'HelloWorld'.

Another case: 'hello_world_abc' becomes 'HelloWorldAbc'.

What about 'a_b_c' becomes 'Abc'.

Yes, that seems correct.

So the code is straightforward. The split on underscores, capitalize each part, join.

But wait, the split method splits on every occurrence of the underscore. So for example, 'hello__world' would split into ['hello', '', 'world'], then capitalize each part. So 'HelloWorld'.

Yes, that's correct.

So the code is as simple as that. So the function is written.

Now, the assert statement is given. So the code would be:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

Then, the assert statement would be:

assert snake_to_camel('python_program') == 'PythonProgram'

So the complete code would be:

def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

But wait, what about if the input is empty? Well, the function would return an empty string, which is correct.

But maybe the problem expects that the input is non-empty. But the problem statement says that the input is a snake case string, which is typically non-empty. But the code handles all cases.

So the code is correct. Let me check the example again. The input is 'python_program', split into ['python', 'program'], capitalize each part, join. So 'PythonProgram' which is correct.

Yes, that's the correct solution.
```

</details>

**Code that ran:**

```python
def snake_to_camel(s):
    return ''.join(part.capitalize() for part in s.split('_'))

# Example usage
assert snake_to_camel('python_program') == 'PythonProgram'
```

**Visible-test report:**

```text
PASS    assert snake_to_camel('python_program')=='PythonProgram'
1 of 1 visible tests passed
```
