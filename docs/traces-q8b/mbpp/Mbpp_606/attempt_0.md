# Mbpp/606, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/606/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 802. Answer tokens: 29.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called radian_degree that converts degrees to radians. Wait, wait, the function name is a bit confusing. Oh right, the problem says to convert degrees to radians, so the function is supposed to take a degree value and return the equivalent in radians.

Wait, the sample assertion is radian_degree(90) equals approximately 1.5707963267948966. Let me check what that number is. Oh right, π/2 is approximately 1.5708, and since 90 degrees is π/2 radians. So the function is correctly converting degrees to radians.

So the formula for converting degrees to radians is radians = degrees * (π / 180). So I need to use the math.pi constant for that.

So the steps are: import math, then multiply the input degrees by math.pi / 180.0.

Wait, but the function is named radian_degree. Wait, maybe that's a typo? Because the function is converting degrees to radians. So maybe the function is supposed to be called degree_to_radian? But the problem says the function is called radian_degree. Hmm, maybe it's a mistake in the problem statement, but I have to follow the given function name.

So the function is named radian_degree, but it's supposed to convert degrees to radians. So the function takes a degree value and returns radians. So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180.0

Wait, but let me check the sample input. For 90 degrees, 90 * π/180 is π/2, which is approximately 1.5707963267948966. So that's correct.

But wait, in Python, math.pi is a float. So when you do 90 * math.pi / 180, it's the same as 90 * π / 180, which is π/2. So the code should work.

So the function is straightforward. But I need to make sure that the function is named exactly as specified, and that the code includes the necessary import.

So the complete code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180.0

But wait, maybe the problem expects the function to be called something else? Let me check the problem again. The user says the function is called radian_degree, and the assertion is radian_degree(90) == 1.5707963267948966. So the function name is correct as given.

So the code should be as above. Let me test it. For example, math.pi is approximately 3.141592653589793. So 90 * math.pi / 180 is 1.5707963267948966, which matches the assertion. So that's correct.

So the code should be written with that function. Also, the problem says to write the function and include any imports. So the code will have the import math statement.

So the final code is:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180.0

Wait, but maybe the problem expects the function to be called something else, but according to the problem statement, the function is named radian_degree. So that's correct.

I think that's the solution. Let me make sure there are no typos. Also, the function is supposed to return the correct value. So the code should work.
```

</details>

**Code that ran:**

```python
import math

def radian_degree(degrees):
    return degrees * math.pi / 180.0
```

**Visible-test report:**

```text
PASS    assert radian_degree(90)==1.5707963267948966
1 of 1 visible tests passed
```
