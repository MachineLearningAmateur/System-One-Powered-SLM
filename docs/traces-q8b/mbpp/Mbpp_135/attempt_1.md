# Mbpp/135, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/135/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 839. Answer tokens: 37.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called hexagonal_num that calculates the nth hexagonal number. Let me think about what a hexagonal number is. From what I remember, hexagonal numbers are a type of figurate number. The formula for the nth hexagonal number might be something like H(n) = n(2n - 1). Wait, let me verify that. 

Let me check the example given. The 10th hexagonal number should be 190. Let's plug n=10 into the formula. 10*(2*10 -1) = 10*(20-1) = 10*19 = 190. Oh right, that matches the example. So the formula is correct.

So the function needs to take an integer n and return n*(2n -1). That's straightforward. 

Wait, but what about the input? The function is supposed to be called hexagonal_num, and it's supposed to take one argument. So the code would be something like:

def hexagonal_num(n):
    return n * (2 * n - 1)

But wait, maybe there's more to it? Like, do I need to handle any edge cases? For example, if n is zero or negative? But according to the problem statement, the function is supposed to find the nth hexagonal number. Assuming that n is a positive integer. The example given is n=10, which is positive. So perhaps the function is intended for n >=1. But the problem doesn't specify, so maybe the function should handle any integer input, but perhaps the test case expects n to be positive. 

But the problem says to write the function, and the assertion is for n=10. So the code is simple. Let me think about the code structure. 

The code needs to include the function and the assertion. Wait, the user says to write a function and include the assertion. But the problem says to write the function, and the user's code will include the assertion. Wait, the problem says that the user's code should have the function, and the assertion is part of the test case. So the code should have the function and the assertion. 

Wait, the problem says "Write a function to find the nth hexagonal number. assert hexagonal_num(10) == 190". So the code should include the function and the assertion. But in Python, the assert statement is part of the code. So the code should have the function definition and then the assert statement. 

So putting it all together, the code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But wait, what about other test cases? For example, when n=1, the hexagonal number is 1*(2*1 -1) = 1*1=1. Which is correct. For n=2, 2*(4-1)=6. Let me check the sequence. The hexagonal numbers start as 1, 6, 15, 28, etc. So yes, the formula is correct.

So the code is correct. Therefore, the complete code would be as above. 

But the user says to reply with the complete code in one code block, including any imports. But in this case, there are no imports needed. So the code is as written. 

So the final answer is the function and the assertion. Let me make sure that the code is correct. 

Yes. So the code should be:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But wait, the problem says to write the function, and the assertion is part of the code. So the code should include that. So the user's code would have that. 

Yes, that's correct. So the code is correct.
```

</details>

**Code that ran:**

```python
def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190
```

**Visible-test report:**

```text
PASS    assert hexagonal_num(10) == 190
1 of 1 visible tests passed
```
