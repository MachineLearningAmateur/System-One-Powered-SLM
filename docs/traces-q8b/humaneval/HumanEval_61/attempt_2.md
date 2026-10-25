# HumanEval/61, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1069. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called correct_bracketing that checks if a string of brackets is properly balanced. Let me think about how to approach this.

So the problem says that every opening bracket must have a corresponding closing bracket. But just checking the counts isn't enough. For example, if the string starts with a closing bracket, that's invalid even if the counts are equal. Like the example given, ")(()", which returns False.

Hmm, right. So the standard way to approach this is using a stack. Each time I see an '(', I push it onto the stack. Each time I see a ')', I check if there's a matching '(' in the stack. If there is, I pop it. If not, then it's invalid.

Wait, but maybe I can do it with a counter. Let me think. Let's track the balance. For each character in the string:

- If it's '(', increment the balance.
- If it's ')', decrement the balance.

But during this process, if the balance ever becomes negative, that means there's a closing bracket without a matching opening one. So return False.

At the end, the balance should be zero. Because every opening bracket has been closed.

Wait, but that's not sufficient. For example, if the string is "(()", the balance would be 1 at the end, which would be invalid. But if the string is "())(", then during processing, the balance would go to 1, then 0, then -1. So during processing, we check if balance is negative. If it ever is, return False. At the end, check if balance is zero.

Yes. So the steps are:

Initialize a counter (balance) to 0.

Loop through each character in the brackets string:

   if the character is '(', add 1 to balance.

   else (it's ')'), subtract 1 from balance.

   if balance is negative at any point, return False.

At the end, return balance == 0.

Wait, that's correct. Because if balance ever goes negative, there's a closing bracket without a matching opening. And if after processing all characters, balance is not zero, then there are unmatched opening brackets.

So for example:

Test case 1: "(" → balance starts at 0. After processing, balance is 1. So returns False. Which matches the first example.

Test case 2: "()" → balance starts at 0, after first '(', balance is 1. Then ')', balance 0. So returns True.

Test case 3: "(()())" → let's see:

Process each character:

'(' → 1

'(' → 2

')' → 1

'(' → 2

')' → 1

')' → 0. So returns True.

Test case 4: ")(()" → first character is ')', balance becomes -1. So return False immediately.

Yes, that's correct.

So the code would be:

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

Wait, but what about if the string is empty? Well, according to the problem statement, the input is a string of brackets. So empty string would return True? Because there are zero opening brackets. But according to the problem's examples, maybe the function is supposed to handle that. Let me check the examples.

The examples given don't include empty string. But according to the problem statement, the function should return True if every opening bracket has a corresponding closing. So for empty string, there are no opening brackets, so it's valid. So the code would return True for empty string.

But according to the code, for empty string, balance is 0, so returns True. Which is correct.

So this code should handle all cases.

Let me test the examples.

First example: correct_bracketing("(") → balance is 1. So returns False. Correct.

Second example: "()" → balance is 0. Returns True.

Third example: "(()())" → balance ends at 0. Returns True.

Fourth example: ")(()" → first char is ')', balance becomes -1. So returns False. Correct.

So this code should work.

So the Python function is as above. Now, the problem says to write the code with the given function definition, including any imports. But since the code doesn't need any imports, the code is straightforward.

So the code would be:

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

Wait, but the function is supposed to return a boolean. The code does that. So that's correct.

Yes. So that's the solution.
```

</details>

**Code that ran:**

```python
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
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("(") == False
PASS    assert correct_bracketing("()") == True
PASS    assert correct_bracketing("(()())") == True
PASS    assert correct_bracketing(")(()") == False
4 of 4 visible tests passed
```
