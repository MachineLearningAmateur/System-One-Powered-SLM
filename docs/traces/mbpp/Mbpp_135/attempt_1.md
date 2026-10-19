# Mbpp/135, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/135/a1/r1`)

Visible tests: **pass**. Thinking tokens: 531. Answer tokens: 286.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to find the nth hexagonal number. The assert statement says that hexagonal_num(10) should equal 190. Let me think about what a hexagonal number is.

Hmm, hexagonal numbers are numbers that can form a hexagonal shape. The formula for the nth hexagonal number is something like 2n² - n. Wait, let me check. Oh right, the formula is H(n) = n(2n - 1). So for example, when n=1, it's 1*(2*1 -1) = 1. For n=2, 2*(4-1)=6. Then n=3: 3*(6-1)=15. Wait, but the example given is 10. Wait, wait, the assert says hexagonal_num(10) is 190. Let me compute that. Let's see: 10*(2*10 -1) = 10*19 = 190. Oh right, so the formula is correct.

So the function needs to compute n*(2n -1). So the code would be straightforward.

So the function can be written as:

def hexagonal_num(n):
    return n * (2 * n - 1)

Wait, but what about the imports? Well, there are no imports needed here. The function is simple. So the code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

Then, the assert statement would check that hexagonal_num(10) is 190. Let me test that. 10*(2*10-1) is 10*19=190. Yes.

So the complete code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But wait, the problem says to write the complete code in one code block. So I need to include the function and the assert. But in Python, the code would be:

def hexagonal_num(n):
    return n * (2 * n - 1)

assert hexagonal_num(10) == 190

But maybe the function is supposed to be part of the code. So the code would be as above. Let me check if there's any other possible way. Oh, no, that's the correct approach. So the code is correct.
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
