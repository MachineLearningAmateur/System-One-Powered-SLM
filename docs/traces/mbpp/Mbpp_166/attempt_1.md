# Mbpp/166, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/166/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1133. Answer tokens: 118.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_even_pair that counts the number of pairs of integers in a list whose XOR is even. The assert statement says that for the list [5,4,7,2,1], the result should be 4. Let me think about how to approach this.

First, I remember that the XOR of two numbers is even if and only if both numbers are even or both are odd. Because even XOR even is even, and odd XOR odd is even. But even XOR odd is odd. So, the XOR result is even when the two numbers have the same parity (both even or both odd).

So, the problem reduces to counting the number of pairs where both numbers are even or both are odd. But wait, how do I count those pairs?

Let me think. Let's say I have a list of numbers. I can separate them into even and odd counts. Let's say even_count is the number of even numbers, odd_count is the number of odd numbers. Then, the number of pairs where both are even is (even_count choose 2), which is even_count * (even_count - 1) / 2. Similarly for the odd numbers. Then the total pairs is the sum of those two.

Wait, but what about the case where there are zero even and zero odd? Well, then the sum would be zero, which is correct.

So the steps would be:

1. Count the number of even and odd numbers in the list.
2. Calculate the combinations for even pairs and odd pairs.
3. Sum them and return the total.

But wait, let me check with the example given. Let's take the example list [5,4,7,2,1]. Let's see:

Numbers are 5 (odd), 4 (even), 7 (odd), 2 (even), 1 (odd). So even_count is 2 (4 and 2), odd_count is 3 (5,7,1).

So even pairs: 2 choose 2 is 1. Odd pairs: 3 choose 2 is 3. Total 1+3=4, which matches the assert. So that's correct.

So the approach is correct.

So the function would:

- Iterate through the list, count even and odd numbers.

Then compute the combinations.

So code steps:

Create a function find_even_pair that takes a list as input.

Initialize even_count and odd_count.

Then, for each number in the list, check if even or odd.

Then compute the combinations.

But how to compute combinations? For even_count, it's even_count * (even_count -1) // 2. Same for odd_count.

So the code would be:

def find_even_pair(nums):
    even_count = 0
    odd_count = 0
    for num in nums:
        if num % 2 == 0:
            even_count +=1
        else:
            odd_count +=1
    return (even_count * (even_count -1) // 2) + (odd_count * (odd_count -1) // 2)

Wait, but what if the list has only one element? Then even_count and odd_count would be 0 or 1. For example, if the list has one element, then the number of pairs is zero. Which is correct.

But let's test with the example. The example list has 5 elements. Even_count is 2, odd_count is 3. So 2*1/2 = 1, 3*2/2=3. Total 4. Correct.

So this code should work.

But wait, what about when there are zero even and zero odd? Like the list is empty? Well, the function returns 0, which is correct.

Another test case: list [2,4,6]. All even. even_count is 3. So 3*2/2 = 3. So the answer is 3. Which is correct, because there are 3 pairs: (2,4), (2,6), (4,6).

Another test case: list [1,3]. odd_count is 2. So 2*1/2 = 1. So answer is 1. Which is correct.

So the code seems correct.

So the code is as written. Now, the problem says to include any imports. But this code doesn't need any imports. So the code is:

def find_even_pair(nums):
    even_count = 0
    odd_count = 0
    for num in nums:
        if num % 2 == 0:
            even_count +=1
        else:
            odd_count +=1
    return (even_count * (even_count -1) // 2) + (odd_count * (odd_count -1) // 2)

But wait, the assert statement is given. Let me check the code again. The function is supposed to return the count. The assert is that find_even_pair([5,4,7,2,1]) ==4. Which the code returns.

So that's correct.

But wait, what about when the list has multiple elements with same parity? Like [2,2,2]. Then even_count is 3. So 3*2/2 = 3. Which is correct, since there are 3 pairs.

Yes.

So this code should work. So the answer is the code above.
```

</details>

**Code that ran:**

```python
def find_even_pair(nums):
    even_count = 0
    odd_count = 0
    for num in nums:
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
    return (even_count * (even_count - 1) // 2) + (odd_count * (odd_count - 1) // 2)

# Test case
assert find_even_pair([5, 4, 7, 2, 1]) == 4
```

**Visible-test report:**

```text
PASS    assert find_even_pair([5, 4, 7, 2, 1]) == 4
1 of 1 visible tests passed
```
