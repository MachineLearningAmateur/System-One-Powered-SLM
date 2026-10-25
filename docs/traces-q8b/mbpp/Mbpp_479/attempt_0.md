# Mbpp/479, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/479/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 948. Answer tokens: 38.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called first_Digit that takes a number and returns its first digit. Let's think about how to approach this.

First, the input can be a positive or negative number? Well, the example given is 123, which is positive. But the problem statement doesn't specify. However, the first digit of a negative number would be the first digit of its absolute value, right? Like first_Digit(-123) should be 1. But maybe the problem assumes the input is a positive integer. But the function should handle negatives as well, maybe.

Wait, the problem says "a given number"—so maybe it's an integer. Let's assume the input is an integer. So how to find the first digit.

One approach is to convert the number to a string, take the first character, and convert it back to an integer. But what about numbers like 0? Well, if the input is 0, the first digit is 0. But maybe the function is supposed to handle that.

But let's think about the steps. For example, for 123, converting to string gives "123", first character is '1', which is 1. For -123, converting to string gives "-123", so the first character is '-', which we don't want. So we need to take the absolute value first.

So the steps could be:

1. Take the absolute value of the number to handle negatives.
2. Convert to string.
3. Take the first character.
4. Convert back to integer.

But what if the number is 0? Then absolute value is 0, string is "0", first character is '0', which is correct.

Another approach is mathematical. For example, for a number n, while n >= 10, divide by 10. The remaining number is the first digit.

Wait, let's see. Let's take 123. 123 divided by 10 is 12.3, but integer division would be 12. Then 12 divided by 10 is 1. Then 1 divided by 10 is 0. So the loop would stop when n is 1. So the first digit is 1.

But for negative numbers, we can take absolute value first. So the steps would be:

def first_Digit(n):
    n = abs(n)
    while n >= 10:
        n = n // 10
    return n

Yes, that would work. Let's test this. For 123, n becomes 123 -> 12 -> 1. Then return 1. For 5, returns 5. For -456, abs is 456, then 45, then 4. So returns 4. That's correct.

So this approach seems better than converting to string, as it's more efficient and handles negatives correctly.

So the function can be written using this method.

Now, let's think about the case when the input is 0. The function returns 0, which is correct.

So the code would be:

def first_Digit(n):
    n = abs(n)
    while n >= 10:
        n = n // 10
    return n

But wait, what if the input is 0? Let's see: n is 0, the loop condition is 0 >=10? No. So returns 0. Correct.

Another example: first_Digit(123) returns 1. Which matches the assertion.

So the code should work.

Now, the problem says to write the function. So the code would be as above.

But let me check for some edge cases. For example, n=9, returns 9. n=10, returns 1. n=-10, returns 1. All correct.

So the code should work.

Therefore, the Python function can be written as such. Now, the problem says to include any imports. But this code doesn't need any imports. So the complete code is:

def first_Digit(n):
    n = abs(n)
    while n >= 10:
        n = n // 10
    return n

But wait, the problem says to write a function that returns the first digit. Let me check the assertion. The example given is first_Digit(123) == 1. Which works.

So this code should be correct.
```

</details>

**Code that ran:**

```python
def first_Digit(n):
    n = abs(n)
    while n >= 10:
        n = n // 10
    return n
```

**Visible-test report:**

```text
PASS    assert first_Digit(123) == 1
1 of 1 visible tests passed
```
