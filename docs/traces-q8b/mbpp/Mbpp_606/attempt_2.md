# Mbpp/606, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 682. Answer tokens: 27.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called radian_degree that converts degrees to radians. Wait, wait, the function name is a bit confusing. Oh right, the problem says to convert degrees to radians, but the function is named radian_degree. Maybe that's a typo? Or maybe it's supposed to return radians when given degrees. Let me check the assertion. The example given is radian_degree(90) should equal approximately 1.5707963267948966. Oh right, 90 degrees in radians is π/2, which is about 1.5708. So the function takes a degree value and returns the equivalent in radians.

So the formula to convert degrees to radians is radians = degrees * (π / 180). So I need to multiply the input by π divided by 180. But how to get π in Python? Oh right, the math module has math.pi.

So the steps are: import math, then define the function, take the degrees as input, multiply by math.pi / 180, and return that value.

Wait, but the function is named radian_degree. Maybe that's a mistake in the problem statement? Like maybe it should be degree_to_radian? But the user provided the assertion as radian_degree(90) == ... So I have to follow that function name.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, let me check the sample input. For 90 degrees, 90 * π/180 is π/2, which is approximately 1.5707963267948966. So the assertion would pass.

But wait, the function is called radian_degree. Maybe the problem statement has a typo, but the user provided that assertion, so I need to make sure the function name is exactly as given.

So the code should be as above. Let me test it. Let me think: math.pi is approximately 3.141592653589793. So 90 * math.pi / 180 is (90/180)*pi = 0.5 * pi, which is pi/2. The value of pi/2 is approximately 1.5707963267948966, which matches the assertion. So the code should work.

So the complete code would include the import math, the function definition, and the return statement. The user's assertion is covered by this function.

So the code is:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

But wait, the problem says to write the function. So that's the code. But maybe the function is supposed to be called something else? But according to the problem statement, the function is named radian_degree. So that's correct.

I think that's all. Let me make sure there are no typos. Oh, the function name is radian_degree, which is correct. So the code should be as written.
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
