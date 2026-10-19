# Mbpp/135, attempt 4

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/135/a4/r1`)

Visible tests: **pass**. Thinking tokens: 352. Answer tokens: 41.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to find the nth hexagonal number. The assert statement says that hexagonal_num(10) should equal 190. Let me think about what a hexagonal number is.

Hmm, hexagonal numbers follow a specific formula. From what I remember, the nth hexagonal number is given by the formula H(n) = n(2n - 1). Let me check that. For example, when n=1, it's 1*(2*1-1)=1. That's correct. For n=2, 2*(4-1)=6. Yeah, that's right. So the formula is correct.

So the function needs to compute n multiplied by (2n - 1). Let me structure the code. The function will take an integer n as input and return the result.

Wait, the assert statement says hexagonal_num(10) is 190. Let me verify that. 10*(2*10 -1) = 10*19 = 190. Yes, that's correct. So the formula is right.

So the code would be straightforward. The function can be written as:

def hexagonal_num(n):
    return n * (2 * n - 1)

But wait, what about the input? The function should take n as an argument. So the code is simple. No imports needed, since it's just basic arithmetic.

Testing the function with n=10 gives 190, which matches the assert. So that's the solution.

I think that's all. The code is simple and doesn't require any imports. Just the function definition.
```

</details>

**Code that ran:**

```python
def hexagonal_num(n):
    return n * (2 * n - 1)

# Test case
assert hexagonal_num(10) == 190
```

**Visible-test report:**

```text
PASS    assert hexagonal_num(10) == 190
1 of 1 visible tests passed
```
