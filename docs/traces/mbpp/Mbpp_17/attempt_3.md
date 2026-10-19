# Mbpp/17, attempt 3

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/17/a3/r1`)

Visible tests: **pass**. Thinking tokens: 218. Answer tokens: 33.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called square_perimeter that takes a side length as input and returns the perimeter. The perimeter of a square is calculated by 4 times the side length. So the function should be straightforward.

Wait, the assert statement says square_perimeter(10) should return 40. Let me check: 10 multiplied by 4 is 40. Yes, that's correct. So the function just needs to return 4 * side_length.

So the code would be something like:

def square_perimeter(side_length):
    return 4 * side_length

Then, the assert statement would check that when the function is called with 10, it returns 40. That's all. No imports are needed here because it's a simple function. So the complete code is just that function and the assert statement.

I should make sure there are no typos. Like, the function name is correct, the parameters are named correctly. Also, the return statement is correct. Yes, that's all.
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
