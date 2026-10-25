# HumanEval/56, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/56/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 997. Answer tokens: 60.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if a string of brackets is correctly bracketed. The function should return True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, the examples given are like "<" returns False because there's an opening but no closing. Then "<>" is True. And "<<" followed by ">>" would be True. But something like "><<" would be False because the first closing bracket is before any opening ones.

So this feels like a classic stack problem. Because whenever I see an opening bracket, I push it onto the stack. When I see a closing bracket, I check if there's a matching opening one. If the stack is empty when I try to pop, that's an error. At the end, the stack should be empty.

Wait, but the brackets here are only "<" and ">". So each opening bracket is "<", and closing is ">". So the logic would be:

Initialize a counter or a stack. For each character in the string:

- If it's "<", push to stack (or increment a counter)
- If it's ">", check if there's a matching "<". So if the stack is not empty, pop it. Else, return False.

At the end, check if the stack is empty. If yes, return True, else False.

So for example, let's take the first example: "<". The stack would have one "<" at the end. So return False.

Another example: "<>". The first character is "<", push. Then ">", pop. Stack is empty, return True.

Third example: "<<><>>". Let's walk through:

Characters: '<', '<', '>', '<', '>', '>'.

Let me track the stack:

Start with empty stack.

1. '<' → stack becomes ['<']
2. '<' → ['<', '<']
3. '>' → pop → ['<']
4. '<' → ['<', '<']
5. '>' → pop → ['<']
6. '>' → pop → empty. So return True.

Yes, that's correct.

Another example: "><<>". Let's see:

Characters: '>', '<', '>', '<'.

First character is '>'. Stack is empty. So return False immediately.

So the algorithm would be:

Initialize a stack (or a counter). For each bracket in the string:

- If it's '<', add to stack.
- Else, if it's '>', check if stack is not empty. If empty, return False. Else, pop from stack.

At the end, check if stack is empty. If yes, return True, else False.

So in Python, the code would be something like:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for b in brackets:
        if b == '<':
            stack.append(b)
        else:
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, that seems straightforward. Let me test the examples.

First example: correct_bracketing("<") → stack is ['<'], returns not stack → False. Correct.

Second example: "<>" → stack after processing is empty. Returns True.

Third example: "<<><>>" → stack is empty at end. True.

Fourth example: "><<" → first character is '>', stack is empty → return False. Correct.

Yes, that seems to handle all the cases.

What about other cases? Like "<<<>>>" → stack after processing: after each '<' added, then three '>'s. Stack is empty. Returns True.

Another case: "><<>" → first '>', stack is empty → return False.

Another case: "<<><" → after processing, stack has one '<'. So returns False.

Yes. So this code should work.

So the code would be as above. Now, the function is supposed to return a boolean. The code uses a list as a stack. The code is simple and efficient.

So the Python code would be:

def correct_bracketing(brackets: str) -> bool:
    stack = []
    for b in brackets:
        if b == '<':
            stack.append(b)
        else:
            if not stack:
                return False
            stack.pop()
    return not stack

Wait, but the problem says that the input is a string of "<" and ">". So the code doesn't need to handle other characters. So this should be okay.

Testing the sample cases:

Sample 1: correct_bracketing("<") → returns False. Correct.

Sample 2: "<>" → True. Correct.

Sample 3: "<<><>>" → True. Correct.

Sample 4: "><<" → returns False. Correct.

Yes. So this code should work. So the code is correct.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    stack = []
    for b in brackets:
        if b == '<':
            stack.append(b)
        else:
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
