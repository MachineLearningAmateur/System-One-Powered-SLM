# HumanEval/61, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/61/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1067. Answer tokens: 69.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called correct_bracketing that takes a string of brackets and returns True if every opening bracket has a corresponding closing bracket. Let me think about how to approach this.

Hmm, the problem is similar to checking if brackets are balanced. The classic way to do this is using a stack. Every time I see an '(', I push it onto the stack. When I see a ')', I check if there's a matching '(' in the stack. If there is, I pop it. If not, then it's invalid.

Wait, but maybe there's a simpler way. Like, keep a counter. For each '(', increment the counter, for each ')', decrement. But if the counter ever goes negative, that's invalid. Also, at the end, the counter should be zero.

Yes, that's right. Let me think. For example, the string "(()())" would have the counter go like: 1, 2, 1, 2, 1, 0. So ends at zero and never went negative. That's valid. For ")(()", the first character is ')', so the counter would go to -1 immediately. So that's invalid.

So the steps are: iterate through each character in the string. Keep a count. For '(', add 1. For ')', subtract 1. If at any point the count is negative, return False. At the end, check if the count is zero.

Yes, that seems correct. Let me test some examples.

First example: "(", the count starts at 0. Then add 1, so count is 1. At end, count is 1, not zero. So returns False. Which matches the sample.

Second example: "()", count starts at 0. First char '(', count 1. Second ')', subtract 1, count 0. So returns True.

Third example: "(()())". Let's track:

Start 0.

'(' → 1.

'(' → 2.

')' → 1.

'(' → 2.

')' → 1.

')' → 0. So ends at zero. Return True.

Fourth example: ")(()". First char ')', count becomes -1. So return False immediately.

Yes, that works. So the algorithm is:

Initialize a counter to 0.

For each char in the string:

   if char is '(', add 1 to counter.

   else, subtract 1.

   if counter < 0 at any point, return False.

At the end, check if counter is 0.

So the code would be:

def correct_bracketing(brackets: str) -> bool:

    count = 0

    for char in brackets:

        if char == '(':

            count +=1

        else:

            count -=1

        if count < 0:

            return False

    return count == 0

Wait, but what about if the string is empty? Well, according to the problem statement, the input is a string of brackets. So empty string would return True? Because there are no brackets to mismatch. But according to the examples, maybe that's allowed. Let me check the sample inputs. The sample inputs include cases where the string is length 1, which returns False. So for empty string, the function would return True. But the problem says "every opening bracket has a corresponding closing bracket". So for empty string, there are no opening brackets, so it's correct. So the code would return True for empty string.

But the problem's examples don't cover that. However, according to the problem statement, the function should return True if every opening bracket has a corresponding closing. So for empty string, that's True.

But the code as written would handle that. Let me test.

Another test case: empty string → returns True.

Another test case: "(()" → count after processing is 1. So returns False.

Yes. So the code seems correct.

So the code is straightforward. Now, the function is supposed to return a boolean. The code seems to handle all cases.

So the Python code would be as written. Let me write that.

Wait, the function is called correct_bracketing, and the parameters are brackets: str. So the code would be:

def correct_bracketing(brackets: str) -> bool:
    count = 0
    for char in brackets:
        if char == '(':
            count += 1
        else:
            count -= 1
        if count < 0:
            return False
    return count == 0

Yes. Let me check the sample inputs.

Sample 1: correct_bracketing("(") → count is 1 at end. So returns False. Correct.

Sample 2: "()" → count is 0. Returns True.

Sample 3: "(()())" → count ends at 0. Returns True.

Sample 4: ")(()" → first char is ')', count becomes -1 → returns False. Correct.

Yes, all samples pass.

So this code should work. I think that's the correct solution.
```

</details>

**Code that ran:**

```python
def correct_bracketing(brackets: str) -> bool:
    count = 0
    for char in brackets:
        if char == '(':
            count += 1
        else:
            count -= 1
        if count < 0:
            return False
    return count == 0
```

**Visible-test report:**

```text
PASS    assert correct_bracketing("(") == False
PASS    assert correct_bracketing("()") == True
PASS    assert correct_bracketing("(()())") == True
PASS    assert correct_bracketing(")(()") == False
4 of 4 visible tests passed
```
