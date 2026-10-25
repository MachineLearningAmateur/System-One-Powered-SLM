# Mbpp/781, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/781/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1047. Answer tokens: 30.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called count_divisors that checks whether the count of divisors of a number is even. Wait, the problem says to check if the count of divisors is even. So the function should return True if the number of divisors is even, else False. 

Wait, the sample assertion is count_divisors(10). Let me think about what that would be. For 10, the divisors are 1, 2, 5, 10. So there are 4 divisors, which is even. So the function should return True for 10. 

But how do I calculate the number of divisors efficiently? Let me think. The standard way is to loop from 1 to sqrt(n) and count divisors. But for each divisor i, if i divides n, then there's another divisor n/i. However, if i is the square root, then it's counted once. So the count of divisors depends on the exponents in the prime factorization. 

Wait, the number of divisors is even if and only if the number is not a perfect square. Because when a number is a perfect square, one of its divisors is repeated (the square root), so the total count becomes odd. Otherwise, divisors come in pairs. 

Oh right! So the problem reduces to checking whether the number is not a perfect square. Because if the count of divisors is even, then the number is not a perfect square. So the function can be simplified to checking whether the number is not a perfect square. 

Wait, let me confirm. For example, 10 is not a perfect square, and has 4 divisors (even). 9 is a perfect square, divisors are 1,3,9 → 3 divisors (odd). So yes, the count is even if and only if the number is not a perfect square. 

So the problem becomes: check if the number is not a perfect square. So the function can be implemented by checking if the square of the integer square root of n equals n. 

Wait, how to check if a number is a perfect square. Let me think. Take the integer part of the square root of n, then square it. If it equals n, then it's a perfect square. 

So for example, for n=10, sqrt(10) is approx 3.16, integer part is 3. 3^2 is 9, which is not equal to 10. So it's not a perfect square. So the count is even. 

So the function can be written as: return not (is_perfect_square(n)).

So the steps are:

1. Compute the integer square root of n. Let's call it s.
2. Check if s*s == n. If yes, then it's a perfect square, so the count is odd. So return False. Else return True.

So how to compute integer square root in Python? Using math.isqrt(n) which returns the floor of the square root. For example, math.isqrt(10) is 3. 

So the code would be:

import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n

Wait, but what about n=0? Well, the problem probably assumes n is a positive integer. The original sample uses 10, which is positive. So perhaps the function is intended for positive integers. 

But the problem says nothing about the input. However, the assertion is for count_divisors(10), which is valid. So perhaps the function is supposed to handle positive integers. 

So the code would be as above. Let me test some examples.

For n=10, math.isqrt(10) is 3. 3*3=9 !=10 → return True. Which is correct.

For n=9, 3*3=9 → return False. Which is correct.

For n=1, 1*1=1 → return False. Which is correct (divisors count is 1, which is odd).

For n=2, sqrt is 1. 1*1=1 !=2 → return True. Divisors are 1 and 2 → count 2, even. Correct.

So this function should work. 

But wait, what about n=0? Well, the problem may not require handling that. Let's assume that the input is a positive integer. 

So the code would be:

import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n

But the problem says to write a function that returns whether the count is even. So this function returns True when the count is even, which is correct. 

So the code should be correct. Let me check the sample assertion. For count_divisors(10), the function returns True. Which matches the sample. 

So the code is correct.
```

</details>

**Code that ran:**

```python
import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n
```

**Visible-test report:**

```text
PASS    assert count_divisors(10)
1 of 1 visible tests passed
```
