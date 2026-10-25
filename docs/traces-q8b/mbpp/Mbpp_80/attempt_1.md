# Mbpp/80, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/80/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 813. Answer tokens: 33.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to find the nth tetrahedral number. Let me think about what a tetrahedral number is. From what I remember, tetrahedral numbers are a figurate number, and they represent the number of dots in a tetrahedron. The formula for the nth tetrahedral number is the sum of the first n triangular numbers. 

Wait, right. The triangular number for a number k is k*(k+1)/2. So the tetrahedral number would be the sum of triangular numbers from 1 to n. So for example, the 5th tetrahedral number is the sum of the first 5 triangular numbers. Let me check that. 

Let me compute it manually. The first triangular numbers are:

1 (1), 3 (1+2), 6 (1+2+3), 10 (1+2+3+4), 15 (sum up to 5). Then adding those up: 1 + 3 is 4, plus 6 is 10, plus 10 is 20, plus 15 is 35. Oh right, so the 5th is 35. Which matches the sample assertion. 

So the formula for the nth tetrahedral number is the sum of the first n triangular numbers. But how do I compute that efficiently?

Alternatively, there's a direct formula for the tetrahedral number. Let me recall. The formula for the nth tetrahedral number is n(n+1)(n+2)/6. Let me check that. For n=5, 5*6*7 /6 = 5*7 = 35. Yes, that works. So that's the formula. 

So the function can be written using that formula. So the function tetrahedral_number(n) would return n*(n+1)*(n+2)//6. Wait, but since we're dealing with integers, we need to make sure that the division is integer division. Since 6 divides the product n(n+1)(n+2), because among any three consecutive numbers, there's at least one multiple of 2 and one multiple of 3, so the product is divisible by 6. 

So the code can be as simple as returning that formula. Let me test with n=5: 5*6*7 = 210, divided by 6 is 35. Correct. 

So the function can be written as:

def tetrahedral_number(n):
    return n * (n + 1) * (n + 2) // 6

But wait, what about when n is zero? Well, the problem probably expects n to be a positive integer. The sample input is 5, which is positive. So the function should handle n >=1. 

But the problem says to write the function, and the assertion is for 5. So the code should be straightforward. 

So the code would be:

def tetrahedral_number(n):
    return n * (n + 1) * (n + 2) // 6

But maybe I should check for n being a non-negative integer. However, the problem's sample uses 5, which is positive. So the function should work for any integer n >=1. 

So the code is simple. Let me test with n=1: 1*2*3 /6 = 6/6=1. Correct. For n=2: 2*3*4=24/6=4. Which is the sum of 1 and 3. Yes. 

So the code should work. Therefore, the Python function is as above. 

Now, the problem says to write the function and include any imports. But since this is a simple mathematical formula, no imports are needed. So the code is as written.
```

</details>

**Code that ran:**

```python
def tetrahedral_number(n):
    return n * (n + 1) * (n + 2) // 6
```

**Visible-test report:**

```text
PASS    assert tetrahedral_number(5) == 35
1 of 1 visible tests passed
```
