# Mbpp/166, attempt 2

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/166/a2/r1`)

Visible tests: **pass**. Thinking tokens: 1139. Answer tokens: 110.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_even_pair that counts the number of pairs of integers in a list whose XOR is even. The example given is that for the list [5, 4, 7, 2, 1], the result should be 4. Let me think about how to approach this.

First, I remember that the XOR of two numbers is even if and only if both numbers are even or both are odd. Because even XOR even is even, and odd XOR odd is even. But even XOR odd is odd. So, the XOR of two numbers is even when they have the same parity (both even or both odd).

So, the problem reduces to finding the number of pairs where both elements are even or both are odd. But wait, how do I count that?

Let me think. Let's say I have a list of numbers. I can separate them into even and odd counts. Let's say even_count is the number of even numbers, odd_count is the number of odd numbers. Then, the number of pairs where both are even is (even_count choose 2), which is even_count * (even_count - 1) / 2. Similarly for odd numbers. Then the total pairs would be the sum of these two.

Wait, but what about the case where there's only one even or one odd? Then the combination would be zero. So, for example, if even_count is 1, then the number of pairs is 0. Similarly for odd_count.

So the formula would be (even_count * (even_count - 1) // 2) + (odd_count * (odd_count - 1) // 2). That's the total number of pairs where XOR is even.

But wait, let me check with the example given. The example list is [5,4,7,2,1]. Let's count even and odd numbers.

5 is odd, 4 even, 7 odd, 2 even, 1 odd. So even_count is 2 (4 and 2), odd_count is 3 (5,7,1). Then the number of pairs is (2 choose 2) + (3 choose 2) = 1 + 3 = 4. Which matches the example. So that's correct.

So the function can be written by first counting the number of even and odd numbers, then calculating the combinations.

So the steps are:

1. Iterate through the list and count how many even and odd numbers there are.

2. Compute the combinations for even and odd counts.

3. Sum them and return the result.

Now, how to implement this in Python.

The function would be:

def find_even_pair(nums):
    even = 0
    odd = 0
    for num in nums:
        if num % 2 == 0:
            even +=1
        else:
            odd +=1
    return (even * (even -1) // 2) + (odd * (odd -1) // 2)

Wait, but what if the list has only one element? Then even and odd counts would be 0 or 1. For example, if the list has one element, then the number of pairs is zero. Which is correct.

Testing the example:

nums = [5,4,7,2,1]

even is 2, odd is 3. (2*1/2) + (3*2/2) = 1 + 3 = 4. Correct.

Another test case: if the list is [2, 4], even_count is 2, so (2*1/2) = 1. So the answer is 1. Which is correct because 2^4 is 6, which is even.

Another test case: [1, 3], even_count 0, odd_count 2. (0* -1 / 2) + (2*1/2) = 1. Which is correct, since 1^3 is 2, even.

So this seems to work.

So the code would be as above. But wait, what about when even_count is 0? Then the even part is 0. Similarly for odd_count.

So the code should handle all cases.

Now, the assert statement in the problem says that find_even_pair([5,4,7,2,1]) ==4. Which is correct.

So the code should be correct.

Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is straightforward.

So the final code is:

def find_even_pair(nums):
    even = 0
    odd = 0
    for num in nums:
        if num % 2 == 0:
            even +=1
        else:
            odd +=1
    return (even * (even -1) // 2) + (odd * (odd -1) // 2)

But wait, what about when even is 0 or odd is 0? For example, if the list has only even numbers, then even is 2, odd is 0. Then the code returns (2*1//2) + 0 = 1. Which is correct. Because the pair is two even numbers, their XOR is even.

Yes.

So this code should work. Let me check the example again. The code returns 4, which is correct.

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
