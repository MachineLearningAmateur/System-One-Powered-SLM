# HumanEval/61, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 990. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called correct_bracketing that checks if a string of brackets is properly nested. Let me think about how to approach this.

So the problem says that every opening bracket must have a corresponding closing bracket. But just checking the counts isn't enough. For example, if the string starts with a closing bracket, like ")(()", that's invalid even though there are two of each. So the order matters.

Hmm, the classic way to solve this is using a stack. Each time I see an '(', I push it onto the stack. When I see a ')', I check if there's a matching '(' in the stack. If there is, I pop it. If not, then it's invalid.

Wait, but maybe I can do it with a counter. Like, keep track of the balance. Start with zero. For each '(', add 1. For each ')', subtract 1. If at any point the balance goes negative, that means there's a closing bracket without a matching opening one. So return False. At the end, the balance should be zero.

Yes, that's a good approach. Let me think about the examples.

First example: "(", balance starts at 0. After processing '(', balance is 1. At the end, it's 1, so return False. Which matches the sample.

Second example: "()", balance starts at 0. After '(', 1. Then ')', 0. So return True.

Third example: "(()())". Let's track balance:

Start 0.

'(' → 1

'(' → 2

')' → 1

'(' → 2

')' → 1

')' → 0. So ends at 0. True.

Fourth example: ")(()". Let's see:

First character is ')', balance becomes -1. So immediately return False. Which is correct.

So the algorithm would be:

Initialize a counter (balance) to 0.

Iterate through each character in the string:

   if the character is '(', increment balance by 1.

   else, decrement balance by 1.

   if at any point balance is negative, return False.

At the end, check if balance is zero. If yes, return True, else False.

Yes, that should work.

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

Wait, that's simple. Let me test the examples.

Test case 1: "(" → balance is 1 at end. So returns False. Correct.

Test case 2: "()" → balance is 0. Returns True.

Test case 3: "(()())" → balance ends at 0. True.

Test case 4: ")(()" → first char is ')', balance becomes -1 → return False. Correct.

What about other cases? Like "(()", balance ends at 1 → returns False. Which is correct.

Another case: "())(", balance after first two is 1, then 0, then 1. At end, balance is 1 → returns False.

Yes, that's correct.

So the code should work. Let me write it with the correct type hints. The function is supposed to return a boolean.

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

That's the code. Let me check if there are any edge cases. What if the string is empty? Then balance is 0, returns True. But according to the problem statement, the input is a string of brackets. But the sample inputs include empty? Well, the problem says that brackets is a string of "(" and ")", but maybe empty is allowed. Let's see the examples. The first sample is "(", which returns False. So for empty string, the function would return True. But according to the problem's examples, perhaps that's acceptable. But the problem says "every opening bracket has a corresponding closing bracket". So empty string has zero opening brackets, so it's correct. So the function returns True. But the problem's examples don't cover that. But according to the problem's description, it's correct.

So the code handles that.

So the code is correct. Let me write it in the required format.
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
