# Mbpp/135, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/135/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 627. Answer tokens: 23.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called hexagonal_num that takes an integer n and returns the nth hexagonal number. Let me think about what a hexagonal number is. 

From what I remember, hexagonal numbers are a type of figurate number. The formula for the nth hexagonal number might be something like H(n) = n(2n - 1). Wait, let me check. For example, the first few hexagonal numbers are 1, 6, 15, 28, etc. Let me test the formula. 

For n=1: 1*(2*1 -1) = 1*1 = 1. Correct. 
n=2: 2*(4-1) = 2*3=6. Yes. 
n=3: 3*(6-1)=3*5=15. Right. 
So the formula seems correct. 

The problem says that hexagonal_num(10) should return 190. Let me check with the formula. For n=10: 10*(2*10 -1) = 10*19 = 190. Yes, that matches the assertion. 

So the function is straightforward. The code would be to take n, compute n*(2n -1), and return that. 

But wait, what about the input? The function should handle integer inputs, and probably n is a positive integer. So the code can be as simple as:

def hexagonal_num(n):
    return n * (2 * n - 1)

But maybe I should make sure that n is an integer. However, the problem says that the function is supposed to find the nth hexagonal number, so the input is expected to be an integer. The assertion given uses 10, which is an integer. So the code should work.

So the complete code would be that function. But the problem says to write the function and include any imports. But since there are no imports needed here, the code is simple.

Wait, but the user wants the code in a code block. So the code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

But let me check if there are any edge cases. For n=1, returns 1. For n=0, it would return 0, but maybe the function is supposed to handle n starting from 1. However, the problem's assertion uses n=10, so perhaps the function is intended for n ≥1. But the code would work for any integer n. 

So the code is correct. Let me write the code as per the problem's instruction. The code needs to include the function and any imports. Since there are no imports, just the function. 

So the final code is as above. Let me test the sample input. For n=10, 10*19=190. Correct. So the code should work.
```

</details>

**Code that ran:**

```python
def hexagonal_num(n):
    return n * (2 * n - 1)
```

**Visible-test report:**

```text
PASS    assert hexagonal_num(10) == 190
1 of 1 visible tests passed
```
