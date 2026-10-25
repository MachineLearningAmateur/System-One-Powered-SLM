# Mbpp/781, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/781/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1581. Answer tokens: 30.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called count_divisors that checks whether the count of divisors of a number is even. Wait, wait. Wait, the problem says to check whether the count of divisors is even. So the function should return True if the number of divisors is even, else False. But wait, the sample assertion is count_divisors(10), but what's the expected output? Let me think.

First, let's think about how to find the number of divisors of a number. For example, 10 has divisors 1, 2, 5, 10. So four divisors. Which is even. So the function should return True for 10. So the sample assertion is probably expecting True. But how to compute the number of divisors.

But how do I compute the number of divisors efficiently? Well, the standard approach is to factorize the number into primes, then use the formula where if the prime factorization is p^a * q^b * r^c..., then the number of divisors is (a+1)*(b+1)*(c+1)... etc. So for example, 10 is 2^1 * 5^1, so (1+1)*(1+1) = 4, which is even.

So the problem reduces to checking whether the product of (exponent + 1) for all primes in the factorization is even. But how to compute that.

Alternatively, perhaps there's a simpler way. Because for the count of divisors to be even, the number must not be a perfect square. Because if a number is a perfect square, then the exponents in its prime factorization are all even. So when you add 1 to each exponent, the product would be odd. Wait, no. Wait, if the number is a perfect square, then each exponent in the prime factorization is even. So for example, 4 is 2^2. The number of divisors is 2+1 =3, which is odd. So for a perfect square, the count of divisors is odd. So the count of divisors is even if and only if the number is not a perfect square. Wait, is that correct?

Wait, let's think. Let's take a number that's not a perfect square. Let's say 10. Its divisors are 1, 2, 5, 10. So 4 divisors. Even. So the count is even. Another example: 6. Divisors are 1, 2, 3, 6. 4 divisors. Even. 9 is a perfect square. Divisors are 1, 3, 9. 3 divisors. Odd. So the count of divisors is even if and only if the number is not a perfect square. So the problem reduces to checking whether the number is not a perfect square. So the function can be written as: return not is_perfect_square(n).

Wait, but how to check if a number is a perfect square. For example, take the square root, round it to integer, and check if the square is equal to the original number. So for example, sqrt(10) is approx 3.16, so integer part is 3. 3^2 is 9, which is not 10. So not a perfect square. So for 10, the count is even. So the function would return True.

So the problem is equivalent to checking whether the number is not a perfect square. Therefore, the function can be implemented by checking whether the square of the integer square root of the number equals the number. If yes, then it's a perfect square, so the count is odd, so return False. Otherwise, return True.

So the steps are:

1. Compute the integer square root of n. For example, for n=10, it's 3.

2. Check if (integer square root)^2 == n. If yes, then it's a perfect square, so the count is odd. So return False. Else, return True.

So the function count_divisors(n) would return True if the number of divisors is even, else False.

But wait, let me test with some examples.

Test case 1: n=1. Divisors: 1. Count is 1, which is odd. So function should return False. Let's see. sqrt(1) is 1, 1^2 =1. So returns False. Correct.

Test case 2: n=4. Divisors: 1,2,4. Count is 3. So function returns False. Which is correct.

Test case 3: n=10. sqrt is 3. 3^2 is 9 !=10. So returns True. Correct.

Another test case: n=9. sqrt is 3. 3^2=9. So returns False. Correct.

Another case: n=6. sqrt is 2.44... integer sqrt is 2. 2^2=4 !=6. So returns True. Correct.

So the function can be implemented as follows.

Now, how to compute the integer square root in Python. Well, the math module has isqrt function in Python 3.8+. For example, math.isqrt(10) returns 3. So for n, we can compute s = math.isqrt(n), then check if s*s ==n.

So the code would be:

import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n

Wait, but what if n is zero? Well, the problem probably assumes n is a positive integer. The original assertion is count_divisors(10), which is positive. So perhaps the function is intended for positive integers. So the code is okay.

But let's think about n=0. But the problem says nothing about it. So maybe the function is supposed to handle n >=1.

But the problem's sample is for 10, which is positive. So the code should work.

So the function is as above.

But wait, the original problem says to write a function that checks whether the count of divisors is even. So the function should return True if the count is even, else False. Which is equivalent to checking whether the number is not a perfect square.

So the code is correct.

So the Python code would be:

import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n

But let's test with the sample. For n=10, s=3, 3*3=9 !=10. So returns True. Which is correct.

Another test case: n=4, returns False. Correct.

So the code should work.

So the code is as above. But need to make sure that the function is named correctly. The problem says to write the function count_divisors. So the code is correct.

But the problem says to write a function that returns whether the count of divisors is even. So the code is correct.

So the code is:

import math

def count_divisors(n):
    s = math.isqrt(n)
    return s * s != n

But wait, what about n=1? s is 1, 1*1=1. So returns False. Which is correct.

Yes, that's correct.

So this code should work. So the answer is to write this function.
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
