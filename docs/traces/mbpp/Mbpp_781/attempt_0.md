# Mbpp/781, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/781/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1369. Answer tokens: 30.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called count_divisors that checks if the count of divisors is even. The example given is assert count_divisors(10), which I should verify.

First, I need to figure out how to find the number of divisors of a number. Let's think. For a number n, the number of divisors is determined by its prime factorization. For example, if n = p1^a1 * p2^a2 * ... * pk^ak, then the number of divisors is (a1+1)*(a2+1)*...*(ak+1). 

But how do I compute that? Well, the straightforward way is to check all numbers up to sqrt(n) and count how many divide n. But for the purpose of this problem, maybe the straightforward approach is acceptable.

Wait, but for the function count_divisors, the input is a number, and the function returns whether the count is even. So, for example, for 10, the divisors are 1, 2, 5, 10. That's 4 divisors, which is even. So count_divisors(10) should return True.

So the steps are: for a given number n, find all divisors, count them, then check if the count is even.

But how to find the divisors efficiently?

The straightforward way is to loop from 1 to n, check if i divides n, and count. But for large n, this could be slow. However, since the problem doesn't specify constraints, maybe this is acceptable for the given problem.

But for n up to say 1e6, this is manageable. But for the code, perhaps the efficient way is better. Let's think.

Another approach: the number of divisors is even if and only if the number is not a perfect square. Because, in the case of perfect squares, one of the divisors is sqrt(n), which is counted once. So for example, 4 has divisors 1, 2, 4. The count is 3, which is odd. So the count is even if and only if the number is not a perfect square.

Wait, that's a key insight! So the problem reduces to checking if the number is a perfect square. Because if it's a perfect square, the number of divisors is odd, else even.

So, the function can be simplified to check if the number is a perfect square. If yes, return False (since count is odd), else return True (count is even).

But how to check if a number is a perfect square?

Well, take the square root, round it to the nearest integer, then square it and see if it equals the original number.

But in Python, we can do this with math.isqrt, which returns the integer square root. For example, math.isqrt(10) is 3, and 3*3 is 9, which is less than 10. So, for a number n, if math.isqrt(n) ** 2 == n, then it's a perfect square.

So the function can be written as:

def count_divisors(n):
    if n < 1:
        return False  # but n is positive?
    root = math.isqrt(n)
    return root * root != n

Wait, but for n=1, math.isqrt(1) is 1, and 1*1 is 1, so returns False. Which is correct, because 1 has 1 divisor, which is odd. So the function returns False, which is correct.

Wait, but the function needs to return True if the count is even. So, for example, if the count is even, return True. So the function would return True if the number is not a perfect square.

So the function is:

import math

def count_divisors(n):
    root = math.isqrt(n)
    return root * root != n

But wait, let's test for n=10. The square root is 3, 3*3=9 != 10. So returns True. Which is correct.

For n=4, square root is 2, 2*2=4. So returns False. Which is correct because 4 has 3 divisors.

So this approach is correct.

So the code can be written as follows.

But wait, what about n=0? Well, the problem probably assumes n is a positive integer. But the function should handle n=0? Well, the problem says "count of divisors", but 0 has infinite divisors. But perhaps the problem expects n to be a positive integer. So the function can assume n is a positive integer.

But in the assert statement, count_divisors(10) is called. So the code should handle n=10.

So the code would be:

import math

def count_divisors(n):
    root = math.isqrt(n)
    return root * root != n

But wait, the problem says "the count of divisors is even". So for n=1, the count is 1, which is odd. So the function returns False. Which is correct.

So the code is correct.

But then, the assert statement would be:

assert count_divisors(10) == True

Which is correct.

So the code is as above.

But wait, what about n=1? The function returns False. Which is correct.

So the code is correct.

Therefore, the solution is to check if the number is a perfect square. If it is, then the count is odd, else even.

So the code is as written.

But the problem says to write a function to check whether the count of divisors is even. So the function returns True if even, False if odd.

So the code is correct.

Now, the code needs to be written with the necessary imports. The math module is needed for math.isqrt.

So the code would be:

import math

def count_divisors(n):
    root = math.isqrt(n)
    return root * root != n

But wait, what if n is 0? Well, math.isqrt(0) is 0, and 0*0 is 0, so returns False. But 0 has infinite divisors, which is not even. But the function would return False, which is correct.

But the problem may not require handling n=0. However, the code as written handles it.

So the code is correct.

Thus, the complete code is as follows.
```

</details>

**Code that ran:**

```python
import math

def count_divisors(n):
    root = math.isqrt(n)
    return root * root != n
```

**Visible-test report:**

```text
PASS    assert count_divisors(10)
1 of 1 visible tests passed
```
