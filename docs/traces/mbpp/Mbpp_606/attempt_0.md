# Mbpp/606, attempt 0

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/606/a0/r1`)

Visible tests: **pass**. Thinking tokens: 795. Answer tokens: 56.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that converts degrees to radians. The user provided an example where radian_degree(90) should return 1.5707963267948966. Let me think about how to do this.

I remember that radians are calculated by multiplying degrees by π/180. So the formula is radians = degrees * (π / 180). But how do I implement this in Python?

First, I need to import math because π is a math constant. So I'll start by importing math. Then, the function will take a degree parameter. Let me define the function as def radian_degree(degrees):.

Wait, the example uses 90 degrees. Let me check: 90 * π / 180. Let me compute that. π is approximately 3.14159..., so 90 * 3.14159 / 180 is 1.570796... which matches the example. So that's correct.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

Wait, but what about floating point precision? The example shows 1.5707963267948966, which is more precise than the standard math.pi value. Let me check. math.pi is approximately 3.141592653589793, so 90 * math.pi / 180 is exactly 1.5707963267948966. So that's correct.

So the function is straightforward. Then, the assert statement would check that radian_degree(90) equals that value. But wait, in Python, when you do 90 * math.pi / 180, it's exactly 1.5707963267948966? Let me compute it.

Let me calculate 90 * math.pi / 180. Let me see: 90 divided by 180 is 0.5. So 0.5 * math.pi. math.pi is 3.141592653589793. So 0.5 * that is 1.5707963267948965. Which matches the example. So the function is correct.

So the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

Then, the assert statement would be:

assert radian_degree(90) == 1.5707963267948966

But wait, in Python, when you do 90 * math.pi / 180, it's a float. So the assert should work.

So putting it all together, the code would be:

import math

def radian_degree(degrees):
    return degrees * math.pi / 180

assert radian_degree(90) == 1.5707963267948966

But I need to make sure that the code is correct. Let me test it. For example, if I call radian_degree(180), it should return π, which is approximately 3.141592653589793. So 180 * math.pi / 180 is math.pi, which is correct.

Yes, this should work. So the code is correct.
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
