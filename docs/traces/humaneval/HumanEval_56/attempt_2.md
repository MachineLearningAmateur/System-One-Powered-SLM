# HumanEval/56, attempt 2

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`HumanEval/56/a2/r1`)

Visible tests: **pass**. Thinking tokens: 815. Answer tokens: 63.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if all the opening brackets in a string have corresponding closing brackets. The function is called correct_bracketing and takes a string of '<' and '>'. The goal is to return True if every opening bracket has a closing one, otherwise False.

Let me think about the approach. So, the basic idea is that for every opening bracket '<', there must be a closing '>', and the order must be correct. But how do I check that?

Hmm, one way is to use a stack. Like, whenever I see an opening bracket, I push it onto the stack. Then, when I see a closing bracket, I pop from the stack. If the stack is empty when I encounter a closing bracket, that means there's an unmatched closing bracket. Also, if the stack is not empty after processing all characters, there are unmatched opening brackets.

Wait, right. So the steps would be:

1. Initialize a stack.
2. Iterate through each character in the string.
3. For each character:
   - If it's '<', push to stack.
   - If it's '>', check if the stack is not empty. If it's empty, return False. Otherwise, pop from the stack.
4. After processing all characters, check if the stack is empty. If not, return False.
5. Otherwise, return True.

Yes, that makes sense. Let me test this logic with the examples given.

Testing the first example: "<" → stack is empty when we process the first '<', so returns False. Correct.

Second example: "<>" → first '<' pushed. Then '>' comes, stack is not empty, pop. Then stack is empty. Return True. Correct.

Third example: "<<><>>" → Let's see. Let's process each character:

First '<' → stack [ '<' ]
Second '<' → stack [ '<', '<' ]
Third '>' → pop → stack [ '<' ]
Fourth '>' → pop → stack empty.
Then the last '>' → stack is empty, so pop. So after processing all, stack is empty. Return True. Correct.

Fourth example: "><<>". Let's process:

First '>' → stack is empty. So when we see '>', check stack is empty → return False. So that's correct.

So this logic should work.

Now, implement this in Python.

So the code would be:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        elif char == '>':
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, but what about the case where there are more opening brackets than closing ones? Like "<<<". Then, the stack would have three elements, and after processing, return False. Correct.

Yes. So that's the code.

Now, check the examples again. Let me see.

Another test case: "<<" → stack has two elements. After processing, stack is not empty → return False. Correct.

Another case: "<>><" → Let's see. First '<' pushed. Then '>' pops. Then '>' again, stack is empty. Then '>', stack is empty → returns False. Correct.

So this code should handle all cases.

So the code is as written above. Now, the problem says to include any imports. But since this is a simple stack operation, no imports are needed. So the code is straightforward.

So the final code is:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        elif char == '>':
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, but in Python, the stack is a list. So the code is correct.

Yes. That should be the solution.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    stack = []
    for char in brackets:
        if char == '<':
            stack.append(char)
        elif char == '>':
            if not stack:
                return False
            stack.pop()
    return not stack
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("<") == False
PASS    assert correct_bracketing("<>") == True
PASS    assert correct_bracketing("<<><>>") == True
PASS    assert correct_bracketing("><<>") == False
4 of 4 visible tests passed
```
