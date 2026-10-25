# Mbpp/17, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/17/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 437. Answer tokens: 31.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called square_perimeter that takes a side length as input and returns the perimeter of a square. Let me think. Oh right, the perimeter of a square is calculated as 4 times the side length. Because a square has four equal sides.

So the function should multiply the input by 4. Let me check the example given. The assert statement says square_perimeter(10) should equal 40. 10 multiplied by 4 is indeed 40. That makes sense.

Wait, what about the parameters? The function needs to take one parameter, which is the side length. So the function definition would be def square_perimeter(side): and then return side * 4.

I don't think there are any edge cases here. The problem probably expects a straightforward solution. Let me make sure there are no typos. Oh right, the function name is square_perimeter, and the input is the side. So the code should be simple.

Let me write the code. First, the function definition. Then return the calculation. Then the assert statement. But the user wants the code to include the function and the assert. Wait, the problem says to write the function, and the assert is part of the test case. So the code should include the function and the assert statement.

Wait, but in Python, the assert is part of the code. So the code should have the function and then the assert. Let me put it all together.

So the code would be:

def square_perimeter(side):
    return side * 4

assert square_perimeter(10) == 40

But wait, the user might want the code to be in a code block. Also, do I need any imports? The problem says to include any imports it needs. But since this is a simple function, no imports are needed. So the code is as above.

Let me check again. The function returns 4 times the side. The assert checks that when the side is 10, the result is 40. That's correct. So this should work.
```

</details>

**Code that ran:**

```python
def square_perimeter(side):
    return side * 4

assert square_perimeter(10) == 40
```

**Visible-test report:**

```text
PASS    assert square_perimeter(10)==40
1 of 1 visible tests passed
```
