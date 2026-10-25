# Mbpp/739, attempt 1

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/739/a1/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 648.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_Index that takes an integer n and returns the index of the smallest triangular number with exactly n digits. The example given is find_Index(2) should return 4. Let me think about how to approach this.

First, what's a triangular number? Oh right, triangular numbers are numbers of the form T_k = k*(k+1)/2. So for each k, we calculate T_k and check how many digits it has. The task is to find the smallest k such that T_k has exactly n digits.

So for example, when n is 2, the smallest triangular number with two digits is 10. Let's check: T_4 is 4*5/2 = 10. So the index is 4, which matches the example.

So the problem is to find the minimal k where T_k has exactly n digits. How to compute this efficiently?

Let me think about how to find T_k's number of digits. The number of digits of a number x in base 10 is given by floor(log10(x)) + 1. So for T_k, we can compute log10(T_k) and check if it's between n-1 and n. But since we need the minimal k, maybe we can find the smallest k such that T_k >= 10^{n-1} and T_k < 10^n.

But how to find this k efficiently? Because for large n, iterating k from 1 upwards until we find the right T_k could be slow. But maybe for the given problem, the constraints aren't too big. Let's see.

But let's think about the mathematical approach. Let me rearrange the equation T_k = k(k+1)/2. We want to find the smallest k where T_k has exactly n digits. So T_k must be >= 10^{n-1} and < 10^n.

So solving for k in the inequality 10^{n-1} <= k(k+1)/2 < 10^n.

But solving this for k might be tricky. Let's approximate. For large k, k^2/2 ≈ T_k, so k ≈ sqrt(2 * 10^{n-1}).

So for a given n, we can compute the lower and upper bounds for k. Let's find the minimal k where T_k has exactly n digits.

But perhaps it's easier to iterate k starting from 1, compute T_k, check the number of digits, and find the first k where the number of digits is exactly n. However, for larger n, this could be slow. For example, if n is 1000, then T_k would be very large, and iterating k from 1 upwards would take a lot of steps. But perhaps for the purposes of this problem, given that the example is small, and maybe the test cases aren't too big, this approach would work.

But let's think about the possible values. For n=2, the minimal k is 4. Let's see:

T_1 = 1 (1 digit)
T_2 = 3 (1)
T_3 = 6 (1)
T_4 = 10 (2 digits). So yes.

So for n=2, the answer is 4.

But how to compute the number of digits of T_k?

Let me think. For each k, compute T_k, then convert it to a string and check the length. But for large k, this could be computationally expensive. Alternatively, compute the logarithm.

But for the sake of code simplicity, perhaps converting to a string is easier. However, for very large numbers, converting to a string might be slower. But maybe for the problem's constraints, it's acceptable.

So the plan is:

Loop k from 1 upwards, compute T_k = k*(k+1)//2 (integer division), check if the number of digits is equal to n. Return the first such k.

But how to compute the number of digits? Let's think. For example, T_k can be calculated as k*(k+1)//2. Then, the number of digits is len(str(T_k)). But for very large numbers, this is acceptable.

But for large n, say n=100, the k would be around sqrt(2*10^{99}) which is a huge number. But even so, for Python, handling big integers is okay. However, looping from 1 upwards until we find the correct k might take a lot of steps. For example, for n=3, the minimal k is 5, since T_5=15 (two digits?), wait no. Wait, n=3 would require numbers with three digits. Let's see:

T_10 is 55 (two digits). T_14 is 105 (three digits). So for n=3, the answer is 14? Let me check.

Wait, let's compute T_14: 14*15/2 = 105. Which has three digits. So the index is 14. So if the function is called with n=3, the answer is 14.

But how to compute this efficiently?

Alternatively, perhaps we can find the lower and upper bounds for k using mathematical equations and then perform a binary search.

Let me think. For a given n, the lower bound is 10^{n-1} and upper bound is 10^n -1. So we need to find the minimal k where T_k >= 10^{n-1} and T_k < 10^n.

But solving for k in T_k >= 10^{n-1}:

k(k+1)/2 >= 10^{n-1}

Which can be approximated as k^2 >= 2*10^{n-1} => k >= sqrt(2*10^{n-1}).

Similarly, for the upper bound, T_k < 10^n => k^2 < 2*10^n => k < sqrt(2*10^n).

So the possible k's are between sqrt(2*10^{n-1}) and sqrt(2*10^n).

But since we need the minimal k, perhaps we can compute the lower bound and check from there.

So for example, for n=2, 10^{n-1} is 10. So sqrt(2*10) is sqrt(20) ≈4.47. So the minimal k is 5? Wait, but T_4 is 10, which is exactly 10. So the lower bound is 4.47, so k starts at 5. But in reality, the correct k is 4. So perhaps the approximation isn't sufficient. Hmm. So maybe the exact approach is better.

Alternatively, perhaps we can find the minimal k such that T_k has exactly n digits by using the formula for T_k and solving the inequalities.

Let me think again. For T_k to have exactly n digits, it must satisfy 10^{n-1} ≤ T_k < 10^n.

So solving for k:

10^{n-1} ≤ k(k+1)/2 < 10^n.

Let me rearrange the first inequality:

k^2 +k - 2*10^{n-1} ≥ 0.

Solving the quadratic equation k^2 +k - 2*10^{n-1} = 0. The positive root is [-1 + sqrt(1 + 8*10^{n-1})]/2.

So the minimal k that satisfies the inequality is the ceiling of this value.

Similarly, for the upper bound, solving k^2 +k - 2*10^n < 0. The positive root is [-1 + sqrt(1 + 8*10^n)]/2. So the maximal k is the floor of this value minus 1.

But since we want the minimal k such that T_k has exactly n digits, perhaps the minimal k is the ceiling of the lower bound.

But perhaps this can be used to compute the possible k's.

So for example, for n=2:

lower bound is sqrt(2*10^{n-1}) = sqrt(20) ≈4.47. So the minimal k is 5? But T_4 is 10, which is exactly 10^1. So the minimal k is 4. So why does the formula not capture this?

Because the exact solution for the lower bound is:

k ≥ [ -1 + sqrt(1 + 8*10^{n-1}) ] / 2.

For n=2, 8*10^{n-1} = 80. So sqrt(81) is 9. So [ -1 +9 ] /2 = 4. So the minimal k is 4. So that's correct.

So the exact formula is that the minimal k is the ceiling of (sqrt(8*10^{n-1} +1) -1)/2.

But perhaps the exact value is the floor or ceiling of that value. So for example, for n=2, the value is exactly 4, so the minimal k is 4.

So perhaps we can compute the lower bound and upper bound for k, and then check which k in that range gives T_k with exactly n digits.

But how to compute this?

So the approach would be:

For a given n:

Compute lower = 10^{n-1}

Compute upper = 10^n

We need to find the minimal k such that T_k is between lower and upper (inclusive of lower, exclusive of upper).

But solving for k in T_k >= lower and T_k < upper.

But how to find the minimal k?

Let me think. Let's compute the k that gives T_k = lower. Let's call this k_low. Then, the minimal k is the smallest integer k such that T_k >= lower. Because once T_k is >= lower, and since T_k increases with k, the first occurrence of T_k >= lower is the minimal k for which T_k has at least n digits. But we also need to ensure that T_k < upper, which is 10^n.

But perhaps for the minimal k, the T_k is exactly the first number with n digits. So for example, for n=2, lower is 10, and the first k where T_k >= 10 is 4. And T_4 is exactly 10, which is the lower bound. Then, we need to check if T_k is less than upper (which is 100). Since T_4 is 10, which is less than 100, then it's valid. So the minimal k is 4.

So the approach is:

Compute the minimal k where T_k >= 10^{n-1} and T_k < 10^n.

But how to find this k?

We can compute the value of k using the formula for the quadratic equation, then check the value.

Let me code this formula.

Let me compute k_low = ceil( (sqrt(8*lower + 1) -1)/2 )

But lower is 10^{n-1}.

Once we compute k_low, we can check if T_k_low is less than upper. If yes, then that's our answer. Otherwise, perhaps there's no such k. Wait, but since T_k increases with k, there must be some k where T_k is in the range.

But how?

Let me think. For example, if n=3, lower is 100. Let's compute k_low.

sqrt(8*100 +1) = sqrt(801) ≈ 28.3. So (28.3 -1)/2 ≈ 13.65. So the ceiling is 14. Then T_14 is 14*15/2 = 105, which is >=100 and <1000. So that's correct. So the minimal k is 14.

So the approach would be:

For a given n:

Compute lower = 10^{n-1}

Compute upper = 10^n

Compute k_low = ceil( (sqrt(8*lower + 1) -1)/2 )

Check if T_k_low is less than upper. If yes, then return k_low. Else, perhaps we need to check higher k?

Wait, no. Because T_k increases as k increases. So once T_k_low is >= lower, and since upper is 10^n, which is larger than lower, there must be some k where T_k is in that range. But how do we know that T_k_low is less than upper?

Wait, for example, if n=3, upper is 1000. T_14 is 105 < 1000. So yes. But what if for some n, T_k_low is >= upper? Then there is no solution. But that can't happen because T_k increases with k. So for example, when n=1, lower is 1, upper is 10. The minimal k is 1 (T_1=1). So for all n, there must be a solution.

So the idea is that the minimal k for which T_k has exactly n digits is the minimal k where T_k >= lower and T_k < upper. So the minimal k is the one found by solving T_k >= lower. Because once T_k reaches lower, it will be in the range.

But perhaps the T_k_low could be >= upper. For example, let's take n=1. Then lower is 1, upper is 10. T_1=1, which is in the range. So it's okay.

Another example: n=4. lower is 1000. upper is 10000.

Compute k_low: sqrt(8*1000 +1) = sqrt(8001) ≈ 89.45. (89.45 -1)/2 ≈ 44.22. So ceil(44.22) is 45. T_45 is 45*46/2 = 1035. Which is between 1000 and 10000. So yes. So the answer is 45.

So the formula gives us the correct k.

So the plan is:

For given n:

Calculate lower = 10^{n-1}

Calculate upper = 10^n

Compute k_low = ceil( (sqrt(8*lower + 1) -1)/2 )

Check if T_k_low is less than upper. If yes, then return k_low. But how?

Wait, but since T_k increases with k, once we find the minimal k where T_k >= lower, then T_k will be in the range [lower, upper) if and only if T_k < upper. So how to ensure that?

Well, since upper is 10^n, and lower is 10^{n-1}, the next triangular number after T_k_low may be in the range. So perhaps the minimal k is k_low.

But perhaps there are cases where T_k_low is >= upper. For example, if n is such that lower is 10^{n-1}, and the next triangular number after that is already >= upper.

But how?

Let me think for n=4. upper is 10000. T_45 is 1035, which is less than 10000. So that's okay.

Another example: Let's say n=5. lower is 10000. upper is 100000.

Compute k_low: sqrt(8*10000 +1) = sqrt(80001) ≈ 282.84. (282.84 -1)/2 ≈ 140.92. So ceil(140.92) is 141. T_141 = 141*142/2 = 141*71 = 10011. Which is between 10000 and 100000. So yes.

So the formula works.

So the approach is:

Calculate k_low as the ceiling of the solution to the equation T_k = lower. Then check if T_k_low is less than upper. If it is, then return k_low. Otherwise, perhaps there's no solution? But that can't happen, because T_k increases with k. So for example, if T_k_low is >= upper, then the next k would be higher, but that would be even larger. Wait, but how can T_k_low be >= upper?

Let me think. For example, let's take n=1. lower is 1, upper is 10. k_low is (sqrt(8*1 +1) -1)/2 = (3-1)/2 = 1. So T_1=1, which is less than 10. So okay.

Another example, n=10. Let's say lower is 10^9. upper is 10^10. So compute k_low = ceil( (sqrt(8*1e9 +1) -1)/2 )

sqrt(8e9) is sqrt(8)*1e4.5 ≈ 2.828 * 31622.7766 ≈ 89442. So 8e9 is 8*1e9. So sqrt(8e9) is sqrt(8)*1e4.5 = sqrt(8)*1e4 * sqrt(10) ?

Wait, perhaps I should compute it numerically. Let me compute 8*1e9 = 8,000,000,000. sqrt(8,000,000,000) is approx 89442.717. So (sqrt(8*lower +1) -1)/2 is (approx 89442.717 -1)/2 ≈ 44720.858. So ceil is 44721. T_44721 is 44721*44722/2. Let me compute that.

But regardless, that T_k would be approximately (44721^2)/2. Which is (approx 2e9)/2 = 1e9. So that's exactly lower. So T_k_low is about 1e9, which is lower than upper (1e10). So yes.

So the formula gives us the correct k_low. Therefore, the minimal k is k_low.

But wait, what if T_k_low is exactly equal to upper? For example, if T_k_low equals upper. Then it's not allowed. But since upper is 10^n, and T_k is k(k+1)/2. For example, suppose for some n, T_k_low equals 10^n. Then, since the upper bound is 10^n, T_k_low is not less than upper, so we need to find the next k. But that's not possible, because T_k increases with k. So in that case, there is no solution. But that's not possible because T_k for k_low is the minimal k where T_k >= lower. So if T_k_low equals upper, then T_k_low is exactly 10^n, which is not less than upper. So then, there's no solution. But that can't happen because the next k would have T_k larger than upper. But how can T_k_low be exactly upper?

Let me think. For example, if lower is 10^{n-1} and upper is 10^n. Suppose that T_k_low equals upper. Then, the T_k_low is 10^n, which is not less than upper. So the minimal k for which T_k has exactly n digits would be the next k. But since T_k increases with k, the next k would have T_k larger than upper. So there's no k with exactly n digits. But that's impossible because for example, the number of digits of T_k is exactly n.

Wait, but how can that happen? For example, suppose that T_k is exactly 10^n. Then, it has n+1 digits. Because 10^n has n+1 digits (like 10^1 is 10, which has 2 digits). So for example, if T_k is exactly 10^n, then it has n+1 digits, which is not what we want. So in that case, the minimal k would not be in the range. So how can that happen?

But for the formula, the k_low is computed as the minimal k where T_k >= lower. If T_k_low is exactly upper, then that would mean that the T_k_low has n+1 digits. So that's not acceptable. Therefore, we need to check whether T_k_low is less than upper. If not, then we need to find the next k. But how?

Wait, but this scenario can't happen. Because for T_k_low to be equal to upper, then upper = 10^n. But T_k_low is the minimal k such that T_k >= lower = 10^{n-1}. So for example, if T_k_low is exactly 10^n, then T_k_low is 10^n, which is larger than lower. But the T_k_low would have n+1 digits, which is not what we want. Therefore, the minimal k would be the next k where T_k is in the range [lower, upper). So perhaps the formula gives us the correct k_low, but we need to check whether T_k_low is less than upper. If not, then we need to find the next k where T_k is in the range.

But how can this happen? Let's think of an example. Let's say n=1. lower is 1, upper is 10. The minimal k is 1. T_1=1 <10. So okay.

Another example: Let's say n=1, but suppose T_k_low is 10. Then, it would have 2 digits. So the minimal k would be 4 (since T_4 is 10). But in this case, the lower is 1, upper is 10. So T_k_low is 10, which is equal to upper. So in this case, the minimal k for n=1 would be 4, but T_4 is 10, which has 2 digits. So this would be invalid. But in reality, for n=1, the minimal k is 1. So how can this scenario happen?

It seems that this scenario can't happen because for T_k to be equal to upper, which is 10^n, then the number of digits is n+1, not n. So the formula for k_low would have to be such that T_k_low is in the range [lower, upper). Therefore, for the formula to give the correct k_low, we need to ensure that T_k_low is less than upper. How can we ensure that?

Let me think. For example, suppose that the minimal k where T_k >= lower is k_low. Then, T_k_low is the first triangular number that is >= lower. But since upper is 10^n, which is larger than lower, then T_k_low could be less than upper, or it could be equal to upper. But if T_k_low is equal to upper, then it's not acceptable. So how to handle this?

Well, perhaps the formula for k_low gives us the minimal k where T_k >= lower. Then, we can check if T_k_low is less than upper. If it is, then return k_low. Else, we need to find the next k where T_k is in the range. But how?

But in reality, since T_k increases with k, once T_k_low is >= lower, then T_k_low is the first triangular number with at least n digits. But since upper is 10^n, which is larger than lower, there must be some k where T_k is in the range [lower, upper). So if T_k_low is equal to upper, then there is no such k. But that's impossible, since T_k increases with k. So for example, if T_k_low is equal to upper, then the next k (k_low +1) would have T_{k_low+1} = T_k_low + (k_low +1). Which is larger than upper. So there is no k for which T_k is in the range. But this would mean that there is no triangular number with exactly n digits. But that can't be true. Because for example, for n=1, there are triangular numbers with exactly 1 digit (like 1, 3, 6, 10 is 2 digits). So for n=1, the minimal k is 1. So how can this scenario happen?

Wait, perhaps this scenario can't happen. Because upper is 10^n, and lower is 10^{n-1}. The difference between upper and lower is 9*10^{n-1}. So for example, for n=1, upper is 10, lower is 1. So the difference is 9. The triangular numbers between 1 and 10 are 1, 3, 6, 10. So T_4 is 10, which is equal to upper. But for n=1, we are looking for numbers with exactly 1 digit. So T_4 is 10, which has 2 digits, so it's not acceptable. Therefore, the minimal k for n=1 is 3 (since T_3=6, which has 1 digit). So why does the formula give k_low as 1?

Wait, let's compute for n=1. lower is 10^{0} =1. upper is 10^1=10. So the formula for k_low is:

sqrt(8*1 +1) = sqrt(9) =3. (3-1)/2 = 1. So k_low is 1. T_1 is 1, which is less than upper (10). So the answer is 1. Which is correct. Because T_1=1 has exactly 1 digit. So the formula works. So even though T_4 is 10, which is equal to upper, but the formula gives the correct k_low.

So the formula gives the correct k_low, and in that case, T_k_low is less than upper. Therefore, the formula gives the correct k.

So, the steps for the code would be:

For a given n:

Compute lower = 10 ** (n-1)

Compute upper = 10 ** n

Compute k_low = ceil( (sqrt(8*lower +1) -1)/2 )

Then compute T_k_low = k_low*(k_low+1)//2

If T_k_low < upper, then return k_low. Else, return k_low +1 ?

Wait, no. Because if T_k_low is equal to upper, then it's not acceptable. But how can that happen?

Let me think again. For example, suppose lower is 10, upper is 100. Suppose that for some n, T_k_low is exactly 100. Then, T_k_low has 3 digits (since 100 is 3 digits), which is not what we want. But in this case, the n would be 3. So lower is 100, upper is 1000. So for n=3, the lower is 100. So if T_k_low is 100, then it's exactly lower, and it's less than upper. So it's acceptable. So the answer is k_low.

But if T_k_low is equal to upper, then it's not acceptable. But how can that happen?

Let me think of an example. Let's say lower is 100, upper is 1000. Suppose that T_k_low is 1000. Then, since T_k_low is equal to upper, which is 1000. Then, the number of digits is 4 (since 1000 has 4 digits). So for n=3, this would be invalid. So how can this happen?

But according to the formula, T_k_low is the minimal k where T_k >= lower. So in this case, T_k_low is 1000, which is >= lower (100), but it's equal to upper (1000). So the number of digits is 4, which is not n=3. So this would be a problem. But how can this happen?

Let me find such an example. Let me find n where T_k_low equals upper.

Let me think: For example, suppose that T_k = upper = 10^n.

So k(k+1)/2 = 10^n.

But this equation must be satisfied for some integer k and n. Let me see if such a case exists.

For example, let me take n=4. upper is 10^4=10000. Let me see if there exists an integer k where k(k+1)/2 = 10000.

Solving k^2 +k - 20000 =0.

Discriminant is 1 + 80000 = 80001. sqrt(80001) is approx 282.84. So k = (-1 + 282.84)/2 ≈ 140.92. So k is not integer. So T_140 is 140*141/2 = 9870, T_141 is 141*142/2 = 10011. So T_141 is 10011, which is larger than 10000. So for n=4, lower is 1000, upper is 10000. The minimal k_low is computed as ceil( (sqrt(8*1000 +1) -1)/2 ). Let me compute that.

sqrt(8001) is approx 89.45. So (89.45 -1)/2 = 44.22. ceil is 45. T_45 is 1035, which is less than upper (10000). So the answer is 45. So no problem here.

Another example: Let me take n=5. upper is 10^5=100000. Let's see if T_k equals 100000. Let me solve k(k+1)/2 = 100000. So k^2 +k - 200000 =0. Discriminant is 1 + 800000 = 800001. sqrt(800001) is approx 894.427. So k is (-1 + 894.427)/2 ≈ 446.71. So k is 447. Let me compute T_447: 447*448/2 = 447 * 224 = let's compute that. 447 * 200 = 89400, 447 * 24 = 10728. Total is 89400 + 10728 = 100128. Which is larger than 100000. So T_447 is 100128. So the lower for n=5 is 10^4=10000. So the formula would compute k_low as the ceil of (sqrt(8*10000 +1) -1)/2. Which is sqrt(80001) ~ 282.84. (282.84-1)/2 ~ 140.92. So ceil is 141. T_141 is 10011, which is less than upper (100000). So the answer is 141. So no problem.

So in all these examples, the T_k_low is less than upper. So perhaps there's no case where T_k_low equals upper. Therefore, the formula is safe.

Therefore, the code can be written as:

For a given n, compute lower = 10^(n-1), upper = 10^n.

Compute k_low as the ceiling of (sqrt(8*lower + 1) -1)/2.

Return k_low.

But how to compute this in Python?

In Python, we can compute the square root with math.sqrt, but since we need to compute the ceiling of the value, we need to handle that.

But how to compute the ceiling of a float? For example, if the value is 4.0, then ceil is 4. If it's 4.1, ceil is 5.

But in Python, math.ceil returns the ceiling of a float.

But we need to compute k_low as the ceiling of the solution to the equation.

But since we're dealing with integers, perhaps we can compute the exact value using math.sqrt, and then do some rounding.

Let me think. For example, for lower = 10^{n-1}:

Compute sqrt_val = sqrt(8 * lower + 1)

Then, k = (sqrt_val - 1) / 2

If this k is an integer, then k_low is k. Else, we take the ceiling of k.

But how to compute that in Python.

For example, in code:

import math

lower = 10 ** (n-1)

sqrt_val = math.sqrt(8 * lower + 1)

k = (sqrt_val - 1) / 2

k_low = math.ceil(k)

But since math.ceil returns the smallest integer greater than or equal to the number.

But in Python, when dealing with floating points, there might be precision issues. For example, when the exact value is an integer, but due to floating point precision, it's represented as something like 4.999999999999999 instead of 5.0. So math.ceil would still return the correct value.

But perhaps to avoid this, we can use integer-based calculations.

Alternatively, perhaps we can compute k_low as the integer part of (sqrt(8*lower +1) -1)/2, and then check if T_k is >= lower. If not, add 1.

But for code purposes, let's proceed with the initial approach.

So the code steps are:

def find_Index(n):

    lower = 10 ** (n-1)

    upper = 10 ** n

    sqrt_val = math.sqrt(8 * lower + 1)

    k = (sqrt_val - 1) / 2

    k_low = math.ceil(k)

    # Now check if T_k_low is less than upper. If not, then increment?

    # Wait, but earlier analysis suggests that this is not needed.

    # But to be safe, perhaps we can compute T_k_low and see.

    # But how?

    # Compute T_k_low

    T_k_low = k_low * (k_low +1) // 2

    # Now check if T_k_low is less than upper. If yes, return k_low. Else, perhaps increment k_low?

    # But how can that happen?

    # For example, if T_k_low is equal to upper, then it's not acceptable. But how?

    # Let's think for n=2, lower=10, upper=100.

    # k_low is (sqrt(81) -1)/2 = (9-1)/2 = 4. So ceil(4) is 4. T_4=10 < 100. So correct.

    # Another example, suppose lower=100, upper=1000.

    # sqrt(8001) is approx 89.45. (89.45-1)/2 = 44.22. ceil is 45. T_45 is 1035 < 1000? No, 1035 is larger than 1000. Wait, wait, upper is 1000. So T_45 is 1035 which is larger than upper. So in this case, the code would return k_low=45, but T_45 is 1035 which is larger than upper (1000). So this would be invalid.

    Wait, but in this case, lower is 100, upper is 1000. So for n=3, the code would compute k_low as 45, but T_45 is 1035, which is larger than upper (1000). So this would be invalid. But according to our previous analysis, this shouldn't happen. What's wrong here?

Wait, this example is for n=3. Let me recheck:

lower = 10^{n-1} = 10^{2} = 100.

upper = 10^3 = 1000.

sqrt_val = sqrt(8*100 +1) = sqrt(801) ≈ 28.3. (28.3 -1)/2 = 13.65
```

</details>

**Code that ran:**

```python
import math

def find_Index(n):
    lower = 10 ** (n - 1)
    sqrt_val = math.sqrt(8 * lower + 1)
    k = (sqrt_val - 1) / 2
    k_low = math.ceil(k)
    return k_low
```

**Visible-test report:**

```text
PASS    assert find_Index(2) == 4
1 of 1 visible tests passed
```
