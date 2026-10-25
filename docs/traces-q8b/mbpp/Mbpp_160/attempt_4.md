# Mbpp/160, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/160/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 960.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_solution that takes three integers a, b, n and returns a tuple (x, y) such that ax + by = n. If there's no solution, return None. The example given is find_solution(2,3,7) returns (2,1) because 2*2 +3*1=7. 

First, I remember that this is related to the linear Diophantine equation. The equation ax + by = n has solutions if and only if the greatest common divisor (gcd) of a and b divides n. So first step is to check if gcd(a, b) divides n. If not, return None.

But how do I find x and y once I know there's a solution? Well, the extended Euclidean algorithm can find x and y such that ax + by = gcd(a, b). Then, if n is a multiple of the gcd, I can scale those solutions accordingly.

So the plan is:

1. Compute the gcd of a and b. Let's call it g.
2. Check if n is divisible by g. If not, return None.
3. Otherwise, find x0, y0 such that ax0 + by0 = g. Then multiply x0 and y0 by (n/g) to get the solution for ax + by = n.

But how to implement the extended Euclidean algorithm?

Let me think. The extended Euclidean algorithm finds integers x and y such that ax + by = gcd(a, b). So I need to implement that.

Let me recall the steps. The standard Euclidean algorithm finds the gcd, but the extended version keeps track of coefficients. Let me think of the recursive approach. For example, for a and b, if a > b, then we can write a = q*b + r. Then, the gcd(a, b) is the same as gcd(b, r). So recursively, we can find the coefficients.

Alternatively, I can implement the extended Euclidean algorithm iteratively. Let me think of the iterative approach.

Let me write a helper function that returns (g, x, y) where g is the gcd of a and b, and x and y are coefficients such that ax + by = g.

Let me try to code that. For example, the algorithm:

def extended_gcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

Wait, that's the recursive approach. Let me test this. For example, a=2, b=3. Let's see:

extended_gcd(2,3) would call extended_gcd(3, 2%3=2). Then extended_gcd(3,2) calls extended_gcd(2, 3%2=1). Then extended_gcd(2,1) calls extended_gcd(1, 2%1=0). Then returns (1, 1, 0). Then backtracking:

For (2,1): g=1, x = y1 (which is 0), y = x1 - (2//1)*y1 = 1 - 2*0 =1. So returns (1, 0, 1). Then for (3,2): x is y1 (which is 1), y is x1 - (3//2)*y1 = 0 - 1*1 = -1. So returns (1, 1, -1). Then for (2,3): x is y1 (which is -1), y is x1 - (2//3)*y1. Wait, a//b here is 2//3=0. So y = 1 - 0*(-1) = 1. So returns (1, -1, 1). So the equation is 2*(-1) +3*(1) = -2 +3 =1. Which is correct. 

So for the example given, when a=2, b=3, and n=7. The gcd is 1, which divides 7. So the solution is x = (-1)*7 = -7, y=1*7=7. But the example expects (2,1). So that's a problem. Because the equation 2*(-7) +3*7 = -14 +21=7. But there are multiple solutions. The example returns (2,1), which is another solution. So how do we find that?

So the problem is that the extended_gcd gives one particular solution, but there are infinitely many solutions. So once we have a particular solution, we can find the general solution. But how to find a solution that satisfies the equation and possibly some constraints (like x and y being integers, but the problem doesn't specify any constraints on x and y, so any solution is acceptable as long as it exists).

Wait, the problem says to return any solution. So perhaps the example's solution is not the one given by the extended_gcd, but another one. So how do I adjust the solution to get the one that the example expects?

Let me think. Once we have a particular solution (x0, y0), all solutions can be expressed as x = x0 + k*(b/g), y = y0 -k*(a/g), where k is any integer. Because the homogeneous equation ax + by =0 has solutions multiples of (b/g, -a/g). 

So for the example, the extended_gcd gives x0=-7, y0=7. Let's compute the general solution. Since g=1, the general solution is x = -7 + 3k, y =7 -2k. For some integer k. So we need to find k such that x and y are integers. But since k can be any integer, there are infinitely many solutions. So the example's solution is (2,1). Let's see if that fits into this general solution.

Let me plug x=2 into x = -7 +3k. So 2 = -7 +3k → 3k=9 → k=3. Then y =7 -2*3=1. Which matches. So that's correct. So the example's solution is part of the general solution.

But the problem is that the extended_gcd gives a solution, but perhaps that's not the one that the example expects. However, the problem allows any solution, so as long as the function returns any valid solution, it's acceptable. So for the example, the function can return any of the possible solutions. So perhaps the code can return the solution from the extended_gcd, but scaled, and then adjusted.

But how to get the solution that the example expects? Well, perhaps the code can find any solution, and the example's solution is just one of them.

So the steps for the code:

1. Compute the gcd of a and b. Let's call it g.

2. Check if n is divisible by g. If not, return None.

3. Else, find x0, y0 such that a*x0 + b*y0 = g. Then multiply x0 and y0 by (n/g) to get x = x0*(n/g), y = y0*(n/g). This will satisfy a*x + b*y = n.

But the problem is that the extended_gcd function returns x0 and y0 such that a*x0 +b*y0 =g. So scaling them gives the solution for n.

But in the example, the code would compute x0=-1, y0=1 (from the extended_gcd for a=2, b=3). Then multiply by 7/gcd (which is 7/1=7). So x = -7, y=7. But the example expects (2,1). So the code would return (-7,7), but the example expects (2,1). So why is that?

Because the problem allows any solution. So the code can return any of them. But the assert in the example is expecting (2,1). So the code must return that. But how to make sure that the code returns that solution?

Wait, but perhaps the code is allowed to return any solution. So the example's solution is just one of many possible correct answers. So the code can return any solution. But how to make sure that the code returns a solution that is correct.

But the problem says that the function should return integers x and y that satisfy the equation. So the code can return any solution. So the example's solution is just one possible correct answer. So the code can return any of them. So perhaps the code can return the solution from the extended_gcd scaled up. But in that case, the example's test would fail unless the code returns that particular solution.

Wait, but the example given is find_solution(2,3,7) == (2,1). So the code must return that solution. But how can we make sure that the code returns that solution?

Alternatively, perhaps the code can find a solution by using the extended Euclidean algorithm and then adjusting the solution to find a particular solution. But how?

Alternatively, perhaps the code can find x and y such that ax + by = n. But how to find x and y.

Wait, maybe the code can use the extended_gcd to find x0 and y0 for the equation ax + by = g. Then, multiply x0 and y0 by (n/g) to get x and y. But that gives one solution. However, the code may return that solution, but in the example, that solution is (-7,7). Which is correct, but the example expects (2,1). So why is the example expecting that?

Because the problem says that the function can return any solution. So the assert is just one possible solution. So perhaps the code can return any solution. But the test case is expecting (2,1). So how can the code return that solution?

But the code's output may vary, but the test case is expecting that particular solution. So perhaps the code needs to find a solution that's in the same equivalence class as the example's solution.

But how? Well, perhaps the code can generate the solution by adjusting the x and y. For example, once the code finds the solution (x0, y0), it can find k such that x is positive, or some other condition. But the problem doesn't specify any constraints on x and y. So the code can return any solution.

But the example's test case is expecting (2,1). So perhaps the code needs to return that solution. But how?

Alternatively, perhaps the code can use the extended Euclidean algorithm and then find a solution that has x and y in certain ranges. For example, perhaps the code can find the solution with minimal x or y, but that's not clear.

Alternatively, maybe the code can use the extended Euclidean algorithm, then adjust the solution to get x and y. Let's think again. Let's take the example.

In the example, the solution given is (2,1). So 2*2 +3*1=7. So the code can return that. But how to find that solution?

The code can find a solution using the extended_gcd and then adjust it. Let me think. The extended_gcd returns x=-1 and y=1 for a=2, b=3, g=1. So the solution is x=-1, y=1. Multiply by 7 gives x=-7, y=7. But that's a solution. But how to get to (2,1)?

Well, the general solution is x = x0 + (b/g)*k, y = y0 - (a/g)*k. For this case, since g=1, the general solution is x = -1 +3k, y=1 -2k. So for k=3, x = -1 +9=8, y=1-6= -5. Not helpful. Wait, but the example's solution is x=2, y=1. Let's see:

2 = -1 +3k → k = (2 +1)/3 = 1. So k=1. Then y=1 -2*1 = -1. Which is not the example's solution. Wait, that's not matching. Wait, what's the general solution again?

Wait, the general solution for ax + by =n is x = x0 + (b/g)*t, y = y0 - (a/g)*t, where t is any integer. Because the homogeneous equation ax + by =0 has solutions x = (b/g)*t, y = -(a/g)*t. 

So in our example, the equation is 2x +3y =7. The particular solution is x0=-7, y0=7. Then the general solution is x = -7 +3t, y=7 -2t. Let me plug t=3: x=-7+9=2, y=7-6=1. Which matches the example. So t=3. 

So the code can return any solution, but how to find the solution that the example expects. But how to find t? Well, perhaps the code can find any t that makes x and y integers, but since t is any integer, the code can choose any t. But how to get the solution that the example expects. 

But the problem says that the function can return any solution. So the code can return the solution given by the extended_gcd scaled by n/g. But in that case, the example's test case would fail. So why is that? Because the code returns (-7,7), but the example expects (2,1). So the code would not pass the test case. 

So the code must return a solution that is acceptable. But the test case is expecting (2,1). So perhaps the code needs to find a solution with positive x and y. But how?

Alternatively, perhaps the code can find the solution using the extended_gcd and then adjust it to find a solution with minimal absolute values or something. But how to do that.

Alternatively, maybe the code can use the extended_gcd to find x and y, and then adjust them to find a solution with x and y in certain ranges. For example, in the example, the code returns x=-7 and y=7. But how to find the solution (2,1) from that.

So perhaps the code can find the solution by finding t such that x and y are integers, but how to find t. But since the code can return any solution, perhaps the code can return the first solution found, but the test case is expecting a specific solution. 

Wait, but the problem says that the function can return any solution. So the test case is just one possible solution. So in the example, the code can return (2,1), but how to make sure that the code returns that solution. 

Alternatively, perhaps the code can find the solution using the extended_gcd and then adjust the solution by adding multiples of b/g to x and subtracting multiples of a/g from y. But how to choose the right multiple. 

Alternatively, maybe the code can use the extended_gcd and then find the solution with x and y being positive. But how to do that. 

But perhaps the problem's test case is just an example, and the code can return any valid solution. So the code can return the solution found by the extended_gcd scaled up. But then the test case would fail. 

So perhaps the code needs to find a solution with x and y as per the example. 

But how? Let's think again. 

The example's solution is (2,1). Let's see what the extended_gcd returns for a=2, b=3. 

As before, the extended_gcd returns x=-1 and y=1. So scaling by 7 gives x=-7, y=7. But how to get to (2,1)?

Well, the general solution is x = -7 + 3t, y =7 -2t. So for t=3, x=2, y=1. So the code needs to find t such that x and y are integers. But how to find that t. 

But the code can't know which t to choose. So perhaps the code can find the solution with minimal x or y, but that's not straightforward. 

Alternatively, perhaps the code can find x and y in a way that x is positive and y is positive. But how?

Alternatively, perhaps the code can use the extended_gcd and then adjust the solution to find x and y. 

But perhaps the code can return any solution, and the test case is just an example. So the code can return any solution. But the test case is expecting (2,1), which is one of the possible solutions. 

So why is the test case expecting (2,1)? Because that's a valid solution. But the code can return any solution. 

But the problem says that the function should return a tuple (x, y) that satisfies ax + by =n. So the code can return any solution. 

But then why does the test case pass? Because the code returns (2,1) for that input. So the code must return that solution. 

So how to make sure that the code returns that solution. 

Wait, perhaps the code can use the extended_gcd and then adjust the solution to find the solution that has the minimal x or y. But how?

Alternatively, maybe the code can find the solution using the extended Euclidean algorithm, but then find the solution by solving for t in the general solution. 

But how to find t. 

Alternatively, perhaps the code can find the solution by using the extended_gcd, then adjust x and y to find a solution with x and y in certain ranges. 

But perhaps there's another approach. Let me think: 

Once we have the solution (x0, y0) from the extended_gcd, we can find all solutions as x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

But since the code can return any solution, perhaps the code can find the solution with x and y as small as possible. 

But how? 

Alternatively, perhaps the code can use the extended_gcd and then find the solution with x and y such that x is in the range [0, b/g) or something like that. 

But this might be complicated. 

Alternatively, perhaps the code can find x and y using the extended_gcd and then adjust them by adding multiples of b/g to x and subtracting multiples of a/g from y to find a solution that meets certain conditions. 

But how to choose the multiple. 

Alternatively, perhaps the code can use the extended_gcd and then find the solution with x and y as per the example. 

But how to find that. 

Alternatively, perhaps the code can find x and y by solving the equation ax + by =n using the extended_gcd and then adjust x and y. 

But perhaps the code can use the extended_gcd and then find x and y by multiplying by (n/g) and then adjust by adding or subtracting multiples of b/g and a/g respectively. 

But how to choose the correct multiple. 

Alternatively, perhaps the code can return the solution found by the extended_gcd scaled up. 

But then the example test case would fail. 

So why does the example test case pass? Because the code returns (2,1) for that input. 

But according to the code that uses the extended_gcd and scales, it would return (-7,7). Which is correct, but the test case expects (2,1). 

So this suggests that the code needs to find a particular solution. 

But how to find that solution. 

Alternatively, perhaps the code can use the extended_gcd, and then find the solution by adjusting the x and y. 

Let me think about the example. The extended_gcd gives x=-1, y=1. So the solution is x=-1*7 =-7, y=1*7=7. 

But the example solution is x=2, y=1. 

So the difference between x is 2 - (-7) =9. Which is 3*3. And the difference between y is 1-7 =-6 = -2*3. 

So t is 3. 

So the code can find t such that x and y are integers. 

But how to find t. 

But the code can't know which t to choose. 

But since the code is allowed to return any solution, perhaps the code can return the solution found by the extended_gcd scaled up. 

But the test case would fail. 

So perhaps the problem's test case is not the only possible solution, and the code can return any solution. 

But then why does the test case expect (2,1)? Because that's just one of the possible solutions. 

So the code needs to return any solution. 

But the test case is expecting (2,1). So perhaps the code needs to return that solution. 

But how to ensure that. 

Alternatively, perhaps the code can find x and y by using the extended_gcd and then adjust the solution to find x and y such that x is positive and y is positive. 

But how to do that. 

Let me think. For the example, the code's solution is (-7,7). So x is negative. But the example's solution has x positive. 

So perhaps the code can find the minimal positive solution. 

But how to do that. 

Well, the general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

To find x and y positive, we can solve for t. 

But for the example, x0 =-7, y0=7. 

So to find t such that x is positive and y is positive. 

For x to be positive: -7 +3t >0 → t> 7/3 → t≥3. 

For y to be positive: 7 -2t>0 → t < 7/2 → t ≤3. 

So t must be 3. 

Thus, x= -7 +3*3=2, y=7-2*3=1. 

So the code can find t such that x and y are positive. 

But how to find t in general. 

But how to do this for any a, b, n. 

Well, the code can find the general solution and then find the t that makes x and y positive. 

But how to compute that. 

Alternatively, the code can find the solution using the extended_gcd, then find t such that x and y are positive. 

But this might be complicated. 

Alternatively, perhaps the code can use the extended_gcd to find x0 and y0, then adjust them to find the solution with x and y positive. 

But how. 

But for the purposes of passing the test case, perhaps the code can return the solution found by the extended_gcd and then adjust it by adding multiples of b/g to x and subtracting multiples of a/g from y until x and y are positive. 

But this would require finding t. 

Alternatively, perhaps the code can find the solution with the smallest absolute value for x. 

But again, this requires some calculation. 

Alternatively, perhaps the code can return the solution found by the extended_gcd scaled up, and the test case is wrong. But that's unlikely. 

But the example says that find_solution(2,3,7) returns (2,1). So the code must return that. 

So perhaps the code should find the solution with x and y positive. 

But how to do that. 

Let me think. Once we have the particular solution (x0, y0), we can compute the general solution. 

For example, in the example, the particular solution is x0=-7, y0=7. 

The general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

We can find t such that x and y are positive. 

But how to find t. 

For the general case, we can solve for t such that x is positive and y is positive. 

But for the code, perhaps it's easier to find the solution with x and y in a certain range. 

Alternatively, the code can find the solution by using the extended_gcd and then adjusting the solution. 

But perhaps the code can use the following approach:

Once we have x0 and y0, the code can compute the solution as x = x0 + k*(b/g), y = y0 -k*(a/g), where k is chosen such that x and y are integers. 

But how to choose k. 

Alternatively, the code can choose k such that x is as small as possible. 

But again, this is getting complicated. 

Alternatively, perhaps the code can use the extended_gcd to find x and y, and then return the solution. 

But in the example, the code returns (-7,7), which is correct but the test case expects (2,1). So the code would fail the test case. 

So what's wrong here? 

Ah! Wait, the function returns integers x and y. The example's solution is (2,1), but the code's solution is (-7,7). Both are correct. But the test case expects (2,1), which suggests that the code should return that solution. 

So how to make the code return that solution. 

Maybe the code should find the solution with x and y positive. 

But how to do that. 

Let me think again. For the example, the general solution is x = -7 +3t, y =7 -2t. 

We want x and y to be positive. 

So for x>0: -7 +3t >0 → t>7/3 → t≥3. 

For y>0: 7-2t>0 → t <7/2 → t ≤3. 

So t must be 3. 

So x=2, y=1. 

So for the general case, the code can find t such that x and y are positive. 

But how to compute t. 

Well, the code can find t such that x is positive and y is positive. 

But how to find such a t. 

Let me think of the general case. 

Once we have x0 and y0, and the general solution x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

We need to find t such that x and y are positive. 

But this may not always be possible. For example, if a and b are both positive and n is positive, but the particular solution has x and y negative. 

But the code can find t such that x and y are positive. 

But how to find t. 

Alternatively, the code can find the minimal t that makes x and y positive. 

But how to compute that. 

Alternatively, the code can solve for t in the general solution. 

But this seems complicated. 

Alternatively, perhaps the code can use the extended_gcd and then find the solution with x and y in the range [0, ...]. 

But for the purposes of the example, perhaps the code can find the solution by adjusting the particular solution. 

But this seems like a lot of work. 

Alternatively, maybe the code can use the extended_gcd, and then adjust the solution to find x and y. 

Let me think. Let's write the code. 

First, implement the extended_gcd function. 

Then, check if n is divisible by g. 

If yes, compute x0, y0. 

Then, multiply x0 and y0 by (n/g). 

Then, return (x0, y0). 

But in the example, this returns (-7,7), which is not the expected solution. 

So how to make it return (2,1). 

But perhaps the code can adjust the solution by adding multiples of b/g to x and subtracting multiples of a/g from y. 

But how to choose the multiple. 

For example, in the example, the code can add 3 to x0 and subtract 2 from y0. 

But how to find the right multiple. 

Alternatively, the code can find the solution with x and y as small as possible. 

But how. 

Alternatively, the code can find the solution with x and y such that x is positive and y is positive. 

But how to find that. 

Alternatively, perhaps the code can use the following approach: 

Once we have x0 and y0, compute the general solution. Then find t such that x is positive and y is positive. 

But how to compute t. 

Let me think of the general solution for x and y. 

The general solution is x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

We can solve for t in the equation x = x0 + (b/g)*t >=0 and y = y0 - (a/g)*t >=0. 

But this is a system of inequalities. 

But solving this system for t is possible. 

For example, in the example, x0 = -7, y0=7. 

So for x >=0: -7 +3t >=0 → t >=7/3 ≈2.333. So t >=3. 

For y >=0: 7-2t >=0 → t <=3.5. So t <=3. 

So t must be 3. 

So the code can find t as the integer that satisfies these inequalities. 

But how to compute t in general. 

For the general case, the code can find t such that x >=0 and y >=0. 

But how to compute this t. 

Alternatively, the code can solve for t in the equation x >=0 and y >=0. 

But this requires solving for t. 

Let me think. 

Let me denote:

x = x0 + (b/g)*t >=0 → t >= -x0 * g / b 

Wait, no. Let me rearrange the inequality: 

x0 + (b/g)*t >=0 → t >= -x0 * g / b. 

Similarly, y = y0 - (a/g)*t >=0 → t <= y0 * g / a. 

But since t must be an integer, the code can find the range of t that satisfies both inequalities. 

But this requires knowing the values of x0 and y0. 

But this seems complicated. 

Alternatively, perhaps the code can find t such that x and y are as small as possible. 

But for the purposes of the example, perhaps the code can adjust the solution to find x and y positive. 

But this seems like a lot of work. 

Alternatively, perhaps the code can return the solution found by the extended_gcd and then adjust it by adding multiples of b/g to x and subtracting multiples of a/g from y until x and y are positive. 

But how to implement this. 

For example, in the example, the code has x0 = -7, y0 =7. 

We can add 3 to x0 (since b/g=3) and subtract 2 from y0 (since a/g=2). 

So t=1: x =-7+3= -4, y=7-2=5. Still x is negative. 

t=2: x=-7+6= -1, y=7-4=3. Still x negative. 

t=3: x=2, y=1. 

So the code can increment t until x is positive and y is positive. 

But how to find the right t. 

But this approach could work. 

So the code can find t such that x and y are positive. 

But how to find t. 

The code can calculate the minimum t needed to make x positive and the maximum t allowed to make y positive. 

Then, if there's an overlap, choose t in that range. 

But this requires some calculations. 

Let me try to implement this. 

Once we have x0 and y0, and the general solution:

x = x0 + (b/g)*t 

y = y0 - (a/g)*t 

We need to find t such that x >=0 and y >=0. 

So:

x >=0 → t >= ceil( (-x0 * g)/b )

Wait, no. Let me rearrange the inequality:

x = x0 + (b/g)*t >=0 → (b/g)*t >= -x0 → t >= (-x0 * g)/b 

But since t must be an integer, t >= ceil( (-x0 * g)/b ). 

Similarly, for y >=0:

y = y0 - (a/g)*t >=0 → (a/g)*t <= y0 → t <= y0 * g / a 

But since t must be an integer, t <= floor( y0 * g / a )

If there exists an integer t in the range [t_min, t_max], then choose any such t. 

For example, in the example:

x0 = -7, y0=7, g=1, a=2, b=3. 

So:

t_min = ceil( (-x0 * g)/b ) = ceil( (7*1)/3 ) = ceil(7/3) = 3 

t_max = floor( y0 * g /a ) = floor(7*1/2) = 3. 

So t must be 3. 

So the code can choose t=3, which gives x=2, y=1. 

So this approach would work. 

But how to implement this in code. 

But what if there is no such t? For example, if the inequalities don't overlap. 

But since the equation has a solution, there must be at least one t. 

But how to calculate t_min and t_max. 

Let me think about the code. 

Once we have x0 and y0, and g, a, b:

t_min = ceil( (-x0 * g) / b )

t_max = floor( y0 * g / a )

But since a and b are positive, and g is positive. 

But how to calculate this in Python. 

But wait, in the general case, a and b can be positive or negative? Or are they assumed to be positive? 

The problem says that a and b are integers. But the function is supposed to find x and y for any integers a and b. 

But the extended_gcd function works for any integers. 

But for the code, perhaps the code should handle negative a and b. 

But for now, let's assume that a and b are positive. 

But the problem statement doesn't specify, so the code must handle any integers. 

But perhaps the code can handle it by taking absolute values? Or not. 

But this is getting complicated. 

But for the purposes of the example, let's proceed. 

So, the code can calculate t_min and t_max as follows:

t_min = ceil( (-x0 * g) / b )

t_max = floor( y0 * g / a )

But how to compute this in Python. 

But in Python, the math.ceil and math.floor functions can be used. 

But since x0, y0, g, a, b are integers, we need to calculate these values. 

But for example, in the case where a and b are positive. 

So, the code can compute t_min and t_max. 

If t_min <= t_max, then choose any t in this range. 

But how to choose t. 

For example, choose t = t_min. 

But how to compute this. 

So, the code can compute t_min and t_max, and choose t = t_min. 

But in the example, this would give t=3, which is correct. 

So, the code can proceed as follows:

After finding x0 and y0, compute t_min and t_max. 

If there's an overlap, choose t = t_min. 

Then compute x = x0 + (b/g)*t, y = y0 - (a/g)*t. 

This would give x and y positive. 

But how to handle cases where a or b is negative. 

This might get complicated. 

But for the purposes of the example, this approach would work. 

So, putting it all together:

The code:

Implement extended_gcd to get x0 and y0. 

Check if n is divisible by g. 

If not, return None. 

Else, compute t_min and t_max as above. 

Choose t = t_min. 

Then compute x and y. 

But how to handle the case when a or b is zero? 

But the problem says that a and b are integers. So if a is zero, then the equation becomes by =n. So if b divides n, then y =n/b, x can be any integer. Similarly for b=0. 

But the code needs to handle those cases. 

But for now, let's proceed with the example. 

So, the code for the example:

a=2, b=3, n=7. 

g=1, x0=-1, y0=1. 

Wait, no. Wait, the extended_gcd(a=2, b=3) returns x0=-1, y0=1, because 2*(-1) +3*1 =-2+3=1. 

Then, when scaling by n/g=7, x0 = -1*7 =-7, y0=1*7=7. 

So, x0 =-7, y0=7. 

Then, to find t_min and t_max:

t_min = ceil( (-x0 * g)/b ) = ceil( (7 * 1)/3 ) = ceil(7/3) = 3. 

t_max = floor( y0 * g /a ) = floor(7*1 /2 ) = 3. 

So t=3. 

x = -7 + 3*3 =2, y=7 - 2*3=1. 

Which is the desired solution. 

So this approach works. 

So the code can proceed with this logic. 

Now, let's think
```

</details>

**Code that ran:**

```python
import math

def find_solution(a, b, n):
    # Compute the gcd of a and b
    g = math.gcd(a, b)

    # If n is not divisible by the gcd, no solution exists
    if n % g != 0:
        return None

    # Helper function for extended Euclidean algorithm
    def extended_gcd(a, b):
        if b == 0:
            return (a, 1, 0)
        else:
            g, x1, y1 = extended_gcd(b, a % b)
            x = y1
            y = x1 - (a // b) * y1
            return (g, x, y)

    # Find one particular solution to ax + by = g
    g_val, x0, y0 = extended_gcd(a, b)

    # Scale the solution to match the target n
    scale = n // g_val
    x = x0 * scale
    y = y0 * scale

    # Adjust t to ensure x and y are positive
    # General form: x = x + (b/g)*t, y = y - (a/g)*t
    # Find t such that x and y are positive
    # Solve for t_min and t_max
    b_over_g = b // g_val
    a_over_g = a // g_val

    # Calculate t_min and t_max
    t_min = math.ceil((-x) / b_over_g)
    t_max = math.floor(y / a_over_g)

    # Choose t within the valid range
    if t_min > t_max:
        return None  # No solution in positive integers
    t = t_min

    # Adjust x and y
    x += b_over_g * t
    y -= a_over_g * t

    return (x, y)
```

**Visible-test report:**

```text
PASS    assert find_solution(2, 3, 7) == (2, 1)
1 of 1 visible tests passed
```
