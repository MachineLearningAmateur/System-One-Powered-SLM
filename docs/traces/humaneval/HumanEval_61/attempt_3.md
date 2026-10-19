# HumanEval/61, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1142. Answer tokens: 63.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if all the opening brackets in a string have corresponding closing brackets. The function is called correct_bracketing and takes a string of parentheses. The goal is to return True if every opening bracket has a closing one, otherwise False.

Let me think about how to approach this. The problem seems similar to checking balanced parentheses. The classic approach for this is using a stack. Whenever I see an '(', I push it onto the stack. When I see a ')', I pop from the stack if it's not empty. If the stack is empty when I pop, that means there's a closing bracket without a matching opening one, so return False.

Wait, but what about the case where the string is empty? Well, the problem says the input is a string of '(' and ')', but maybe the function can handle empty strings. But according to the examples, like the first one, the input is "(" which is invalid. So the function should return False for empty string? Well, the problem says the input is a string, but maybe the function is supposed to handle empty strings as well. But the examples don't include that. Let's see.

But the problem says the input is a string of '(' and ')', so maybe the function can assume that the input is non-empty. But the code should handle all possible cases.

So the steps are:

Initialize a stack. Iterate through each character in the string.

For each character:

- If it's '(', push it onto the stack.
- If it's ')', check if the stack is not empty. If it's empty, return False. Otherwise, pop the top element.

At the end, if the stack is empty, return True. Otherwise, return False.

Wait, but what if the stack is not empty at the end? That means there are more opening brackets than closing ones. So the function returns False.

Yes. So for example, the input ")(" would have the stack as empty after processing the first ')', then when processing the '(', the stack is not empty, so we pop. Wait, no. Let me think.

Let me take the example of ")(".

First character is ')', stack is empty. So we check if stack is empty, return False. So the function returns False, which is correct.

Another example: ")(()". Let's see:

First character is ')', stack is empty. So return False. Which matches the example.

Another example: "(()())". Let's process each character:

Index 0: '(', push. Stack: ['(']
Index 1: '(', push. Stack: ['(', '(']
Index 2: ')', pop. Stack: ['(']
Index 3: '(', push. Stack: ['(', '(']
Index 4: ')', pop. Stack: ['(']
Index 5: ')', pop. Stack empty. Return True. So that's correct.

So the stack approach works here.

So the code would be:

Initialize a stack. For each char in brackets:

if char is '(', push to stack.

else if char is ')', check if stack is empty. If yes, return False. Else, pop.

At the end, check if stack is empty. If yes, return True, else False.

So the code in Python would be:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, but what about the case where the string is empty? Well, the function would return True, but according to the problem's examples, the input is a string of '(' and ')', but perhaps the function can handle empty strings. But the problem's examples don't have that. However, the problem says that the input is a string of '(' and ')', but maybe the function should return True if the string is empty? Well, the problem says that the input is a string of '(' and ')', but perhaps the function is supposed to return True if the string is empty. But in the examples, the first case is "(" which is invalid. So for the empty string, the function would return True, which is correct.

But let's check the code. For example, if the input is empty, then the stack is empty, so return True. Which is correct.

So the code seems to handle all cases.

Testing the examples:

correct_bracketing("(") → returns False. Because stack is empty after processing the '(', so returns False.

correct_bracketing("()") → stack is empty at the end. Returns True.

correct_bracketing("(()())") → returns True.

correct_bracketing(")(()") → first character is ')', stack is empty. Return False.

Yes, that's correct.

So the code should be correct.

Now, I need to write this in Python, including any necessary imports. But since there are no imports needed, the code is straightforward.

So the code is:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, but in Python, the stack is a list. So the code is correct.

Yes. So that's the solution.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return not stack
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("(") == False
PASS    assert correct_bracketing("()") == True
PASS    assert correct_bracketing("(()())") == True
PASS    assert correct_bracketing(")(()") == False
4 of 4 visible tests passed
```
