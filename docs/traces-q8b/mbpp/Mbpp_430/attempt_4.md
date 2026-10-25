# Mbpp/430, attempt 4

3 rounds; no visible pass after round 3; final code on the hidden tests: ❌ fail. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/430/a4/r1`)

Visible tests: **fail**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 947.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called parabola_directrix that takes three parameters, probably the coefficients of a parabola equation. The assertion given is that when the function is called with 5,3,2, it returns -198. Let me think about how to approach this.

First, I should recall the standard form of a parabola and its directrix. Wait, the problem might be referring to a parabola in the form of y = ax² + bx + c. But wait, the directrix of a parabola depends on its orientation. For a vertical parabola (opening up or down), the directrix is a horizontal line. For a horizontal parabola (opening left or right), the directrix is vertical. 

But the given assertion is for inputs 5,3,2. Let me think about what those parameters represent. Maybe the function is given the coefficients of the parabola in the form y = ax² + bx + c. Or perhaps it's a different form. Wait, the standard form for a vertical parabola is y = a(x - h)^2 + k, where the vertex is (h,k). The directrix for this is y = k - 1/(4a). But if the equation is in the general form y = ax² + bx + c, then I need to convert it to vertex form to find the directrix.

Alternatively, maybe the function is given parameters a, b, c for the equation of a parabola in the form x = ay² + by + c, which would be a horizontal parabola. But then the directrix would be different. But the assertion given is that when the inputs are 5,3,2, the output is -198. Let me try to compute that.

Let me think: For a vertical parabola, the directrix is y = k - 1/(4a). Let me see. Suppose the equation is y = ax² + bx + c. Then the vertex is at x = -b/(2a). Let me compute the vertex's y-coordinate. Then the directrix is y = k - 1/(4a), where k is the y-coordinate of the vertex. 

Let me compute for the given example: 5,3,2. Wait, perhaps the parameters are a, b, c for the equation y = ax² + bx + c. Let's take a=5, b=3, c=2. Then the vertex's x-coordinate is -b/(2a) = -3/(10) = -0.3. The y-coordinate is c - b²/(4a). Let me compute that. c is 2, so 2 - (9)/(4*5) = 2 - 9/20 = (40 -9)/20 = 31/20 = 1.55. Then the directrix is y = k - 1/(4a). So 1.55 - 1/(20) = 1.55 - 0.05 = 1.5. But that's 31/20 - 1/20 = 30/20 = 3/2. So the directrix is y = 3/2. But the assertion says the function returns -198, which is way off. So that can't be the case. Therefore, perhaps the parameters are not for a vertical parabola.

Alternatively, maybe the function is for a horizontal parabola. For example, the equation x = ay² + by + c. Then the directrix would be a vertical line. Let me think. For a horizontal parabola in the form x = a(y - k)^2 + h, the directrix is x = h - 1/(4a). So if the equation is x = ay² + by + c, then we need to find the vertex form. Let me try with the given example: a=5, b=3, c=2. So the equation is x = 5y² +3y +2. Let me find the vertex. The vertex is at y = -b/(2a) = -3/(2*5) = -3/10. Then substituting back into x: x = 5*( (-3/10)^2 ) + 3*(-3/10) + 2. Let me compute that:

(-3/10)^2 = 9/100. Multiply by 5: 9/20. Then 3*(-3/10) = -9/10. So adding 9/20 -9/10 + 2. Let me convert to 20 denominator. 9/20 - 18/20 + 40/20 = (9-18+40)/20 = 31/20. So the vertex is at (31/20, -3/10). The directrix is x = h - 1/(4a). Here, h is 31/20, and a is 5. So 31/20 - 1/(4*5) = 31/20 - 1/20 = 30/20 = 3/2. So the directrix is x=3/2. But again, the assertion is that the function returns -198, which doesn't match. So this approach is not correct.

Hmm. So perhaps the parameters are not for the standard parabola equations. Maybe the function is given different parameters. Let me think again. The problem says "find the directrix of a parabola" and the assertion is parabola_directrix(5,3,2) == -198. So what could be the parameters?

Alternatively, perhaps the function is given the coefficients of the parabola in the form y = ax² + bx + c, but the directrix is calculated in a different way. Wait, perhaps the problem is referring to a parabola in the form of x^2 = 4py, where the directrix is x = -p. But how does that relate to the given parameters?

Alternatively, maybe the parameters are for the general equation of a parabola. Let me think. For example, a parabola can be represented as (y - k)^2 = 4p(x - h), which opens to the right. The directrix is x = h - p. Or (x - h)^2 = 4p(y - k), which opens upward, with directrix y = k - p. 

But how to get from the coefficients to the directrix? Let me think. Let me suppose that the function is given the coefficients a, b, c for the equation of a parabola in the form y = ax² + bx + c. Then, perhaps the directrix is calculated using the formula. But earlier calculation didn't match the assertion. 

Wait, the assertion says that when the inputs are 5,3,2, the output is -198. Let me think about what calculation would give that. Let's suppose that the formula is something like - (something involving a, b, c). Let me think. Let me try to find a formula that when a=5, b=3, c=2, gives -198.

Let me think about the formula for the directrix. For a vertical parabola (y = ax² + bx + c), the directrix is y = k - 1/(4a), where k is the y-coordinate of the vertex. The vertex's y-coordinate is (4ac - b²)/(4a). So the directrix is (4ac - b²)/(4a) - 1/(4a) = (4ac - b² -1)/(4a). 

Let me compute that for a=5, b=3, c=2. 

Numerator: 4*5*2 - 3^2 -1 = 40 -9 -1 = 30. Denominator: 4*5 = 20. So 30/20 = 3/2. Which is 1.5, not -198. So that's not matching. 

Hmm. What if the formula is different? Maybe the parabola is in the form of x = ay² + by + c. Then the directrix is x = h - 1/(4a), where h is the x-coordinate of the vertex. Let me compute that. For x = 5y² + 3y + 2. The vertex y-coordinate is -b/(2a) = -3/(10). Then the x-coordinate is h = 5*( (-3/10)^2 ) + 3*(-3/10) + 2. As before, that's 5*(9/100) - 9/10 + 2 = 9/20 - 9/10 + 2 = 9/20 - 18/20 + 40/20 = 31/20. Then the directrix is x = h - 1/(4a) = 31/20 - 1/(20) = 30/20 = 3/2. Again, not matching.

So maybe the parameters are not for the standard equations. Maybe the function is given the coefficients of the parabola in a different form. For example, maybe the equation is given in the form of y = a(x - p)^2 + q, where the directrix is y = q - 1/(4a). But then again, the calculation would not give -198. 

Alternatively, perhaps the problem is not about a vertical or horizontal parabola, but a different orientation. But that's more complicated. 

Alternatively, maybe the function is given parameters for a parabola in the general form. For example, the general equation of a parabola can be written as Ax² + Bxy + Cy² + Dx + Ey + F = 0. But that's more complicated and requires solving for the directrix. But that's probably beyond the scope of this problem. 

Alternatively, perhaps the problem is referring to the directrix of a parabola defined by three points. But that would require more parameters. 

Wait, the assertion is that parabola_directrix(5,3,2) returns -198. Let me think: what if the formula for the directrix is something like - (some expression). Let me think of the example: 5,3,2 gives -198. Let me try to find a formula that would produce this. For example, if the formula is - ( (something) ), let's see. Let me think: 5*3*2 = 30. Not 198. 5*3^2*2 = 5*9*2=90. 5^2*3*2= 25*6=150. Not 198. 

Alternatively, perhaps the formula is -( (some combination) ). Let me think of 5*3*2 = 30, but 198 is 30*6.6. Not sure. 

Alternatively, maybe the parameters are for a different form. Let me think. Suppose the function is given the parameters a, b, c for the equation of a parabola in the form y = ax² + bx + c. Then, the directrix is y = (some value). But how to get -198 from that. 

Alternatively, perhaps the function is for the directrix of a parabola in the form of x = ay² + by + c. Then, the directrix is x = h - 1/(4a), where h is the x-coordinate of the vertex. But earlier calculation for a=5, b=3, c=2 gives h = 31/20, and the directrix is 31/20 - 1/(20) = 30/20 = 3/2. 

Hmm. Not matching. 

Alternatively, maybe the function is given the parameters for the standard form of a parabola that opens to the left or right, but with different coefficients. For example, the standard form is (y - k)^2 = 4p(x - h). The directrix is x = h - p. So if the equation is given as (y - k)^2 = 4p(x - h), then the directrix is x = h - p. But how to get this from the parameters. 

But how would the parameters be passed? For example, if the function is given a, b, c such that the equation is (y - k)^2 = 4p(x - h), but I don't see how to get a, b, c from that. 

Alternatively, perhaps the parameters are for a different form. Let me think again. Maybe the problem is not about a standard parabola, but a different one. 

Alternatively, maybe the problem is referring to the directrix of a parabola that is defined by the focus and the directrix. But that seems not helpful. 

Alternatively, perhaps the function is given the coefficients of a quadratic equation in x, such as y = ax^2 + bx + c, and the directrix is calculated as something else. Let me think again. 

Wait, perhaps there's a mistake in my previous calculation. Let me re-calculate the directrix for the given example. 

Let me re-derive the formula for the directrix. 

For a parabola in the form y = ax² + bx + c, the vertex is at x = -b/(2a). The y-coordinate of the vertex is y = a*(-b/(2a))² + b*(-b/(2a)) + c. Let me compute that:

= a*(b²/(4a²)) - b²/(2a) + c 
= b²/(4a) - b²/(2a) + c 
= -b²/(4a) + c 
= c - b²/(4a)

So the vertex is at (h, k) where h = -b/(2a), k = c - b²/(4a). 

The standard form of a parabola is (x - h)^2 = 4p(y - k), where p is the distance from the vertex to the focus (and also from the vertex to the directrix, but in the opposite direction). 

In this case, the parabola opens upwards if a > 0. The directrix is y = k - p. 

But for the standard form, the equation is y = ax² + bx + c. Let me relate this to the standard form. 

The standard form (x - h)^2 = 4p(y - k) can be expanded as x² - 2hx + h² = 4p y - 4pk. Rearranging gives x² - 2hx + h² - 4pk = 4p y. Then, solving for y: y = (1/(4p))x² - (2h)/(4p) x + (h² - 4pk)/(4p). 

Comparing this to y = ax² + bx + c, we can see that:

a = 1/(4p) => p = 1/(4a)
b = -2h/(4p) = -h/(2p)
c = (h² - 4pk)/(4p)

But since p = 1/(4a), substituting:

b = -h/(2*(1/(4a))) ) = -h/( (1/(2a)) ) = -h * 2a => h = -b/(2a), which matches the earlier result.

And for the directrix, it's y = k - p. 

But k is the y-coordinate of the vertex, which is c - b²/(4a). 

So the directrix is y = k - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

So for the given example, a=5, b=3, c=2. 

So substituting into this formula:

directrix_y = 2 - (3^2 +1)/(4*5) = 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. Which is 3/2. Still not matching the assertion. 

So this suggests that the function isn't for this case. 

But the assertion says that the function returns -198. So what's the formula that would give that?

Let me think of the formula for the directrix in terms of a, b, c. Maybe I'm missing something. Let me think of other possibilities.

Alternatively, perhaps the function is given parameters a, b, c for the equation of the parabola in the form of x = ay^2 + by + c. Then, the directrix is x = h - 1/(4a), where h is the x-coordinate of the vertex. 

Let me compute this for a=5, b=3, c=2. 

The vertex y-coordinate is -b/(2a) = -3/(10) = -0.3. The x-coordinate of the vertex is 5*(-0.3)^2 + 3*(-0.3) + 2. Let me compute:

5*(0.09) = 0.45. 3*(-0.3) = -0.9. So total is 0.45 -0.9 + 2 = 1.55. 

Then the directrix is x = 1.55 - 1/(4*5) = 1.55 - 0.05 = 1.5. Again, 3/2. 

Still not matching. 

Hmm. What if the parameters are for the equation of a parabola in the form y = ax^2 + bx + c, but the directrix is calculated as something else. Like, maybe the formula is - (some expression). Let me think. 

Wait, maybe the function is given the coefficients of a parabola in the form of y = a(x - p)^2 + q, and the directrix is y = q - 1/(4a). But that's the same as earlier. 

Alternatively, maybe the parameters are not for the standard parabola but for the general conic section. But that would require more parameters. 

Alternatively, perhaps the problem is not about a parabola in the standard orientation, but for a different orientation. For example, a parabola that opens to the left or right, but the parameters are given differently. 

Alternatively, perhaps the function is given the parameters a, b, c for the equation of a parabola in the form y^2 = 4ax. In this case, the directrix is x = -a. But then, how do the parameters relate to this? For example, if the equation is y^2 = 4a x, then the directrix is x = -a. But if the function is given parameters a, b, c, perhaps it's not applicable. 

Alternatively, maybe the function is given the parameters for the equation of a parabola in the form (x - h)^2 = 4p(y - k), and the directrix is y = k - p. But how to get h, k, and p from the given a, b, c. 

Alternatively, maybe the parameters are a, b, c for the equation of the parabola in the form y = ax^2 + bx + c, and the directrix is calculated as - (some expression involving a, b, c). Let me think of the example. For the given assertion, the output is -198. Let me think of a formula that would give that. 

For example, if the formula is - ( (b^2 - 4ac) * something ). Let me try. 

For the example a=5, b=3, c=2. 

b^2 -4ac = 9 - 40 = -31. 

If I multiply by some number, say 6.4, I get -31 * 6.4 = -198.4, which is close to -198. But that's not exact. 

Wait, 31 * 6.4 = 198.4. So if the formula is -( (b^2 -4ac) * something ), perhaps. 

But why would that be the case? 

Alternatively, perhaps the directrix is calculated as something like -( (b^2 -4ac) * ... ). 

But I'm not sure. 

Alternatively, maybe the function is not about the directrix of a standard parabola, but about something else. 

Alternatively, perhaps the function is given the parameters a, b, c for the equation of a parabola in the form y = ax^2 + bx + c, and the directrix is calculated as -( (b^2 - 4ac) ) / (4a) or something similar. 

Wait, let me compute for the example: 

If the formula is -(b^2 - 4ac) / (4a). 

For a=5, b=3, c=2: 

b^2 -4ac = 9 -40 = -31. 

So -( -31 ) / (20) = 31/20 = 1.55. Not matching. 

Alternatively, -(b^2 -4ac) / (a). 

That would be 31/5 = 6.2. No. 

Hmm. 

Alternatively, maybe the directrix is calculated as something like - ( (4ac - b^2) / (4a) ) - something. 

Wait, earlier calculation for the directrix was y = k - 1/(4a), where k = c - b²/(4a). So substituting, it's c - b²/(4a) - 1/(4a) = c - (b² + 1)/(4a). 

So for the example, this is 2 - (9 +1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. 

But the assertion is that the function returns -198. 

So perhaps the function is not for a standard parabola, but for a different form. 

Alternatively, perhaps the problem is referring to the directrix of a parabola defined by three points. But that would require more parameters. 

Alternatively, maybe the function is given the coefficients of the parabola in the form of x = ay^2 + by + c, and the directrix is calculated as x = something. But earlier calculation for a=5, b=3, c=2 gives 3/2, not -198. 

But maybe I'm missing something. Let me think about the directrix formula again. 

For a parabola that opens to the right, the standard form is (y - k)^2 = 4p(x - h). The directrix is x = h - p. 

If I can express the equation x = ay^2 + by + c in this form, then I can find the directrix. 

Let me try to rewrite x = 5y^2 + 3y + 2 into the standard form. 

Rearranging: 5y^2 + 3y + (2 - x) = 0. 

This is a quadratic in y. Let me complete the square. 

5y^2 + 3y = x - 2 

Divide both sides by 5: 

y^2 + (3/5)y = (x-2)/5 

Complete the square for y: 

y^2 + (3/5)y + (3/(10))^2 = (x-2)/5 + (3/10)^2 

So, y^2 + (3/5)y + 9/100 = (x-2)/5 + 9/100 

Left side is (y + 3/10)^2. 

So, (y + 3/10)^2 = (x-2)/5 + 9/100 

Multiply both sides by 100 to eliminate denominators: 

100(y + 3/10)^2 = 20(x-2) + 9 

=> 100(y + 3/10)^2 = 20x - 40 +9 = 20x -31 

Rearranged: 

(y + 3/10)^2 = (20x -31)/100 

Which can be written as (y + 3/10)^2 = (1/50)(20x -31) 

But this is (y - k)^2 = 4p(x - h). Let me compare. 

Let me write it as (y + 3/10)^2 = (1/50)(20x -31) 

=> (y + 3/10)^2 = (20/50)(x - 31/20) 

Simplify: (y + 3/10)^2 = (2/5)(x - 31/20) 

So comparing to (y - k)^2 = 4p(x - h), we have 4p = 2/5 => p = 1/10. 

The standard form is (y - k)^2 = 4p(x - h), so the directrix is x = h - p. 

In this case, h is 31/20, and p is 1/10. So the directrix is x = 31/20 - 1/10 = 31/20 - 2/20 = 29/20 = 1.45. Still not matching -198. 

Hmm. I'm stuck. Let me think of another approach. 

The assertion says that when the inputs are 5, 3, 2, the output is -198. So I need to find a formula that for a=5, b=3, c=2, gives -198. 

Let me try to think of possible formulas. 

Let me think of the formula as something involving the coefficients. For example, perhaps the directrix is calculated as - ( (b^2 - 4ac) * something ). 

Let me compute b^2 - 4ac for a=5, b=3, c=2: 9 - 40 = -31. 

If I multiply by 6.4, I get -31 * 6.4 = -198.4, which is close to -198. So maybe the formula is -(b^2 -4ac) * (some factor). 

But why would that be the case? 

Alternatively, maybe the formula is -( (b^2 - 4ac) * something else). 

Let me think: 31 * 6 = 186, 31 * 6.4 = 198.4. So if the formula is -( (b^2 -4ac) * 6.4 ), but how to get that from the parameters. 

Alternatively, perhaps the formula is something like - ( (b^2 -4ac) * (a + b + c) ). 

Let me compute for the example: 

b^2 -4ac = -31. a + b + c = 5 +3 +2 = 10. So -(-31)*10 = 310. Not -198. 

Hmm. 

Alternatively, maybe it's - ( (b^2 - 4ac) * (some expression) ). Let me think. 

Let me think of the example: the desired output is -198. So for a=5, b=3, c=2, we need to find a formula that gives -198. 

Let me try to find a combination of a, b, c that equals -198. 

Let me think: 5 * 3 * 2 = 30. 5 * 3^2 * 2 = 90. 5^2 * 3 * 2 = 150. 5^3 * 3 * 2 = 750. Not helpful. 

What about 5*3*2* something. 30 * something = -198. So something is -6.6. 

Not sure. 

Alternatively, maybe the formula is -( (b^2 - 4ac) * (a + b) ). 

For the example, b^2 -4ac = -31, a + b = 8. So -(-31)*8 = 248. Not -198. 

Alternatively, -( (b^2 - 4ac) * (a - b) ). 

a - b = 5-3=2. So -(-31)*2 = 62. No. 

Hmm. 

Alternatively, maybe the directrix is calculated as -( (b^2 - 4ac) * (something involving a) ). 

Let me think: 5 * 3 * 2 = 30. 30 * 6.6 = 198. So if the formula is -( (b^2 -4ac) * (something) ). 

But how to get that something. 

Alternatively, maybe the function is for a parabola in the form of y = ax^2 + bx + c, and the directrix is calculated as something like - (4ac - b^2) / (4a). 

Wait, for the example, 4ac - b^2 is 4*5*2 - 3^2 = 40 -9 = 31. Divided by 4a is 31/(20) = 1.55. So -1.55 is not -198. 

Alternatively, maybe the formula is -( (4ac - b^2) * something ). 

For example, if the formula is -( (4ac - b^2) * (a + b + c) ), then for the example: 4ac -b^2 = 31, a+b+c=10, so -31*10 = -310. Not -198. 

Hmm. 

Alternatively, maybe the formula is -( (b^2 + 4ac) * something ). 

For the example, b^2 + 4ac = 9 +40 = 49. 49 * something = 198. So something is 198/49 ≈ 4.04. Not sure. 

Alternatively, maybe it's a different approach. Let's think about the directrix of a parabola in terms of its focus and directrix. But I don't see how that helps. 

Alternatively, perhaps the function is not about a parabola in the standard form, but about a different type of problem. For example, perhaps the parameters are for a parabola defined by its focus and directrix, but that would require more parameters. 

Alternatively, maybe the problem is a trick question, and the directrix is calculated as - (some value). For example, if the function is given a, b, c, and the directrix is calculated as - ( (b^2 - 4ac) / (4a) ) * something. 

Wait, let's try to think of the example. If the desired output is -198, and the input is a=5, b=3, c=2. Let me try to find a formula that gives -198. 

Let me think of 5 * 3 * 2 = 30. 30 * 6.6 = 198. So if the formula is - ( (a * b * c) * 6.6 ). But why would that be? 

Alternatively, maybe the formula is - ( (b^2 - 4ac) * 6.6 ). For the example, it's - ( -31 * 6.6 ) = 204.6, which is not -198. 

Alternatively, maybe it's - ( (b^2 -4ac) * 6.4 ). For the example, it's - ( -31 * 6.4 ) = 198.4, which is close to 198. Perhaps the problem uses integer division or rounding. 

But why would that be the case? 

Alternatively, maybe the formula is - ( (b^2 -4ac) * (something) ). For example, if the formula is - ( (b^2 -4ac) * (a + b + c) ) / something. 

Let me try: (b^2 -4ac) = -31, a + b + c = 10. So -31 * 10 = -310. If I divide by something, like 1.666..., it would give -186. But not 198. 

Alternatively, maybe it's (4ac - b^2) * something. 

For the example, 4ac -b^2 = 31. If I multiply by 6.4, I get 31 * 6.4 = 198.4. So if the formula is - (4ac - b^2) * 6.4, then it would be -198.4, which rounds to -198. 

But why would that be the case? 

Alternatively, perhaps the directrix is calculated as - ( (4ac - b^2) * (some coefficient) ). 

But where would this coefficient come from? 

Alternatively, perhaps the problem is not about the standard directrix, but about something else, like the directrix of a parabola in a different form. 

Alternatively, perhaps the function is for a parabola defined by the equation x = a(y - k)^2 + h, and the directrix is x = h - 1/(4a). But how does that relate to the given parameters? 

If the function is given a, b, c, perhaps the parameters are a, b, c for the equation x = a(y - b)^2 + c. In this case, the directrix is x = c - 1/(4a). For example, if a=5, b=3, c=2, then directrix is 2 - 1/(20) = 1.95. Not matching. 

But the assertion is -198. 

Hmm. I'm stuck. Let me think of another approach. 

Maybe the function is given the coefficients of the parabola in the form of y = ax^2 + bx + c, and the directrix is calculated as - ( (4ac - b^2) / (4a) ) - something. 

Wait, for the example, 4ac - b^2 is 31. Divided by 4a is 31/20 = 1.55. If I multiply by 126, I get 1.55 * 126 = 195.3. Not 198. 

Alternatively, maybe the formula is - ( (4ac - b^2) * (something) ). 

Let me try to think of the example: 4ac -b^2 = 31. 31 * 6.4 = 198.4, which is close to 198. So if the formula is - ( (4ac - b^2) * 6.4 ), then it would be -198.4, which rounds to -198. 

But why would the formula be like that? 

Maybe the problem is not about the standard directrix, but about something else. For example, the directrix of a parabola defined by the equation y = ax^2 + bx + c, but with a different definition. 

Alternatively, perhaps the problem is a trick, and the directrix is calculated as - ( (b^2 -4ac) * (some expression) ). 

But without knowing the correct formula, it's hard to proceed. 

Alternatively, maybe the function is for a parabola in the form of y = a(x - h)^2 + k, and the directrix is y = k - 1/(4a). But how to get from the parameters. 

Wait, let's assume that the function is given a, b, c for the equation y = a(x - h)^2 + k, and the directrix is y = k - 1/(4a). But how to get h and k from a, b, c? 

In this case, the equation is y = a(x - h)^2 + k. Expanding, y = a x^2 - 2a h x + a h^2 + k. So comparing to y = ax^2 + bx + c, we have b = -2a h => h = -b/(2a), and c = a h^2 + k => k = c - a h^2. 

Then, the directrix is y = k - 1/(4a) = c - a h^2 - 1/(4a). 

Substituting h = -b/(2a), we get h^2 = b^
```

</details>

**Code that ran:**

```python
def parabola_directrix(a, b, c):
    return -(b**2 - 4*a*c) / (4*a)
```

**Visible-test report:**

```text
FAIL    assert parabola_directrix(5,3,2)==-198
        AssertionError: assertion failed
0 of 1 visible tests passed
```

## Round 2 (`Mbpp/430/a4/r2`)

Visible tests: **fail**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 1295.

<details><summary>Thinking</summary>

```text
Okay, let's see. The user wants me to find the correct formula for the directrix of a parabola given the coefficients a, b, c. The previous code didn't work for the test case parabola_directrix(5,3,2) which should return -198. Let me think about how to approach this.

Wait, the standard form of a parabola is usually given as y = ax² + bx + c. But the directrix of a parabola depends on its orientation. For a vertical parabola (which opens up or down), the directrix is a horizontal line. The formula for the directrix in this case is y = k - p, where p is the focal length. Alternatively, I remember that the directrix can be calculated using the formula derived from the vertex form of the parabola.

Let me recall the formula. For a parabola in the form y = ax² + bx + c, the vertex is at (-b/(2a), f(-b/(2a))). The directrix is located at a distance of 1/(4a) from the vertex. Wait, no, maybe I need to think about the standard form. Let me think again.

The standard form of a parabola that opens up or down is (x - h)^2 = 4p(y - k), where (h, k) is the vertex. The directrix is y = k - p. The focal length p is 1/(4a) if the equation is in the form y = ax² + bx + c. Wait, maybe I need to derive it.

Alternatively, the formula for the directrix of a parabola given in general form (y = ax² + bx + c) can be found by using the formula for the directrix. Let me check the formula.

I think the correct formula for the directrix of a parabola y = ax² + bx + c is y = c - (b² + 1)/(4a). Wait, maybe not. Let me think again. Let me derive it.

The vertex form of a parabola is y = a(x - h)^2 + k. The directrix is y = k - 1/(4a) if a is positive. But when we expand this to the standard form, we can find the relationship between the coefficients.

Let me expand the vertex form. Let's say the vertex is (h, k). Then the equation is y = a(x - h)^2 + k. Expanding this gives y = a(x² - 2hx + h²) + k = ax² - 2ahx + ah² + k. Comparing this to y = ax² + bx + c, we have b = -2ah, and c = ah² + k. 

The directrix is y = k - 1/(4a). Let's express this in terms of a, b, c. From b = -2ah, h = -b/(2a). Then, substituting into c = ah² + k, we get k = c - ah². So substituting h:

k = c - a*(b²/(4a²)) = c - b²/(4a). 

So the directrix is y = k - 1/(4a) = [c - b²/(4a)] - 1/(4a) = c - (b² + 1)/(4a). Wait, but that would be the case if the parabola is in the form y = a(x - h)^2 + k. But maybe I made a mistake here.

Wait, the standard form for a vertical parabola is (x - h)^2 = 4p(y - k). The directrix is y = k - p. The focal length p is 1/(4a) if the equation is written as y = ax² + bx + c. Wait, let me think again. Let me take the standard form (x - h)^2 = 4p(y - k). Expanding this gives x² - 2hx + h² = 4py - 4pk. Rearranged as x² - 2hx + h² - 4py + 4pk = 0. Which can be written as y = (1/(4p))x² - (h/(2p))x + (h²/(4p) + k). Comparing this with y = ax² + bx + c, we can see that a = 1/(4p), so p = 1/(4a). Then, the directrix is y = k - p. 

But from the equation, the vertex is (h, k). So in terms of the coefficients, we can find k. Let me see. Let's take the equation y = ax² + bx + c. The vertex is at x = -b/(2a). So substituting into the equation, the y-coordinate of the vertex is y = a*(-b/(2a))² + b*(-b/(2a)) + c = a*(b²/(4a²)) - b²/(2a) + c = b²/(4a) - b²/(2a) + c = -b²/(4a) + c. So k = c - b²/(4a). 

Then, the directrix is y = k - p. Since p = 1/(4a), substituting gives y = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

Wait, but that would mean the formula for the directrix is y = c - (b² + 1)/(4a). But let's test this with the given test case. 

The test case is a=5, b=3, c=2. Let's compute the directrix using this formula. 

So, substituting into the formula: 

directrix = 2 - (3² + 1)/(4*5) = 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. But the expected result is -198. That's way off. So clearly, my formula is wrong. 

Wait, that's a problem. So my previous approach must have an error. Let me re-examine.

Wait, maybe the formula for the directrix is different. Let me check another approach. 

Alternatively, the directrix of a parabola given by y = ax² + bx + c can be found using the formula y = (c - (b²/(4a)) ) - (1/(4a)) ? Or perhaps I made a mistake in the derivation. 

Wait, the standard form of the parabola is (x - h)^2 = 4p(y - k). The directrix is y = k - p. 

But in the equation y = ax² + bx + c, the coefficient a is 1/(4p), so p = 1/(4a). 

The vertex (h, k) is at x = -b/(2a), and y = k = c - b²/(4a) as before. 

So the directrix is y = k - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

But when I plug in a=5, b=3, c=2, this gives 2 - (9 + 1)/(20) = 2 - 10/20 = 2 - 0.5 = 1.5. Which is not -198. So clearly, this formula is incorrect. 

But the test case says that parabola_directrix(5,3,2) should return -198. So there's a mistake in my understanding of the formula. 

Wait, maybe the formula is different. Let me think again. Maybe I'm using the wrong formula. 

Alternatively, perhaps the directrix is given by y = (b² - 4ac) / (4a) - something. 

Alternatively, perhaps the user is referring to a different form of the parabola. For example, maybe the parabola is given in the form of x = ay² + by + c, which is a horizontal parabola. In that case, the directrix would be different. 

Let me check. For example, if the parabola is x = ay² + by + c, then the directrix is vertical. 

But the original problem's test case is parabola_directrix(5,3,2) returning -198. Let me compute what that would imply. 

If the formula is returning -198 for a=5, b=3, c=2. Let me think: 

If the directrix is given by some formula involving a, b, c. Let's suppose that the formula is something like (b² - 4ac)/(4a) or similar. 

Let me compute (b² - 4ac) / (4a) for a=5, b=3, c=2. 

b² -4ac = 9 - 4*5*2 = 9 - 40 = -31. Divided by 4a is -31/(20) = -1.55. Not -198. 

Alternatively, maybe the formula is -(b² - 4ac) / (4a). For the same numbers: -( -31 ) / 20 = 31/20 = 1.55. Still not matching. 

Wait, the original code was returning -(b² -4ac)/(4a). Which for the test case gives -(9 - 40)/20 = -(-31)/20 = 31/20 = 1.55. Which is not -198. 

But the test case expects -198. So clearly, the formula is different. 

So perhaps the problem is not about a vertical parabola, but a horizontal one? Let's think. 

If the parabola is in the form y² = 4ax, then the directrix is x = -a. But that's for a standard parabola. 

But how to get the directrix for a general parabola given in the form y = ax² + bx + c. 

Alternatively, maybe the problem is not about the standard parabola, but about a different form. 

Wait, maybe the user is referring to the directrix of a parabola given in the form of a general quadratic equation. For example, maybe the parabola is given in the form of Ax² + Bxy + Cy² + Dx + Ey + F = 0, but that's more complicated. 

Alternatively, perhaps the problem is about a parabola in the form of x = ay² + by + c. Let me check that. 

For example, if the equation is x = ay² + by + c, then the directrix is a vertical line. Let me find the formula for that. 

The standard form for a horizontal parabola is (y - k)^2 = 4p(x - h). The directrix is x = h - p. 

Expanding this gives y² - 2ky + k² = 4p x - 4p h. Rearranged to y² - 2ky + k² -4p x +4p h = 0. 

Which can be written as x = (1/(4p))y² - (k/(2p))y + (k²/(4p) + h). 

Comparing with x = a y² + b y + c, we have a = 1/(4p), so p = 1/(4a). The vertex is at (h, k). The directrix is x = h - p. 

The vertex's y-coordinate is k. To find h, we can use the equation. Let me find the vertex in terms of a and b. 

The vertex occurs at y = -b/(2a) (since for x = a y² + b y + c, derivative dx/dy = 2a y + b = 0 → y = -b/(2a)). 

Substituting this into the equation gives x = a*(-b/(2a))² + b*(-b/(2a)) + c = a*(b²/(4a²)) - b²/(2a) + c = b²/(4a) - b²/(2a) + c = -b²/(4a) + c. 

So the vertex is at (h, k) = (c - b²/(4a), -b/(2a)). 

The directrix is x = h - p. Since p = 1/(4a), then x = h - 1/(4a). 

Substituting h = c - b²/(4a), we get x = c - b²/(4a) - 1/(4a) = c - (b² + 1)/(4a). 

So for a horizontal parabola (x = ay² + by + c), the directrix is x = c - (b² + 1)/(4a). 

But the test case is for a=5, b=3, c=2. Let's compute that. 

x = 2 - (3^2 + 1)/(4*5) = 2 - (9+1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. Still not -198. 

Hmm. So this approach also doesn't give the expected result. 

Alternatively, perhaps the problem is not about the standard parabola, but about a different form. Let me think again. 

The user provided the test case: parabola_directrix(5,3,2) should return -198. Let's see what formula would give that. 

Let me compute -198 using the given a=5, b=3, c=2. 

Let me suppose that the formula is something like -(b² - 4ac) / (4a) multiplied by some factor. 

Let me compute -(b² - 4ac) / (4a) = -(9 - 40)/20 = -(-31)/20 = 31/20 = 1.55. 

But the expected value is -198. So maybe there's a mistake in the formula. 

Alternatively, perhaps the formula is (b² - 4ac) / (4a) but with a negative sign. 

Wait, the original code was returning -(b² -4ac) / (4a). Which for the test case gives 31/20, but the expected is -198. So that's not matching. 

So what's the correct formula for the directrix of a parabola given by ax² + bx + c? 

Alternatively, perhaps the user is referring to a different form of the parabola. For example, if the parabola is given in the form y = ax² + bx + c, then the directrix is y = c - (b² + 1)/(4a). But that doesn't match the test case. 

Alternatively, maybe the user is referring to the directrix of the parabola in the form of y = ax^2 + bx + c, but the formula is different. 

Let me think again. Let me derive the directrix formula properly. 

Let me consider the definition of a parabola: the set of points equidistant from the focus and the directrix. 

Let me suppose the parabola is y = ax² + bx + c. Let me find the focus and directrix. 

The standard form of a parabola is y = (1/(4p)) (x - h)^2 + k, where p is the distance from the vertex to the focus and directrix. 

The directrix is y = k - p. 

The focus is (h, k + p). 

So for a general parabola y = ax² + bx + c, we can find the vertex, then find the directrix. 

The vertex is at x = -b/(2a), and y = a*(-b/(2a))^2 + b*(-b/(2a)) + c = a*(b²/(4a²)) - b²/(2a) + c = b²/(4a) - b²/(2a) + c = -b²/(4a) + c. 

So the vertex is at ( -b/(2a), c - b²/(4a) ). 

The coefficient a is 1/(4p), so p = 1/(4a). 

Therefore, the directrix is y = k - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

So the directrix is y = c - (b² + 1)/(4a). 

But for the test case, with a=5, b=3, c=2: 

directrix = 2 - (3^2 + 1)/(4*5) = 2 - (10)/20 = 2 - 0.5 = 1.5. 

But the expected value is -198. This is a contradiction. 

So why is the test case expecting -198? 

Let me think about the possibility that the user provided the wrong test case, or perhaps the function is supposed to return something else. 

Alternatively, maybe the function is not about the directrix of the parabola y = ax² + bx + c, but about the directrix of a different form. 

Wait, perhaps the function is supposed to return the directrix for the parabola in the form of x = ay² + by + c, and the test case is using that. 

Let me try that. 

For x = ay² + by + c, the directrix is x = h - p, where h is the x-coordinate of the vertex. 

The vertex of x = ay² + by + c is at y = -b/(2a). 

Substituting into x, we get x = a*(b²/(4a²)) + b*(-b/(2a)) + c = b²/(4a) - b²/(2a) + c = -b²/(4a) + c. 

So the vertex is at (c - b²/(4a), -b/(2a)). 

The value of p is 1/(4a), as before. 

So the directrix is x = vertex_x - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

So for the test case, a=5, b=3, c=2: 

x = 2 - (3^2 + 1)/(4*5) = 2 - 10/20 = 2 - 0.5 = 1.5. 

Still not matching -198. 

Hmm. So this approach isn't working. 

Maybe there's a mistake in the way the coefficients are passed. For example, perhaps the function is supposed to take the coefficients of a different form. 

Alternatively, maybe the user made a mistake in the test case. But assuming the test case is correct, I need to find the formula that would give -198 for a=5, b=3, c=2. 

Let me calculate what formula would give that. 

Let me call the desired result D = -198. 

So, for a=5, b=3, c=2, D = -198. 

Let me see what formula would give this. 

Let me suppose that the formula is something like -(b^2 - 4ac) / (4a) * some factor. 

Let me compute -(b^2 -4ac) = -(9 - 40) = 31. 

If I divide that by 4a = 20, I get 31/20 = 1.55. 

But the desired value is -198. So, perhaps there's a scaling factor. 

Wait, 31/20 is 1.55. To get -198, maybe I need to multiply by something. 

But how? 

Alternatively, maybe the formula is -(b^2 - 4ac) / (a) * something. 

Let me see: 

If I take -(b^2 -4ac) / a = -(9-40)/5 = 31/5 = 6.2. Still not matching. 

Alternatively, -(b^2 -4ac) * something. 

Let me see: 31 * something = -198 → something = -198 /31 ≈ -6.387. Not sure. 

Alternatively, maybe the formula is - (b^2 + 4ac) / (4a). 

For the test case, that would be -(9 + 40)/20 = -49/20 = -2.45. Not -198. 

Hmm. 

Alternatively, perhaps the formula is -(b^2 - 4ac) / (a) - something. 

Let me think: 

Let me suppose that the formula is -(b^2 - 4ac) / (4a) multiplied by some factor. 

But without knowing the correct formula, it's hard to proceed. 

Alternatively, maybe the user's test case is incorrect, but that's unlikely. 

Wait, maybe the problem is not about the standard parabola. Maybe it's about the directrix of the parabola defined by the general equation of a conic section. 

The general equation of a parabola is Ax² + Bxy + Cy² + Dx + Ey + F = 0. 

But solving this for the directrix is more complex. 

Alternatively, maybe the user is referring to the directrix of the parabola in the form of y = ax^2 + bx + c, but the formula is different. 

Let me try to find the directrix using the definition. 

Let me take a point (x, y) on the parabola. The distance from this point to the focus (h, k + p) should be equal to the distance to the directrix y = k - p. 

Let me assume that the parabola is y = ax² + bx + c. 

The focus is at (h, k + p), and the directrix is y = k - p. 

The vertex is at (h, k), where h = -b/(2a), and k = c - b²/(4a). 

As before, p = 1/(4a). 

So the directrix is y = k - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

So for the test case, this formula gives 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. 

But the expected result is -198. 

So there's a contradiction here. 

Alternatively, perhaps the user is referring to the directrix of a parabola in the form of x = ay^2 + by + c, and the function is supposed to return x = ... 

Wait, let's try that. 

If the parabola is x = ay^2 + by + c, then the directrix is x = h - p. 

Where h is the x-coordinate of the vertex, and p is 1/(4a). 

The vertex is at y = -b/(2a), and x = a*(-b/(2a))^2 + b*(-b/(2a)) + c = a*(b²/(4a²)) - b²/(2a) + c = b²/(4a) - b²/(2a) + c = -b²/(4a) + c. 

So the directrix is x = h - p = c - b²/(4a) - 1/(4a) = c - (b^2 + 1)/(4a). 

For the test case, this gives 2 - (9 + 1)/20 = 2 - 0.5 = 1.5. Still not matching. 

Hmm. 

Maybe the user made a mistake in the test case, or perhaps the function is supposed to return something else. 

Wait, the original code was returning -(b^2 -4ac)/(4a). For the test case, this gives -(9 - 40)/20 = 31/20 = 1.55. But the test case expects -198. 

But perhaps the function is supposed to return the directrix of a different type of parabola. 

Alternatively, maybe the function is supposed to compute the directrix of a parabola given by the general form Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0, and the user provided the coefficients in a different way. 

But without more information, it's hard to say. 

Alternatively, perhaps the function is supposed to return the directrix for the parabola defined by the equation y = ax^2 + bx + c, but with a different formula. 

Let me think about the directrix formula again. 

Let me take the standard form of a parabola: y = ax^2 + bx + c. 

The directrix is y = k - p, where k is the y-coordinate of the vertex, and p is the focal length. 

As before, k = c - b^2/(4a), p = 1/(4a). 

So directrix is y = c - b^2/(4a) - 1/(4a) = c - (b^2 + 1)/(4a). 

But this gives 1.5 for the test case. 

But the test case says it should return -198. 

So perhaps the user's test case is incorrect, but that's unlikely. 

Alternatively, maybe the function is supposed to return the directrix of the parabola in a different form, such as the directrix of the parabola defined by the equation ax^2 + bx + c = 0. But that's not a standard parabola. 

Alternatively, perhaps the function is supposed to return the directrix of the parabola defined by the equation y = ax^2 + bx + c, but the formula is different. 

Wait, perhaps the formula for the directrix is y = - (b^2 - 4ac)/(4a). Let's compute that for the test case. 

b^2 -4ac = 9 - 4*5*2 = 9 - 40 = -31. So -(-31)/(4a) = 31/(20) = 1.55. Still not matching. 

But the test case expects -198. 

Wait, what if the formula is -(b^2 + 4ac)/(4a)? 

For the test case: -(9 + 40)/20 = -49/20 = -2.45. Not -198. 

Alternatively, maybe the formula is -(b^2 - 4ac) / (4a) * something. 

Let me see: 

If I multiply by -1, it's (b^2 -4ac)/(4a). For the test case, it's 31/20 = 1.55. 

But how to get to -198? 

Let me try to see what value of (b^2 -4ac) would give -198 when divided by 4a. 

Let's say (b^2 -4ac)/ (4a) = -198. 

For a=5, b=3, c=2: 

(9 - 4*5*2) / (4*5) = (9-40)/20 = -31/20 = -1.55. 

But this is not -198. 

So, unless there's a mistake in the test case, I'm missing something. 

Wait, maybe the function is supposed to return the directrix of the parabola defined by the equation x^2 + bx + c = 0. But that's not a parabola. 

Alternatively, perhaps the function is supposed to return the directrix of the parabola defined by the equation y^2 = 4ax + bx + c. 

But this is getting too speculative. 

Alternatively, perhaps the user made a mistake in the test case, but I need to find a formula that would give -198 for the given inputs. 

Let me think: 

Let me suppose that the formula is -(b^2 - 4ac) / (a). 

For the test case: -(9 - 40)/5 = 31/5 = 6.2. No. 

If the formula is -(b^2 - 4ac) * a. 

-(9-40) * 5 = 31 * 5 = 155. No. 

If the formula is -(b^2 -4ac) * 4a. 

-(9-40) * 20 = 31 * 20 = 620. No. 

Wait, what if the formula is -(b^2 -4ac) * something. Let me see: 

Let me set up the equation: 

-(b^2 -4ac) * k = -198. 

For the test case, -(9 - 40) * k = -198 → 31 * k = -198 → k = -198/31 ≈ -6.387. 

So if the formula is -(b^2 -4ac) multiplied by -6.387, it would give -198. 

But this seems arbitrary. 

Alternatively, perhaps the formula is (b^2 -4ac) * (something). 

But this approach is not leading anywhere. 

Maybe the user's test case is incorrect. But since the user says it's failing, I need to find the correct formula. 

Alternatively, perhaps the function is supposed to return the directrix of a parabola in a different form, such as the directrix of the parabola defined by the equation y = ax^2 + bx + c, but with the directrix formula being y = - (b^2 - 4ac) / (4a). 

Wait, let's compute that for the test case: 

-(b^2 -4ac)/(4a) = -(9-40)/20 = 31/20 = 1.55. Still not matching. 

Alternatively, maybe the formula is -(b^2 + 4ac) / (4a). 

For the test case: -(9 + 40)/20 = -49/20 = -2.45. 

No. 

Alternatively, maybe the formula is -(b^2 - 4ac) / (2a). 

For the test case: -(9-40)/10 = 31/10 = 3.1. 

No. 

Alternatively, maybe the formula is (b^2 - 4ac) / (4a) * something. 

But I'm stuck. 

Wait, let's think about the original code. The original code was returning -(b^2 -4ac)/(4a). For the test case, this gives 31/20 = 1.55. But the expected value is -198. 

So the correct formula must be something else. 

Let me try to find what formula would give -198 for a=5, b=3, c=2. 

Let me assume the formula is something like - (b^2 - 4ac) * k. 

Let me solve for k: 

- (9 - 40) * k = -198 → 31 * k = -198 → k = -198/31 ≈ -6.387. 

But this is arbitrary. 

Alternatively, perhaps the function is supposed to return the directrix of a parabola defined by the equation x = ay^2 + by + c, and the directrix is x = - (b^2 + 4ac) / (4a). 

Let me try that: 

For a=5, b=3, c=2: 

- (3^2 + 4*5*2) / (4*5) = -(9 + 40)/20 = -49/20 = -2.45. Still not matching. 

Hmm. 

Alternatively, perhaps the formula is - (b^2 - 4ac) / (4a) * a. 

For the test case: - (9-40)/20 *5 = 31/20 *5 = 31/4 = 7.75. No. 

Alternatively, maybe the formula is - (b^2 - 4ac) / (4a) * something else. 

But I'm not making progress. 

Maybe I should look for a different approach. Let me think about the test case: 

parabola_directrix(5,3,2) == -198. 

Let me compute what value of the formula would give -198. 

Let me assume the formula is something like - (b^2 - 4ac) * (something). 

Let me compute -(b^2 -4ac) = 31. So 31 * x = -198 → x = -198/31 ≈ -6.387. 

But what is this number? Let me see: 

-198/31 is approximately -6.387. 

But what is this number? Maybe it's related to the coefficients. 

Alternatively, perhaps the formula is - (b^2 - 4ac) * (a) * something. 

But I'm not seeing it. 

Alternatively, perhaps the function is supposed to return the directrix of the parabola defined by the equation ax^2 + bx + c = 0, but that's not a parabola. 

Alternatively, maybe the function is supposed to return the directrix of the parabola defined by the equation y = ax^2 + bx + c, but the formula is different. 

Wait, let me think about the directrix of the parabola in terms of the focus. 

For a parabola, the directrix is a line such that any point on the parabola is equidistant from the focus and the directrix. 

Let me take the standard parabola y = ax^2. The directrix is y = -1/(4a). 

So for a=5, this would be y = -1/(20) = -0.05. 

But the test case is for a=5, b=3, c=2. 

Let me think about the general case. 

Let me take the parabola y = ax^2 + bx + c. 

The focus is at (h, k + p), where h = -b/(2a), k = c - b^2/(4a), and p = 1/(4a). 

So the focus is at (-b/(2a), c - b^2/(4a) + 1/(4a)) = (-b/(2a), c - (b^2 -1)/(4a)). 

The directrix is y = k - p = c - b^2/(4a) - 1/(4a) = c - (b^2 + 1)/(4a). 

So for the test case, this gives 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. 

But the test case expects -198. 

This suggests that either the test case is wrong, or the function is supposed to return a different value. 

But since the user says that the test case is failing, I must find the correct formula. 

Maybe the function is supposed to return the directrix of a parabola defined by the equation x = ay^2 + by + c, and the directrix is x = - (b^2 + 4ac) / (4a). 

Let me compute this for a=5, b=3, c=2: 

- (3^2 + 4*5*2) / (4*5) = -(9 + 40)/20 = -49/20 = -2.45. Still not -198. 

Hmm. 

Alternatively, perhaps the directrix is calculated as - (b^2 - 4ac) / (4a) * something. 

Wait, let me think of the test case: 5, 3, 2. 

Let me compute - (b^2 - 4ac) / (4a) = - (9 - 40)/20 = 31/20 = 1.55. 

But the expected value is -198. 

So, what if the formula is - (b^2 - 4ac) / (4a) * (some factor)? 

Let me see: 1.55 * x = -198 →
```

</details>

**Code that ran:**

```python
def parabola_directrix(a, b, c):
    return -(b**2 - 4*a*c) / (4*a)
```

**Visible-test report:**

```text
FAIL    assert parabola_directrix(5,3,2)==-198
        AssertionError: assertion failed
0 of 1 visible tests passed
```

## Round 3 (`Mbpp/430/a4/r3`)

Visible tests: **fail**. Hidden tests: **❌ fail**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 870.

<details><summary>Thinking</summary>

```text
Okay, let's see. The user wants me to fix the parabola_directrix function so that it passes the test case where a=5, b=3, c=2, and the expected output is -198. The previous code they had was returning -(b² -4ac)/(4a). But that's not giving the correct result. Let me think about how to find the directrix of a parabola.

Wait, the standard form of a parabola is y = ax² + bx + c. The directrix of a parabola in this form is given by the formula y = c - (b² - 4ac)/(4a). Wait, but maybe I'm mixing up the formula. Let me recall. Alternatively, maybe the formula for the directrix is y = - (b² - 4ac)/(4a) + c? Or perhaps I need to derive it.

Let me think. For a parabola in the form y = ax² + bx + c, the vertex is at x = -b/(2a). The focus and directrix are related to the vertex. The directrix is a horizontal line. The distance from the vertex to the focus is 1/(4a) if the parabola is in the form y = ax². But when there are linear terms, maybe the formula changes.

Alternatively, maybe the directrix can be found using the formula y = k - 1/(4a), where (h, k) is the vertex. Wait, but the vertex form of a parabola is y = a(x - h)^2 + k. The directrix is y = k - 1/(4a) if a is positive. But in the standard form y = ax² + bx + c, the vertex is at (-b/(2a), c - b²/(4a)). Wait, maybe I should derive the directrix formula.

Let me try to derive it. Let's consider the standard parabola y = ax² + bx + c. Let me rewrite it in vertex form. The vertex is at x = -b/(2a). Plugging that into the equation gives y = a*(b²/(4a²)) + b*(-b/(2a)) + c. Let me compute that:

y = (a*b²)/(4a²) - (b²)/(2a) + c = (b²)/(4a) - (2b²)/(4a) + c = (-b²)/(4a) + c. So the vertex is at ( -b/(2a), c - b²/(4a) ). 

Now, for a parabola, the directrix is a line that is a distance of 1/(4a) away from the vertex. Wait, no. Wait, for the standard parabola y = (1/(4p))x², the directrix is y = -p. So the distance between the vertex (which is at (0,0)) and the directrix is p. So in this case, the formula for the directrix is y = -p. But since the coefficient is 1/(4p), then p = 1/(4a). So the directrix is y = -1/(4a). 

But in the case of the standard parabola y = ax², the vertex is at (0,0), and the directrix is y = -1/(4a). 

So for a general parabola y = a(x - h)^2 + k, the directrix is y = k - 1/(4a). 

So applying that to the vertex form. So in the case of the original equation, the vertex is at (h, k) = (-b/(2a), c - b²/(4a)). So the directrix is y = k - 1/(4a) = [c - b²/(4a)] - 1/(4a) = c - (b² + 4a)/(4a). Wait, that seems off. Let me re-calculate:

Wait, the vertex is at (h, k) where k = c - b²/(4a). Then the directrix is y = k - 1/(4a). So substituting k:

y = c - b²/(4a) - 1/(4a) = c - (b² + 1)/(4a). Wait, that doesn't seem right. Wait, maybe I made a mistake here. Let me think again.

Wait, the standard form is y = a(x - h)^2 + k. The directrix is y = k - 1/(4a) if a is positive. Wait, but in this case, the standard form is y = ax² + bx + c. So the vertex form is y = a(x - h)^2 + k, where h = -b/(2a), and k = c - b²/(4a). So the directrix is y = k - 1/(4a) = [c - b²/(4a)] - 1/(4a) = c - [b² + 4a]/(4a). Wait, that's c - (b² + 4a)/(4a) = c - b²/(4a) - 1/(4a). 

But that's not matching the previous code. The previous code was returning -(b² -4ac)/(4a). Let's compute that. Let me take the test case: a=5, b=3, c=2. 

Original code: -(b² -4ac)/(4a) = -(9 - 4*5*2)/(4*5) = -(9-40)/20 = -(-31)/20 = 31/20 = 1.55. But the expected result is -198. So clearly, the previous code is wrong.

So the user's code is returning the wrong formula. So I need to find the correct formula for the directrix.

Wait, maybe the formula for the directrix is y = c - (b² + 1)/(4a) ? Or perhaps I need to re-derive it.

Let me think again. Let's take the standard equation of a parabola. Let me consider the general case of a parabola in the form y = ax² + bx + c. Let me find the directrix.

Alternatively, maybe I can use the formula for the directrix of a parabola given in standard form. Let me look up the formula for the directrix of a parabola given by y = ax² + bx + c.

Wait, according to some references, the directrix of a parabola y = ax² + bx + c is given by y = (c - (b² + 1)/(4a)) ?

No, that doesn't seem right. Let me think again. Let me consider the standard form of a parabola. The general equation of a parabola can be written as y = (1/(4p))x², where p is the distance from the vertex to the focus. The directrix is y = -p. So for this case, the directrix is y = -p = - (1/(4*(1/(4p))))? Wait, no. Wait, if the equation is y = (1/(4p))x², then the directrix is y = -p. So for example, if the parabola is y = x², then 1/(4p) = 1 → p = 1/4. So directrix is y = -1/4. 

Now, for the equation y = ax² + bx + c, the vertex is at (-b/(2a), c - b²/(4a)). The distance from the vertex to the focus is 1/(4a) if the parabola is in the form y = a(x - h)^2 + k. Wait, but in that case, the standard form is y = a(x - h)^2 + k. Then the directrix is y = k - 1/(4a) if a is positive. So in our case, the vertex is at (h, k) = (-b/(2a), c - b²/(4a)). So the directrix is y = k - 1/(4a) = c - b²/(4a) - 1/(4a) = c - (b² + 1)/(4a). Wait, but that's not matching the test case.

Let me plug in the test case: a=5, b=3, c=2. Then the directrix would be y = 2 - (3² + 1)/(4*5) = 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. But the expected result is -198. That's way off. So clearly, this approach is wrong.

Wait, perhaps I'm mixing up the formula for the directrix. Let me think again. Let me try to derive the directrix from the definition.

A parabola is the set of points equidistant from the focus and the directrix. Let's consider the standard parabola y = ax² + bx + c. Let me find the focus and directrix.

Alternatively, perhaps I can find the formula for the directrix using the standard form. Let me consider the general parabola in the form y = ax² + bx + c. Let me find the directrix.

Let me recall that for a parabola in the form y = ax² + bx + c, the directrix is given by y = c - (b² - 4ac)/(4a) - 1/(4a) ?

Wait, perhaps I should find the formula for the directrix by considering the vertex and the distance from the vertex to the focus. Let me try that.

The vertex of the parabola y = ax² + bx + c is at (h, k) where h = -b/(2a), and k = c - b²/(4a). 

The standard parabola y = ax² has focus at (0, 1/(4a)) and directrix y = -1/(4a). So for the general case, when the parabola is shifted, the focus and directrix are shifted accordingly. 

So for the parabola y = a(x - h)^2 + k, the focus is at (h, k + 1/(4a)) and directrix is y = k - 1/(4a). 

So for our case, the vertex is at (h, k) = (-b/(2a), c - b²/(4a)). So the directrix is y = k - 1/(4a) = [c - b²/(4a)] - 1/(4a) = c - (b² + 4a)/(4a) ?

Wait, let's compute that:

c - [b²/(4a) + 1/(4a)] = c - (b² + 1)/(4a). 

But for the test case, a=5, b=3, c=2. So this would be 2 - (9 + 1)/(4*5) = 2 - 10/20 = 2 - 0.5 = 1.5. But the expected answer is -198. That's not matching. So clearly, this approach is incorrect. 

Hmm. Maybe the formula for the directrix is different. Let me think again. 

Alternatively, maybe the formula for the directrix is y = (c - (b^2 - 4ac)) / (4a) ?

Wait, the user's previous code was returning -(b^2 -4ac)/(4a). Let's compute that for the test case. 

b^2 -4ac = 3^2 -4*5*2 = 9 - 40 = -31. So -( -31 )/(4*5) = 31/20 = 1.55. But the expected answer is -198. So that's not matching. 

So the user's code is wrong. So what's the correct formula?

Alternatively, perhaps the directrix is given by y = ( -b^2 + 4ac ) / (4a) ?

Wait, let me think of the standard form. Let me take a parabola in the form y = ax² + bx + c. Let me find the directrix. 

Alternatively, perhaps the directrix is given by the formula y = - (b^2 - 4ac) / (4a) ?

Wait, for the test case, that would be -(9 - 40)/20 = 31/20 = 1.55. Still not matching. 

Wait, the test case expects -198. So for the input (5,3,2), the output is -198. Let me compute what formula would give that. 

Let me compute -198. Let me see: 

Let me suppose that the correct formula is something like ( - (b^2 - 4ac) ) / (4a) - something. 

Wait, let me think again. Maybe the directrix is calculated differently. Let me check the formula for the directrix of a parabola given in the general form.

Looking up the formula for the directrix of a parabola. 

Upon checking, the directrix of a parabola given by y = ax² + bx + c is y = c - (b² + 1)/(4a) ? Or perhaps I need to derive it properly.

Alternatively, perhaps I should use the formula for the directrix of a parabola in standard form. Let me consider the general equation of a parabola. 

Let me recall that the standard form of a parabola that opens up or down is (x - h)^2 = 4p(y - k), where the vertex is at (h, k), and the directrix is y = k - p. The focus is at (h, k + p). 

So if we have the equation (x - h)^2 = 4p(y - k), then the directrix is y = k - p. 

Let me convert the given equation y = ax² + bx + c into this form. 

Let me complete the square. 

y = ax² + bx + c 

Let me factor out a from the first two terms:

y = a(x² + (b/a)x) + c 

Now, complete the square inside the parentheses. 

The coefficient of x is b/a. Half of that is b/(2a), square is b²/(4a²). 

So:

y = a[ x² + (b/a)x + b²/(4a²) - b²/(4a²) ] + c 

= a[ (x + b/(2a))^2 - b²/(4a²) ] + c 

= a(x + b/(2a))^2 - a*(b²/(4a²)) + c 

= a(x + b/(2a))^2 - b²/(4a) + c 

So the equation becomes:

y = a(x + b/(2a))^2 + (c - b²/(4a))

Which is in the form y = a(x - h)^2 + k, where h = -b/(2a), and k = c - b²/(4a). 

Comparing to the standard form (x - h)^2 = 4p(y - k), we can rearrange:

a(x - h)^2 + k = y 

=> a(x - h)^2 = y - k 

=> (x - h)^2 = (y - k)/a 

Comparing to (x - h)^2 = 4p(y - k), we have 4p = 1/a → p = 1/(4a). 

So the directrix is y = k - p = k - 1/(4a). 

Substituting k:

y = [c - b²/(4a)] - 1/(4a) = c - (b² + 1)/(4a). 

Wait, but for the test case, this would give:

c is 2, b is 3, a is 5. 

So:

y = 2 - (3^2 + 1)/(4*5) = 2 - (9 + 1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. 

But the test case expects -198. That's way off. So clearly, this formula is not correct. 

Wait, maybe I made a mistake in the derivation. Let me check the standard form again. 

The standard form (x - h)^2 = 4p(y - k) has directrix y = k - p. 

In the equation derived above, (x - h)^2 = (y - k)/a → (x - h)^2 = 4p(y - k), where 4p = 1/a → p = 1/(4a). 

So the directrix is y = k - p = k - 1/(4a). 

But in the test case, the formula gives 1.5, but the expected answer is -198. So there's a contradiction here. 

Hmm. So either the test case is wrong, or my understanding of the problem is incorrect. 

Wait, the user says that the function should return -198 for input (5,3,2). Let me try to find what formula would give that. 

Let me compute for a=5, b=3, c=2. The expected directrix is -198. 

Let me try to find a formula that gives -198. 

Let me see:

Suppose the formula is ( - (b^2 - 4ac) ) / (4a) ?

For the test case, that would be -(9 - 40)/20 = 31/20 = 1.55. Not matching. 

What if the formula is ( - (b^2 - 4ac) ) / (4a) multiplied by something? 

Alternatively, maybe the formula is -(b^2 - 4ac) / (4a) - something. 

Wait, let me think of the directrix as being related to the focus. Let me consider that the directrix is a line, and for a parabola, the distance from the vertex to the directrix is p. 

But maybe I'm missing a negative sign. 

Wait, in the standard form (x - h)^2 = 4p(y - k), the directrix is y = k - p. So if p is positive, the directrix is below the vertex. 

But in our case, the equation is (x - h)^2 = (y - k)/a → which implies that 4p = 1/a → p = 1/(4a). 

So if a is positive, then p is positive, and the directrix is y = k - p. 

But in the test case, the directrix is -198. Let me see what value of k and p would give that. 

Let me compute k for the test case. 

k = c - b²/(4a) = 2 - (9)/(20) = 2 - 0.45 = 1.55. 

Then p = 1/(4a) = 1/(20) = 0.05. 

So the directrix is y = 1.55 - 0.05 = 1.5. 

But the expected answer is -198. So clearly, this is not matching. 

So there's something wrong here. Perhaps the user is not referring to the standard parabola, but a different form. 

Wait, maybe the problem is not about the standard parabola y = ax² + bx + c, but about a parabola in a different form. 

Wait, the problem says "directrix of a parabola". Perhaps the user is referring to a parabola in the form x = ay² + by + c, which opens to the left or right. 

For example, the directrix of a parabola that opens to the right or left would be a vertical line. 

If the parabola is in the form x = ay² + by + c, then the directrix is a vertical line x = - (b² - 4ac) / (4a) - something. 

But the user's test case is expecting a value of -198. Let me try to see what formula would give that. 

Let me suppose that the parabola is of the form x = ay² + by + c. Let me derive the directrix for this case. 

Let me consider the standard form of a parabola that opens to the right: y² = 4p(x - h). The directrix is x = h - p. 

Let me take the equation x = ay² + by + c. Let me rearrange it to y² = (1/a)x - (b/a)y - c/a. 

Completing the square for y:

y² + (b/a)y = (1/a)x - c/a 

y² + (b/a)y + (b²)/(4a²) = (1/a)x - c/a + (b²)/(4a²) 

Left side is (y + b/(2a))². 

So:

(y + b/(2a))² = (1/a)x - c/a + b²/(4a²) 

Let me write this as:

(y + b/(2a))² = (1/a)(x - c + b²/(4a)) 

Which is similar to the standard form y² = 4p(x - h). 

Comparing, the standard form is (y - k)^2 = 4p(x - h). 

So in this case, (y + b/(2a))² = (1/a)(x - (c - b²/(4a))) 

Which implies that 4p = 1/a → p = 1/(4a). The vertex is at (h, k) = (c - b²/(4a), -b/(2a)). 

The directrix for this parabola is x = h - p = (c - b²/(4a)) - 1/(4a) = c - (b² + 1)/(4a). 

Wait, but this is the same as before. So for this case, the directrix is x = c - (b² + 1)/(4a). 

But if the parabola is in the form x = ay² + by + c, then the directrix is x = c - (b² + 1)/(4a). 

But the test case is expecting a value of -198. Let me compute this for a=5, b=3, c=2. 

x = 2 - (3² + 1)/(4*5) = 2 - (9+1)/20 = 2 - 10/20 = 2 - 0.5 = 1.5. Still not matching. 

So this suggests that the test case is expecting a different formula. 

Alternatively, perhaps the user made a mistake in the test case. But since the user provided that the test case should pass, I need to find what formula would produce -198 for a=5, b=3, c=2. 

Let me compute what value of the formula would give -198. 

Let me assume the formula is something like - (b^2 - 4ac) / (4a) multiplied by some factor. 

For the test case: 

b^2 -4ac = 9 - 40 = -31. 

So -(b^2 -4ac) = 31. 

Divided by 4a (20) gives 31/20 = 1.55. 

But the expected value is -198. So if I multiply by -something: 

Let me see: 

If the formula is - (b^2 - 4ac) / (4a) * something. 

Let me suppose that the correct formula is -(b^2 -4ac) / (4a) * something. 

But for the test case, -(b^2 -4ac) is 31. 

If I multiply by - something to get -198, then 31 * something = 198 → something = 198/31 ≈ 6.387. 

Not sure. 

Alternatively, maybe the formula is (b^2 - 4ac) / (4a) multiplied by some factor. 

But this seems arbitrary. 

Alternatively, perhaps the user is referring to the directrix of the parabola in a different form. Let me think. 

Wait, maybe the problem is about a parabola in the form y = ax^2 + bx + c, and the directrix is y = something, but the formula is different. 

Let me think about the standard formula for directrix. 

Another approach: the directrix of a parabola is a line such that any point on the parabola is equidistant from the focus and the directrix. 

Let me take the standard parabola y = ax² + bx + c. Let me find its directrix. 

Let me assume that the directrix is y = d. 

Let me take a point (x, y) on the parabola. The distance from (x, y) to the focus (h, k) must equal the distance from (x, y) to the directrix y = d. 

But I need to find the focus and directrix. 

Alternatively, since the vertex is at (h, k), and the directrix is y = k - p, and the focus is at (h, k + p), where p is the distance from the vertex to the focus. 

But earlier calculations showed that for the parabola y = ax² + bx + c, the directrix is y = k - p = [c - b²/(4a)] - 1/(4a) = c - (b² + 1)/(4a). 

But this doesn't match the test case. 

Wait, but maybe the formula is different. Let me think again. 

Let me consider the standard parabola y = ax^2. Its directrix is y = -1/(4a). 

Now, let's take a=5, then directrix is y = -1/(20) = -0.05. 

But the test case is for a=5, b=3, c=2, and the expected directrix is -198. 

So perhaps the user is referring to a different form of the parabola. 

Alternatively, perhaps the user is referring to the directrix of the parabola in the form x = ay^2 + by + c, which opens to the right or left. 

Let me try that. 

For example, for the parabola x = ay^2 + by + c, the directrix is x = - (b^2 - 4ac) / (4a) - 1/(4a). 

Wait, let's derive it. 

For the parabola x = ay^2 + by + c. Let me complete the square. 

x = a(y^2 + (b/a)y) + c 

= a[ y^2 + (b/a)y + (b^2)/(4a^2) ] - a*(b^2)/(4a^2) + c 

= a(y + b/(2a))^2 - b^2/(4a) + c 

So x = a(y + b/(2a))^2 + (c - b^2/(4a)) 

This is in the form x = a(y - k)^2 + h, where k = -b/(2a), and h = c - b^2/(4a). 

This is similar to the standard form (y - k)^2 = (x - h)/a. 

So, comparing to the standard form (y - k)^2 = 4p(x - h), we have 4p = 1/a → p = 1/(4a). 

The directrix of this parabola is x = h - p = (c - b^2/(4a)) - 1/(4a) = c - (b^2 + 1)/(4a). 

So for the test case, a=5, b=3, c=2:

x = 2 - (3^2 + 1)/(4*5) = 2 - 10/20 = 2 - 0.5 = 1.5. Still not matching -198. 

So this is not working. 

Wait, but the test case expects -198. What if the formula is something like (b^2 - 4ac) / (4a) multiplied by -something. 

Let me calculate for the test case: 

b^2 -4ac = 9 - 40 = -31. 

If the formula is -(b^2 -4ac) / (4a) = 31/20 = 1.55. 

But the expected answer is -198. 

Wait, maybe the formula is -(b^2 -4ac) / (4a) * something. 

Let me see what would make 31/20 * something = -198. 

something = (-198) * (20/31) = - (198 * 20)/31 = - 3960/31 ≈ -127.74. 

That doesn't seem like a meaningful number. 

Alternatively, maybe the formula is (b^2 - 4ac) / (4a) multiplied by some factor. 

For example, if the formula is (b^2 - 4ac) / (4a) * something. 

For the test case, (b^2 -4ac) is -31. Divided by 4a (20) is -31/20 = -1.55. 

If I multiply by something to get -198, then something = (-198) / (-1.55) ≈ 127.74. 

Again, not helpful. 

Hmm. This is perplexing. Maybe there's a mistake in the test case? Or perhaps I'm misunderstanding the problem. 

Alternatively, perhaps the user is referring to the directrix of the parabola in the form y = ax^2 + bx + c, but the directrix is given by the formula y = - (b^2 - 4ac) / (4a) - something. 

Wait, let's look at the test case. The expected result is -198. Let me compute what value would give that. 

Let me assume that the formula is -(b^2 - 4ac) / (4a) - c. 

For the test case: -(9 - 40)/20 - 2 = 31/20 - 2 = 1.55 - 2 = -0.45. Not -198. 

Alternatively, perhaps it's -(b^2 + 4ac) / (4a) ?

For the test case: -(9 + 40)/20 = -49/20 = -2.45. Still not -198. 

Alternatively, maybe the formula is -(b^2 - 4ac) / (4a) multiplied by some factor. 

Wait, what if the formula is -(b^2 - 4ac) / (4a) * (something). Let's try to see what factor would give -198 from the previous value of 31/20. 

Let me set 31/20 * k = -198. 

k = -198 * 20 / 31 = -3960/31 ≈ -127.74. 

That doesn't seem like a meaningful factor. 

Alternatively, maybe the formula is (b^2 - 4ac) / (4a) * something. 

Let me try: (9 - 40)/20 = -31/20 = -1.55. If I multiply by something to get -198, then something is 198 / 1.55 ≈ 127.74. 

Still not helpful. 

This suggests that the initial assumption about the formula is incorrect. 

Wait, let me think about the test case. 

The user says that parabola_directrix(5,3,2) should return -198. 

Let me calculate what formula would give this. 

Let me assume that the formula is - (b^2 - 4ac) / (4a) - something. 

For the test case, the current value is 31/20 = 1.55. To get -198, we need to subtract 199.55. 

But why would that be? 

Alternatively, perhaps the formula is - (b^2 - 4ac) / (4a) * (something). 

But without knowing the correct formula, it's hard to proceed. 

Wait, perhaps the user is referring to the directrix of the parabola in the form x = ay^2 + by + c. Let me try that. 

For example, if the parabola is x = ay^2 + by + c, then the directrix is x = - (b^2 - 4ac) / (4a) - 1/(4a). 

Let me compute this for a=5, b=3, c=2. 

- (b^2 -4ac) is -(9 - 40) = 31. Divided by 4a is 31/20 = 1.55. Subtract 1/(4a) = 0.05. So 1.55 - 0.05 = 1.5. Still not -198. 

Hmm. 

Alternatively, maybe the formula is - (b^2 - 4ac) / (4a) - (b^2 - 4ac) / (4a) ? 

For the test case, that would be 31/20 - 31/20 = 0. Not helpful. 

Alternatively, maybe the formula is - (b^2 - 4ac) / (4a) - 1/(4a) ? 

Which is -(b^2 - 4ac + 1) / (4a). 

For the test case: -(9 - 40 + 1)/20 = -( -30)/20 = 30/20 = 1.5. 

Still not matching. 

This is really confusing. Maybe there's a mistake in the test case, or perhaps I'm missing something. 

Wait, let me think about the original code. The user's previous code was returning -(b^2 -4ac)/(4a). For the test case, this gives 31/20 = 1.55, but the expected value is -198. 

So the correct formula must be something else. 

Let me think: perhaps the directrix is given by - (b^2 - 4ac) / (4a) multiplied by something. 

Wait, let me think about the standard formula for directrix. 

In the case of the parabola y = ax^2 + bx + c, the directrix is y = c - (b^2 + 1)/(4a). 

But for the test case, this is 2 - (9 + 1)/(20) = 2 - 10/20 = 1.5. 

But the expected value is -198. 

Wait, perhaps the formula is y = (c - (b^2 - 4ac)) / (4a) ? 

Let me compute that for the test case: 

c - (b^2 -4ac) = 2 - (9 - 40) = 2 - (-31) = 33. Divided by 4a = 20: 33/20 = 1.65. Not matching. 

Alternatively, maybe it's (b^2 - 4ac) / (4a) ? 

For the test case: (9 - 40)/20 = -31/20 = -1.55. Still not -198. 

Wait, what if the formula is -(b^2 -4ac) / (4a) - c? 

For the test case: 31/20 - 2 = 1.55 - 2 = -0.45. No. 

Alternatively, perhaps the formula is - (b^2 - 4ac) / (4a) - (b^2 -4ac) / (4a) ? 

Which is -2*(b^2 -4ac)/(4a) = -(b^2 -4ac)/(2a). 

For the test case: -(9-40)/10 = 31/10 = 3.1. Not matching. 

Hmm. 

Maybe the user made a mistake in the test case, or perhaps the function is supposed to return something else. 

Alternatively, perhaps the directrix is calculated for a different type of parabola, like in the form y = ax^2
```

</details>

**Code that ran:**

```python
def parabola_directrix(a, b, c):
    return c - (b**2 - 4*a*c) / (4*a)
```

**Visible-test report:**

```text
FAIL    assert parabola_directrix(5,3,2)==-198
        AssertionError: assertion failed
0 of 1 visible tests passed
```
