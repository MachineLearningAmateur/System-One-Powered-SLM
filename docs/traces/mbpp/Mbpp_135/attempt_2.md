# Mbpp/135, attempt 2

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/135/a2/r1`)

Visible tests: **pass**. Thinking tokens: 556. Answer tokens: 37.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to find the nth hexagonal number. The assert statement says that hexagonal_num(10) should equal 190. Let me think about what a hexagonal number is.

Hmm, hexagonal numbers follow a specific formula. Oh right, the nth hexagonal number is given by the formula H(n) = n(2n - 1). Let me check that. For example, when n=1, it's 1*(2*1-1) = 1*1=1. For n=2, 2*(4-1)=6. Then n=3: 3*(6-1)=15. Wait, but the example given is 10. Wait, wait, the assert is for n=10, which would be 10*(20-1) = 10*19=190. Oh right, that's correct. So the formula is correct.

So the function needs to compute n*(2n-1). So the code would be straightforward.

Wait, but how to handle the function? Let's define a function called hexagonal_num that takes an integer n as input and returns the nth hexagonal number.

So the code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

Then, the assert statement would check that hexagonal_num(10) is 190. Let me test that. 10*(20-1) is 10*19=190. Yes.

But wait, what about the input? The function should take an integer, and the assert is for 10. So the code should be correct.

So the complete code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But wait, do I need to import anything? The problem says to include any imports it needs. But the function is simple, no imports are needed. So the code is just the function and the assert.

So the final code is:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But maybe the problem expects the function to be part of a module, but the user just wants the code. So the code is as above.

I think that's all. Let me check if there's any edge cases. For example, n=1, returns 1. n=2 returns 6. Which is correct. So the formula is correct.
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
