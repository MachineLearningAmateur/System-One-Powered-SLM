# Mbpp/606, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 687. Answer tokens: 243.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that converts degrees to radians. The user provided an example where radian_degree(90) should return 1.5707963267948966. Let me think about how to do this.

I remember that radians are calculated by multiplying degrees by π/180. So the formula is radians = degrees * (π/180). But how do I implement this in Python?

First, I need to import the math module because it has the π value. So I'll start by importing math. Then, the function will take a degree as input. Let me define the function as radian_degree(degrees).

Wait, the function name is radian_degree, and it takes one argument, which is the degrees. So the function would be something like:

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, what about the precision? The example given has 1.5707963267948966, which is about π/2. Let me check: π is approximately 3.141592653589793. So π/2 is 1.5707963267948966. So the function would return that value when degrees is 90.

But wait, the math.pi is a float, so when we multiply by math.pi and divide by 180, it should give the correct value. So the code should be straightforward.

But I need to make sure that the function is correctly implemented. Let me test with 90 degrees. Let's see: 90 * math.pi is 282.74333882308138, divided by 180 gives 1.5707963267948966. Which matches the example. So that's correct.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

Then, the assert statement would check that radian_degree(90) equals the given value. But wait, the assert is in the problem statement. So the code should include that.

But the user wants the complete code, including any imports. So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966

But wait, the assert statement is part of the code. So the code should include that. So the complete code would be that.

Wait, but the user says to write a correct Python solution. So the function is correct, and the assert is correct. So that's the code.

I think that's all. Let me check if there are any possible errors. For example, what if the input is not a number? But the problem doesn't mention handling that, so perhaps the function is supposed to take a float, and the assert is for 90. So the code should be correct.
```

</details>

**Code that ran:**

```python
import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966
```

**Visible-test report:**

```text
PASS    assert radian_degree(90)==1.5707963267948966
1 of 1 visible tests passed
```
