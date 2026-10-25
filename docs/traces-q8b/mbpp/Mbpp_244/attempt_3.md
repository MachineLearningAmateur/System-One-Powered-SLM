# Mbpp/244, attempt 3

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/244/a3/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 36.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called next_Perfect_Square that takes a number and returns the next perfect square greater than it. Let's see. The example given is next_Perfect_Square(35) should return 36. Because 6 squared is 36, which is the next after 35.

Hmm, so first, I need to find the smallest integer n such that n² is greater than the input number. Then return n squared.

Wait, but how to find that n? Let's think. For example, if the input is 35, the square root of 35 is about 5.916. So the next integer is 6, and 6 squared is 36. So the approach is to take the square root of the input, take the ceiling of that, then square it. But wait, maybe there's a case where the input is already a perfect square. Like if the input is 36, then the next perfect square would be 49? Wait, no. Wait, the problem says "greater than a given number". So if the input is 36, the next perfect square is 49? Or is it 36? Wait, no. Because 36 is the given number. So the next one has to be larger. So for input 36, the answer is 49. But if the input is 35, the answer is 36. So the function needs to find the next square after the input, even if the input is a square.

So the approach would be: take the square root of the input, take the ceiling of that, then square it. But wait, let's test that. For example, input 35: sqrt(35) is ~5.916, ceiling is 6, square is 36. Correct. For input 36: sqrt(36) is 6.0, ceiling is 6, square is 36. But that's equal to the input. So that's not correct. So in that case, we need to take the ceiling of the square root, but if the square root is an integer, then we need to add 1. Wait, no. Because if the input is 36, then the next perfect square is 49. So how to handle that?

So the problem is that if the input is a perfect square, then the next square is (sqrt(n)+1)^2. So for example, input 36: sqrt is 6, so next is 7^2=49. So the approach is to compute the square root, take the ceiling of that, then square it. Wait, but if the input is a perfect square, then the square root is an integer. So taking the ceiling would be the same as the integer. So then we need to add 1. Wait, perhaps the correct approach is to take the square root, take the ceiling, but if the original number is a perfect square, then the ceiling is the same as the square root, so we need to add 1. Wait, maybe not. Let's think again.

Let me think of the steps. For any given number x, find the smallest integer n such that n² > x. Then return n².

So for x = 35, n is 6. For x=36, n is 7. For x=37, n is 7. So how to find n?

So n is the floor of sqrt(x) + 1? Wait, let's see. For x=35, sqrt(x) is ~5.916. The floor is 5. So floor(sqrt(x)) +1 is 6. Then square is 36. For x=36, sqrt(x) is 6.0. floor is 6. So floor(sqrt(x)) +1 is 7. Square is 49. That works. For x=37, floor(sqrt(x)) is 6, so +1 is 7. Square is 49. Which is correct. So that seems to work.

So the formula is: compute the integer part of the square root of x, then add 1, then square it.

Wait, but how to compute the integer part? For example, in Python, math.sqrt returns a float. So for x=35, math.sqrt(35) is ~5.916. The integer part is 5. So adding 1 gives 6. So the formula is to take the integer part of sqrt(x), add 1, then square.

But how to compute the integer part? Well, in Python, we can use math.isqrt for integers. Wait, but for example, math.isqrt(35) returns 5. Because it returns the floor of the square root. So for x=35, math.isqrt(35) is 5. So then adding 1 gives 6. So then square is 36. For x=36, math.isqrt(36) is 6, adding 1 gives 7, square is 49. So that's correct.

So the steps would be:

1. Compute the integer square root of x (floor of sqrt(x)).

2. Add 1 to it.

3. Square the result.

So the function can be written as:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return (n + 1) ** 2

Wait, but in that case, even if x is a perfect square, the code would return (n+1)^2. So for x=36, n is 6, so (6+1)^2 is 49. Which is correct. So the code can be simplified. Because regardless of whether x is a perfect square or not, the code would be:

n = math.isqrt(x)
return (n + 1) ** 2

Wait, let me test that. For x=35, n=5, (5+1)^2=36. Correct. For x=36, n=6, (6+1)^2=49. Correct. For x=37, n=6, same as 36. So (6+1)^2=49. Which is correct. For x=48, n=6 (sqrt(48) is 6.928..., isqrt returns 6). So (6+1)^2=49. Which is correct. For x=49, n=7, (7+1)^2=64. Which is correct. So this code would work for all cases.

Wait, but what if x is 0? Let's see. For x=0, the next perfect square is 1. Which is correct. Because 0 is a perfect square (0^2), but the next is 1^2. So the code would return (0 +1)^2=1. Correct.

So the code can be written as:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

Wait, but why is that? Because math.isqrt returns the floor of the square root. So for any x, the next perfect square is (floor(sqrt(x)) + 1)^2. Which is correct. So that's the solution.

So the code is simple. Let me test the example given. For x=35, math.isqrt(35) is 5. 5+1=6, 6^2=36. Correct. So the code works.

But wait, what if x is a negative number? The problem says "given number", but the function is supposed to find the next perfect square greater than it. But for negative numbers, the next perfect square would be 0, but maybe the function is supposed to handle that. But the problem's example uses 35, which is positive. But the problem statement doesn't specify. However, since the function is supposed to return a perfect square greater than the given number, for example, if x is -5, then the next perfect square is 0 (since 0 is greater than -5). But 0 is a perfect square. However, maybe the function is intended for positive numbers. But the problem says "given number" so perhaps it's possible that the input is negative. Let me think.

But according to the problem's example, it's possible that the input is a positive integer. But the function should handle all numbers. Let me think about x = -5. The next perfect square greater than -5 is 0. But according to the code, math.isqrt(-5) would raise an error. Wait, because math.isqrt is for non-negative integers. So in Python, math.isqrt is available in Python 3.8 and above, and it takes an integer argument >=0. So if x is negative, math.isqrt(x) would throw a ValueError. So the code as written would not handle negative numbers. However, the problem's example is for a positive number. But perhaps the function is intended to work for positive numbers. However, the problem says "given number" so perhaps we need to handle all numbers. But maybe the function is supposed to take a non-negative integer. But the problem's example is for 35, which is positive.

But perhaps the problem expects that the input is a non-negative integer. So the code is correct for that case. But perhaps we need to handle other cases. But since the problem's example is for 35, and the code works for that, maybe that's acceptable.

But the problem says "given number", but the function is supposed to return the next perfect square greater than it. So for example, if the input is 0, the next perfect square is 1. Which the code would return. For input 1, the next is 4. Which is correct. So the code works for that.

So the code seems to handle all non-negative integers. So the code is correct.

So the code is:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

Wait, but what if x is not an integer? For example, if x is 35.5. Then math.isqrt(35.5) would raise an error. Because math.isqrt is for integers. So the function is supposed to take a number, which could be a float. But the problem's example uses an integer. So perhaps the function is intended to work with integers. But the problem says "given number", which could be a float. However, the problem's example uses an integer. But the code may need to handle that.

Wait, but in the problem's example, the input is 35, which is an integer. So perhaps the function is supposed to take an integer. But the problem says "given number", which could be a float. For example, if the input is 35.5, the next perfect square is 36. So the code would take math.isqrt(35.5) which would raise an error. So perhaps the function is supposed to take an integer. But the problem's sample input is 35, which is an integer.

But the problem says "given number", which could be a float. So perhaps the code should handle that. But how? For example, if x is 35.5, then the square root is 5.95... so the integer part is 5. Then (5+1)^2=36. Which is correct. So the code would work if x is a float, as long as it's non-negative. But math.isqrt in Python requires that the argument is an integer. So if x is a float, like 35.5, then math.isqrt(x) would raise a TypeError. Because math.isqrt is for integers. So the code as written would not handle floats. So perhaps the function is supposed to take an integer. So the problem's sample input is an integer. But the problem says "given number", which may be a float. So maybe we need to adjust the code.

Wait, but the problem says "given number" but the sample input is an integer. So perhaps the function is intended to take an integer. So perhaps the code is correct as written. But perhaps the function should handle floats. But how?

Alternatively, perhaps the function is intended to take an integer. So the code is correct. But perhaps the code should take the input as an integer. But the problem's sample input is 35, which is an integer. So perhaps the code is correct.

But if the function is supposed to take a float, then perhaps we need to convert it to an integer. But that's not clear. However, given the sample input, and the problem's description, perhaps the code is correct as written. So the code would work for integers. So the code is correct.

So the code is as follows. Let me check for x=35, returns 36. Correct. For x=36, returns 49. Correct. For x=0, returns 1. Correct. For x=1, returns 4. Correct. For x=2, returns 4. Correct. For x=4, returns 9. Correct. So the code works.

So the code is:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

But wait, what about when x is 0.0? Then math.isqrt(0.0) would raise an error. Because math.isqrt requires an integer. Oh, right. Because math.isqrt is for integers. So if x is a float, like 0.0, then math.isqrt(x) would throw a TypeError. So the code would fail for non-integer inputs. So perhaps the function is supposed to take an integer. But the problem's sample input is an integer. So perhaps the code is correct.

But the problem says "given number", which may be a float. So perhaps the function should handle that. For example, if x is 35.5, then the code would need to compute the next perfect square. But how to handle that. So perhaps the code should take the floor of the square root. But for that, perhaps we need to convert x to an integer. Or perhaps the function is intended to take an integer. So the problem's sample input is 35, which is an integer. So perhaps the function is intended to take an integer, and the code is correct.

But the problem says "given number" which may be a float. So perhaps the code should handle that. For example, if x is 35.5, then the next perfect square is 36. So the code would need to compute the integer part of sqrt(x), but how?

In that case, perhaps we need to use math.sqrt(x), then take the ceiling of that. But that would be different from the previous approach. Let me think.

If x is 35.5, then sqrt(x) is approx 5.958. So the ceiling is 6, and 6^2 is 36. Which is correct. So for x=35.5, the code would need to compute the ceiling of sqrt(x). But how to do that.

But in that case, the code would be:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    return n * n

But then, for x=35, sqrt_x is 5.916..., ceil is 6, so 36. Correct. For x=36, sqrt_x is 6.0, ceil is 6.0, so 36. But that's not greater than x. So the function would return 36, which is not greater than x. So in that case, the code would be wrong. So for x=36, the function should return 49. So the code would need to check if the square is greater than x. But how?

So for example, if x is a perfect square, then the code would return x, which is not greater than x. So the code would need to return (n+1)^2. So how to handle that.

So the problem is that when x is a perfect square, the code using math.ceil(sqrt(x)) would return n = sqrt(x), so n^2 is x. Which is not greater than x. So in that case, the code would need to return (n+1)^2.

So for example, for x=36, the code using math.ceil(sqrt(x)) would return 6. So 6^2 is 36, which is not greater than x. So the code needs to return (6+1)^2 = 49.

But how to detect that. So perhaps the code should be:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But then, for x=35.5, the code would return 6^2 =36. Which is correct. For x=36, it returns 49. For x=36.0, same. For x=37, sqrt_x is 6.08..., ceil is 7. 7^2 is 49. Which is correct. So this code would handle both integers and floats.

But then, what about x=0.0? Then sqrt_x is 0.0, ceil is 0.0, so 0^2 is 0. Which is not greater than x. So the code returns (0+1)^2=1. Which is correct. For x=0.5, sqrt_x is ~0.707, ceil is 1, 1^2 is 1>0.5. Correct.

So this code would handle all cases. But then, what about x being a negative number? Well, math.sqrt would throw an error. So the function should handle only non-negative numbers. So the problem's function may assume that x is non-negative.

So the problem's sample input is 35, which is positive. So the code would work.

But how to handle x being a float. So the code is more general than the previous one. But the problem's sample input is 35, which is an integer. So which approach is correct?

The original approach using math.isqrt is better for integers. But if the function is supposed to handle floats, then the code using math.sqrt and math.ceil is better.

But the problem says "given number" which could be a float. So perhaps the code should handle that. But how to decide which approach to take.

But the problem's sample input is 35, which is an integer. But the code using math.sqrt and math.ceil would also work for integers. Let's see. For x=35, math.sqrt(35) is ~5.916, ceil is 6, 6^2 is 36. Correct. For x=36, math.sqrt(36) is 6.0, ceil is 6.0. So 6^2 is 36. Which is not greater than x. So the code would check if n^2 ==x. In that case, return (n+1)^2. So for x=36, returns 49. Which is correct. So the code would work for integers and floats.

So the code would be:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But wait, what about x=35.0? The code would compute sqrt_x as 5.916..., ceil is 6.0. 6.0^2 is 36.0, which is greater than x. So returns 36.0. Which is correct.

But what if x is 36.0? Then n is 6.0. n^2 is 36.0 ==x. So returns 49.0. Which is correct.

But what about x=36.1? sqrt_x is 6.008..., ceil is 7.0. 7^2 is 49.0, which is greater than x. So returns 49.0. Which is correct.

So this code seems to handle all cases. But how about when x is not a perfect square. For example, x=35.5, the code returns 36.0. Which is correct.

But what if x is 35.0, which is not a perfect square. Then the code returns 36.0. Correct.

So this code seems to handle all cases. But then, what about when x is 0.0? The code returns 1.0. Correct.

So this code would work for all non-negative numbers, whether they are integers or floats.

But the problem's sample input is 35, which is an integer. So the code would work.

But the original approach using math.isqrt would work for integers. But for floats, it would not. So which approach is better?

The problem says that the function should return the next perfect square greater than the given number. So the code using math.sqrt and math.ceil is more general.

But then, what about the case where x is exactly a perfect square. Like x=36.0. The code would return 49.0. Which is correct.

But how to handle the case where x is a perfect square. So the code would check if n*n == x. If yes, then return (n+1)^2. Otherwise, return n^2.

So the code is correct.

But how to implement this in Python. Let's test with the sample input.

Sample input: 35. The code would compute sqrt(35) ≈5.916, ceil is 6. 6*6=36, which is greater than 35. So returns 36. Correct.

Another test case: x=36. sqrt(36)=6.0, ceil is 6.0. 6.0*6.0=36.0 ==x. So returns (6+1)^2=49. Correct.

Another test case: x=37. sqrt is ~6.08, ceil is 7. 7^2=49>37. So returns 49. Correct.

Another test case: x=49. sqrt is 7.0, ceil is 7.0. 7^2 ==x. So returns 8^2=64. Correct.

Another test case: x=48. sqrt is ~6.928, ceil is 7. 7^2=49>48. So returns 49. Correct.

Another test case: x=0.0. sqrt is 0.0. ceil is 0.0. 0^2 ==x. So returns 1. Correct.

Another test case: x=0.5. sqrt is ~0.707. ceil is 1. 1^2=1>0.5. So returns 1. Correct.

So the code seems to handle all cases.

But what about when x is a float that is a perfect square. For example, x=4.0. Then, the code returns 9.0. Which is correct.

So the code is correct for all non-negative numbers.

So the code would be:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But wait, what if x is a float that is a perfect square, but with decimal points? Like x=4.0, which is 4.0. The code would return 9.0. Correct. But what if x=4.0, but the code's n is 2.0. n*n is 4.0, which equals x. So returns (2+1)^2 =9.0. Correct.

So this code is correct.

But what about x=36.0, which is a perfect square. The code returns 49.0. Correct.

But what about x=36.0? The code would return 49.0. So the function returns a float. But the sample input expects an integer. However, the problem's example is for an integer input, but the function could return a float. However, in Python, 36.0 is equal to 36. So perhaps the function should return an integer. But the problem's sample shows that it returns 36, which is an integer. So perhaps the function should return an integer.

But for x=35, which is an integer, the code returns 36.0. Which is a float. But the sample expects 36. So perhaps the function should return an integer. So how to handle that.

But the problem's sample uses assert next_Perfect_Square(35) == 36. So the function returns 36, which is an integer. But the code as written would return 36.0. So the assert would fail. So the code needs to return an integer.

So how to handle that. Well, the code can return an integer by converting the result to an integer. Or perhaps the function is supposed to return an integer. So in the code, for example, when x is an integer, the code returns an integer. But when x is a float, it returns a float. But in the problem's sample, it's expected to return an integer.

So perhaps the function should be written to return an integer. So the code can cast the result to an integer. But how?

Wait, in the code, for x=35, the code returns n*n, which is 6*6=36.0. So it's a float. So the assert would fail. So the code needs to return an integer.

But why is that? Because the problem's sample uses 35 and expects 36. So the function should return an integer.

So how to adjust the code. Well, perhaps the function is intended to take an integer input. So the code can be adjusted to return an integer. But how?

Well, the code can cast the result to an integer. So for example, return int(n * n). But for x=35, that would be 36.0 → 36. For x=36, returns 49.0 →49. So the code would return an integer. But what about when x is a float, like 35.5, then the code returns 36.0 → 36, which is an integer. But the function is supposed to return the next perfect square greater than the input, which is 36. So it's correct.

So modifying the code:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But then, for x=35, the return is 36.0. So to make it an integer, we can cast it to int. But in Python, 36.0 is equal to 36. So the assert would pass if the function returns 36.0. Because in Python, 36.0 ==36 is True. So the assert would pass.

But the problem's sample uses assert next_Perfect_Square(35) == 36. So if the function returns 36.0, then the assert would pass. Because in Python, 36.0 ==36 is True.

But perhaps the problem expects an integer. So perhaps the code should return an integer. So the code can return int(n * n). But in that case, for x=35, it returns 36. For x=36, returns 49. For x=35.5, returns 36. So the code is correct.

But in Python, math.ceil returns an integer? Or a float? Let's see. For example, math.ceil(5.916) returns 6.0 as a float. So n is a float. Then n * n is 36.0. So the code returns 36.0. So the assert would pass.

But the problem's sample uses 36 as the expected value. So in Python, the assert would pass because 36.0 ==36 is True.

So the code as written is correct.

But perhaps the function should return an integer. So to ensure that, we can cast the result to int. So for example:

return int(n * n)

But for x=35.5, it would return 36, which is correct. For x=36.0, returns 49. So the code would work.

So the code can be modified to return int(n * n) in the else clause, and (n+1)^2 in the if clause.

But in the case where x is a perfect square, the code returns (n+1)^2, which is an integer. So for example, x=36.0, returns 49.0 → int(49.0) is 49.

So the code can be written as:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But the return values are floats. So for x=35, it returns 36.0, which is equal to 36. So the assert would pass.

But perhaps the problem expects an integer. So to make sure, perhaps the code should cast to int. But that's not necessary, because the assert would pass as is.

But the problem's sample uses assert next_Perfect_Square(35) == 36. So if the function returns 36.0, then the assert would pass. Because in Python, 36.0 ==36 is True.

So the code is correct.

But what about if x is a float that is not a perfect square. For example, x=35.5, the code returns 36.0, which is correct. So the function returns a float, but the assert would pass.

But the problem's sample uses an integer input and expects an integer output. So the code is correct.

So the code is as follows:

import math

def next_Perfect_Square(x):
    sqrt_x = math.sqrt(x)
    n = math.ceil(sqrt_x)
    if n * n == x:
        return (n + 1) ** 2
    else:
        return n * n

But what about when x is a very large number? For example, x=10^18. The code should handle that. But math.sqrt can handle that, as long as the float is precise enough. But for very large numbers, there may be precision issues. For example, if x is a very large perfect square, like (10^9)^2 = 1e18. But math.sqrt(1e18) would return 1e9.0, so ceil is 1e9.0. n*n ==x is True, so returns (1e9 +1)^2. Which is correct.

But for numbers that are very large and not perfect squares, math.sqrt may have precision issues. For example, if x is a very large number that is very close to a perfect square, but not exactly. But this is a general problem with floating point precision. However, for the purposes of this problem, it's assumed that the function is correct for the given inputs.

So the code is correct.

But comparing n*n ==x may have issues with floating point precision. For example, if x is a very large number that is a perfect square, but due to floating point precision, math.sqrt(x) returns a value slightly less than the actual square root. So math.ceil would give n as the actual square root, but due to precision, the comparison may fail.

But in Python, math.sqrt is precise for integers up to certain limits. But for very large integers, it may not be precise. For example, for x= (2^53)^2, which is a very large number, math.sqrt(x) would return exactly 2^53. But for numbers larger than that, the floating point representation may not be precise enough.

But given that the problem's sample input is small, and the code passes the sample, perhaps it's acceptable.

But the original approach using math.isqrt is better for integers. Because math.isqrt returns the exact integer square root for integers. So for example, math.isqrt(35) is 5, and math.isqrt(36) is 6. So the code can be written as:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

But this code assumes that x is a non-negative integer. Because math.isqrt requires that x is an integer >=0.

So for x=35, returns 36. For x=36, returns 49. For x=0, returns 1. Correct.

But what about if x is a float? For example, x=35.0, which is an integer. But math.isqrt(35.0) would raise an error. Because math.isqrt takes an integer. So the code would fail.

But the problem's sample input is 35, which is an integer. So the code is correct for that case.

So which approach is better? The first approach (using math.sqrt and math.ceil) is more general but may have precision issues for very large numbers. The second approach (using math.isqrt) is more precise for integers, but only works for integers.

But the problem's sample input is an integer. So perhaps the code using math.isqrt is better.

But the problem says "given number", which could be a float. So the code needs to handle that. So the first approach is better.

But the problem may expect the code to handle integers only. So perhaps the code using math.isqrt is better.

But how to handle the case where x is a perfect square. For example, x=36. The code using math.isqrt returns 6, so (6+1)^2 is 49. Correct.

So the code is correct for integers.

So the code using math.isqrt is better for integers, and handles all cases correctly.

But the problem's sample input is 35, which is an integer. So the code using math.isqrt would work.

So the code is:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

But what about if x is a float, like 35.5? Then math.isqrt(x) would raise a TypeError. So the code would fail. But the problem's sample input is an integer. So perhaps the function is intended to take an integer. So the code is correct.

But the problem's description says "given number", which may be a float. So perhaps the code should handle that. But the code using math.isqrt would not. So the code using math.sqrt and math.ceil is better.

But in the sample input, the code using math.isqrt would work.

So the problem is to choose between the two approaches. Which one is correct?

Let me think about the problem statement again. It says "given number" but the sample input is an integer. The function is expected to return the next perfect square greater than the given number. So the code must work for any non-negative number. So the first approach using math.sqrt and math.ceil is better.

But what about when x is an integer, like 35? The code using math.sqrt would work. But math.sqrt(35) returns a float, and math.ceil returns a float. So the code returns a float. But the sample expects an integer. But in Python, the assert would pass.

So the code using math.sqrt and math.ceil is correct.

But the code using math.isqrt is correct for integers.

But the problem may expect the code to handle integers only. So the code using math.isqrt is correct.

But how to decide?

The problem says "Write a python function to find the next perfect square greater than a given number." The sample input is 35, which is an integer. So the function is likely intended to take an integer. So the code using math.isqrt is correct.

But what about when the input is 36, which is a perfect square? The code returns 49, which is correct.

So the code using math.isqrt is correct.

But why does the code return (n +1)^2? Because n is the integer square root of x. For example, x=35: n=5, so (5+1)^2=36. For x=36: n=6, (6+1)^2=49. Correct.

So the code is correct.

So the code is:

import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2

But this code would raise an error if x is a float. But the problem's sample input is an integer.

So the code is correct for the given problem.

So the correct
```

</details>

**Code that ran:**

```python
import math

def next_Perfect_Square(x):
    n = math.isqrt(x)
    return (n + 1) ** 2
```

**Visible-test report:**

```text
PASS    assert next_Perfect_Square(35) == 36
1 of 1 visible tests passed
```
