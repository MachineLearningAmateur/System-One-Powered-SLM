# Mbpp/415, attempt 2

2 rounds; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/415/a2/r1`)

Visible tests: **fail**. Hidden tests: **❌ fail**. Thinking tokens: 7208. Answer tokens: 205.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that finds a pair of integers in an array that gives the highest product. The example given is when the input is [1,2,3,4,7,0,8,4], the output should be (7,8). Let me think about how to approach this.

First, the problem is to find two numbers in the array such that their product is maximum. But how do I do that efficiently?

Hmm, the straightforward way would be to check all possible pairs, calculate their products, and keep track of the maximum. But for a large array, that would be O(n²) time, which might not be efficient. However, maybe for the problem's constraints, it's acceptable. But maybe there's a smarter way.

Wait, the maximum product can be either the product of the two largest numbers or the product of the two smallest (which could be negative numbers, leading to a positive product). For example, if the array has two large negatives, their product would be a large positive. So, the maximum product could be either the product of the two largest numbers or the product of the two smallest (most negative) numbers.

So, the optimal approach would be to find the top two largest numbers and the two smallest numbers, then compare their products. That way, we can find the maximum product in O(n) time.

Let me think about that. For example, in the given sample input, the two largest numbers are 8 and 7, product is 56. The two smallest are 0 and 1, product is 0. So the maximum is 56, which is correct. But if there were two negative numbers, say [-10, -5, 1, 2], then the maximum product would be (-10)*(-5)=50, which is larger than 1*2=2.

So, the plan is:

1. Find the two largest numbers in the array.
2. Find the two smallest numbers in the array.
3. Compute the product of the two largest and the product of the two smallest.
4. Return the pair with the maximum product.

But wait, what if the array has only two elements? Then the pair is those two. Also, what if the array has more than two elements but the two largest are positive, and the two smallest are negative? Then the maximum product is between the two largest or the two smallest.

So, the steps would be:

- Find the two largest numbers (max1, max2)
- Find the two smallest numbers (min1, min2)
- Compare the products (max1*max2) vs (min1*min2)
- The maximum of these two is the answer.

But then, how to find the two largest and two smallest numbers?

One way is to sort the array. But sorting would take O(n log n) time. However, if we can find them in O(n) time, that's better. For example, in a single pass, track the two largest and two smallest numbers.

Let me think about how to do that.

For the two largest numbers:

Initialize max1 and max2. Initially, set them to negative infinity. Then iterate through each number. For each number, if it's greater than max1, then update max2 to be max1, and max1 to be the current number. Else if it's greater than max2, update max2. Similarly for the two smallest numbers, but with min1 and min2, and checking if the current number is less than min1, etc.

But wait, what if there are duplicates? Like in the sample input, there are two 4s. But that's okay, since the code would handle them.

So, the plan is:

- Iterate through the array once to find the two largest and two smallest numbers.
- Then compute the products of the two largest and the two smallest.
- Compare these two products, and select the pair with the higher product.

But wait, what if there are more than two elements? For example, if the array has three elements, like [a, b, c], then the two largest are a and b, and the two smallest are a and b. But maybe the product of the two largest is the maximum.

But in any case, the approach should work.

Now, let's think about the sample input:

[1,2,3,4,7,0,8,4]

The two largest are 8 and 7. Their product is 56.

The two smallest are 0 and 1. Their product is 0. So the maximum is 56, so the pair is (7,8). Which matches the sample.

Another example: [-10, -5, 1, 2]. The two largest are 2 and 1, product 2. The two smallest are -10 and -5, product 50. So the answer is (-10,-5).

Another example: [-5, -4, -3, -2]. The two largest are -2 and -3, product 6. The two smallest are -5 and -4, product 20. So the answer is (-5,-4).

So, the code needs to compare the two products and choose the pair accordingly.

But then, how to handle when the array has only two elements? For example, [3,5]. Then the two largest are 5 and 3, product 15. The two smallest are 3 and 5, same product. So the pair is (3,5).

So, the code can proceed with this approach.

Now, the steps for the code:

1. Find the two largest numbers (max1, max2) and two smallest (min1, min2).

But how to handle if the array has less than two elements? Well, the problem says it's an array of integers, but the function needs to find a pair. So the input array must have at least two elements. The assert statement in the example has 8 elements. So the function can assume that the input array has at least two elements.

So, proceed.

Now, code steps:

Initialize max1, max2, min1, min2.

Initially, set max1 and max2 to negative infinity. Similarly for min1 and min2 to positive infinity.

Then iterate through each number in the array:

For each number in the array:

- Check if the number is greater than max1. If so, then set max2 to max1, and max1 to the number.

- Else if the number is greater than max2, then set max2 to the number.

Similarly for the min1 and min2:

- Check if the number is less than min1. If so, set min2 to min1, and min1 to the number.

- Else if the number is less than min2, set min2 to the number.

Wait, but what if the array has duplicates? For example, if the array is [5,5], then max1 is 5, max2 is 5. Similarly for min1 and min2.

But that's okay.

Once we have all four values, compute product1 = max1 * max2, product2 = min1 * min2.

Compare product1 and product2. The maximum between them is the answer.

But wait, what if the array has more than two elements, but the maximum product is between max1 and max2, but there are other pairs that could have higher product? For example, if the array has three elements, say [10, 2, 3]. Then the two largest are 10 and 3, product 30. The two smallest are 2 and 3, product 6. So the maximum is 30. But what if there's another pair, like 10 and 2? 20, which is less. So the code works.

But what if the array has three elements, like [10, -10, 2]. Then the two largest are 10 and 2, product 20. The two smallest are -10 and 2, product -20. So the maximum is 20. But the maximum product is actually 10 * -10 = -100, which is not. Wait, no. Wait, in this case, the maximum product is between the two largest numbers (10 and 2) which is 20. But the two smallest are -10 and 2. So the product is -20. So the maximum is 20. But what if the array has two negative numbers and a positive?

Wait, for example, [-10, -5, 3]. The two largest are 3 and -5. Product is -15. The two smallest are -10 and -5. Product is 50. So the maximum is 50. So the code would choose that.

So the code would correctly find that.

So, the code needs to compare the product of the two largest and the product of the two smallest. Then choose the pair with the higher product.

But then, how to handle when the array has multiple pairs with same product?

For example, if the array is [3, 4, 5, 6], then the two largest are 6 and 5, product 30. The two smallest are 3 and 4, product 12. So the answer is (5,6).

But what if the array is [5,5,5,5], then the product is 25, and the code would return (5,5) as the pair.

But how to handle the case where the two largest are same as the two smallest? For example, [ -5, -5, 5,5]. The two largest are 5 and 5 (product 25), the two smallest are -5 and -5 (product 25). So the maximum is 25. So the code would return either pair. But the problem says to return the pair with the highest product. But in this case, both pairs have same product. So which one to return?

The problem's example returns (7,8) which are the two largest. So perhaps, in case of a tie, we can return the pair with the two largest numbers. Or perhaps, the code can compare the products and if they are equal, return the pair with the two largest numbers. But the problem's sample expects the pair of the two largest numbers. So perhaps, in the case of a tie, the code can return the pair of the two largest numbers.

But how to handle that? Well, the code would compare the products. If product1 is equal to product2, then which pair to return? Well, the problem's sample returns (7,8) which is the pair of the two largest numbers. So perhaps, in the case of a tie, we can return the pair of the two largest numbers.

But how to handle that in code?

So, the code would compute product1 and product2. Then compare them. If product1 is greater than product2, then the pair is (max1, max2). If product2 is greater, then the pair is (min1, min2). If they are equal, then which one to choose? For example, if the array is [ -5, -5, 5,5], then product1 is 25 and product2 is 25. So the code would return either pair. But the problem's sample expects the pair with the two largest numbers. So perhaps, in that case, we can return the pair of the two largest numbers.

So, in code, after comparing product1 and product2, if they are equal, we can choose the pair (max1, max2) or (min1, min2). But how to decide which one?

But the problem's example expects the pair with the two largest numbers. So perhaps, in the case of a tie, the code can return the pair with the two largest numbers. So, the code can compare the products, and if they are equal, then return the pair (max1, max2).

So, in code:

if product1 > product2:

    return (max1, max2)

elif product2 > product1:

    return (min1, min2)

else:

    return (max1, max2)  # or (min1, min2) ?

But in the case of a tie, which pair to return? Well, the problem's sample returns the pair of the two largest. So perhaps, in that case, the code can return (max1, max2) as the pair.

But perhaps, the code should return the pair with the highest product, but if there are multiple pairs with the same product, which one to choose? The problem's example returns (7,8), which are the two largest. So perhaps, in the case of a tie, we can return the pair of the two largest numbers.

So, the code can proceed as such.

Now, the next step is to implement this in Python.

But how to find the two largest and two smallest numbers?

Let me think about the code for that.

Initialize:

max1 = max2 = -infinity

min1 = min2 = +infinity

Then, for each number in the array:

if number > max1:

    max2 = max1

    max1 = number

elif number > max2:

    max2 = number

Similarly for the min1 and min2:

if number < min1:

    min2 = min1

    min1 = number

elif number < min2:

    min2 = number

But wait, what if the array has only one element? Well, the problem says that the input is an array of integers, and the function is supposed to find a pair. So the input array must have at least two elements.

But during the code, for example, if the array is [5, 5], then max1 is 5, max2 is 5. min1 is 5, min2 is 5.

So, the code would compute product1 as 25, product2 as 25. Then return (max1, max2) which is (5,5).

So, that's correct.

Now, let's code this.

But how to handle the initial values? For example, for the first element, the code would compare.

Let me think about the code:

def max_product(arr):

    # find max1, max2, min1, min2

    max1 = max2 = float('-inf')

    min1 = min2 = float('inf')

    for num in arr:

        # update max1 and max2

        if num > max1:

            max2 = max1

            max1 = num

        elif num > max2:

            max2 = num

        # update min1 and min2

        if num < min1:

            min2 = min1

            min1 = num

        elif num < min2:

            min2 = num

    # compute products

    product1 = max1 * max2

    product2 = min1 * min2

    if product1 > product2:

        return (max1, max2)

    else:

        return (min1, min2)

Wait, but in the sample input, the code would return (8,7) or (7,8)? Because max1 is 8 and max2 is 7. So the code returns (max1, max2) which is (8,7). But the sample expects (7,8). But the assert is (7,8). So the order of the pair matters?

Wait, the sample says that the assert is (7,8). But according to the code, the pair would be (8,7). But the product is same. So, the problem's assertion may not be checking the order. Wait, but the sample's assertion is (7,8). But the code returns (8,7). However, in Python, tuples are ordered, so (8,7) and (7,8) are different. So this would cause the assert to fail.

Wait, that's a problem. Because the sample expects (7,8), but the code would return (8,7). So the code would not pass the test case.

So, what's the issue here?

The problem says that the function should return the pair with the highest product. However, the order of the pair may not matter, but the sample expects (7,8). So perhaps the code should return the pair in the order of the two numbers, but in the sample, the two numbers are 7 and 8, and the code returns (8,7). Which is a different tuple. So the assert would fail.

So, the code needs to return the pair in the correct order. But how?

Wait, the sample input is [1,2,3,4,7,0,8,4]. The two largest numbers are 8 and 7. So the code returns (max1, max2) which is 8 and 7. But the sample expects (7,8). So the code would return (8,7), which is not matching the sample.

So, the code's current approach would not pass the sample.

Ah, so the problem is that the order of the pair is important. But why does the sample expect (7,8) instead of (8,7)?

Well, perhaps the problem expects the pair to be in the order of the numbers as they appear in the array, but that's not possible. Or perhaps the problem expects the pair to be ordered in ascending order. But the sample shows that (7,8) is the expected output, but the code returns (8,7). So the code would not pass the test.

So, how to handle this?

The problem's assertion is that max_product([1,2,3,4,7,0,8,4]) == (7,8). So the code must return (7,8) as the pair. But according to the code's current approach, it returns (8,7). So the code is wrong.

So, what's the issue here?

The code's approach is to return the pair (max1, max2), but the max1 is the largest, and max2 is the second largest. So, in the sample, the max1 is 8, max2 is 7. So the code returns (8,7). But the sample expects (7,8). So the code's output is different from the sample's expected output.

So, this is a problem. How to resolve this?

The problem may not care about the order of the pair, but the sample's assertion is written in that way. So, perhaps the code should return the pair in ascending order.

But how can we ensure that?

In the sample, the pair is (7,8). So, the code should return the pair in ascending order. So, perhaps the code should return the pair sorted in ascending order.

So, in the code, after finding the pair (max1, max2), we can sort them and return as a tuple. Or, in the case of product2 being larger, sort the min1 and min2.

But how?

For example, in the sample, the code would return (8,7) as the pair. But the sample expects (7,8). So, the code should return the pair sorted.

So, the code should return the pair in ascending order. So, the code should return (min of the two, max of the two).

So, for the code, after determining which pair to return, we can sort the pair and return as a tuple.

So, for example:

if product1 is larger, then the pair is (max1, max2), but sorted. So, (min(max1, max2), max(max1, max2)).

Wait, but max1 is larger than max2. So, the pair (max1, max2) would be (8,7). So, sorted, it's (7,8).

Similarly, if the pair is (min1, min2), which is (0,1), then sorted is (0,1).

So, the code should return the pair sorted.

So, the code should return the pair in sorted order.

But how to do that?

So, in the code, after determining which pair to return, we need to sort the two numbers and return them as a tuple.

So, in the code:

if product1 > product2:

    return tuple(sorted([max1, max2]))

else:

    return tuple(sorted([min1, min2]))

But in the sample, this would return (7,8), which matches the sample.

So, this would fix the problem.

But what about when the two numbers are the same, like [5,5], then sorted would return (5,5), which is correct.

So, the code needs to sort the pair before returning.

So, the code needs to be modified to sort the pair.

So, the code would be:

def max_product(arr):

    # find max1, max2, min1, min2

    max1 = max2 = float('-inf')

    min1 = min2 = float('inf')

    for num in arr:

        # update max1 and max2

        if num > max1:

            max2 = max1

            max1 = num

        elif num > max2:

            max2 = num

        # update min1 and min2

        if num < min1:

            min2 = min1

            min1 = num

        elif num < min2:

            min2 = num

    # compute products

    product1 = max1 * max2

    product2 = min1 * min2

    if product1 > product2:

        return tuple(sorted([max1, max2]))

    else:

        return tuple(sorted([min1, min2]))

Wait, but in the case where product1 is equal to product2, which pair to return? For example, if the array is [-5, -5, 5,5], then product1 is 25 and product2 is 25. So, the code would return the sorted pair of max1 and max2, which is (5,5). But the other pair is (-5,-5), which is also sorted. But the code would return (5,5) in this case. Which is correct? Well, the problem's sample expects the pair with the highest product, but if there are multiple pairs with same product, which one to return? The problem's sample returns the pair of the two largest numbers. So, perhaps, in this case, the code is correct.

But in the case where the product1 and product2 are equal, which pair to return? Well, the code returns the pair from the max1 and max2. Which is the pair of the two largest numbers. Which would be correct.

So, the code now would return the pair sorted in ascending order.

Let's test the sample input.

Sample input: [1,2,3,4,7,0,8,4]

max1 is 8, max2 is 7. product1 is 56.

min1 is 0, min2 is 1. product2 is 0. So product1 is larger. So, the code returns sorted([8,7]) which is (7,8). Which matches the sample. So the code would pass the test.

Another example: [-10, -5, 1, 2]. The two largest are 2 and 1. product is 2. The two smallest are -10 and -5. product is 50. So code returns sorted([-10,-5]) which is (-10,-5). Which is correct.

Another example: [-5, -4, -3, -2]. The two largest are -2 and -3. product is 6. The two smallest are -5 and -4. product is 20. So code returns sorted([-5,-4]) which is (-5,-4).

Another example: [5,5]. The code returns (5,5).

Another example: [3, 4, 5, 6]. The code returns (5,6).

Another example: [ -10, -5, 2, 3]. The two largest are 3 and 2. product is 6. The two smallest are -10 and -5. product is 50. So code returns (-10,-5).

So, the code seems to handle all these cases.

Now, what about if the array has two elements?

For example, [3,5]. The code returns (3,5), which is correct.

Another case: [5,3]. The code returns (3,5).

So, the code seems to handle that.

But what about if the array has more than two elements, and the two smallest are negative, but the two largest are positive, but the product of the two smallest is larger than the product of the two largest?

Yes, like the example [-10, -5, 1, 2]. The code returns the pair (-10,-5).

So, the code is correct.

Now, the code is written. Let's code it in Python.

But also, need to handle the case when the array has only two elements. For example, [3,5], then the code returns (3,5).

Now, the code can be written.

But what about when the array has multiple elements, but the two largest are the same as the two smallest? Like [ -5, -5, 5,5]. The code returns (5,5) as the pair.

But what if the array is [ -5, -5, 5, 5, 3]. The two largest are 5 and 5. product is 25. The two smallest are -5 and -5. product is 25. So code returns (5,5).

So, the code returns (5,5) in that case.

So, the code is correct.

Now, the code should handle all cases.

Now, the code in Python:

def max_product(arr):
    max1 = max2 = float('-inf')
    min1 = min2 = float('inf')
    for num in arr:
        # Update max1 and max2
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2:
            max2 = num
        # Update min1 and min2
        if num < min1:
            min2 = min1
            min1 = num
        elif num < min2:
            min2 = num
    product1 = max1 * max2
    product2 = min1 * min2
    if product1 > product2:
        return tuple(sorted([max1, max2]))
    else:
        return tuple(sorted([min1, min2]))

But wait, what if the array has only two elements, say [5, 3], then the code would return (3,5) which is correct.

Testing the sample input:

arr = [1,2,3,4,7,0,8,4]

max1 is 8, max2 is 7. product1 is 56.

min1 is 0, min2 is 1. product2 is 0. So returns (7,8).

Which matches the sample.

So, the code should work.

Now, the code needs to be written with the assert statement as per the problem's example.

But the problem says to write a function, and the assert is given.

So, the code should be written as a function, and the assert is part of the test.

So, the complete code would be:

import sys

def max_product(arr):
    max1 = max2 = float('-inf')
    min1 = min2 = float('inf')
    for num in arr:
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2:
            max2 = num
        if num < min1:
            min2 = min1
            min1 = num
        elif num < min2:
            min2 = num
    product1 = max1 * max2
    product2 = min1 * min2
    if product1 > product2:
        return tuple(sorted([max1, max2]))
    else:
        return tuple(sorted([min1, min2]))

# Test case
assert max_product([1,2,3,4,7,0,8,4]) == (7,8)

But wait, the code may have a problem if the array has only one element. But the problem says that the input is an array of integers, and the function is supposed to find a pair. So the input array has at least two elements. So the code can assume that.

But what about if the array has two elements, like [1,2], the code returns (1,2) which is correct.

Another test case: [-10, -5, 1, 2] should return (-10,-5).

Another test case: [ -5, -4, -3, -2 ] returns (-5,-4).

Another test case: [5,5] returns (5,5).

Another test case: [1, -2, -3, 4] returns (4,-3) ?

Wait, let's compute:

The array is [1, -2, -3,4].

The two largest are 4 and 1. product is 4*1=4.

The two smallest are -3 and -2. product is 6. So the code returns (-3,-2) sorted as (-3,-2) which is the pair with higher product.

So the code returns (-3,-2).

Yes.

So the code seems correct.

Now, the code is written. The function is called max_product, and the assert is included.

But the problem says to write the function, and the assert is part of the test.

So, the code should include the function and the assert.

But the problem says to write the code in one code block, including any imports. However, the code does not need any imports. So, the code is as written.

But in the code, the function is written, and the assert is included.

But the problem says that the user should write the code that passes the given assert. So the code should be written as a function, and the assert is part of the code.

So, the code as written should be correct.

Now, the code is written. Let me check for possible errors.

Wait, in the code, when initializing min1 and min2, for the first element, if the array has only two elements, like [5,3], then during the first iteration, num is 5. For min1, it is initially inf. So, 5 < inf, so min2 becomes inf, and min1 becomes 5. Then, next number is 3. For min1, 3 < 5. So min2 is set to 5, min1 is set to 3. Then, after processing all elements, min1 is 3, min2 is 5. So product2 is 3*5=15. product1 is 5*3=15. So the code returns sorted([3,5]) which is (3,5). Which is correct.

But in this case, the code would return (3,5) which is correct.

So, the code is correct.

Another possible case: [ -5, 0, 0, 0 ].

The two largest are 0 and 0. product is 0. The two smallest are -5 and 0. product is 0. So code returns sorted([0,0]) which is (0,0). Which is correct.

Another case: [ -5, 0, 0, 1 ].

The two largest are 1 and 0. product is 0. The two smallest are -5 and 0. product is 0. So code returns (0,0) or (0,1) ?

Wait, product1 is 1*0=0. product2 is -5*0=0. So the code returns the pair from product1, which is (0,1). sorted is (0,1). But the pair (0,0) is also a valid pair. But the code returns (0,1) because product1 is equal to product2? Or how does the code choose?

Wait, in this case, product1 is 0 and product2 is 0. So the code returns the pair from product1, which is (0,1). But the pair (0,0) has the same product. But the code returns (0,1), which is correct? Or is there a mistake here?

Wait, the code compares product1 and product2. If product1 is equal to product2, then the code returns the pair from product1, which is the two largest. So, in this case, the code would return (0,1). But the pair (0,0) has the same product. So, which pair is considered the correct one?

The problem says to return the pair with the highest product. Since both pairs have the same product, the code returns the pair of the two largest numbers. But the problem's sample expects the pair of the two largest numbers. So, the code's approach is correct.

But in this case, the pair (0,1) has the same product as (0,0), but the code returns (0,1). But which pair is correct? The problem may not specify, but the code is correct as per the approach.

So, the code is correct.

So, the code is correct.

Now, the code should be written as per the problem's instruction. The code includes the function and the assert statement.

So, the final code is as written above.
```

</details>

**Code that ran:**

```python
def max_product(arr):
    max1 = max2 = float('-inf')
    min1 = min2 = float('inf')
    for num in arr:
        # Update max1 and max2
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2:
            max2 = num
        # Update min1 and min2
        if num < min1:
            min2 = min1
            min1 = num
        elif num < min2:
            min2 = num
    product1 = max1 * max2
    product2 = min1 * min2
    if product1 > product2:
        return tuple(sorted([max1, max2]))
    else:
        return tuple(sorted([min1, min2]))

# Test case
assert max_product([1,2,3,4,7,0,8,4]) == (7,8)
```

**Visible-test report:**

```text
ERROR   assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
        NameError: name 'max_Product' is not defined
0 of 1 visible tests passed
```

## Round 2 (`Mbpp/415/a2/r2`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 325. Answer tokens: 205.

<details><summary>Thinking</summary>

```text
Okay, let's see. The user provided a Python function called max_product, but the test case is using max_Product with a capital P. Oh right, Python is case-sensitive. So the function name in the code is max_product, but the assert statement is calling max_Product. That's a NameError because the function isn't defined with the capital P.

So the fix is to change the function name to match what the test expects. Let me check the code again. The original code has def max_product(arr):, but the test is using max_Product. So I need to rename the function to max_Product. That's the main issue here.

Wait, are there any other possible issues? Let me think. The code logic seems correct. It tracks the two largest and two smallest numbers, then compares their products. For the given test case [1,2,3,4,7,0,8,4], the two largest are 8 and 7, so the product is 56. The two smallest are 0 and 1, product is 0. So the function returns (7,8) as expected. So the logic is correct. The only problem is the function name case.

So the corrected code should have the function named max_Product. Let me adjust that. Also, the test case uses assert max_Product(...), so the function name must match exactly. So changing the function definition to def max_Product(arr): should fix the NameError.

I think that's the only change needed. Let me write the corrected code with the function name capitalized.
```

</details>

**Code that ran:**

```python
def max_Product(arr):
    max1 = max2 = float('-inf')
    min1 = min2 = float('inf')
    for num in arr:
        # Update max1 and max2
        if num > max1:
            max2 = max1
            max1 = num
        elif num > max2:
            max2 = num
        # Update min1 and min2
        if num < min1:
            min2 = min1
            min1 = num
        elif num < min2:
            min2 = num
    product1 = max1 * max2
    product2 = min1 * min2
    if product1 > product2:
        return tuple(sorted([max1, max2]))
    else:
        return tuple(sorted([min1, min2]))

# Test case
assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
```

**Visible-test report:**

```text
PASS    assert max_Product([1,2,3,4,7,0,8,4]) == (7,8)
1 of 1 visible tests passed
```
