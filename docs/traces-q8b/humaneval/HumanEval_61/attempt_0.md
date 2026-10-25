# HumanEval/61, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1211. Answer tokens: 134.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if a string of brackets is correctly balanced. The function should return True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, I remember that a common way to check for balanced brackets is using a stack. The idea is to iterate through each character in the string. Whenever I see an opening bracket '(', I push it onto the stack. When I see a closing bracket ')', I check if there's a matching opening bracket in the stack. If there is, I pop it from the stack. If not, then it's unbalanced.

Wait, but what about cases where the closing bracket comes before an opening one? Like the example given, ")(()", which should return False. Let me see. For the first character ')', the stack is empty, so that's invalid. So the stack approach would catch that.

So the steps would be:

1. Initialize an empty stack.
2. Iterate over each character in the input string.
3. For each '(', push it onto the stack.
4. For each ')', check if the stack is empty. If it is, return False. Otherwise, pop the top element (which should be '(').
5. After processing all characters, check if the stack is empty. If not, there are unmatched '(', so return False. Otherwise, return True.

Let me test this logic against the examples.

First example: correct_bracketing("(") → returns False. The stack would have one '(', and after processing, the stack isn't empty. So returns False. Correct.

Second example: "()" → stack starts empty. First '(', push. Then ')', check stack not empty, pop. Stack is empty, return True. Correct.

Third example: "(()())". Let's walk through:

- '(', push → stack: ['(']
- '(', push → stack: ['(', '(']
- ')', pop → stack: ['(']
- '(', push → stack: ['(', '(']
- ')', pop → stack: ['(']
- ')', pop → stack empty. Return True. Correct.

Fourth example: ")(()". Let's see:

- First character ')', stack is empty → return False. So the function returns False. Correct.

So this logic should work.

Now, how to implement this in Python.

The function is called correct_bracketing, takes a string brackets.

Implementing the stack as a list. Let's code:

Initialize stack = []

for char in brackets:

    if char == '(':

        stack.append(char)

    else:  # char is ')'

        if not stack:

            return False

        stack.pop()

At the end, return len(stack) == 0.

Yes. So the code would be:

def correct_bracketing(brackets: str) -> bool:

    stack = []

    for char in brackets:

        if char == '(':

            stack.append(char)

        else:

            if not stack:

                return False

            stack.pop()

    return len(stack) == 0

Wait, but what about other characters? The problem says that the input is a string of '(' and ')', so no need to handle other characters. So the code is okay.

Testing the sample cases:

Test case 1: "(" → stack after processing is ['('], so returns False. Correct.

Test case 2: "()" → stack is empty after processing. Returns True.

Test case 3: "(()())" → stack is empty. Returns True.

Test case 4: ")(()" → first char is ')', stack is empty → returns False. Correct.

So this should work.

I think that's the correct approach. So the code should be as above. Let me write the code with the correct syntax and include the docstring as specified.

Wait, the function is supposed to have the docstring as given. Let me check the original problem's sample.

The sample shows:

def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """

So the function's docstring is as given. So the code should include that.

So the code would be:

def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        else:
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

Wait, but in Python, the function's docstring is included as the first string. So the code as written would have the docstring as specified.

Yes. So that's the code. Let me check for any possible errors.

What about empty string? For example, correct_bracketing("") → returns True. Because there are no brackets to mismatch. But according to the problem statement, the input is a string of brackets. So empty string is allowed. The function would return True, which is correct.

Another test case: "(()". The stack would have one '(', so returns False. Correct.

Another case: "()()". Stack is empty, returns True. Correct.

So the code should handle all cases correctly.

So the code is correct.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str):
    """ brackets is a string of "(" and ")".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("(")
    False
    >>> correct_bracketing("()")
    True
    >>> correct_bracketing("(()())")
    True
    >>> correct_bracketing(")(()")
    False
    """
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        else:
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("(") == False
PASS    assert correct_bracketing("()") == True
PASS    assert correct_bracketing("(()())") == True
PASS    assert correct_bracketing(")(()") == False
4 of 4 visible tests passed
```
