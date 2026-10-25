# HumanEval/56, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/56/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1094. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to check if a string of brackets is correctly balanced. The function is called correct_bracketing and takes a string of '<' and '>'. The goal is to return True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, I remember that for bracket balancing problems, a stack is usually useful. Like, whenever we see an opening bracket, we push it onto the stack, and when we see a closing bracket, we check if there's a matching opening one. But wait, in this case, the brackets are only '<' and '>'. So maybe it's simpler than other bracket problems where there are multiple types.

Wait, the problem says that every opening bracket must have a corresponding closing bracket. So, for example, if there's a '<', there must be a '>' later. But also, the order matters. Like, if we have '><', that's invalid because the first character is '>', which is a closing bracket but there's no opening one before it.

So the approach would be to iterate through each character in the string. Let's think of using a counter. Let's say we have a variable called balance. When we see a '<', we increment the balance by 1. When we see a '>', we decrement it by 1. But we need to make sure that the balance never goes negative. Because if it does, that means there's a closing bracket without a matching opening one.

Wait, yes. For example, if the string starts with '>', then balance would be -1, which is invalid. So during the iteration, if at any point the balance becomes negative, we return False. Also, after processing all characters, the balance should be zero. Because each opening bracket must have a closing one.

So the steps are:

1. Initialize a balance counter to 0.
2. Iterate over each character in the brackets string.
3. For each character:
   a. If it's '<', add 1 to balance.
   b. If it's '>', subtract 1 from balance.
   c. If balance becomes negative at any point, return False.
4. After processing all characters, check if balance is zero. If yes, return True; else, False.

Let me test this logic against the examples.

First example: correct_bracketing("<") → returns False. Let's see. The balance starts at 0. The first character is '<', balance becomes 1. Then, after processing all characters, balance is 1. So it's not zero → returns False. Correct.

Second example: "<>". Process first '<' → balance 1. Then '>', balance 0. After processing, balance is 0 → returns True. Correct.

Third example: "<<><>>". Let's walk through:

Characters: '<', '<', '>', '<', '>', '>'.

Balance steps:

Start 0.

After first '<': 1.

Second '<': 2.

Third '>': 1.

Fourth '<': 2.

Fifth '>': 1.

Sixth '>': 0. So balance ends at 0. So returns True. Correct.

Fourth example: "><<>". Let's see:

First character is '>', balance becomes -1 → immediately return False. So the function returns False. Which matches the example.

So this logic seems to work.

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

Wait, but what about cases where the balance is positive but not zero? Like, if the string is "<<<", then balance would be 3, so returns False. Which is correct.

Yes, that seems to handle all cases.

So the code is straightforward. Let me check the sample test cases again.

Testing the first sample:

correct_bracketing("<") → balance is 1 at end → returns False. Correct.

Second sample: "<>" → balance 0 → True. Correct.

Third sample: "<<><>>" → balance ends at 0 → True. Correct.

Fourth sample: "><<>" → first char is '>', balance becomes -1 → returns False. Correct.

So this code should work.

Now, I need to write this in Python. The function is supposed to return a boolean. The code is simple. So the code would be as above.

Wait, but the function is called correct_bracketing and takes brackets as a string. So the code is as written.

So the complete code would be:

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

But wait, the problem says that the input is a string of '<' and '>'. So we don't need to handle other characters. So the code is safe.

Yes. So this should be the correct solution.
```

</details>

**Code that ran:**

```python
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
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("<") == False
PASS    assert correct_bracketing("<>") == True
PASS    assert correct_bracketing("<<><>>") == True
PASS    assert correct_bracketing("><<>") == False
4 of 4 visible tests passed
```
