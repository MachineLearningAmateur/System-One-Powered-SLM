# HumanEval/56, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/56/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1078. Answer tokens: 141.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if a string of brackets is correctly balanced. The function should return True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, the problem is similar to the classic valid parentheses problem. The standard approach for that is using a stack. Every time I see an opening bracket, I push it onto the stack. When I see a closing bracket, I check if there's a matching opening one. If the stack is empty when I encounter a closing bracket, that's invalid. Also, after processing all characters, the stack should be empty.

Wait, but in this case, the brackets are only '<' and '>'. So the logic is similar. Let me think about the steps.

So, for each character in the string:
- If it's '<', push it onto the stack.
- If it's '>', check if the stack is not empty. If it's empty, return False. Otherwise, pop the top element (which should be '<').

At the end, if the stack is empty, return True, else False.

Let me test this logic against the examples.

First example: correct_bracketing("<") → returns False. Because the stack would have one '<' left, so the stack isn't empty. Correct.

Second example: "<>" → stack starts empty. Push '<', then when '>', pop. Stack is empty. Return True. Correct.

Third example: "<<><>>". Let's walk through:

Characters: '<', '<', '>', '<', '>', '>'.

Process:
- '<' → stack: ['<']
- '<' → stack: ['<', '<']
- '>' → pop → stack: ['<']
- '<' → stack: ['<', '<']
- '>' → pop → stack: ['<']
- '>' → pop → stack empty. So return True. Correct.

Fourth example: "><<>". Let's see:

Characters: '>', '<', '<', '>'.

Process:
First character is '>'. Stack is empty → return False. So the function returns False. Which matches the example.

So the logic seems solid.

Now, how to implement this in Python.

The function will take a string 'brackets'. Initialize a stack (a list). Iterate through each character in the string. For each character:

if it's '<', append to stack.

else (it's '>'):

   if stack is empty → return False.

   else, pop from stack.

At the end, check if stack is empty. Return True if yes, else False.

So code steps:

def correct_bracketing(brackets: str) -> bool:

    stack = []

    for char in brackets:

        if char == '<':

            stack.append(char)

        else:

            if not stack:

                return False

            stack.pop()

    return len(stack) == 0

Wait, that's the core logic. Let me test the sample cases.

Sample 1: input is "<". The stack after processing is ['<'], so returns False. Correct.

Sample 2: "<>", stack after processing is empty → returns True.

Sample 3: "<<><>>" → stack is empty at the end → True.

Sample 4: "><<>" → first character is '>', stack is empty → return False. Correct.

Yes, that seems to handle all cases.

What about other edge cases? Like empty string? Well, according to the problem statement, the input is a string of brackets. But the empty string would return True, since there are no unmatched brackets. But the problem's examples don't cover that. However, the function would return True for empty string.

But according to the problem's examples, the function is supposed to return True when all opening brackets are closed. So empty string is a valid case.

Another test case: "<<<>>>" → stack after processing: after three '<', then three '>', so stack is empty. Return True.

Another case: "<<<>>" → stack has one '<' left → return False.

So the code seems to handle all these cases.

So the code is straightforward. Now, the code needs to be written in Python, with the given function signature. Also, the docstring is provided, but the code should include the correct function.

So the code would be:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        else:
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

Wait, but the function is supposed to return True if every opening bracket has a corresponding closing bracket. So this code does that. Because the stack is empty at the end, which means all opening brackets have been matched.

Yes. So that's the correct solution.

I think that's all. Let me check the sample inputs again.

Sample 1: correct_bracketing("<") → returns False. Correct.

Sample 2: "<>" → True.

Sample 3: "<<><>>" → True.

Sample 4: "><<>" → returns False. Correct.

Yes. So the code should work.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    """
    brackets is a string of "<" and ">".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("<")
    False
    >>> correct_bracketing("<>")
    True
    >>> correct_bracketing("<<><>>")
    True
    >>> correct_bracketing("><<>")
    False
    """
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        else:
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("<") == False
PASS    assert correct_bracketing("<>") == True
PASS    assert correct_bracketing("<<><>>") == True
PASS    assert correct_bracketing("><<>") == False
4 of 4 visible tests passed
```
