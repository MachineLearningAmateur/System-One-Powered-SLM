# Mbpp/801, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/801/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 845. Answer tokens: 57.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called test_three_equal that takes three integers as arguments and returns the count of how many of them are equal. Let's see. The example given is when all three are 1, the result is 3. So, if all three are the same, return 3. If two are the same, like 1,1,2, then return 2. If all are different, return 0.

Hmm, how to approach this. Let's think about the possible cases. The three numbers can be all equal, two equal and one different, or all different. So the function needs to check these scenarios.

Let me think about the logic. Let's say the three numbers are a, b, c. So first, check if a equals b and b equals c. If yes, then return 3. Otherwise, check if any two are equal. Like, if a equals b, or b equals c, or a equals c. But wait, if two are equal and the third is different, then the count is 2. But if all three are different, then 0.

Wait, but how to count? For example, if two are equal, then the count is 2. So the function should return the number of equal numbers. So if all three are same, 3. If two are same, 2. Else 0.

So the approach is: check if all three are equal. If yes, return 3. Else, check if any two are equal. If yes, return 2. Else return 0.

Wait, but what if two pairs are equal? Like, if all three are same, then all pairs are same. But that's already covered in the first condition. So the steps could be:

Check if a == b and b == c. If yes, return 3.

Else, check if a == b or b == c or a == c. If any of these is true, return 2.

Else return 0.

Yes, that seems right.

So let's code that.

So the function would be:

def test_three_equal(a, b, c):
    if a == b and b == c:
        return 3
    elif a == b or b == c or a == c:
        return 2
    else:
        return 0

Wait, but what about cases where two are same but the third is different. Like 1,1,2. Then the first condition is false, but the second condition is true. So returns 2. Which is correct.

Another example: 1,2,1. Then a == c is true, so returns 2.

Another case: 1,2,3. All different. Returns 0.

Another case: 2,2,2. Returns 3.

Yes, that seems to cover all cases.

So that's the code. Let me test the sample input. The assert test_three_equal(1,1,1) == 3. Which would return 3. Correct.

Another test case: test_three_equal(1,1,2) should return 2. And test_three_equal(1,2,3) returns 0. And test_three_equal(2,2,3) returns 2. All correct.

So the code should work. Now, I need to write this in Python. The function is called test_three_equal, and it takes three parameters. So the code would be as written above.

I think that's the correct approach. Let me think if there's any edge cases I'm missing. Like when two are same and the third is same as them. Wait, that's the first condition. So no problem.

Another case: 1, 2, 1. The code checks a == b? 1 == 2? No. Then checks if b == c (2 == 1? No). Then a == c (1 == 1? Yes). So returns 2. Correct.

Yes, that's right. So the code should work.
```

</details>

**Code that ran:**

```python
def test_three_equal(a, b, c):
    if a == b and b == c:
        return 3
    elif a == b or b == c or a == c:
        return 2
    else:
        return 0
```

**Visible-test report:**

```text
PASS    assert test_three_equal(1,1,1) == 3
1 of 1 visible tests passed
```
