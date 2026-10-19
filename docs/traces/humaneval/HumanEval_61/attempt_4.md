# HumanEval/61, attempt 4

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`HumanEval/61/a4/r1`)

Visible tests: **pass**. Thinking tokens: 983. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if all the opening brackets in a string have corresponding closing brackets. The function is called correct_bracketing and takes a string of parentheses. The goal is to return True if every opening bracket has a closing one, otherwise False.

Let me think about the approach. So, the basic idea is to make sure that at no point does the number of closing brackets become negative. Because if at any point there are more closing brackets than opening ones, that's a problem.

Wait, right. For example, if the string is ")(()", then the first character is ')', which would make the count of closing brackets negative. So the function should return False.

So the approach would be to track the balance of the brackets. For each character in the string:

- If it's '(', increment the balance.
- If it's ')', decrement the balance.

But if at any point the balance becomes negative, return False.

At the end, if the balance is zero, then all brackets are properly closed. Otherwise, if the balance is positive, that means there are more opening brackets than closing ones, so return False.

So the steps are:

Initialize a variable, say balance, to 0.

Loop through each character in the brackets string:

   if char is '(', add 1 to balance.

   else, subtract 1 from balance.

   if balance < 0 at any point, return False.

After processing all characters, check if balance is 0. If yes, return True, else False.

Yes, that makes sense.

Now, let's test the examples.

First example: "(" → balance starts at 0. Then, when we process '(', balance becomes 1. Then, after processing, balance is 1. So return False. Which matches the first test case.

Second example: "()" → balance starts at 0. Process '(', balance 1. Then ')', balance 0. At end, balance is 0 → True.

Third example: "(()())" → Let's see:

Process '(', balance 1.

Then '(', balance 2.

Then ')', 1.

Then '(', 2.

Then ')', 1.

Then ')', 0. So balance is 0. Return True.

Fourth example: ")(()" → first character is ')', balance becomes -1. So return False immediately. Which is correct.

So the code should work.

Now, implement this in Python.

The function is called correct_bracketing, takes a string brackets.

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

Wait, but what about the case where the string is empty? Well, according to the problem statement, the input is a string of '(', ')', but the function is supposed to return True if every opening has a closing. For example, an empty string would return True, since there are no unbalanced brackets. But according to the code, balance starts at 0, and since there are no characters, the loop doesn't run. Then return balance == 0, which is True. So that's correct.

Another test case: "(()" → balance after processing first two '(', then third ')', balance is 1. So returns False. Which is correct.

So this code should handle all cases.

Now, check the examples again.

The code would return True for "(()())" as expected.

So the code seems correct.

Now, write the code with the required imports. But since it's a simple function, no imports are needed. The code is as written.

So the final code is:

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

Yes, that's the code. Let me check the examples again.

For the first example, correct_bracketing("(") → returns False. The code processes the single '(', balance becomes 1. Then returns balance == 0? No. So returns False. Correct.

Second example: "()" → balance goes to 0. Returns True.

Third example: "(()())" → balance ends at 0. Returns True.

Fourth example: ")(()" → first char is ')', balance becomes -1. Return False. Correct.

Yes, this should work.
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
