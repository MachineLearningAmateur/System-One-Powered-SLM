# Mbpp/244, attempt 4

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/244/a4/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 1224. Answer tokens: 452.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called next_Perfect_Square that takes a number and returns the next perfect square greater than it. Let's think about how to approach this.

First, what's a perfect square? It's a number that's the square of an integer. Like 36 is 6 squared, 25 is 5 squared, etc. So the task is to find the smallest number that is a perfect square and is larger than the given input.

Let me think about the steps. For example, if the input is 35, the next perfect square is 36. So how do I find that?

One approach is to find the square root of the given number, round it up to the next integer, and then square that. But wait, there's a catch. Let me see.

Let's take the example of 35. The square root of 35 is approximately 5.916. Rounding up gives 6. Then 6 squared is 36, which is correct.

Another example: if the input is 36, the next perfect square would be 49. But wait, the function needs to be greater than the given number. So if the input is exactly a perfect square, we need to find the next one. So for input 36, the next is 49.

So the steps would be:

1. Take the input number n.
2. Compute the square root of n. Let's call it sqrt_n.
3. Take the ceiling of sqrt_n. Because if the sqrt is not an integer, we need to round up to the next integer. For example, sqrt(35) is ~5.916, ceiling is 6.
4. Then square that ceiling value to get the next perfect square.

But how do I compute the ceiling of the square root in Python?

Well, in Python, I can use the math module. The math.isqrt function returns the integer square root, which is the floor of the actual square root. For example, math.isqrt(35) is 5. So if I take the integer square root of n, then add 1, and square it, that should give me the next perfect square.

Wait, let me test this logic.

For n=35:

sqrt_n = 5.916..., integer sqrt is 5. Adding 1 gives 6. Square is 36. Correct.

For n=36: integer sqrt is 6. Add 1 gives 7. Square is 49. Correct.

Another example: n=10. sqrt is ~3.16, integer sqrt is 3. Add 1 gives 4, square is 16. Correct.

What about n=1? The next perfect square is 4. So for n=1, the function would return 4. Which is correct.

So the steps are:

Compute the integer square root of n, then add 1, then square.

But how to compute the integer square root?

In Python, math.isqrt(n) returns the floor of the square root. So for example, math.isqrt(35) is 5. So adding 1 gives 6, then squared is 36.

So the code would be:

import math

def next_Perfect_Square(n):
    sqrt_n = math.isqrt(n)
    next_sqrt = sqrt_n + 1
    return next_sqrt * next_sqrt

Wait, but what if the input is 0? Well, 0 is a perfect square (0^2), but the next would be 1. So for n=0, the function returns 1. Which is correct.

Another test case: n=2. sqrt is 1.414, isqrt is 1. Add 1 gives 2, square is 4. Correct.

So this seems to work.

But let me check for n=1. math.isqrt(1) is 1. Adding 1 gives 2, square is 4. Which is correct.

So the code seems to handle all cases.

Now, the assert statement in the problem says that next_Perfect_Square(35) should be 36. Which the code would return.

So the code should be:

import math

def next_Perfect_Square(n):
    sqrt_n = math.isqrt(n)
    next_sqrt = sqrt_n + 1
    return next_sqrt * next_sqrt

But wait, what if the input is a perfect square? Like n=36. Then sqrt_n is 6, next_sqrt is 7, square is 49. Which is correct.

So this should work.

So the code is correct. Now, the problem says to include any necessary imports. The math module is needed, so we need to import math.

So the complete code would be:

import math

def next_Perfect_Square(n):
    sqrt_n = math.isqrt(n)
    next_sqrt = sqrt_n + 1
    return next_sqrt * next_sqrt

Then, the assert statement would be:

assert next_Perfect_Square(35) == 36

But the user wants the code to include the imports and the function. So the code block would be as above.

I think that's correct. Let me test with some examples.

Another test case: n=100. The next perfect square is 121. Let's see: math.isqrt(100) is 10. next is 11, square is 121. Correct.

Another test case: n=121. The next is 144. math.isqrt(121) is 11, next is 12, square is 144. Correct.

Yes, this should work.
```

</details>

**Code that ran:**

```python
import math

def next_Perfect_Square(n):
    sqrt_n = math.isqrt(n)
    next_sqrt = sqrt_n + 1
    return next_sqrt * next_sqrt

# Test case
assert next_Perfect_Square(35) == 36
```

**Visible-test report:**

```text
PASS    assert next_Perfect_Square(35) == 36
1 of 1 visible tests passed
```
