# Mbpp/606, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 674. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called radian_degree that converts degrees to radians. Wait, wait, the function name is a bit confusing. Oh right, the problem says to convert degrees to radians, so the function is supposed to take a degree value and return the equivalent in radians.

Wait, the sample assertion is radian_degree(90) equals approximately 1.5707963267948966. Let me check what that number is. Oh right, pi/2 is approximately 1.5708, and 90 degrees is pi/2 radians. So the function is correct.

So the formula to convert degrees to radians is radians = degrees * (pi / 180). So I need to multiply the input by pi over 180.

Now, in Python, the math module has pi. So I should import math and use math.pi.

So the steps are: import math, then define the function, take degrees as input, multiply by math.pi / 180, and return that value.

Wait, the function is named radian_degree. Wait, that's a bit odd. Because the function is converting degrees to radians. So the name might be a bit confusing. But the problem says to write the function with that name. So I have to follow that.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, let me check the sample input. For 90 degrees, 90 * pi/180 is pi/2, which is approximately 1.5707963267948966. So the assertion would pass.

But wait, the function is called radian_degree. So maybe the name is supposed to be degree_to_radian? But the problem says to write the function as radian_degree. So perhaps the name is correct as per the problem's instruction.

So the code is straightforward. Let me test it. Let's see, if I call radian_degree(90), it returns 90 * math.pi / 180. Which is math.pi / 2. And math.pi is approximately 3.141592653589793, so divided by 2 is 1.5707963267948966. Which matches the assertion.

So the code should be correct. Now, I need to make sure that the function is correctly named and that the code is properly formatted.

So the complete code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, the problem says to write the function. So that's all. The assertion would check that when you call radian_degree(90), it returns the correct value. So the code should work.

I think that's all. Let me check if there's any possible mistake. Oh, maybe the function should be called degree_to_radian, but the problem says to use radian_degree. So the code is correct as per the problem's instruction.
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
