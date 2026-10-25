# HumanEval/56, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/56/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1186. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if a string of brackets is correctly bracketed. The function should return True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, the examples given are like "<" returns False because there's an opening but no closing. Then "<>" is True. For "<<><>>", it's True. But "><<" is False. So the main idea is that every opening bracket must have a matching closing one, and they must be properly nested.

Wait, this reminds me of the classic valid parentheses problem. Oh right! The standard approach for that is using a stack. Every time we see an opening bracket, we push it onto the stack. When we see a closing bracket, we check if there's a matching opening one. If the stack is empty when we encounter a closing bracket, that's invalid. Also, after processing all characters, the stack should be empty.

But wait, in this problem, the brackets are only "<" and ">", not other characters. So the logic is similar. Let me think: for each character in the string:

- If it's a '<', push it onto the stack.
- If it's a '>', check if the stack is not empty. If it's empty, return False. Otherwise, pop the top element (which should be a '<').

Wait, but since the brackets are only two types, maybe we can just track the balance. Like, for each '<', we increment a counter, and for each '>', we decrement. But we have to make sure that the counter never goes negative. Also, at the end, the counter should be zero.

Yes! That's another approach. Let's think about it. Let's say we have a variable called balance. For each character:

- If it's '<', balance += 1.
- If it's '>', balance -= 1.

But during this process, if balance ever becomes negative, that means there's a closing bracket without a matching opening one. So return False. At the end, check if balance is zero.

That's a simpler approach. Let me test this logic against the examples.

First example: "<" → balance starts at 0. Process '<', balance becomes 1. Then end of string. Balance is 1, which is not zero → return False. Correct.

Second example: "<>" → balance starts at 0. Process '<' → 1. Then '>' → 0. End. Balance is zero → return True. Correct.

Third example: "<<><>>". Let's process each character:

- '<' → 1
- '<' → 2
- '>' → 1
- '<' → 2
- '>' → 1
- '>' → 0. So balance ends at zero. Return True. Correct.

Fourth example: "><<". Let's see:

- '>' → balance becomes -1. So during processing, balance is negative. So return False. Correct.

Yes! So this approach works. So the steps are:

Initialize balance to 0.

Loop through each character in the string:

- For each '<', add 1 to balance.
- For each '>', subtract 1 from balance.
- If at any point balance is negative, return False.

After processing all characters, check if balance is zero. If yes, return True, else False.

This seems straightforward. So implementing this in Python.

So the code would be:

def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '<':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

Wait, that's all? Let me test the sample cases.

Sample 1: correct_bracketing("<") → balance is 1, after loop, check if balance is zero → 1 != 0 → return False. Correct.

Sample 2: "<>" → balance goes 1, then 0. After loop, balance is 0 → return True. Correct.

Sample 3: "<<><>>" → balance steps: 1, 2, 1, 2, 1, 0. All steps are non-negative. At end, 0 → True. Correct.

Sample 4: "><<" → first character is '>', balance becomes -1 → return False. Correct.

Yes. So this code should work.

But wait, what about cases where the balance is zero but there are unmatched brackets? Like "<<<>>>" → balance would be 3, then 2, 1, 0. So returns True. Which is correct.

Another test case: "><" → first char '>', balance -1 → return False.

Another case: "<<<>>>" → returns True. Correct.

So this approach works. So the code is as above.

So the code needs to be written with that logic. Also, the function is supposed to return a boolean. So the code is straightforward.

Now, the code needs to be written in Python. The function is called correct_bracketing, takes a string, returns a boolean.

So the code would be:

def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for c in brackets:
        if c == '<':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

Yes. That's the code. Let me check the sample inputs again.

Yes, the sample inputs are covered. So this should be the correct solution.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for c in brackets:
        if c == '<':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("<") == False
PASS    assert correct_bracketing("<>") == True
PASS    assert correct_bracketing("<<><>>") == True
PASS    assert correct_bracketing("><<>") == False
4 of 4 visible tests passed
```
