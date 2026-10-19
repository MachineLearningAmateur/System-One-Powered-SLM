# Mbpp/166, attempt 3

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/166/a3/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 936. Answer tokens: 110.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_even_pair that counts the number of pairs of integers in a list whose XOR is even. The assert statement says that when the input is [5,4,7,2,1], the output should be 4. Let me think about how to approach this.

First, I remember that XOR between two numbers has some properties. Let me recall: the XOR of two numbers is even if and only if both numbers are even or both are odd. Because if both are even, their XOR is even. If both are odd, their XOR is even. But if one is even and the other is odd, their XOR is odd. So, the key here is to find pairs where both numbers are even or both are odd.

So the problem reduces to counting the number of pairs in the list where both elements are even or both are odd. But wait, how do I count those pairs?

Let me think. Let's say I have a list of numbers. I can split them into two groups: even numbers and odd numbers. Then, the number of pairs that are both even is (count_even choose 2), and similarly for odd. The total number of such pairs would be the sum of those two.

Wait, yes. Because for even numbers, any pair of two even numbers will have an even XOR. Same for odd numbers. So the total number of pairs is (number of even numbers choose 2) + (number of odd numbers choose 2).

But wait, what about the case where there's only one even or one odd? Then, the choose 2 would be zero. So that's handled automatically.

So the steps would be:

1. Count the number of even numbers in the list.
2. Count the number of odd numbers in the list.
3. Compute the combinations for even and odd, sum them.

So for the example given: [5,4,7,2,1]

Even numbers are 4, 2 → count_even = 2. Odd numbers are 5,7,1 → count_odd = 3.

Then, (2 choose 2) is 1, (3 choose 2) is 3. Total 1+3=4, which matches the assert. So that's correct.

So the function can be implemented as follows.

Now, how to implement this in Python.

First, the function find_even_pair takes a list as input. Then, we can count the even and odd counts.

Then, compute combinations:

For even_count, the number of pairs is even_count * (even_count - 1) // 2.

Same for odd_count.

Sum them.

So the code would be:

def find_even_pair(nums):
    even = 0
    odd = 0
    for num in nums:
        if num % 2 == 0:
            even += 1
        else:
            odd += 1
    return (even * (even - 1) // 2) + (odd * (odd - 1) // 2)

Wait, but what if the list is empty? Well, the code would return 0, which is correct. But the problem says "pairs of integers in a list"—so if the list has less than two elements, there are zero pairs. Which is handled by the formula.

So that's the code. Let me test with the example.

Test case: [5,4,7,2,1]

even = 2, odd = 3. (2*1/2) + (3*2/2) → 1 + 3 =4. Correct.

Another test case: [1,3]. even=0, odd=2. (0* -1 /2) + (2*1/2) → 1. So the answer is 1. Which is correct because the pair (1,3) has XOR 2, which is even.

Another test case: [2,4,6]. even count is 3. (3*2/2) =3. So the answer is 3. Which is correct.

So this code should work.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is straightforward.

So the final code is as written above. Let me check for possible errors.

Wait, what about when the list has zero elements? Well, the function returns 0, which is correct.

So the code is correct.
```

</details>

**Code that ran:**

```python
def find_even_pair(nums):
    even = 0
    odd = 0
    for num in nums:
        if num % 2 == 0:
            even += 1
        else:
            odd += 1
    return (even * (even - 1) // 2) + (odd * (odd - 1) // 2)

# Test case
assert find_even_pair([5, 4, 7, 2, 1]) == 4
```

**Visible-test report:**

```text
PASS    assert find_even_pair([5, 4, 7, 2, 1]) == 4
1 of 1 visible tests passed
```
