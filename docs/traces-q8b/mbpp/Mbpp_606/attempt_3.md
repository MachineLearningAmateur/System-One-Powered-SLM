# Mbpp/606, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 812. Answer tokens: 56.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called radian_degree that converts degrees to radians. Wait, wait, the function name is a bit confusing. Oh right, the problem says to convert degrees to radians, but the function is named radian_degree. Maybe that's a typo? Or maybe it's supposed to return radians when given degrees. Let me check the assert statement. The example given is radian_degree(90) should equal approximately 1.5707963267948966. Oh right, 90 degrees in radians is π/2, which is about 1.5708. So the function takes a degree value and returns the equivalent in radians.

So the formula to convert degrees to radians is radians = degrees * (π / 180). So I need to use the math.pi constant for that. 

First, I'll need to import the math module. Then, the function will take a parameter, say 'degrees', and return degrees multiplied by math.pi divided by 180. 

Wait, let me test that. For 90 degrees, 90 * π/180 is π/2, which is approximately 1.5707963267948966. That matches the assert. So the function is straightforward.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, the function name is radian_degree, which is a bit odd. But the problem says that's the function name. So that's correct.

Let me check if there are any edge cases. For example, 0 degrees should return 0.0. 180 degrees would be π, which is about 3.14159... So the function seems correct.

So the code should be as simple as that. The assert statement in the problem would check that 90 degrees gives the correct value. 

I think that's all. So the complete code would include the import, the function definition, and the assert. But the problem says to write the function, so the code should have the function and the assert. Wait, the problem says to write the function, but the user's example includes an assert. But the user's instruction says to write a function that meets the assert. So the code should include the function and the assert statement. But the problem says to write the function, but the user's code block might need to include the assert as a test.

Wait, the user's problem says "Write a function to convert degrees to radians." and includes an assert. So the code should include the function and the assert. But when the user says "reply with the complete code in one code block", including any imports. So the code should have the function and the assert. Let me check the example again.

The example given is:

assert radian_degree(90)==1.5707963267948966

So the code should have that assert. So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966

But wait, when you run this, the assert would pass. But in Python, if you run this code, the assert will check that the value is equal. However, when using floating points, there might be precision issues. But the given value is the exact value of π/2, so the calculation should be precise enough. 

So the code should be correct. Let me make sure that the function is named radian_degree, and that the calculation is correct. Yes. So this should be the solution.
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
