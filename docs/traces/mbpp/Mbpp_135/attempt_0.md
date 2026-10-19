# Mbpp/135, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/135/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 462. Answer tokens: 37.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to find the nth hexagonal number. The assert statement says that hexagonal_num(10) should equal 190. Let me think about what a hexagonal number is.

Hmm, hexagonal numbers follow a specific formula. Oh right, the formula for the nth hexagonal number is something like n*(2n-1). Wait, let me check. For example, the first few hexagonal numbers are 1, 6, 15, 24, etc. Let's see:

n=1: 1*(2*1-1) = 1*1=1. Correct.
n=2: 2*(4-1)=2*3=6. Correct.
n=3: 3*(6-1)=3*5=15. Yep. So the formula is n*(2n-1).

So the function needs to compute this. Let me think about the steps.

The function will take an integer n as input and return the nth hexagonal number. So the code would be something like:

def hexagonal_num(n):
    return n * (2 * n - 1)

Wait, but what about the assert? Let's test with n=10. 10*(20-1) = 10*19=190. Which matches the assert. So that's correct.

So the code is straightforward. But wait, are there any edge cases? Like n=0? Well, the problem probably assumes n is a positive integer. But the function can handle n=0 by returning 0*(2*0-1) = 0. But the assert given is for n=10, which works.

So the code is simple. Just implement the formula. No need for any imports. The function is just returning the computed value.

So the complete code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

Then, the assert statement would check that hexagonal_num(10) is 190. So the code should be correct.

I think that's all. Let me write the code with the function and the assert.
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
