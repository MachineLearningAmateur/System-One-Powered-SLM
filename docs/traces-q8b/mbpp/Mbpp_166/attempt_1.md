# Mbpp/166, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/166/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 1089. Answer tokens: 83.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called find_even_pair that counts the number of pairs in a list which XOR to an even number. Let me think about how to approach this.

First, I remember that the XOR of two numbers is even if and only if both numbers are even or both are odd. Because XOR between two numbers depends on their binary representations. Let me think: the XOR result's least significant bit (LSB) determines if it's even or odd. For the LSB to be 0 (even), the two numbers must have the same LSB. Since even numbers end with 0 and odd with 1, so if both are even or both are odd, their XOR will be even.

So the problem reduces to counting all pairs of numbers that are both even or both odd.

Wait, right. So the approach is to count the number of even numbers and the number of odd numbers in the list. Then, the number of pairs is (number of even choose 2) + (number of odd choose 2). Because each pair of evens will XOR to even, same with odds.

So for example, if there are 3 even numbers, the number of pairs is 3*2/2 = 3. Similarly for odds.

So the steps are:

1. Iterate through the list and count how many even and odd numbers there are.
2. Calculate combinations for even and odd counts.
3. Sum them and return.

Let me test this logic with the sample input.

Sample input: [5,4,7,2,1]

Let's list the numbers:

5 is odd, 4 even, 7 odd, 2 even, 1 odd.

So even count is 2 (4 and 2). Odd count is 3 (5,7,1).

Number of even pairs: 2C2 = 1. Odd pairs: 3C2 = 3. Total is 1+3=4. Which matches the sample output. So that's correct.

So the function can be implemented by counting even and odd numbers, then compute (e*(e-1)//2) + (o*(o-1)//2).

So the code steps:

- Initialize even_count and odd_count to 0.
- Loop through each number in the input list.
- For each number, check if it's even or odd. Increment the respective count.
- Then calculate the combinations for even and odd counts.
- Return the sum.

Now, code-wise, how to implement this.

The function find_even_pair takes a list as input.

So code:

def find_even_pair(nums):
    even = 0
    odd = 0
    for num in nums:
        if num % 2 == 0:
            even +=1
        else:
            odd +=1
    return (even*(even-1)//2) + (odd*(odd-1)//2)

Wait, but what about the case when there are zero even or zero odd? Like, if all numbers are even, then the formula works. For example, if even is 0, then 0*(0-1)/2 is 0. Same for odd.

Yes, that's correct.

Testing the sample input:

even is 2, odd is 3.

2*1/2 = 1, 3*2/2 = 3. Sum is 4. Correct.

Another test case: if the list is [2,4,6], all even. Then even count is 3. So 3*2/2 = 3. Which is correct. The pairs are (2,4), (2,6), (4,6).

Another test case: [1,3,5]. All odd. So 3*2/2 = 3. Which is correct.

What if the list is empty? Well, the problem probably assumes that the list has at least two elements, but the code would return 0 in that case. But since the problem's sample has 5 elements, perhaps the function is supposed to handle any list.

So the code should work.

So the code is straightforward. Now, I need to write it in Python, with proper syntax.

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

Wait, but what about when the list has only one element? Then even or odd count is 1, and (1*0)/2 is 0. So the function returns 0, which is correct because there are no pairs.

So that's correct.

So the code should work. Let me check the sample input again. The sample input is [5,4,7,2,1], which gives even count 2, odd count 3. So 2*1//2 = 1, 3*2//2 =3. Sum is 4. Which matches the assertion.

So this code should be correct.
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
```

**Visible-test report:**

```text
PASS    assert find_even_pair([5, 4, 7, 2, 1]) == 4
1 of 1 visible tests passed
```
