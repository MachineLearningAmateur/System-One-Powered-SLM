# Mbpp/223, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/223/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 125.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_majority that checks if an element is the majority element in a sorted array. The majority element occurs more than n/2 times. Let's think about how to approach this.

First, the array is sorted. That's a key point. So, if the array is sorted, the majority element must appear more than n/2 times. Since the array is sorted, the majority element would be the one that appears in the middle of the array. Wait, but how do I find it efficiently?

Wait, the array is sorted, so if the element is the majority, then it must be the case that the element is the same as the first occurrence of the majority element. But maybe there's a better way. Let me think.

For example, in the sample input [1,2,3,3,3,3,10], the majority element is 3. The array is sorted, so the majority element must be the one that appears more than n/2 times. So for n=7, 3 is more than 3.5 times. So 3 occurs 4 times, which is more than 3.5. So the function returns True.

So the approach is: check if the element is the majority. Since the array is sorted, the majority element must be the same as the element at the middle position. Wait, but what if there are multiple elements? For example, if the array is [1,1,2,2,3,3,3], then the majority element is 3, which is the middle element. Wait, but the array is sorted. So for even n, like 6, the majority element would need to be more than 3. So for n=6, the majority element must appear at least 4 times. So in a sorted array, the majority element would be the one that is in the middle of the array. Wait, but how to find that?

Alternatively, since the array is sorted, we can use the Boyer-Moore Majority Vote algorithm. That algorithm works by maintaining a current candidate and a count. For each element, if the count is zero, we set the current candidate to the current element. If the current element is the same as the candidate, increment count, else decrement. Since the array is sorted, the majority element will be the candidate after processing all elements. But since the array is sorted, the majority element must be the one that appears more than n/2 times, so the Boyer-Moore algorithm would correctly find it.

But maybe there's a simpler way. Since the array is sorted, the majority element must be the same as the element at the position n//2. Wait, for example, in the sample input, n=7, so n//2 is 3. The element at index 3 is 3, which is the majority. So for a sorted array, the majority element is the element at the position n//2. But wait, what if the array is even length? Let's take an example. Suppose the array is [1,1,2,2,3,3], n=6. The majority element would need to occur more than 3 times. So 3 times is not enough. So in this case, there's no majority element. But if the array is [1,1,1,2,2,2], then the majority element is 1, which occurs 3 times. For n=6, 3 is more than 3? No, 3 is equal to 3 (n/2 is 3). Wait, the majority element must occur more than n/2 times. So for n=6, it needs to be more than 3, i.e., 4 or more times. So in that case, the array [1,1,1,2,2,2] has 3 elements of 1, which is not more than 3. So the majority element would not exist. So in this case, the function would return False.

But if the array is [1,1,1,1,2,2,2,2], n=8. The majority element is 1, which occurs 4 times. 4 is more than 8/2=4? No, 4 is equal to 4. So it's not more than. So the function would return False. Wait, the problem says "more than n/2 times". So for n=7, 3 is more than 3.5. So for n=7, 3 occurs 4 times, which is more than 3.5. So the majority element is the one that occurs more than n/2 times.

So in the sorted array, the majority element must be the element at the position n//2. Wait, let's take the sample input. The array is [1,2,3,3,3,3,10], n=7. The middle index is 3 (since 7//2 is 3). The element at index 3 is 3, which is the majority. So that's correct.

Another example: array [1,1,2,2,3,3,3], n=7. The middle index is 3, element is 2. But the majority element is 3, which occurs 3 times. Wait, 3 occurs 3 times, which is 3 times. For n=7, 3 is more than 3.5? No, 3 is less than 3.5. So the majority element would not be present. So the function would return False. But in this case, the array is [1,1,2,2,3,3,3], the majority element is 3, which occurs 3 times. So the function would return False. But according to the problem statement, the majority element must occur more than n/2 times. So in this case, n=7, 3 is not more than 3.5. So the function would return False.

But if the array is [1,1,1,1,1], n=5. The majority element is 1, which occurs 5 times. 5 is more than 2.5. So yes. The middle index is 2 (n//2 is 2). The element at index 2 is 1. So the function would return True.

So the approach is: for a sorted array, the majority element is the element at index n//2. Because the array is sorted, the majority element must be the one that occurs more than n/2 times. So in the sorted array, the majority element must be the element at the middle position. So the function can be written as follows: check if the element at index n//2 is equal to the given element.

But wait, what if the array has multiple elements that are the same, but not at the middle? For example, consider the array [1,1,2,2,2,2,2], n=7. The majority element is 2, which occurs 5 times. The middle index is 3 (n//2=3). The element at index 3 is 2. So the function would return True. So that's correct.

Another example: [1,2,2,2,2,2,3], n=7. The majority element is 2, which occurs 5 times. The middle index is 3, element is 2. So the function returns True.

So the approach is: check if the element at index n//2 is equal to the given element. But wait, what if the array is [1,2,2,2,3,3,3], n=7. The majority element is 3, which occurs 3 times. 3 is not more than 3.5. So the function would return False. But the element at index 3 is 2. So the function would check if the given element is 2, but in this case, the given element is 3, so the function would return False. Which is correct.

So the logic is: if the array is sorted, the majority element must be the element at index n//2. So the function can be written as follows:

def is_majority(arr, n, x):
    return arr[n//2] == x

But wait, what if the array is [1,1,1,1,1], n=5. The middle index is 2, element is 1. So returns True. Which is correct.

But what if the array is [1,1,2,2,2,2,2], n=7. The middle index is 3, element is 2. So returns True. Which is correct.

But what if the array is [1,1,2,2,3,3,3], n=7. The middle index is 3, element is 2. The given element is 3. So returns False. Which is correct.

So this approach would work. So the function is as simple as checking if the element at index n//2 is equal to x.

But why is that the case? Because in a sorted array, the majority element must be the one that occurs more than n/2 times. So the majority element must be the one that is in the middle of the array. Because if there's a majority element, then it must be the same as the element at the middle index. So this approach is correct.

So the code would be:

def is_majority(arr, n, x):
    return arr[n//2] == x

But wait, what if the array is not of even length? For example, n=6. The middle index is 3 (n//2 is 3). For example, array [1,2,3,4,5,6]. The majority element would need to occur more than 3 times. But in this case, there's no majority element. So the function would return False. But the code would check arr[3] == x. So if x is 3, then returns True. But in this case, the array has no majority element. So the code would return True, which is incorrect.

Wait, but in this case, the array is [1,2,3,4,5,6], n=6. The majority element would need to occur more than 3 times. But in this array, each element occurs once. So the function would return arr[3] == x. For example, if x is 3, then arr[3] is 4. So returns False. Which is correct. But if x is 2, then arr[3] is 4. So returns False. So the code would correctly return False. So in this case, the code works.

But what if the array is [1,1,1,2,2,2], n=6. The majority element is 1, which occurs 3 times. 3 is more than 3? No, 3 is equal to 3. So the function would return arr[3] == x. The arr[3] is 2. So if x is 1, returns False. Which is correct. So the code would return False, which is correct.

So the code works. So the function is as simple as checking if the element at index n//2 is equal to x.

But wait, what if the array is [1,1,1,1,2,2], n=6. The majority element is 1, which occurs 4 times. So the code would check arr[3] == x. The arr[3] is 1. So if x is 1, returns True. Which is correct.

So the code works.

Therefore, the function can be written as follows.

But wait, what if the array is [1,1,2,2,2,2,2], n=7. The majority element is 2. The code checks arr[3] which is 2. So returns True. Correct.

So the code is correct.

So the code is:

def is_majority(arr, n, x):
    return arr[n//2] == x

But wait, what if the array is empty? Well, the problem says that the array is sorted, and the length is n. So n is at least 1.

So the code is correct.

So the code would be:

But the problem says that the array is sorted. So the code is correct.

But let me test the sample input.

Sample input: [1,2,3,3,3,3,10], n=7, x=3. The middle index is 3. arr[3] is 3. So returns True. Which is correct.

Another test case: [1,2,3,4,5], n=5, x=3. arr[2] is 3. So returns True. But the majority element would need to occur more than 2.5 times. So 3 occurs once. So the function returns True, but the actual majority element is not present. Wait, but in this case, the array is [1,2,3,4,5], n=5. The majority element is not present. So the function would return True, but the actual answer is False. Wait, but according to the code, arr[2] is 3. So if x is 3, then the code returns True. But in this case, the element is not the majority. So what's wrong here?

Wait, this is a problem. Because the code is checking if the element at the middle index is equal to x. But in the case where the array is [1,2,3,4,5], the majority element is not present. So the code would return True if x is 3, but the actual majority element is not present. So why is that?

Wait, no. Because the array is sorted. So if the array is [1,2,3,4,5], the majority element is not present. So the code would return True if x is 3, but in reality, the majority element is not present. So the code is wrong.

Wait, but how can that be? Because the code is based on the assumption that the majority element is the one at the middle index. But in this case, the array is [1,2,3,4,5], and the majority element is not present. So the code would return True if x is 3, but the actual answer is False.

Wait, but in this case, the array is [1,2,3,4,5], n=5. The majority element is the element that occurs more than n/2 times. For n=5, that's more than 2.5 times. So the element must occur 3 times or more. But in this array, each element occurs once. So there's no majority element. So the code would return arr[2] == x. So if x is 3, then arr[2] is 3, so returns True. But the actual answer is False.

So this is a problem. So the code is incorrect.

Wait, but why? Because the code is assuming that the majority element is at the middle index. But in this case, the array is [1,2,3,4,5], and the majority element is not present. So the code would return True for x=3, but the correct answer is False.

So what's wrong here?

Ah, because the code is not checking if the element is the majority. So the code is correct only when the element is the majority. But in this case, the code returns True when the element is not the majority. So the code is incorrect.

So why is that? Because the code is checking if the element at the middle index is equal to x, but that's not sufficient. Because in the case where the array is [1,2,3,4,5], the element at the middle index is 3, but the element is not the majority. So the code is wrong.

So what's the problem here? The code is based on the assumption that the majority element is the one at the middle index. But that's only true if the array has a majority element. So the code is not sufficient.

So how can we fix this?

The problem is that the code is not checking if the element is actually the majority. So even if the element is at the middle index, it's possible that there is no majority element. So the code would return True when there is no majority element.

So in the case where the array is [1,2,3,4,5], the code would return True if x is 3, but the correct answer is False. So the code is incorrect.

So the code is not correct. So what's the correct approach?

Ah, the problem is that the code assumes that the majority element is at the middle index, but that's not always the case. For example, in the array [1,2,3,3,3,3,10], the majority element is at the middle index. But in the array [1,2,3,4,5], there is no majority element, but the code would return True if x is 3.

So the code is not correct. So what's the correct approach?

The correct approach is to check if the element is the majority. So the code needs to check if the element occurs more than n/2 times. But how to do that efficiently, given that the array is sorted.

So for a sorted array, the majority element can be found by checking if the element at the middle index is the majority. But in the case where the array is [1,2,3,4,5], the code would return True for x=3, but the actual majority is not present. So the code is not correct.

So the problem is that the code is not checking if the element is actually the majority. So how to fix this?

Wait, the code is correct if the element is the majority. But in the case where the array is [1,2,3,4,5], the code returns True for x=3, but the actual answer is False. So the code is incorrect.

So what's the correct way to check if the element is the majority?

In a sorted array, the majority element must be the same as the element at the middle index. So if the element at the middle index is x, then x is the majority element. But this is only true if x occurs more than n/2 times.

But how can we know that?

Wait, in a sorted array, if the element at the middle index is x, then x must be the majority element. Because if there is a majority element, then it must be the same as the element at the middle index. Because the array is sorted. For example, if the array is [1,1,1,2,2,2,3], n=7. The middle index is 3, which is 2. The majority element is 1, which occurs 3 times. Wait, no. Wait, in this array, the majority element is 1 (3 times) but the middle index is 2 (element 2). So the code would return False, but the actual majority element is 1. So the code is wrong.

Wait, this is a problem. So the code is not correct.

So the code is incorrect. So what's the correct approach?

The problem is that the code assumes that the majority element is the one at the middle index, but that's not always the case. For example, in an array where the majority element is not at the middle index, but the code returns True. So how can we find the majority element?

The correct approach is to use the Boyer-Moore algorithm. Because the array is sorted, the majority element can be found using the Boyer-Moore algorithm. Let's think about that.

The Boyer-Moore algorithm works by maintaining a candidate and a count. For each element in the array, if the count is zero, we set the candidate to the current element. If the current element is the same as the candidate, increment the count, else decrement. The candidate is the majority element if it exists.

But in a sorted array, the majority element is the one that is the same as the candidate. So the algorithm can be applied.

But since the array is sorted, the majority element must be the candidate. So the algorithm would return the candidate as the majority element.

So for example, in the array [1,1,1,2,2,2,3], n=7. The candidate would be 1, and the count would be 3. So the algorithm would return 1 as the majority element. But the code that checks the middle element would return 2, which is not the majority. So the code is wrong.

So the code that checks the middle element is not correct. So the correct approach is to use the Boyer-Moore algorithm.

So how to implement that.

Let me think. The Boyer-Moore algorithm for majority element.

Initialize candidate as None, count as 0.

For each element in the array:

   if count is 0:

       candidate = element

   if element == candidate:

       count +=1

   else:

       count -=1

At the end, the candidate is the majority element.

But since the array is sorted, the majority element must be the candidate. So the candidate is the majority element.

So in the example [1,1,1,2,2,2,3], the candidate would be 1. So the function would return True.

So the code can be written as:

def is_majority(arr, n, x):

    candidate = None

    count = 0

    for num in arr:

        if count == 0:

            candidate = num

        if num == candidate:

            count +=1

        else:

            count -=1

    return candidate == x

But wait, in the sample input, the candidate would be 3. Because the array is [1,2,3,3,3,3,10]. Let's simulate:

count starts at 0.

First element is 1: count is 0, candidate is 1. count becomes 1.

Second element is 2: not equal to candidate (1). count becomes 0.

Third element is 3: count is 0, candidate is 3. count becomes 1.

Fourth element is 3: equal to candidate. count becomes 2.

Fifth element is 3: count becomes 3.

Sixth element is 3: count becomes 4.

Seventh element is 10: not equal to candidate (3). count becomes 3.

So the candidate is 3. So returns True if x is 3. Which is correct.

In the case of [1,2,3,4,5], the candidate is 2 (let's see):

count starts at 0.

First element 1: count is 0, candidate is 1. count 1.

Second element 2: not equal to 1. count 0.

Third element 3: count 0, candidate is 3. count 1.

Fourth element 4: not equal to 3. count 0.

Fifth element 5: count 0, candidate is 5. count 1.

So the candidate is 5. So returns True if x is 5. But in this case, the array has no majority element. So the code returns True, but the correct answer is False.

Wait, but in this case, the array is [1,2,3,4,5], n=5. The majority element must occur more than 2.5 times. So the element must occur 3 or more times. But in this array, each element occurs once. So the code returns candidate == x, which is 5 == 5, returns True. But the actual answer is False.

So the code is incorrect.

So what's wrong here?

The Boyer-Moore algorithm returns the candidate, but in this case, the candidate is 5, but there's no majority element. So the algorithm is correct, but the code is not checking whether the candidate is actually the majority. So the code is not correct.

So the problem is that the Boyer-Moore algorithm returns the candidate, but the candidate is not the majority element in this case. So the code needs to check if the candidate is the majority element. But how?

Wait, the Boyer-Moore algorithm guarantees that if there is a majority element, it will be the candidate. So in the case where there is no majority element, the candidate is not the majority element. So the code needs to check if the candidate is the majority element. But how?

Wait, the algorithm works as follows: if there is a majority element, then it will be the candidate. So if the candidate is the majority element, then the code returns True. But in the case where there is no majority element, the candidate is not the majority element. So the code would return False.

Wait, no. The algorithm returns the candidate, but the code must check if the candidate is the majority element. So the code would return True if the candidate is the majority element, and False otherwise.

But how to know if the candidate is the majority element? Because the algorithm returns the candidate, but the candidate may not be the majority element.

So the code should check if the candidate is the majority element. But how to do that?

Wait, in the case where the array is [1,2,3,4,5], the candidate is 5. But the majority element is not present. So the code would return True if the candidate is 5 and x is 5. But the actual answer is False.

So the code is incorrect. So the code needs to check if the candidate is the majority element. But how?

Wait, the Boyer-Moore algorithm returns the candidate, but the candidate is the majority element if it exists. So the code can check if the candidate is equal to x, but also check if the count of the candidate in the array is more than n/2. But how to do that?

Alternatively, since the array is sorted, the candidate is the majority element if it occurs more than n/2 times. So in the case where the array is [1,2,3,4,5], the candidate is 5, which occurs once. So the code would return True if x is 5, but the actual answer is False.

So the code needs to check if the candidate is the majority element. But how?

But the problem is that the code can't check that unless we know the count of the candidate in the array. So for a sorted array, the candidate is the majority element if and only if it is the same as the element at the middle index. So how?

Wait, in the case of a sorted array, the majority element must be the candidate. So if the array is sorted and the candidate is x, then x is the majority element. But this is not true. For example, in the case where the array is [1,1,2,2,3,3,3], n=7. The candidate is 3. So the code would return True if x is 3. Which is correct.

But in the case of [1,2,3,4,5], the candidate is 5, but there's no majority element. So the code would return True if x is 5, but the actual answer is False.

So the problem is that the code is not checking whether the candidate is the majority element. So how to fix this?

The correct approach is to use the Boyer-Moore algorithm and then check if the candidate is indeed the majority element. But how?

Wait, in the case of a sorted array, the majority element is the one that occurs more than n/2 times. So if the array is sorted, then the majority element is the one that is the same as the candidate. So if the array is sorted, and the candidate is x, then x is the majority element if and only if it occurs more than n/2 times.

But how to check that?

In a sorted array, if the candidate is x, then the majority element is x if and only if x appears more than n/2 times. So the code can check if the candidate is x, and then check if the count of x in the array is more than n/2. But how to do that efficiently?

But in a sorted array, the majority element is the candidate, so if the candidate is x, then the count of x in the array is at least n/2 + 1. So how to check that?

But in the case of the array [1,2,3,4,5], the candidate is 5, but the count is 1. So the code would return True if x is 5, but the actual answer is False. So the code needs to check if the candidate is the majority element.

So the correct approach is:

1. Use the Boyer-Moore algorithm to find the candidate.

2. Check if the candidate is the majority element by counting how many times it appears in the array.

But for a sorted array, this can be done by checking the first occurrence and the last occurrence.

Alternatively, since the array is sorted, if the candidate is the majority element, then it must appear more than n/2 times. So in the case of the array [1,2,3,4,5], the candidate is 5, which occurs once. So the code would return True if x is 5, but the actual answer is False.

So the code needs to check if the candidate is the majority element. But how?

So the code can be written as follows:

def is_majority(arr, n, x):

    candidate = None

    count = 0

    for num in arr:

        if count == 0:

            candidate = num

        if num == candidate:

            count +=1

        else:

            count -=1

    # Now check if candidate is x and if it is the majority element

    # How to check if the candidate is the majority element?

    # In a sorted array, the majority element is the candidate if it occurs more than n/2 times.

    # So we can check if the candidate is x, and then check if it appears more than n/2 times.

    # But how to do that efficiently?

    # Since the array is sorted, we can check the first occurrence and the last occurrence of the candidate.

    # Or, since the array is sorted, the candidate is the majority element if the first occurrence is at index 0 and the last occurrence is at index n-1.

    # But this is not necessarily true.

    # Alternatively, since the array is sorted, the candidate is the majority element if it occurs more than n/2 times. So we can check if the candidate is x and then check if the number of times x appears in the array is more than n/2.

    # But how to count the occurrences?

    # For a sorted array, we can use binary search to find the first and last occurrence of the candidate.

    # For example, in the array [1,2,3,3,3,3,10], the first occurrence of 3 is at index 2, last at index 5. The number of occurrences is 4, which is more than 3.5.

    # So for the candidate x, we can check if the number of occurrences is more than n/2.

    # So in code:

    # find the first and last occurrence of x in the array.

    # if the first occurrence is at index i, and last at index j, then the number of elements is j - i + 1.

    # if j - i + 1 > n/2, then return True.

    # So how to implement this.

    # For example, in the array [1,2,3,4,5], the candidate is 5. The first occurrence is 0, last is 4. The number of elements is 5, which is 5 > 5/2 (2.5). But in this case, the array has 5 elements, and the candidate is 5, which occurs once. So the code would return False.

Wait, but in this case, the number of occurrences is 1, which is not more than 5/2 (2.5). So the code would return False.

So the code would need to check if the number of occurrences of the candidate is more than n/2.

So the code can be written as:

def is_majority(arr, n, x):

    candidate = None

    count = 0

    for num in arr:

        if count == 0:

            candidate = num

        if num == candidate:

            count +=1

        else:

            count -=1

    # Now check if candidate is x and if the number of occurrences is more than n/2

    if candidate != x:

        return False

    # Now find the number of occurrences of x in the array

    # since the array is sorted, we can use binary search to find the first and last occurrence

    # but for a sorted array, the first occurrence of x can be found using bisect_left, and the last using bisect_right.

    # So, import bisect.

    import bisect

    first = bisect.bisect_left(arr, x)

    last = bisect.bisect_right(arr, x) - 1

    # number of occurrences is last - first + 1

    if (last - first + 1) > n / 2:

        return True

    else:

        return False

But this would work. For example, in the case of [1,2,3,4,5], the candidate is 5. first is 4, last is 4. number of occurrences is 1. 1 > 5/2 (2.5)? No. So returns False.

In the sample input, the candidate is 3, and the number of occurrences is 4, which is more than 3.5. So returns True.

In the array [1,1,1,2,2,2], n=6. The candidate is 1. first is 0, last is 2. number of occurrences is 3. 3 > 3? No. So returns False.

So this code would correctly handle the cases.

But the code would need to import bisect.

But the problem says to write a correct Python solution, and the code must include any necessary imports.

So the complete code would be:

import bisect

def is_majority(arr, n, x):

    candidate = None

    count = 0

    for num in arr:

        if count == 0:

            candidate = num

        if num == candidate:

            count += 1

        else:

            count -= 1

    if candidate != x:

        return False

    first = bisect.bisect_left(arr, x)

    last = bisect.bisect_right(arr, x) - 1

    return (last - first + 1) > n / 2

But wait, in the case where the array has multiple elements, but the candidate is x. For example, the array [1,1,1,1,2,2,2], n=7. The candidate is 1. first is 0, last is 4. number of occurrences is 5. 5 > 3.5 → True. So returns True.

So this code would work.

But what about the case where the array is [1,1,1,1,1], n=5. The candidate is 1. first is 0, last is 4. number of occurrences is 5. 5 > 2.5 → True. So returns True. Correct.

But what about the case where the array is [1,1,1,2,2,2,2], n=7. The candidate is 1. first is 0, last is 2. number of occurrences is 3. 3 > 3.5? No. So returns False. Which is correct, because the majority element is 2, which occurs 4 times.

So the code would return False if x is 1, and True if x is 2.

So this code is correct.

But the problem is that the code is not as efficient as possible. For example, for large arrays, using bisect may be slow, but given that the array is sorted, it's acceptable.

But the original code that checks the middle element is incorrect, but this code is correct.

So the correct solution is to use the Boyer-Moore algorithm to find the candidate, then check if the candidate is x and if it occurs more than n/2 times.

So the code would be as above.

But the problem says that the array is sorted. So the code is correct.

So the final code would include the import of bisect, and the function as described.

But the original problem's sample input would return True.

Let me test the sample input.

Sample input: [1,2,3,3,3,3,10], n=7, x=3.

The candidate is 3. first is 2, last is 5. number of occurrences is 4. 4 > 3.5 → True. So returns True. Correct.

Another test case: [1,1,1,2,2,2,2], n=7, x=1. first is 0, last is 2. 3 > 3.5 → False. So returns False.

Another test case: [1,1,1,1,1], n=5, x=1. first is 0, last is 4. 5 > 2.5 → True. So returns True.

So the code is correct.

So the final code is:

import bisect

def is_majority(arr, n, x):

    candidate = None

    count = 0

    for num in arr:

        if count == 0:

            candidate = num

        if num == candidate:

            count += 1

        else:

            count -= 1

    if candidate != x:

        return False

    first = bisect.bisect_left(arr, x)

    last = bisect.bisect_right(arr, x) - 1

    return (last - first + 1) > n / 2

But wait, the code may have to import bis
```

</details>

**Code that ran:**

```python
import bisect

def is_majority(arr, n, x):
    candidate = None
    count = 0
    for num in arr:
        if count == 0:
            candidate = num
        if num == candidate:
            count += 1
        else:
            count -= 1
    
    if candidate != x:
        return False
    
    first = bisect.bisect_left(arr, x)
    last = bisect.bisect_right(arr, x) - 1
    return (last - first + 1) > n / 2
```

**Visible-test report:**

```text
PASS    assert is_majority([1, 2, 3, 3, 3, 3, 10], 7, 3) == True
1 of 1 visible tests passed
```
