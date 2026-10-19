# Mbpp/17, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/17/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 284. Answer tokens: 33.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that calculates the perimeter of a square based on its side length. The assert statement says that when the input is 10, the output should be 40. Let me think.

The perimeter of a square is calculated by adding all four sides. Since all sides are equal, the formula is 4 multiplied by the side length. So, if the side is s, perimeter is 4*s.

So the function should take a parameter, say, s, and return 4 * s. That's straightforward.

Wait, what about the imports? The problem says to include any necessary imports. But since this is a simple function, there's no need for any imports. The code will just be a function definition.

Let me structure the code. The function is called square_perimeter, takes one argument, side_length. Then returns 4 * side_length.

Testing with assert square_perimeter(10) == 40. That should work because 4*10 is 40.

So the code would be:

def square_perimeter(side_length):
    return 4 * side_length

Then, the assert statement checks if when 10 is passed, the result is 40. That's correct.

I think that's all. No imports needed. So the complete code is just that function and the assert.
```

</details>

**Code that ran:**

```python
def square_perimeter(side_length):
    return 4 * side_length

assert square_perimeter(10) == 40
```

**Visible-test report:**

```text
PASS    assert square_perimeter(10)==40
1 of 1 visible tests passed
```
