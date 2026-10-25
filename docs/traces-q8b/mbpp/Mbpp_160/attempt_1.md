# Mbpp/160, attempt 1

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/160/a1/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 748.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_solution that takes three integers a, b, n and returns a tuple (x, y) such that ax + by = n. If there's no solution, return None. The example given is find_solution(2,3,7) returns (2,1) because 2*2 +3*1 =7. 

First, I remember that this is related to the linear Diophantine equation. The equation ax + by = n has solutions if and only if the greatest common divisor of a and b divides n. So the first step is to check if gcd(a, b) divides n. If not, return None.

But how do I find x and y once I know that a solution exists? Well, the extended Euclidean algorithm can find x and y such that ax + by = gcd(a, b). Then, if n is a multiple of the gcd, I can scale those solutions accordingly.

So the plan is:

1. Compute the gcd of a and b. Let's call it g.
2. Check if n is divisible by g. If not, return None.
3. Otherwise, find x0 and y0 such that ax0 + by0 = g.
4. Multiply x0 and y0 by (n/g) to get the solution for ax + by = n. So x = x0*(n/g), y = y0*(n/g).

But wait, how do I compute the extended Euclidean algorithm in Python? I need to implement that or find a way to get x and y.

Let me think about the extended Euclidean algorithm. The algorithm finds gcd(a, b) and coefficients x and y such that ax + by = gcd(a, b). So I need to implement that.

Let me think about the steps for the extended Euclidean algorithm. Let me write a helper function to compute the extended GCD.

For example, the function could return (g, x, y) where g is the gcd, and x and y are coefficients.

Let me recall the steps. The algorithm works recursively. For example:

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

Wait, yes. Let me test this with a=2, b=3. Let's see:

extended_gcd(2,3) would call extended_gcd(3, 2%3=2). Then extended_gcd(3,2) calls extended_gcd(2, 3%2=1). Then extended_gcd(2,1) calls extended_gcd(1, 2%1=0). Then returns (1, 1, 0). Then backtracking:

For (2,1), the x is y1 (0), y is x1 - (2//1)*y1 = 1 - 2*0 = 1. So returns (1, 0, 1). Then for (3,2), x is y1 (1), y is x1 - (3//2)*y1 = 0 - 1*1 = -1. So returns (1, 1, -1). Then for (2,3), x is y1 (-1), y is x1 - (2//3)*y1. Wait, a is 2, b is 3. So in the call to extended_gcd(3, 2), which returns (g, x1, y1) = (1, 1, -1). Then in the previous step, x = y1 = -1, y = x1 - (a//b)*y1. Here, a is 2, b is 3, so a//b is 0. So y is 1 - 0 * (-1) = 1. So returns (1, -1, 1). So the equation is 2*(-1) +3*(1) = -2 +3 = 1, which is correct. 

So for the example given, when a=2, b=3, n=7. The gcd is 1, which divides 7. Then the extended_gcd returns (1, -1, 1). Multiply by 7 to get x=-7, y=7. But the sample expects (2,1). Wait, but that's another solution. Because ax + by =n has infinitely many solutions once you have one. So how do we get the correct x and y?

Wait, the sample solution is (2,1) because 2*2 +3*1=7. Let me check: 2*2 is 4, 3*1 is 3, sum is 7. So that's correct. But according to the extended_gcd, the solution would be x=-7, y=7. But that's also a solution. So why does the sample return (2,1)? Because there are infinitely many solutions. So the problem is to return any one solution. So the function can return any solution, but the sample expects a particular one. How do I get that?

But the problem says to return any solution. So the sample solution is (2,1). How do I get that from the extended_gcd?

Well, the extended_gcd gives one solution, but there are infinitely many. So perhaps the function can return any solution. But how to get the solution that the sample expects?

Wait, perhaps the sample is just one possible solution. So the function can return any solution. So the problem is to find any solution, not necessarily the one in the sample. But the sample is just an example.

But the problem says that the function must return (2,1) for that case. So perhaps the function is expected to return the solution with minimal x and y, or some other criteria. But the problem says that any solution is acceptable as long as it satisfies the equation. However, the sample is given, so perhaps the function should return a solution that is in the form of the extended_gcd multiplied by the scaling factor. But perhaps there are multiple solutions, and the sample is just one of them.

So the problem is to find any solution, but how to ensure that the function returns one. So perhaps the extended_gcd approach is correct, but the sample solution is another possible solution. So how to get that?

Alternatively, maybe there's a way to find the solution with positive x and y, but that's not always possible.

Wait, in the sample case, the solution (2,1) is correct. Let me see. The extended_gcd gives x=-1 and y=1 for the equation 2x +3y =1. Multiply by 7 gives x=-7, y=7. But that's one solution. But there are other solutions. For example, adding multiples of b/gcd to x and subtracting multiples of a/gcd from y. Because the general solution is x = x0 + (b/g)*k, y = y0 - (a/g)*k, where k is any integer. So for the sample case, the general solution is x = -7 + 3k, y =7 - 2k. So for k=3, x = -7 +9 =2, y=7-6=1. Which is the sample solution. So the function can return any solution, but perhaps the sample is expecting a particular one.

So the problem is, how to find x and y such that ax + by =n, and return any such pair. So the approach is:

- Check if the gcd divides n. If not, return None.

- Else, find x0, y0 such that ax0 + by0 = gcd(a,b). Then multiply by (n/gcd) to get x = x0 * (n/gcd), y = y0 * (n/gcd).

But then, the solution may not be the one in the sample. However, the sample is just one possible solution, and the problem says to return any solution. So perhaps the sample is just an example, and the function can return any correct solution.

But the problem says that the sample should return (2,1). So how can we ensure that the function returns that particular solution? Well, perhaps the way we compute x0 and y0 with extended_gcd may vary depending on the implementation. For example, in the sample case, the extended_gcd returns x=-1, y=1. Then multiplying by 7 gives x=-7, y=7. But that's not the sample solution. However, by adjusting k, we can find the sample solution. But how to get that in the code?

But the problem says that the function can return any solution. So perhaps the sample is just one possible solution, and the code can return any solution. However, the assertion in the problem is that find_solution(2,3,7) returns (2,1). So the code must return that specific solution. But how?

Wait, perhaps the function is supposed to return the solution with minimal x and y? Or perhaps the code is supposed to return the solution with x and y positive? But that's not possible for all cases.

Alternatively, maybe the problem expects that the code returns the solution found by the extended Euclidean algorithm, but scaled. However, in the sample case, the code would return (-7,7), which is not the same as the sample. But the problem's assertion is that it returns (2,1). So perhaps the code must return a solution, but the sample is just one possible solution, and the code can return any solution. However, the sample assertion is given, so the code must return that solution for that case. But how to ensure that?

Wait, perhaps the problem is not requiring the code to return any solution, but to return a particular one. But how to find that?

Alternatively, perhaps the code is supposed to find x and y such that x is non-negative and y is non-negative, but that's not always possible.

In the sample case, the solution (2,1) is valid. Let me think: the general solution is x = -7 + 3k, y =7 - 2k. So to find x and y positive, we can find k such that x>0 and y>0. For example:

x = -7 +3k >0 → k>7/3 → k≥3.

y=7-2k>0 → k <7/2 →k ≤3. So k=3. So x= -7+9=2, y=7-6=1. So that's the solution. So perhaps the code should find the solution with x and y positive, but how?

But how to find that in code? Well, the code can generate the general solution and find the correct k. But that's more complicated.

But perhaps the problem expects the code to return any solution, but the sample is just one possible solution. However, the code's output must match the sample. So how can we ensure that?

Alternatively, perhaps the code can return the solution found by the extended Euclidean algorithm, but then adjust it to find a solution with positive x and y. But that's complicated.

Alternatively, maybe the code can return the solution (x0 * (n/g), y0 * (n/g)) and that's acceptable. But in the sample case, that would give (-7,7), which is not the sample's solution. However, the problem's assertion is that the sample returns (2,1). So that suggests that the code must return that particular solution. How?

Wait, perhaps the code is supposed to return the solution with minimal x and y? Or perhaps the code is supposed to return the solution with x positive and y positive, if possible. But how to find that?

Alternatively, perhaps the problem's sample is just an example, and the code is allowed to return any correct solution. So the code's output may differ from the sample, but the assertion in the problem is just an example. However, the code must return a correct solution, and the assertion is just one possible case. But the user's code is supposed to pass the given assertion. So in the sample case, the code must return (2,1). 

But how to make sure that the code returns that solution?

Let me think again. Let me compute the sample case with the code.

Sample input: a=2, b=3, n=7.

gcd(2,3) is 1, which divides 7. So proceed.

extended_gcd(2,3) returns (1, -1, 1). So x0 = -1, y0 = 1. Multiply by 7 gives x=-7, y=7. But the sample expects (2,1). How to get that?

The general solution is x = -7 + 3k, y =7 - 2k. So for k=3, x=2, y=1. So the code can find k such that x and y are positive. But how to compute k?

But perhaps the code can find the solution with minimal x and y. But how?

Alternatively, perhaps the code can find x and y such that x is positive and y is positive. But how to find that?

Alternatively, perhaps the code can find the solution by using the extended_gcd and then adjusting the solution to find the correct one. But that's complicated.

Alternatively, maybe the code should return the solution found by the extended_gcd, but the sample is just an example. However, the sample's solution is not the one returned by the code. So perhaps there's a mistake in the approach.

Alternatively, perhaps the code should return the solution with the minimal x, or minimal absolute value. But how?

Alternatively, perhaps the code is supposed to return the solution where x is positive and y is positive. So for the sample case, that would be (2,1). But how to find that?

But how to find such a solution in code. Let's think.

Once we have x0 and y0, the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t, where t is any integer.

We can find t such that x and y are positive. For example, in the sample case, x0 = -7, y0 =7. So the general solution is x = -7 +3t, y=7-2t.

We need to find t such that x>0 and y>0.

So:

-7 +3t >0 → t>7/3 → t≥3.

7-2t >0 → t <7/2 → t ≤3.

So t=3. So x=2, y=1.

So how to find t in code?

Well, perhaps the code can compute the general solution and then find the t that makes x and y positive. But how?

But that's not always possible. For example, if n is negative, or if the solution requires negative numbers.

But the problem says to return any solution. So perhaps the code can return the solution found by the extended_gcd, but the sample is just an example. However, the sample's solution is not the one found by the code, so the code would fail the assertion. So this suggests that the approach is not correct.

But why does the sample solution (2,1) work? Let me see: 2*2 +3*1 =7. So how to find that solution?

Alternatively, perhaps the code should use the extended Euclidean algorithm, but find x and y with the minimal absolute values. Or perhaps the code should return the solution with x positive and y positive. 

Alternatively, perhaps the code can find x and y by using the extended_gcd and then adjusting the solution to find one with positive x and y.

But how to implement that?

Alternatively, maybe the problem's sample is not the only solution, and the code can return any solution. But the assertion is given, so the code must return that solution. However, the code as written would return (-7,7), which is not the sample solution. So the code would not pass the assertion. Therefore, there must be a different approach.

Wait, perhaps the code is supposed to find x and y such that x is the minimal positive solution. Or perhaps the code should find the solution with the smallest x. But how?

Alternatively, perhaps the problem's sample is incorrect, but that's unlikely. So perhaps the code should return the solution (x, y) such that x and y are positive. But how to find that?

Alternatively, perhaps the code should find the solution where x is positive and y is positive. Let me think about the sample case again. How to find that?

In the general solution, x = x0 + (b/g)*t, y = y0 - (a/g)*t. So for the sample case, x0 = -7, y0 =7, and the general solution is x = -7 +3t, y =7 -2t.

We need x>0 and y>0. So solving:

-7 +3t >0 → t>7/3 → t≥3.

7-2t>0 → t <7/2 → t ≤3.

So t=3 is the only integer that satisfies both. So x=2, y=1. So the code can find this t. How?

In code, perhaps find t such that x and y are positive. But how to compute t?

Alternatively, the code can compute t as follows: 

t = (x0 + (b/g)*t) ... but I'm not sure.

Alternatively, once we have x0 and y0, we can compute t such that x is positive. For example, for the sample case, x0 is -7. We can find t such that x0 + (b/g)*t is positive. But how?

Alternatively, we can find t that makes x as small as possible, but positive. But how?

Alternatively, perhaps the code should compute the solution with x and y positive. So for the general solution, find t such that x and y are positive. 

But how to compute that in code?

Let me think. Let's suppose that we have x0 and y0. Then the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. We can find t such that x and y are positive. 

But how to find such t?

Let me think about the sample case. The general solution is x = -7 +3t, y =7-2t. We need x>0 and y>0. 

So solving for t:

-7 +3t >0 → t>7/3 → t≥3.

7-2t>0 → t<7/2 → t≤3. So t=3.

So t is 3. So for this case, t is the floor of (7/3) or something. 

But how to compute this in code? For general cases, it's possible that there are multiple t's that make x and y positive, or none. So perhaps the code can find the t that makes x and y positive, if possible. 

But how to find that t?

Alternatively, perhaps the code can find the t that makes x as small as possible and y as small as possible. 

But this seems complicated. However, for the purpose of passing the sample assertion, perhaps the code can find such a t. 

But how?

Let me think: once we have x0 and y0, the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. We can find t such that x and y are positive. 

But how to find t? 

Alternatively, we can find t such that x is positive and y is positive. 

Let me think: 

We can solve for t in the inequalities:

x0 + (b/g)*t > 0 → t > -x0 * g / b 

y0 - (a/g)*t > 0 → t < y0 * g /a 

But since g is the gcd of a and b, and a and b are positive? Or are they allowed to be negative?

Wait, the problem says that a and b are integers. But in the sample, they are positive. But the code should handle any integers. 

But perhaps the code can assume that a and b are positive. Or not. 

But in the problem statement, the sample uses positive integers. 

But for the code, perhaps it's better to handle all cases. 

But perhaps the code can proceed under the assumption that a and b are positive. 

But regardless, the code needs to find t that satisfies the inequalities. 

But how to compute that in code?

Alternatively, perhaps the code can compute t as follows:

t = (x0 + (b/g)*t) ... no, that's not helpful. 

Alternatively, for the general solution, the code can find the value of t that makes x and y positive. 

But how?

Alternatively, the code can compute the minimal t such that x is positive. Then check if y is positive. 

For example, in the sample case:

x0 = -7, b/g = 3, so t_min is 3. 

Then check y: 7 - 2*3 = 1>0. So it's acceptable. 

So for code, perhaps compute t_min such that x is positive. 

But how?

Let me think. For x to be positive, t must be greater than ( -x0 * g ) / b. But since x0 is from the extended_gcd, which may be negative. 

Alternatively, the code can find t as follows:

t = ceil( ( -x0 * g ) / b )

But I'm not sure. 

Alternatively, for the general solution, the code can find the t that makes x and y positive. 

But this seems complicated. 

But perhaps for the purpose of passing the sample assertion, the code can find the solution with x and y positive. 

So, in the code, after finding x0 and y0, we can compute the general solution and find t such that x and y are positive. 

But how to do that?

Let me think about the code steps:

Once we have x0 and y0, then the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

We can find t such that x and y are positive. 

Let me think about solving for t:

x = x0 + (b/g)*t > 0 → t > (-x0 * g)/b 

y = y0 - (a/g)*t > 0 → t < (y0 * g)/a 

So the valid t must be in the interval ( (-x0 * g)/b , (y0 * g)/a )

But since t must be an integer, we can find t in that range. 

But how to find such a t?

For example, in the sample case:

x0 = -7, y0=7, g=1, a=2, b=3.

So the interval for t is:

t > (-(-7)*1)/3 → 7/3 ≈ 2.333 → t>2.333 → t≥3.

t < (7*1)/2 → 3.5 → t <3.5 → t≤3.

So t=3 is the only integer in that range. 

So the code can compute t as the floor of the lower bound, or something like that. 

But how to find this t in code?

Alternatively, the code can compute the t that makes x and y positive. 

But how to compute it?

Well, the code can compute the lower and upper bounds for t and choose any integer in that range. 

But how to compute this in code?

For example:

t_low = ceil( (-x0 * g) / b )

t_high = floor( (y0 * g) / a )

If t_low <= t_high, then there is a t that satisfies the conditions. 

Once we find such a t, we can compute x and y. 

But how to compute this in code?

Let me think. For the sample case, the code would find t_low = ceil( (7)/3 ) = 3, t_high = floor( 7/2 ) =3. So t=3. 

So x = -7 +3*3 = 2, y=7-2*3=1. 

So this would give the sample solution. 

But how to implement this in code?

So, the code steps would be:

After finding x0 and y0, compute g = gcd(a, b). 

Then, the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

We need to find t such that x and y are positive. 

So compute:

t_low = ceil( ( -x0 * g ) / b )

t_high = floor( (y0 * g ) / a )

If t_low <= t_high, then choose any t in that range. 

But how to compute t_low and t_high in Python?

But in Python, we can compute this using math.ceil and math.floor. 

But what if a or b is zero? Well, the problem says that the function returns None if no solution exists. So a and b cannot both be zero. 

But for the code, we need to handle cases where a or b is zero. 

But perhaps the code can assume that a and b are not both zero. 

But this is getting complicated. 

Alternatively, perhaps the code can compute t such that x and y are positive, and return the first solution found. 

But this may not always be possible, but for the sample case, it works. 

So, in code, after finding x0 and y0, and knowing that g divides n, we can proceed as follows:

Compute the general solution, then find t such that x and y are positive. 

But how to implement this?

Let me try to write code for this. 

Once x0 and y0 are found, and g is the gcd(a, b), then:

t_low = ceil( ( -x0 * g ) / b )

t_high = floor( (y0 * g ) / a )

But wait, the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

Wait, the general solution is derived from the equation ax + by =n. 

But the original equation after scaling is ax + by =n. 

But the extended_gcd gives ax0 + by0 = g. 

So, when we multiply by k = n/g, we get ax0*k + by0*k = n. 

So the solution is x = x0 *k, y = y0 *k. 

But the general solution is x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

Wait, no. The general solution for ax + by = n is x = x0 + (b/g)*t, y = y0 - (a/g)*t, where t is any integer. 

So, for the sample case, after scaling, x0 is -7, y0 is7, and the general solution is x = -7 +3t, y =7 -2t. 

So the code needs to find t such that x and y are positive. 

But how to compute t_low and t_high?

Let me think again. 

We have:

x = x0 + (b/g)*t >0 → t > (-x0 * g)/b 

y = y0 - (a/g)*t >0 → t < (y0 * g)/a 

So t must be in the interval ( (-x0 * g)/b , (y0 * g)/a )

But since t is an integer, we can find the smallest integer t_low that satisfies t > (-x0 * g)/b. 

t_low = floor( (-x0 * g)/b ) + 1 

Similarly, t_high = floor( (y0 * g)/a )

If t_low <= t_high, then there is a solution. 

But how to compute this in code?

Let me try with the sample case:

x0 = -7, y0=7, g=1, a=2, b=3.

So:

(-x0 * g)/b = (7*1)/3 = 7/3 ≈ 2.333. 

So t_low = floor(2.333) + 1 = 2 +1 =3.

(y0 * g)/a = (7 *1)/2 = 3.5 → floor is 3. So t_high=3. 

So t_low=3, t_high=3. So t=3. 

So x= -7 + 3*3 = 2, y=7-2*3=1. 

So that's the sample solution. 

So this approach works. 

So the code can compute t_low and t_high as follows:

t_low = math.ceil( (-x0 * g) / b )

t_high = math.floor( (y0 * g) / a )

Wait, but earlier calculation says t_low is floor( (-x0 * g)/b ) +1. 

Wait, for example, (-x0 * g)/b is 7/3 = 2.333. The t must be greater than this value. The smallest integer greater than 2.333 is 3. So math.ceil(2.333) is 3. 

So t_low = math.ceil( (-x0 * g)/b )

Similarly, t_high = math.floor( (y0 * g)/a )

If t_low <= t_high, then choose any t in that range. 

So the code can choose t = t_low, and compute x and y. 

But how to handle this in code?

So, the steps for the code would be:

1. Compute g = gcd(a, b). 

2. Check if n % g != 0 → return None.

3. Else, compute k = n // g.

4. Compute x0, y0 using extended_gcd(a, b).

5. x = x0 *k, y = y0 *k. 

6. Then, find t such that x and y are positive. 

But how?

Wait, no. The general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

Wait, no. The general solution for ax + by =n is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

But x0 and y0 are solutions to ax0 + by0 = g. 

So when we scale by k = n/g, the solution is x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

Wait, no. Let me think again. 

The original equation is ax + by = n. 

The extended_gcd gives ax0 + by0 = g. 

So multiplying both sides by k = n/g gives ax0*k + by0*k = n. 

So x0*k and y0*k is a solution. 

The general solution is x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

So for the code, after finding x0 and y0, the code can compute x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

So to find t such that x and y are positive, we can compute:

x = x0*k + (b/g)*t > 0 → t > (-x0*k * g ) / b 

Wait, no. Let me re-arrange:

x = x0*k + (b/g)*t > 0 → t > - (x0*k * g)/b 

Wait, but this seems complicated. 

Alternatively, since x0*k is the initial solution, and the general solution is x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

So, for the sample case, x0*k is -7, y0*k is 7. 

So, the general solution is x = -7 + 3t, y =7 - 2t. 

So the code needs to find t such that x and y are positive. 

So, the code can compute t_low and t_high as:

t_low = ceil( (-x0*k * g)/b )

Wait, no. Let me think again. 

The general solution is x = x0*k + (b/g)*t. 

We want x > 0 → x0*k + (b/g)*t > 0 → t > - (x0*k * g)/b 

Similarly, y = y0*k - (a/g)*t >0 → t < (y0*k * g)/a 

So, t_low = math.ceil( - (x0*k * g)/b )

t_high = math.floor( (y0*k * g)/a )

But in the sample case, x0*k is -7, y0*k is 7, g=1, a=2, b=3.

So:

t_low = ceil( - (-7 * 1)/3 ) = ceil(7/3) = 3.

t_high = floor( (7 * 1)/2 ) = 3.

So t=3. 

So x = -7 +3*3 =2, y=7-2*3=1. 

This gives the sample solution. 

So in code, after finding x0 and y0, and k = n/g, the code can compute:

t_low = math.ceil( (-x0*k * g ) / b )

Wait, no. The formula for t_low is:

t > - (x0*k * g ) / b ?

Wait, the equation x = x0*k + (b/g)*t > 0 → (b/g)*t > -x0*k → t > (-x0*k * g)/b 

Yes. 

So t_low = math.ceil( (-x0*k * g)/b )

Similarly, t_high = math.floor( (y0*k * g)/a )

So in code:

import math

...

t_low = math.ceil( (-x0 * k * g) / b )

t_high = math.floor( (y0 * k * g) / a )

But wait, in the sample case, x0*k is -7, g is 1. So -x0*k *g is 7*1 =7. Divided by b=3 →7/3=2.333. So math.ceil(2.333) is 3. 

Yes. 

So this seems correct. 

So the code can compute t_low and t_high, and if t_low <= t_high, then choose t = t_low, and compute x and y. 

But what if there is no such t? For example, if the interval is empty. Then, there is no solution with positive x and y. But the problem says that there is a solution, so there must be at least one t. 

But perhaps the code can choose any t in the range. 

But how to handle cases where the solution may have negative x or y? 

Well, the problem says that any solution is acceptable. So the code can return any solution, but the sample requires a particular one. 

So, for the code to pass the sample assertion, it's necessary to find the solution with positive x and y. 

So, the code can proceed as follows:

Once the code has x0, y0, and k = n/g, compute the general solution's x and y as x = x0*k + (b/g)*t, y = y0*k - (a/g)*t. 

Then compute t_low and t_high as above. 

If there is at least one t in that range, choose t = t_low, compute x and y. 

But how to handle cases where the solution has x or y negative?

But the problem says that any solution is acceptable. So the code can return the solution found by the extended_gcd, but the sample requires a particular solution. 

But with this approach, the code would return the sample solution. 

So, integrating this into the code:

So, the code would be:

Implement extended_gcd, check if gcd divides n, then compute k, then find t_low and t_high, and choose t = t_low, and compute x and y. 

But how to handle cases where a or b is zero? 

But let's proceed with the code. 

Now, the code steps:

Implement extended_gcd.

Then, for the given a, b, n:

Compute g = gcd(a, b).

If n % g != 0 → return None.

Else:

k = n // g.

Compute x0, y0 via extended_gcd(a, b).

Then compute t_low and t_high as above.

If t_low <= t_high, choose t = t_low, compute x = x0*k + (b/g)*t, y = y0*k - (a/g)*t.

Else, return None? No, because the equation has solutions, but there is no t that makes x and y positive. So the code can return any solution, like x0*k and y0*k. 

But in that case, the code can return x0*k and y0*k. 

But how to handle that? 

But the problem says to return any solution. So, the code can return x0*k and y0*k. 

But for the sample case, that would give x = -7, y=7. 

But the sample expects (2,1). 

So, to pass the sample, the code must find the solution with positive x and y. 

So, the code must find t_low and t_high and choose a t in that range. 

But how to handle cases where there is no such t? 

But the equation has solutions, so there must be at least one solution. 

But the code can choose any solution. So, if there is
```

</details>

**Code that ran:**

```python
import math

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def find_solution(a, b, n):
    g, x0, y0 = extended_gcd(a, b)
    if n % g != 0:
        return None

    k = n // g
    x = x0 * k
    y = y0 * k

    # Find t to ensure x and y are positive
    b_div_g = b // g
    a_div_g = a // g

    # Compute t_low and t_high for x > 0 and y > 0
    numerator_x = -x * g
    t_low = math.ceil(numerator_x / b)
    numerator_y = y * g
    t_high = math.floor(numerator_y / a)

    if t_low <= t_high:
        t = t_low
        x = x0 * k + b_div_g * t
        y = y0 * k - a_div_g * t
        return (x, y)

    # Fallback to original solution if no positive t found
    return (x, y)
```

**Visible-test report:**

```text
PASS    assert find_solution(2, 3, 7) == (2, 1)
1 of 1 visible tests passed
```
