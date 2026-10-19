# HumanEval/61, attempt 0

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`HumanEval/61/a0/r1`)

Visible tests: **pass**. Thinking tokens: 981. Answer tokens: 72.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if all the opening brackets in a string have corresponding closing brackets. The function is called correct_bracketing and takes a string of parentheses. The goal is to return True if every opening bracket has a closing one, otherwise False.

Let me think about how to approach this. So, the basic idea is to track the balance of the brackets. Every time I see an '(', the balance increases by 1. Every time I see a ')', the balance decreases by 1. If at any point the balance goes negative, that means there's an unmatched opening bracket, so the answer is False. Also, if the balance ends up being zero, that's okay, but if it's not zero at the end, then there's an imbalance.

Wait, right. So the steps would be:

1. Initialize a counter (let's call it balance) to 0.
2. Iterate through each character in the string.
3. For each character:
   - If it's '(', increment balance by 1.
   - If it's ')', decrement balance by 1.
4. During this process, if balance ever goes below zero, return False immediately.
5. After processing all characters, check if balance is zero. If not, return False.
6. Otherwise, return True.

Yes, that makes sense. Let me test this logic with the examples given.

Testing the first example: correct_bracketing("(") → returns False. Let's see. The balance starts at 0. The first character is '(', so balance becomes 1. Then, since there's no other characters, the balance is 1. At the end, balance is not zero, so return False. Correct.

Second example: "()" → balance starts at 0. First '(', balance 1. Then ')', balance 0. At end, balance is zero. So returns True. Correct.

Third example: "(()())" → Let's walk through. Initial balance 0. First '(', 1. Second '(', 2. Third ')', 1. Fourth '(', 2. Fifth ')', 1. Sixth ')', 0. So balance ends at 0. All steps are non-negative. So returns True. Correct.

Fourth example: ")(()". Let's see. First character is ')', balance becomes -1. So immediately return False. Which is correct.

So the logic seems solid.

Now, coding this in Python. The function is called correct_bracketing, takes a string brackets. So the code would be:

def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

Wait, but what about if the string is empty? Well, according to the problem statement, the input is a string of '(' and ')', but maybe the function is supposed to handle empty strings? Well, the examples don't include that. But according to the problem, the function returns True if every opening bracket has a corresponding closing one. For an empty string, there are no brackets, so it's valid. So the code would return True. Let's see. For example, if the input is empty, the loop doesn't run, balance is 0, so returns True. Which is correct.

Another test case: "(()". The balance after first two '(', then third ')', balance is 1. So returns False. Because the balance is not zero.

So the code seems to handle all cases.

Now, the code needs to be written with the correct imports. But since there are no imports needed here, the code is just the function.

So the complete code would be:

def correct_bracketing(brackets: str) -> bool:
    balance = 0
    for char in brackets:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        if balance < 0:
            return False
    return balance == 0

Wait, but the problem says to include any imports. But in this case, there are no imports needed. So the code is as above.

Testing the examples:

For the first example, correct_bracketing("(") → returns False. The code would process the '(', balance becomes 1. Then, after the loop, balance is 1, so returns False. Correct.

Another example: ")(()" → the first character is ')', balance becomes -1. So returns False immediately. Correct.

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
        elif char == ')':
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
