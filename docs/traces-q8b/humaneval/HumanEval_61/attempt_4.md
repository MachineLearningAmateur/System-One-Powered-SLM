# HumanEval/61, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 742. Answer tokens: 143.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called correct_bracketing that takes a string of brackets and returns True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, the problem is similar to checking if brackets are balanced. The classic way to do this is using a stack. Every time I see an '(', I push it onto the stack. When I see a ')', I check if there's a matching '(' in the stack. If there is, I pop it. If not, then it's unbalanced.

Wait, but maybe there's a simpler way. Like, track the balance. For each character in the string, increment a counter for '(' and decrement for ')'. If at any point the counter goes negative, that means there's a closing bracket without a matching opening one. Also, at the end, the counter should be zero.

Yes, that's right. Let's think of examples. For example, the string ")(", the balance would start at -1 right away. So return False. For "(()())", the balance would go 1, 2, 1, 2, 1, 0. So ends at zero and never negative. So return True.

So the steps would be:

Initialize a counter, say balance = 0.

Loop through each character in the string:

- For each '(', add 1 to balance.
- For each ')', subtract 1 from balance.

If at any point balance is negative, return False.

After processing all characters, check if balance is zero. If yes, return True, else False.

Yes, that seems correct. Let me test this logic against the examples.

First example: "(" → balance starts at 0. After processing, balance is 1. So returns False. Correct.

Second example: "()" → balance goes 1, then 0. No negatives, ends at 0 → True. Correct.

Third example: "(()())" → balance steps: 1, 2, 1, 2, 1, 0. All steps okay. Returns True.

Fourth example: ")(()" → first character is ')', balance becomes -1 → return False. Correct.

So this logic works. So the code can be written as:

def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

Wait, but what about cases where the balance is zero but there are unmatched brackets? Like "(()". Wait, in that case, the balance would be 1. So returns False. Which is correct.

Another example: "())(" → balance steps: 1, 0, -1 → returns False.

Yes. So this code should handle all cases.

So the code is straightforward. Let me check the sample test cases.

Sample 1: correct_bracketing("(") → returns False. Correct.

Sample 2: "()" → returns True. Correct.

Sample 3: "(()())" → returns True. Correct.

Sample 4: ")(()" → returns False. Correct.

So this code should work. Now, I need to write this in Python, with the function definition and the docstring as given.

Wait, the function is supposed to return a boolean. The code above does that. So the code should be correct.

I think that's the solution. Let me code it.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    """
    brackets is a string of "(" and ")".
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
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        else:
            balance -= 1
        if balance < 0:
            return False
    return balance == 0
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("(") == False
PASS    assert correct_bracketing("()") == True
PASS    assert correct_bracketing("(()())") == True
PASS    assert correct_bracketing(")(()") == False
4 of 4 visible tests passed
```
