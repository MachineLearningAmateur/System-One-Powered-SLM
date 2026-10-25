# Mbpp/160, attempt 0

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/160/a0/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 746.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_solution that takes three integers a, b, n and returns a tuple (x, y) such that ax + by = n. If there's no solution, return None. The example given is find_solution(2,3,7) returns (2,1) because 2*2 +3*1 =7. 

First, I should think about how to find x and y. This seems like a linear Diophantine equation. The equation ax + by = n. I remember that for this equation to have a solution, the greatest common divisor (gcd) of a and b must divide n. So first, I need to check if gcd(a, b) divides n. If not, return None.

But how to find x and y once we know there's a solution? Well, the extended Euclidean algorithm can find x and y such that ax + by = gcd(a, b). Then, if n is a multiple of the gcd, we can scale those coefficients accordingly.

So the steps I need to take are:

1. Compute the gcd of a and b. Let's call it g.
2. Check if n is divisible by g. If not, return None.
3. Otherwise, find x0, y0 such that ax0 + by0 = g.
4. Multiply x0 and y0 by (n/g) to get the solution. So x = x0*(n/g), y = y0*(n/g).

But how to implement the extended Euclidean algorithm in Python?

Let me think. The extended Euclidean algorithm finds gcd(a, b) and coefficients x, y. Let me write a helper function for that.

Wait, but what if a or b is zero? Well, the problem says to return integers x and y. Let me think about edge cases. For example, if a is zero, then the equation becomes by = n. So if b divides n, then y = n/b, x can be anything. But the problem requires to return a solution. However, the example given has a and b non-zero. But I need to handle cases where a or b is zero.

Wait, but the problem says that the function should return integers x and y. So for example, if a is zero, then the equation is by = n. So if b divides n, then y = n/b. But x can be any integer. However, the problem requires to return a specific solution. But how to choose x? Well, maybe the problem expects that when a is zero, then x can be zero, but perhaps the code needs to handle that.

But maybe the problem expects that a and b are non-zero? Or perhaps the code should handle all cases.

But let's proceed. Let's think about the general case.

So, the helper function for extended Euclidean algorithm:

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = extended_gcd(b, a % b)
        return (g, y, x - (a//b)*y)

Wait, this is a recursive approach. Let me test this. For example, for a=2, b=3, the extended_gcd would compute the gcd(2,3) which is 1. Then, the coefficients would be x and y such that 2x +3y =1. Let's see. The example given in the problem is 2*2 +3*1 =7. Which is 7=2*2 +3*1. So for the equation 2x +3y =7, the solution is x=2, y=1. But the extended_gcd would give for 2 and 3, the coefficients x and y such that 2x +3y =1. Let me see. For example, the extended_gcd(2,3) would return (1, -1, 1), because 2*(-1) +3*1 = 1. Then, when we multiply by 7 (since n=7 is 7 times the gcd), we get x = -7, y =7. But that's not the solution given. Wait, but the example solution is (2,1). So perhaps there are multiple solutions. So how to get the correct one?

Wait, the problem says to return any solution. So perhaps the example is just one possible solution. But the code needs to return a valid solution. However, the example given is (2,1). Let me check. For the equation 2x +3y =7. The solution (2,1) gives 4 +3 =7. Another solution is x= -1, y=3, because 2*(-1) +3*3= -2 +9=7. So there are multiple solutions. So the code can return any of them.

So in the example, the code returns (2,1). How to get that from the extended Euclidean algorithm?

Let me think. The extended_gcd(2,3) returns (1, -1, 1). So the solution for 2x +3y =1 is x=-1, y=1. Then, for 7, we multiply by 7. So x = -7, y=7. But that's a valid solution. However, the example expects (2,1). So perhaps the code needs to find a particular solution, but the problem allows any. But the example is just one possible solution. So the code can return any valid solution.

But the problem's test case is expecting (2,1). So perhaps the code's approach is to find the solution via the extended Euclidean algorithm, then adjust it to find a particular solution. But how?

Wait, perhaps the code should find the general solution. Once we have a particular solution (x0, y0), then the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t for any integer t. So, perhaps we can adjust t to find x and y that are integers. However, for the problem's purpose, any solution is acceptable. So the code can return the one found via the extended_gcd scaled by n/g.

But in the example, the code returns (2,1). Let me see. Let me compute the extended_gcd(2,3) gives (1, -1, 1). So the solution for 2x +3y =1 is x=-1, y=1. Then, multiply by 7, we get x=-7, y=7. Which is a valid solution. However, the example's solution is (2,1). How to get that?

So the problem is that the extended_gcd gives a solution, but perhaps there are multiple solutions, and the code needs to return one of them. However, the example's solution is (2,1). So perhaps there's a way to adjust the solution to get that.

But the problem says that the function can return any solution. So perhaps the code can return any solution. However, the test case expects (2,1). So how to get that?

Alternatively, perhaps the code's approach is to find the solution via the extended Euclidean algorithm, and then adjust it to find a solution with minimal positive values or something. But perhaps the code is supposed to return any solution, and the test case is just one example.

But the problem says that the code must return the correct solution. So how to make sure that the code returns the correct solution in the test case?

Alternatively, perhaps the code is supposed to return the solution with the smallest possible x or y. But that's not clear. However, the problem's example is (2,1). So perhaps the code needs to return that.

But how to get that from the extended Euclidean approach?

Alternatively, perhaps the code is not using the extended Euclidean algorithm, but another method. Let me think.

Another approach is to iterate through possible x values and check if (n - a*x) is divisible by b. For example, for each x in a certain range, compute y = (n - a*x)/b and check if it's integer. But this approach is not efficient for large numbers. However, given that the problem may not have constraints on the size of a, b, n, this approach may not be feasible for large values. But perhaps the problem expects that.

But for the given example, let's see. For a=2, b=3, n=7. We can iterate x from 0 to 7//2=3. For x=0: 7-0=7, divided by 3 is not integer. x=1: 7-2=5, 5/3 not integer. x=2: 7-4=3, 3/3=1. So y=1. So (2,1) is found. So this approach would work for the example. But for larger numbers, this approach is not feasible. So for the problem, perhaps the code needs to use the extended Euclidean algorithm.

But the problem is that the code needs to return any solution. So perhaps the code can use the extended Euclidean algorithm, and then adjust the solution to find x and y. However, the example's solution is different from what the extended Euclidean approach gives. So perhaps there's a mistake in the approach.

Wait, perhaps the code can use the extended Euclidean algorithm, but then find the solution (x0 * k, y0 * k), where k is n/gcd(a,b). But in the example, the gcd is 1, so k is 7. So the solution would be x0 *7, y0 *7. But the extended_gcd returns x0=-1 and y0=1. So x=-7, y=7. Which is a valid solution. However, the example expects x=2 and y=1. How to get that?

Well, the general solution for ax + by = n is x = x0 + (b/g)*t, y = y0 - (a/g)*t, where t is any integer. So for the example, the general solution is x = -7 + 3t, y = 7 - 2t. So for t=3, x= -7 +9=2, y=7-6=1. So that's the solution (2,1). So the code can choose t such that x and y are positive, or any other condition. But how to find the correct t?

But the problem requires to return any solution. So the code can return any of them. However, the test case expects (2,1), which is one of the possible solutions. So the code needs to find that solution. But how to do that?

Alternatively, perhaps the code can use the extended Euclidean algorithm and then find the solution with the minimal x or y. But how to do that?

Alternatively, perhaps the code can compute x0 and y0 using extended Euclidean, and then adjust x and y by adding multiples of b/g and subtracting multiples of a/g. But how to find the right t?

But perhaps the code can just return the solution from the extended Euclidean algorithm multiplied by k, and that's acceptable. But in the example, that gives a different solution. However, the test case is expecting (2,1), but the code's solution would be (-7,7). But the problem says that any solution is acceptable. However, the test case is expecting (2,1). So perhaps the code's approach is not correct. But why?

Wait, the problem's assert statement says that find_solution(2,3,7) returns (2,1). So the code must return that solution. But how?

So perhaps the code needs to find x and y such that x is non-negative and y is non-negative. Or perhaps the code needs to find the solution with the minimal x or y. But how to ensure that?

Alternatively, perhaps the code is supposed to return the solution found by the extended Euclidean algorithm, but with some adjustments. Let me think.

Let me re-examine the example. The extended_gcd(2,3) returns (1, -1, 1). So the equation is 2*(-1) +3*1=1. Multiply by 7: 2*(-7) +3*7 =7. So that's a solution. But the example's solution is (2,1). So how to find that?

The general solution is x = -7 + 3t, y=7-2t. So to find x and y such that x is positive and y is positive. Let's find t such that x and y are positive.

x = -7 +3t >0 → 3t>7 → t>7/3 → t≥3. Similarly, y=7-2t>0 → 2t <7 → t<3.5 → t ≤3. So t must be 3. So x=-7 +9=2, y=7-6=1. Which gives the solution (2,1). So the code can find t such that x and y are positive. But how to compute that?

But how to find t in general? For the code, perhaps after finding the initial solution (x0, y0), we can adjust t to find the solution with x and y positive. However, this may not be feasible for all cases. For example, if the equation has solutions but x and y are negative, but the code needs to return a solution with x and y positive.

But perhaps the problem does not require x and y to be positive, but any integers. So the code can return any solution. However, the test case expects (2,1), which is a solution. So perhaps the code needs to return that solution. But how?

Alternatively, perhaps the code should use the extended Euclidean algorithm and then find the solution with minimal x or y. But how to do that?

Alternatively, perhaps the code can use the extended Euclidean algorithm and then adjust the solution by adding multiples of b/g and subtracting multiples of a/g to find a solution that satisfies some condition.

But perhaps the code can proceed as follows:

Once we have the initial solution (x0, y0) for ax + by = g, then multiply by k = n/g to get (x0*k, y0*k). Then, adjust x and y to find a solution where x and y are positive. However, this may not always be possible. But for the test case, it works.

But how to adjust x and y?

Alternatively, perhaps the code can find the solution using the extended Euclidean algorithm and then return that solution. However, the test case's solution is different. So perhaps the code is not correct. But why?

Wait, perhaps the code's approach is to find any solution, and the test case's solution is just one of the possible solutions. So the code can return any solution. However, the test case's solution is (2,1), which is correct. So how to make sure that the code returns that solution?

But the code's approach using the extended Euclidean algorithm gives a different solution. So perhaps the code needs to find the solution with the minimal x or y. But how?

Alternatively, perhaps the code should find the solution with the minimal x. For example, in the test case, x can be -7, 2, etc. So how to find the minimal x?

Alternatively, perhaps the code can find the solution using the extended Euclidean algorithm, and then adjust the solution by adding multiples of b/g to x and subtracting multiples of a/g from y. But how to find the correct t?

This seems complicated. However, perhaps the code can proceed with the initial solution, and then return that. But the test case expects a different solution. So the code would fail the test case.

But why does the test case expect (2,1)? Because that's one possible solution. So the code can return any solution. So perhaps the code is correct as long as it returns any solution, and the test case is just one example.

But the problem says that the function should return the correct solution. So perhaps the code needs to return the solution found by the extended Euclidean algorithm scaled by k. However, that would not match the test case. So why is the test case expecting (2,1)?

Wait, perhaps the code is not using the correct approach. Let me think again.

Another approach: the equation ax + by = n. Let's find x and y such that x = (n - by)/a. So for each possible y, check if (n - by) is divisible by a. But for large values of a and b, this approach is not feasible. However, for the purpose of solving the problem, perhaps the code can use this approach for small values.

But how to find y? Well, the code can iterate y from 0 to some upper limit. For example, for the test case, a=2, b=3, n=7. We can iterate y from 0 to 7//3=2. For y=0: 7 -0 =7. 7%2=1, not zero. y=1: 7-3=4, 4/2=2. So x=2. So that's the solution. So this approach would find the solution. But for large numbers, this approach is not feasible.

But perhaps the code can use this approach for small values. However, the problem may not have constraints on the input size. So this approach may not be efficient.

But given that the problem requires to return any solution, perhaps the code can use the extended Euclidean algorithm approach and then adjust the solution to find x and y that are in a certain range.

Alternatively, perhaps the code can use the extended Euclidean algorithm and then find the solution with the minimal x or y. For example, in the test case, the code can find x=2, y=1.

But how to do that programmatically?

Let me think. Once we have the general solution x = x0 + (b/g)*t, y = y0 - (a/g)*t. We can find t such that x and y are positive. For example, in the test case, the general solution is x = -7 + 3t, y =7 - 2t. We can find t such that x and y are positive. For x to be positive, 3t >7 → t> 7/3 → t≥3. For y to be positive, 7-2t>0 → t< 3.5 → t ≤3. So t=3 is the only possible value. So x= -7 +9=2, y=7-6=1.

So the code can find t such that x and y are positive. But how to find this t?

In general, for the solution x0, y0, and the general solution x = x0 + (b/g)*t, y = y0 - (a/g)*t. We need to find t such that x and y are integers (which they are for any integer t). But perhaps the code can find t such that x and y are positive. However, this may not always be possible. For example, if the equation has solutions but all possible x and y are negative. However, the problem allows any integers, not necessarily positive.

But the code can return any solution, so perhaps the code can find the solution with minimal absolute values, or any other criteria. But how to implement this?

Alternatively, perhaps the code can find the solution using the extended Euclidean algorithm, then adjust it by adding or subtracting multiples of b/g and a/g respectively to find a solution with x and y positive.

But this seems complicated. However, given the example, perhaps the code can proceed as follows:

After finding the initial solution (x0, y0), which is scaled by k = n/gcd(a, b), the code can adjust x and y by adding multiples of b/g and subtracting multiples of a/g to find a solution where x and y are positive.

But how to compute this?

Let me think. For the test case, the initial solution is x=-7, y=7. To find x and y positive, we can add 3 (b/g=3/1=3) to x, and subtract 2 (a/g=2/1=2) from y. So each increment of t adds 3 to x and subtracts 2 from y. So for t=3, x becomes -7 + 3*3 = 2, y becomes 7 - 2*3 =1. Which is the solution.

So the code can compute t as follows: find t such that x is positive and y is positive. However, how to find t?

Alternatively, the code can compute the minimal t that makes x positive. Or find t that makes x and y as small as possible.

But this seems complicated. However, perhaps the code can proceed with the following steps:

Once the code finds the initial solution (x0, y0), which is (x0*k, y0*k), then find t such that x = x0 + (b/g)*t is as small as possible, or adjust t to make x and y positive.

But how to find t?

Alternatively, the code can compute x and y using the extended Euclidean algorithm, and then return them as is. But in the test case, that would return (-7, 7), which is a valid solution. However, the test case expects (2,1). So why is that?

The problem's assert statement says that find_solution(2,3,7) returns (2,1). So the code must return that. But how to get that from the extended Euclidean approach?

Ah! Wait, perhaps I made a mistake in the extended Euclidean algorithm. Let me recheck the extended_gcd function.

Let me recompute the extended_gcd for a=3, b=2. Because the code may have a mistake in the order of parameters.

Wait, the extended_gcd function is called with a and b. Let me think again. For example, for a=2, b=3, the extended_gcd(2,3) would call extended_gcd(3, 2%3=2). Then, extended_gcd(3, 2) calls extended_gcd(2, 3%2=1). Then, extended_gcd(2,1) calls extended_gcd(1, 2%1=0). Then, returns (1, 1, 0). Then, returns (1, 0, 1 - (2//1)*0) = (1, 0, 1). Then, returns (1, 1, 0 - (3//2)*1) = (1, 1, -1). Then, returns (1, -1, 1 - (2//3)*-1) → wait, this is getting complicated. Let me trace the steps.

Let me write the extended_gcd function again. Let's take a=2, b=3.

extended_gcd(2,3):

since b !=0, compute extended_gcd(3, 2%3=2). So call extended_gcd(3, 2).

extended_gcd(3,2):

b !=0, call extended_gcd(2, 3%2=1).

extended_gcd(2,1):

b !=0, call extended_gcd(1, 2%1=0).

extended_gcd(1,0):

returns (1, 1, 0).

Now, returning back:

For extended_gcd(2,1), returns (g, y, x - (a//b)*y). Here, a=2, b=1. So g=1, x=1, y=0. So returns (1, 0, 1 - (2//1)*0) = (1, 0, 1).

Then, for extended_gcd(3,2), which had a=3, b=2. The returned values are (g=1, x=0, y=1). Now, the return is (g, y, x - (a//b)*y). So a=3, b=2. a//b is 1. So returns (1, 1, 0 - 1*1) = (1, 1, -1).

Then, for extended_gcd(2,3), which had a=2, b=3. The returned values are (g=1, x=1, y=-1). So returns (1, -1, 1 - (2//3)*-1). Wait, a=2, b=3. So a//b is 0. So the return is (1, -1, 1 - 0 * -1) = (1, -1, 1). So the extended_gcd(2,3) returns (1, -1, 1). Which means that 2*(-1) +3*(1) = -2 +3 =1. So that's correct.

So the initial solution for ax + by = g is x=-1, y=1. Multiply by k=7, gives x=-7, y=7. Which is correct. But the example's solution is (2,1). So how to get there?

So the general solution is x = -7 + 3t, y=7 -2t. We need to find t such that x and y are integers. The example solution is when t=3.

But how to find t programmatically?

Well, perhaps the code can find t such that x is as small as possible, or find t that makes x and y positive. However, how?

Alternatively, the code can compute x and y using the extended Euclidean algorithm, and then adjust them by adding multiples of b/g and subtracting multiples of a/g to find a solution with x and y positive.

But how to compute t?

Let me think about the general solution. For the equation ax + by = n, once we have a particular solution (x0, y0), all solutions are given by:

x = x0 + (b/g)*t

y = y0 - (a/g)*t

where t is an integer.

To find a solution where x and y are positive, we can solve for t in the inequalities:

x0 + (b/g)*t >= 0

y0 - (a/g)*t >= 0

But solving these inequalities for t may give a range of t values. For example, in the test case, x0 = -7, y0 =7, g=1. So:

-7 +3t >=0 → t >= 7/3 → t >= 3 (since t is integer)

7 -2t >=0 → t <= 7/2 → t <= 3 (since t is integer)

So t must be 3. So x = -7 +3*3 =2, y=7-2*3=1.

Thus, the code can find t in this way. But how to implement this?

The code can compute the range of t that satisfies both inequalities, and choose t as the one that makes x and y positive. But how to compute this in code.

Alternatively, the code can compute t such that x is minimized or something.

But this seems complicated. However, given that the code must return a solution, perhaps the code can proceed as follows:

Once the code has x0 and y0, compute t such that x is as small as possible and y is as small as possible. But how?

Alternatively, the code can compute t = ceil( ( -x0 ) / (b/g) ), but this may not work in all cases.

Alternatively, the code can compute t = floor( (y0) / (a/g) ). But again, not sure.

Alternatively, the code can find t such that x is minimized. For example, t can be chosen to make x as small as possible. But this may not always work.

But perhaps for the code, it's easier to compute t such that x is in a certain range. For example, in the test case, the code can compute t = ceil( ( -x0 ) / (b/g) ), which for x0=-7, b/g=3, gives t = ceil(7/3) = 3.

So the code can compute t = ( -x0 + (b/g -1) ) // (b/g) ?

But perhaps this is getting too complex.

Alternatively, perhaps the code can compute t as follows:

t = ( -x0 ) // (b/g) 

But this is just a guess.

But perhaps the code can find the t that makes x and y positive by solving for t in the inequalities.

But how to implement this in code.

Let me think. For the general case:

x = x0 + (b/g) * t >= 0 → t >= -x0 / (b/g)

y = y0 - (a/g)*t >= 0 → t <= y0 / (a/g)

So the code can compute the range of t that satisfies both inequalities.

For example, in the test case, x0=-7, y0=7, b/g=3, a/g=2.

t >= 7/3 → t >= 2.333 → t >=3 (since t must be integer).

t <= 7/2 → t <=3.5 → t <=3.

So t=3 is the only integer that satisfies both.

So the code can compute t_min = ceil( (-x0) / (b/g) ), and t_max = floor( y0 / (a/g) ). If t_min <= t_max, then choose t = t_min or any value in between.

But how to compute this in code.

But for code, how to handle floating points? For example, in Python, we can use math.ceil and math.floor functions.

But this requires handling division and possible floating point inaccuracies.

But perhaps the code can proceed as follows:

Once we have x0 and y0, compute:

t_min = ceil( (-x0) / (b/g) )

t_max = floor( y0 / (a/g) )

if t_min <= t_max, then choose t = t_min, and compute x and y.

But how to compute this in code.

But this seems complex, but perhaps manageable.

But what if there is no such t? For example, if x0 and y0 are such that there is no t that makes x and y positive. For example, if the equation is 2x + 3y = 5. The solution could be x=1, y=1. But suppose we have a solution x0= -1, y0=1. Then, the general solution is x = -1 +3t, y=1-2t. So to find t such that x and y are positive:

x >=0 → -1 +3t >=0 → t >= 1/3 → t >=1.

y >=0 → 1-2t >=0 → t <=0.5 → t <=0. So no solution. So in this case, there is no solution with x and y positive. But there are solutions with negative values. For example, x=2, y=-1 (2*2 +3*(-1) =4-3=1, which is not 5. So perhaps I'm not thinking of the correct example.

Wait, the equation 2x +3y =5. One solution is x=1, y=1. Another solution is x=1+3t, y=1-2t. For example, t=1: x=4, y=-1. 2*4 +3*(-1)=8-3=5. So that's a valid solution. So even though there is no t that makes x and y both positive, there are solutions with one positive and one negative.

So the code can return any solution. So the code can return the solution found by the extended Euclidean algorithm, and it's acceptable.

But the problem's test case expects (2,1), which is a solution with both x and y positive. So how to make sure that the code returns that solution?

Perhaps the code can find the solution with the smallest x or y. But how?

Alternatively, perhaps the code can use the extended Euclidean algorithm and then adjust the solution by adding multiples of b/g to x and subtracting multiples of a/g from y until x and y are positive. But how to implement this.

But for the code, perhaps the best approach is to use the extended Euclidean algorithm to find x0 and y0, then compute t such that x is positive and y is positive. If there is no such t, then return the initial solution.

But this seems complicated. However, perhaps the code can proceed with the following steps:

1. Compute g = gcd(a, b).

2. Check if n is divisible by g. If not, return None.

3. Else, compute k = n / g.

4. Use extended Euclidean to find x0, y0 such that a*x0 + b*y0 = g.

5. Multiply x0 and y0 by k to get x = x0*k, y = y0*k.

6. Now, find t such that x + (b/g)*t and y - (a/g)*t are integers (which they are for any t).

7. Adjust t to find x and y that are integers. But how to choose t?

But the problem allows any solution. So perhaps the code can return x and y as computed in step 5.

But the test case expects (2,1), which is different from what step 5 gives. So why is that?

Because the code's solution is (-7,7), which is valid. But the test case expects (2,1). So the code would fail the test case.

But the problem says that the function should return any solution. So the test case's solution is just one of many possible solutions. So why does the test case expect (2,1)? Because it's a valid solution, but the code's solution is also valid. So the code's solution would pass the test case if the assert is checking for any solution.

Wait, but the assert in the problem is find_solution(2,3,7) == (2,1). So the code must return (2,1). But the code's solution returns (-7,7), which is a different tuple. So the code would fail the test case.

So the code must return (2,1) for this input. So the code must find that solution.

So the code needs to return a solution that matches the example. So how to achieve that?

Ah, perhaps the code is not using the correct initial solution. Let me think: perhaps the code should find x and y such that x is positive and y is positive. But how?

So perhaps the code can use the extended Euclidean algorithm to find x0 and y0, then find t such that x and y are positive.

So, for the test case, the code can find t=3. But how to compute that t.

Let me think of the general case. Let's say we have x = x0 + (b/g)*t, y = y0 - (a/g)*t.

We want to find t such that x >=0 and y >=0.

So:

x0 + (b/g)*t >= 0 → t >= -x0 * g / b

y0 - (a/g)*t >=0 → t <= y0 * g / a

So the code can compute the range of t and choose t within this range.

But how to compute this in code.

In code:

t_min = math.ceil( (-x0 * g) / b )

Wait, no. Let me re-express the inequalities:

For x >=0:

x0 + (b/g)*t >= 0 → t >= -x0 * g / b.

But since b/g is a positive integer (since g is the gcd of a and b), and x0 is the coefficient from the extended Euclidean algorithm.

But this may involve floating points.

Alternatively, since b/g is an integer, we can write:

t >= ceil( (-x0) * g / b )

Wait, not sure. Let me think again.

x = x0 + (b/g)*t >=0 → t >= -x0 * g / b.

But since b/g is a positive integer, and g is the gcd of a and b.

But perhaps it's easier to compute t_min and t_max as:

t_min = ceil( (-x0) / (b/g) )

t_max = floor( y0 / (a/g) )

So for the test case, x0=-7, y0=7, b/g=3, a/g=2.

t_min = ceil(7/3) = 3.

t_max = floor(7/2) =3.

So t=3.

So x = -7 +3*3 = 2, y=7-2*3=1.

So this gives the desired solution.

Thus, the code can compute t_min and t_max, and choose t as t_min if possible.

But how to implement this in code.

So, the code would:

After finding x0 and y0, compute:

b_div_g = b // g

a_div_g = a // g

t_min = math.ceil( (-x0) / b_div_g )

t_max = math.floor( y0 / a_div_g )

if t_min <= t_max:

   t = t_min

   x = x0 + b_div_g * t

   y = y0 - a_div_g * t

else:

   # no solution with x and y positive, return the initial solution or any other solution

But how to handle cases where t_min > t_max. For example, if there is no t that makes x and y positive, then return the initial solution.

But how to handle this in code.

But the code can proceed with this approach. So in the test case, this would work.

But how to implement this in Python.

But what if the division is not exact? For example, if (-x0) is not divisible by b_div_g.

But in Python, math.ceil can handle floating points.

But let's think about the test case.

x0 = -7, b_div_g =3.

(-x0) =7. 7 /3 is 2.333... ceil(2.333) is 3.

Yes.

So
```

</details>

**Code that ran:**

```python
import math

def find_solution(a, b, n):
    g = math.gcd(a, b)
    
    if n % g != 0:
        return None
    
    def extended_gcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            g, x, y = extended_gcd(b, a % b)
            return (g, y, x - (a // b) * y)
    
    g, x0, y0 = extended_gcd(a, b)
    k = n // g
    x = x0 * k
    y = y0 * k
    
    b_div_g = b // g
    a_div_g = a // g
    
    # Find t such that x and y are non-negative
    t_min = math.ceil((-x) / b_div_g)
    t_max = math.floor(y / a_div_g)
    
    if t_min <= t_max:
        t = t_min
        x = x + b_div_g * t
        y = y - a_div_g * t
    
    return (x, y)
```

**Visible-test report:**

```text
PASS    assert find_solution(2, 3, 7) == (2, 1)
1 of 1 visible tests passed
```
