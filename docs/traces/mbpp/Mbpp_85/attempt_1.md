# Mbpp/85, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/85/a1/r1`)

Visible tests: **pass**. Thinking tokens: 853. Answer tokens: 67.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function to calculate the surface area of a sphere. Let me think. The formula for the surface area of a sphere is 4πr², right? So the function needs to take the radius as an input and compute that.

Wait, the user provided an example where the radius is 10. Let me check what the expected output is. The example says surfacearea_sphere(10) should return 1256.6370614359173. Let me compute that with radius 10. 

Calculating 4 * π * (10)^2. 10 squared is 100. Multiply by 4 gives 400. Then 400 * π. Let me compute that. π is approximately 3.141592653589793. So 400 * π is about 1256.6370614359173. Which matches the example. So the formula is correct.

So the function should take radius as a parameter. Let me think about the imports. I need to import math, because the formula uses π. So the code will have import math, then the function.

Wait, the function is called surfacearea_sphere, and it takes a single argument, which is the radius. So the code would be:

def surfacearea_sphere(radius):
    import math
    return 4 * math.pi * radius ** 2

But wait, maybe it's better to use math.pi directly. So the code would be:

import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

Yes, that's better. Because math.pi is a constant, and using it is more efficient. So the function is straightforward.

Now, the assert statement checks that when the function is called with 10, it returns the correct value. The assert uses math.isclose, which checks if the result is close to the expected value. The rel_tol is 0.001, which is 0.1% relative tolerance. So the code should work.

So the complete code would be:

import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

Then, the assert statement. But the user wants the code to include the imports. So the code should have the import statement and the function.

Wait, the user says to write a correct Python solution, including any imports. So the code should have the import math, and the function.

So the code would be:

import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

Then, the assert statement. But the user's example is an assert statement. So the code should include that.

Wait, the problem says to write a function and then the assert. So the code would be:

import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)

But the user's example shows that the assert is part of the code. So the code should include that.

So putting it all together, the code is:

import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)

Wait, but the function is called surfacearea_sphere, and the assert is checking that. So that's correct.

I think that's all. The code should work. Let me check for possible errors. For example, if radius is not a number, but the problem says to assume it's a valid radius. So the function is correct.

Yes, this should be the correct solution.
```

</details>

**Code that ran:**

```python
import math

def surfacearea_sphere(radius):
    return 4 * math.pi * radius ** 2

assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)
```

**Visible-test report:**

```text
PASS    assert math.isclose(surfacearea_sphere(10), 1256.6370614359173, rel_tol=0.001)
1 of 1 visible tests passed
```
