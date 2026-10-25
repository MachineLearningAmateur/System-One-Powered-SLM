# Mbpp/606, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 823. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called radian_degree that converts degrees to radians. Wait, wait, the function name is a bit confusing. Oh right, the problem says to convert degrees to radians, so the function is supposed to take a degree value and return the equivalent in radians.

Wait, the sample assertion is radian_degree(90) equals approximately 1.5707963267948966. Let me check what that number is. Oh right, π/2 is approximately 1.5708, and since 90 degrees is π/2 radians. So the function is correct.

So how to convert degrees to radians? The formula is radians = degrees * (π / 180). So I need to multiply the input by π divided by 180.

In Python, the math module has pi. So I should import math and use math.pi.

So the steps are: take the input degrees, multiply by math.pi, divide by 180.0, and return that value.

Wait, but the function is named radian_degree. Wait, that's a bit confusing. Because the function is converting degrees to radians. So the function name might be a bit misleading. But the problem says to write the function as radian_degree. So maybe it's a typo, but the user says to follow the assertion.

So the function is called radian_degree, which takes a degree value and returns radians. So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180.0

Wait, but what about the precision? The sample assertion uses 1.5707963267948966, which is the value of math.pi/2. So when we compute 90 * math.pi / 180, that's math.pi/2, which is exactly that value.

But when we do the calculation, since math.pi is a float with limited precision, but the assertion is using a specific value. However, the problem's assertion is expecting that exact value, which is the same as math.pi/2. So the code should work.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

Wait, but wait, in Python, dividing by 180.0 or 180? Well, in Python 3, dividing by 180 (an integer) would result in a float. So it's okay.

Testing the sample input: 90 degrees. 90 * math.pi / 180 = math.pi / 2, which is approximately 1.5707963267948966. So the assertion should pass.

So the code should be correct. Let me check if there are any other possible issues. For example, does the function need to handle any edge cases? The problem doesn't specify, so perhaps it's just a straightforward conversion.

So the complete code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, the function name is radian_degree. Wait, that's a bit confusing. Because the function is converting degrees to radians. So perhaps the function should be called degree_to_radian? But the problem says to write the function as radian_degree. So maybe the user made a typo, but we have to follow the given name.

So the code is correct. Let me check the sample assertion. When we call radian_degree(90), it returns 90 * pi / 180 = pi/2, which is approximately 1.5707963267948966. So the assertion is correct.

Therefore, the code should work.
```

</details>

**Code that ran:**

```python
import math

def radian_degree(degrees):
    return degrees * math.pi / 180
```

**Visible-test report:**

```text
PASS    assert radian_degree(90)==1.5707963267948966
1 of 1 visible tests passed
```
