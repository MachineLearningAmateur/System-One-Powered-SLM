# Mbpp/606, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 827. Answer tokens: 247.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that converts degrees to radians. The user provided an example where radian_degree(90) should return 1.5707963267948966. Let me think about how to do this.

I remember that radians are calculated by multiplying degrees by π/180. So the formula is radians = degrees * (π / 180). But how do I implement this in Python?

First, I need to import the math module because it has the π value. So I'll need to import math. Then, the function will take a degree as input. Let me structure the function.

Wait, the function is called radian_degree, and it takes one argument, which is the degrees. So the function would be something like:

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, what about the precision? The example given is 1.5707963267948966, which is approximately π/2. Let me check: π is about 3.141592653589793. So π/2 is 1.5707963267948966. So the calculation is correct.

But the math module's pi is a float, so when we multiply by math.pi and divide by 180, it should give the correct value. So the function should work.

Testing with 90 degrees: 90 * math.pi / 180 = 0.5 * math.pi, which is indeed π/2. So that's correct.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

Then, the assert statement would check that radian_degree(90) equals the given value. But wait, the example shows that the result is 1.5707963267948966. Let me check with Python.

Let me calculate 90 * math.pi / 180. Let me see, math.pi is approximately 3.141592653589793. So 90 * 3.141592653589793 is 282.74333882308138. Divided by 180 gives 1.5707963267948966. Which matches the example. So the function is correct.

So the code should import math, define the function, and then the assert statement. But the user wants the complete code in one code block. So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966

Wait, but in Python, the assert statement needs to be in the code. So the code would be as above. But I need to make sure that the imports are included.

So the complete code is:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966

Yes, that should work. Let me check if there are any possible issues. For example, what if the input is not a number? But the problem says to write a function that converts degrees to radians, so the input is expected to be a number. The assert statement is testing the function with 90, which is correct.

So that's the solution.
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
