# Mbpp/782, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/782/a1/r1`)

Visible tests: **pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 692.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that calculates the sum of all odd-length subarrays of a given array. The example given is that for [1,2,4], the sum is 14. Let me think about how to approach this.

First, I remember that a subarray is a contiguous part of the array. So for an array of length n, the subarrays of odd length would be all possible contiguous sequences where the length is 1, 3, 5, etc. But how do I compute their sum efficiently?

The brute force approach would be to generate all possible subarrays of odd lengths and sum them. But for larger arrays, this could be slow. For example, if the array is of size n, there are O(n^2) subarrays, but since we're only considering odd lengths, maybe there's a smarter way.

Wait, but for the given example, let's see. The array is [1,2,4]. The odd-length subarrays are:

Length 1: [1], [2], [4] → sum is 1+2+4=7.

Length 3: [1,2,4] → sum is 7.

Total sum is 7 +7 =14, which matches the example. So the approach is correct.

But how to compute this efficiently?

Let me think about the brute force method first. For each possible starting index i, and for each possible odd length l (like 1,3,5,...), check all subarrays starting at i and of length l. But for each i, the possible l's are 1, 3, 5, etc., up to the array length.

But for an array of size n, the number of subarrays of odd length is O(n^2). For n=1000, that's 1e6 operations, which is manageable. But maybe there's a smarter way.

Alternatively, I can think about the sum of all subarrays of odd length. Let me think about the sum of all subarrays of odd length. For each position in the array, how many times does it contribute to the sum?

For example, consider the element at index i. How many times does it appear in subarrays of odd length?

Let me think. For each element, the number of times it's included in a subarray of odd length depends on the positions around it.

But maybe there's a pattern here. For example, for each element, the number of subarrays that include it and have odd length. But how?

Alternatively, maybe we can find the sum of all subarrays of odd length by using the formula for the sum of all subarrays, and then subtracting the even-length ones. But that might not be straightforward.

Wait, the sum of all subarrays of odd length can be calculated as the sum of all subarrays minus the sum of all subarrays of even length. But how to compute that?

But maybe that's not helpful. Let me think again.

Another approach: For each possible odd length l (1,3,5,...), compute the sum of all subarrays of length l, then add them all together.

But how to compute the sum of all subarrays of length l?

For example, for l=1, the sum is the sum of all elements. For l=3, the sum is the sum of elements at positions i, i+1, i+2 for each i where i+2 < n.

But for each l, the sum can be computed as follows:

For each i from 0 to n - l, sum the elements from i to i + l -1.

But for l=1, the sum is sum of all elements. For l=3, sum of elements in positions 0-2, 1-3, 2-4, etc.

But for each l, the sum can be calculated by sliding window. But for each l, the sum is O(n) time. So for all possible odd l, the total time would be O(n^2), which is acceptable for small n.

But for larger n, this might be slow. However, given that the problem is to find a correct solution, perhaps this approach is acceptable.

But let's think about the example. For the array [1,2,4], the possible l's are 1 and 3.

For l=1: sum is 1+2+4=7.

For l=3: sum is 1+2+4=7. Total 14.

So the code would need to loop over all possible odd l's, and for each l, compute the sum of all subarrays of length l.

But how to generate all possible l's?

The possible l's are 1, 3, 5, ..., up to the maximum possible odd length. For example, if the array length is n, the maximum l is n if n is odd, or n-1 if even.

So, for each l in 1, 3, 5, ... up to n (if odd), compute the sum of all subarrays of length l.

But how to generate these l's?

In code, for a given array, we can iterate l from 1 to len(arr), stepping by 2. For each l, if l is <= len(arr), then compute the sum.

So for the example [1,2,4], len(arr) is 3. So l can be 1 and 3.

So the code would be:

def odd_length_sum(arr):
    total = 0
    n = len(arr)
    for l in range(1, n+1, 2):
        for i in range(n - l + 1):
            sub = arr[i:i+l]
            total += sum(sub)
    return total

But for the example, this would work. Let's test it.

For l=1, n=3, i ranges from 0 to 2 (inclusive). So 3 subarrays. Sum is 1+2+4=7.

For l=3, i ranges from 0 to 0 (since 3-3+1=1). So sum is 1+2+4=7. Total 14. Correct.

But for larger arrays, this would be O(n^2) time. For example, if n is 1000, then for each l (up to 999, 997, etc.), and for each i, sum is O(l) time. So total time is O(n^3), which is not acceptable for n=1000. But for the problem's constraints, maybe it's acceptable. However, the problem may expect a more efficient solution.

So, the question is, can we find a more efficient way?

Alternative approach: For each element in the array, determine how many times it appears in the sum of odd-length subarrays.

For example, for each element at index i, how many subarrays of odd length include it?

Let me think. For a given element at index i, the number of subarrays of odd length that include it depends on the positions to the left and right.

For example, for the element at index i, the number of subarrays that include it and have odd length can be calculated as follows:

The number of subarrays that include i and have odd length is equal to (number of possible left choices) * (number of possible right choices) where the length is odd.

But perhaps there's a way to compute this.

Let me think. For a subarray to include index i, the subarray must start at some position <= i and end at some position >= i.

The length of the subarray is (end - start + 1). For the length to be odd, (end - start + 1) must be odd. So end - start + 1 is odd → end - start is even → end - start is even → end and start have the same parity.

So for the element at index i, the number of subarrays that include it and have odd length is equal to the number of pairs (start, end) where start <= i <= end, and end - start is even.

But how to compute this?

Alternatively, for each element, the number of subarrays that include it and have odd length can be determined by considering the number of possible starting positions and ending positions.

But perhaps there's a formula here.

Let me think of the total number of subarrays that include the element at index i. For all subarrays that include i, the length can be any odd number. For example, for a subarray that starts at s and ends at e, where s <= i <= e.

The number of such subarrays is (i - s + 1) * (n - e + 1) ?

No, perhaps not. Alternatively, for a given i, the number of subarrays that include i is (i+1) * (n - i). Because for each possible starting position s (from 0 to i), and each possible ending position e (from i to n-1). So total is (i+1)*(n - i). But that's the total number of subarrays that include i. But how many of these have odd length?

So for each i, the number of subarrays that include i and have odd length is equal to the number of subarrays that include i and have odd length.

But how to compute that?

The length of the subarray is (e - s + 1). For this to be odd, e - s + 1 is odd → e - s is even → e and s have the same parity.

So for each i, the number of subarrays that include i and have odd length is equal to the number of pairs (s, e) where s ≤ i ≤ e, and s and e have the same parity.

But how to compute this?

Let me think. For a given i, the possible s can be from 0 to i, and e can be from i to n-1.

So for each s, the e must be such that e - s is even.

But for each s, the e must be in the range [i, n-1], and e must have the same parity as s.

So for a given s, the number of e's that satisfy e >= i and e has the same parity as s.

But how to compute this?

Alternatively, for each i, the number of possible (s, e) pairs where s ≤ i ≤ e and e - s is even.

But perhaps we can find for each i, the number of possible s and e pairs where s and e have the same parity, and s ≤ i ≤ e.

But this seems complicated.

Alternatively, for each i, the number of subarrays that include i and have odd length is equal to the number of subarrays that start at s ≤ i and end at e ≥ i, and (e - s + 1) is odd.

Which is equivalent to (e - s) is even.

So for each i, the number of such subarrays is equal to the number of (s, e) pairs where s ≤ i, e ≥ i, and e - s is even.

But how to compute this?

Let me think of the possible s and e.

For a given i, the possible s can be from 0 to i. The possible e can be from i to n-1.

For each s, the e must be such that e is in [i, n-1], and e has the same parity as s.

But for each s, the e can be any of the elements in the range [i, n-1] with the same parity as s.

So for each s, the number of e's is equal to the number of elements in the range [i, n-1] with the same parity as s.

But how?

Let me think of the parity of s. For example, for a given s, the parity is even or odd. Let me consider the parity of s.

Let me think of the number of e's in [i, n-1] with parity equal to s's parity.

The total number of e's in [i, n-1] is (n-1 - i + 1) = n - i.

The number of e's with even parity is (number of even numbers in the range from i to n-1), and same for odd.

But how to compute that?

Alternatively, for the range [i, n-1], the number of elements with even parity is equal to:

If the first element (i) is even: (n - i) // 2 + 1 if (i is even) ?

Wait, perhaps there's a formula here. Let me think.

The number of even numbers in the range [a, b] is:

floor((b - (a % 2 == 0 ? a : a +1 )) / 2) + 1 ?

Alternatively, the number of even numbers from a to b inclusive is:

count_even = ((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Not sure. Let me think of an example.

For example, a=2, b=4. The numbers are 2,3,4. Even numbers are 2,4 → 2 numbers. So the count is (4 -2)/2 +1 = (2/2)+1 = 1 +1=2. Correct.

Another example: a=1, b=4. The even numbers are 2,4 → 2 numbers. The formula would be (4 - 1) = 3. (3 // 2) is 1. 1 +1 = 2. Correct.

Another example: a=0, b=0. Even numbers is 1. Formula: (0 -0)/2 +1 = 0 +1=1. Correct.

Another example: a=3, b=5. Even numbers are 4. So count is 1. The formula: (5-3) = 2. 2//2 =1. 1+1=2? No. Wait, the formula is (b - a) // 2 + 1 if a is even?

Wait, maybe the formula is:

count_even = ((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Alternatively, perhaps the number of even numbers between a and b inclusive is:

((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Alternatively, perhaps it's easier to compute the number of even numbers in [a, b] as:

count_even = ((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Not sure. But perhaps there's a simpler way. For the range [a, b], the number of even numbers is ((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Alternatively, perhaps the number of even numbers in [a, b] is ((b - (a % 2 == 0 ? a : a +1 )) // 2) + 1 ?

Alternatively, the number of even numbers is ( (b - (a % 2 == 0 ? a : a +1 )) // 2 ) + 1 ?

But perhaps I can find a formula for the number of even numbers in [a, b] as:

if a is even: (b - a) // 2 + 1

if a is odd: (b - a + 1) // 2

But that's not correct. For example, a=1, b=4. The even numbers are 2,4. So (4-1) is 3. (3 +1)/2 = 2. Correct. So for a=1 (odd), the count is (b - a +1) // 2 ?

Yes. For a=1, b=4: (4-1+1) =4 → 4//2=2. Correct.

For a=2 (even), b=4: (4-2) =2 → 2//2 +1 =1 +1=2. Correct.

So the formula for the number of even numbers in [a, b] is:

if a is even: ((b - a) // 2) + 1

if a is odd: ((b - a + 1) // 2)

But how to compute this in code?

Alternatively, the number of even numbers in [a, b] is ((b - a) // 2) + 1 if a is even, else ((b - a + 1) // 2).

But perhaps there's a simpler way. Let me think of the total numbers in the range [a, b] as (b - a +1). The number of even numbers is ( (b - a +1) + (a % 2 - b % 2) ) // 2.

Wait, perhaps not. Let me think: For a range of numbers, the number of even numbers is equal to the ceiling of (length of range) / 2 if the range starts with even, or floor of (length of range)/2 if it starts with odd. Hmm.

Alternatively, the number of even numbers in the range [a, b] is ( (b - a + 1) + (a % 2 - b % 2) ) // 2.

But I'm not sure. Let me test with some examples.

Example 1: a=2, b=4. Length is 3. a is even, b is even. (3 + (0 - 0 )) / 2 = 3/2 = 1.5 → floor is 1. But actual is 2. So that formula is incorrect.

Hmm. Maybe I need to think differently.

Another approach: The number of even numbers in [a, b] is equal to:

floor( (b - a + 1) / 2 ) + ( (a % 2) == 0 ? 1 : 0 )

Wait, for a=2, b=4: (4-2+1)/2 = 3/2=1.5 → floor is 1. Then add 1 (since a is even). So 1 +1=2. Correct.

For a=1, b=4: (4-1+1)/2 = 4/2=2 → floor is 2. a is odd, so add 0. So 2 +0=2. Correct.

For a=1, b=3: (3-1+1)/2 = 3/2=1.5 → floor 1. a is odd, add 0. So 1. Correct (even numbers are 2).

For a=0, b=0: (0-0+1)/2 = 0.5 → floor 0. a is even, add 1. 0 +1=1. Correct.

For a=3, b=5: (5-3+1)/2 = 3/2=1.5 → floor 1. a is odd, add 0 → 1. Correct (even number is 4).

Yes, this formula seems to work.

So the number of even numbers in [a, b] is:

count_even = ( (b - a +1) + (a % 2 == 0 ? 1 : 0 )) // 2 ?

Wait, no. Let me think again. The formula is:

count_even = ((b - a +1) + (a % 2 == 0 ? 1 : 0 )) // 2 ?

No, that's not correct. Wait, the formula is:

count_even = ( (b - a +1) + (a % 2 == 0 ? 1 : 0 )) // 2 ?

Wait, no. For example, in the case where a is even and b is even, the formula gives (3 + 1)/2 = 2, which is correct. For a=1, b=4, (4-1+1) is 4, and since a is odd, add 0. 4/2 = 2. Correct.

But how to compute this in code?

Well, the formula can be written as:

count_even = ((b - a + 1) + (a % 2 == 0 ? 1 : 0 )) // 2

But in code, we can compute it as:

if a % 2 == 0:
    count_even = ((b - a + 1) + 1) // 2
else:
    count_even = (b - a + 1) // 2

But that's equivalent to:

count_even = ( (b - a + 1) + (a % 2 == 0) ) // 2

Yes. So, for a given a and b, the number of even numbers in [a, b] is ((b - a + 1) + (a % 2 == 0)) // 2.

But how to use this for our problem?

Back to the original problem. For each element at index i, we need to find the number of subarrays that include it and have odd length. Let's think of the possible s and e for the subarrays that include i.

But for each i, the s can be from 0 to i, and e can be from i to n-1. For each such (s, e) pair, the length is e - s + 1, which is odd. So e - s is even.

So for each s (from 0 to i), the number of e's (from i to n-1) that have the same parity as s.

But for each s, the e must be in the range [i, n-1], and have the same parity as s.

So for each s, the number of e's is:

if s is even: the number of even numbers in [i, n-1].

if s is odd: the number of odd numbers in [i, n-1].

But how to compute this for each s?

But for each s, the parity is known. So for each s in 0..i, the number of e's is:

if s is even: count_even_e = number of even numbers in [i, n-1]

if s is odd: count_odd_e = number of odd numbers in [i, n-1]

But how to compute count_even_e and count_odd_e?

Well, for the range [i, n-1], the number of even numbers is:

if i is even: ((n - 1 - i) + 1) // 2 → (n - i) // 2 + 1 ?

Wait, no. Let me think again. For the range [i, n-1], the number of even numbers is:

count_even = ((n-1 - i) + 1) + (i % 2 == 0) ) // 2 ?

Wait, perhaps I can use the formula I derived earlier.

For the range [a, b], where a is i and b is n-1, the number of even numbers is:

count_even = ((b - a + 1) + (a % 2 == 0)) // 2

So, for a given a (i) and b (n-1), count_even is (( (n-1 - i + 1) ) + (i % 2 == 0 )) // 2 → ((n - i) + (i % 2 == 0 )) // 2.

But for a given i, the e's are in the range [i, n-1]. So for each s, the number of e's is:

if s is even: count_even_e = ((n - i) + (i % 2 == 0 )) // 2

if s is odd: count_odd_e = ((n - i) + (i % 2 == 1 )) // 2 ?

Wait, no. The count_odd_e is the number of odd numbers in [i, n-1], which is:

count_odd = ((n - i) + (i % 2 == 1 )) // 2 ?

Yes. Because for the range [i, n-1], the number of odd numbers is:

if i is odd: ((n - i) + 1) // 2.

if i is even: (n - i) // 2.

But again, the formula can be written as:

count_odd = ((n - i) + (i % 2 == 1 )) // 2.

So for each s in 0 to i, the number of e's that have the same parity as s is:

if s is even: count_even_e = ((n - i) + (i % 2 == 0 )) // 2.

if s is odd: count_odd_e = ((n - i) + (i % 2 == 1 )) // 2.

But how to compute this for all s?

But for each s in 0 to i, the number of e's is:

if s is even: count_even_e

if s is odd: count_odd_e

But the sum over all s in 0 to i of (count_even_e or count_odd_e) would be the total number of subarrays that include i and have odd length.

But wait, for each s, the e's are in the range [i, n-1], and the parity of e must be same as s's parity. So for each s, the count is the number of e's in [i, n-1] with same parity as s.

But for each s, the count is either count_even_e or count_odd_e, depending on the parity of s.

But how to compute this for all s?

But for a given i, the total number of such subarrays is the sum over s from 0 to i of (number of e's in [i, n-1] with same parity as s).

But how to compute this sum?

Let me think. For each s in 0 to i, the parity of s is known. So for the s's that are even, the count is count_even_e, and for the s's that are odd, the count is count_odd_e.

But the count_even_e and count_odd_e are the same for all s in 0 to i, because they depend only on i and n.

Wait, no. For example, if i is even, then count_even_e is the number of even numbers in [i, n-1], which is fixed. And for s even, the count is count_even_e. For s odd, the count is count_odd_e, which is the number of odd numbers in [i, n-1].

But for a given i, the total number of s's is i+1 (from 0 to i). So for the s's that are even, their count is count_even_e, and for s's that are odd, their count is count_odd_e.

So the total number of subarrays that include i and have odd length is:

(number of even s in 0..i) * count_even_e + (number of odd s in 0..i) * count_odd_e.

But the number of even s in 0..i is (i+1 + (i % 2 == 0)) // 2 ?

Wait, the number of even numbers in 0..i is (i//2) + 1 if i is even, else (i//2) ?

For example:

i=0: 0 is even → 1 even numbers (0).

i=1: 0 is even → 1 even (0), 1 is odd → 1 even.

i=2: 0, 1, 2 → 2 even numbers.

So the number of even numbers in 0..i is (i//2) + 1 if i is even, else (i//2) + 1? No, wait:

Wait, for i=1 (odd), the number of even numbers is 1 (0).

i=2 (even): 0,1,2 → 2 even numbers.

i=3 (odd): 0,1,2,3 → 2 even numbers.

So the number of even numbers in 0..i is (i//2) + 1 if i is even, else (i//2) ?

Yes. For i even: (i//2) +1 = (i/2) +1.

For i odd: (i//2) + 0? Wait, i=1, i//2 is 0. So 0 +0=0? No, but for i=1, the even numbers are 0 → count is 1.

So the formula is (i // 2) + 1 if i is even, else (i // 2) + 1? No. Wait, for i=1, the count is 1. Which is (1//2) + 1 → 0 +1=1. Correct.

For i=2, (2//2) +1 =1 +1=2. Correct.

For i=3: (3//2) +1 =1 +1=2. Correct.

So the number of even numbers in 0..i is (i // 2) + 1 if i is even, else (i//2) +1? No. Wait, for i even, it's (i//2) +1. For i odd, (i//2) +1? For i=1, (1//2) is 0, +1 → 1. Correct.

Yes. So the number of even s in 0..i is (i//2) + 1 if i is even or odd? Wait, no. Wait, for any i, the number of even numbers in 0..i is (i // 2) + 1 if i is even, else (i // 2) + 1? No, because for i even, the number is (i/2) + 1. For i odd, it's (i//2) + 1.

But i//2 is floor(i/2). So for any i, the number of even numbers in 0..i is (i + 1) // 2.

Yes! Because for i even, (i+1)//2 = (i/2 + 0.5) floored → i/2 + 0.5 is (i+1)/2. For example, i=2: (2+1)/2=1.5 → floor is 1. But the actual count is 2. Wait, no. Wait, i=2, the number of even numbers is 2 (0,2). (i+1)//2 is (3)//2 =1. Which is incorrect. So my previous reasoning was wrong.

Hmm, this is getting complicated. Let me think again.

The number of even numbers in 0..i is floor((i+1)/2) if i is even?

No. Let's think of it as follows:

The even numbers in 0..i are 0, 2, 4,..., up to the maximum even number ≤i.

The count is (i//2) + 1 if i is even, else (i//2) + 0? Wait, for i=1, the even numbers are 0 → count is 1. i//2 is 0. So 0 + 1 =1. Correct.

For i=2, even numbers are 0,2 → count 2. i//2 is 1. So 1 +1=2. Correct.

For i=3, even numbers are 0,2 → count 2. i//2 is 1. So 1 +1=2. Correct.

For i=4, even numbers are 0,2,4 → count 3. i//2 is 2. 2+1=3. Correct.

So the number of even numbers in 0..i is (i//2) + 1 if i is even, else (i//2) + 1?

Wait, for i=1, which is odd, i//2 is 0. So 0 +1 =1. Correct.

So for any i, the number of even numbers in 0..i is (i//2) +1.

Yes! Because for any i, the number of even numbers in 0..i is (i//2) +1. Because for i even, it's (i/2) +1, and for i odd, (i//2) +1 = ( (i-1)/2 ) +1 = (i+1)/2, which is the same as floor((i+1)/2).

So the number of even s in 0..i is (i//2) +1.

Similarly, the number of odd s in 0..i is (i+1) // 2.

Because for i even, the number of odd numbers is (i//2) → for i=2, (2//2) =1. But the odd numbers are 1 → count is 1. So (i+1)//2 = (2+1)//2 = 1.5 → 1. Correct.

For i=3, (3+1)//2=2, which is correct (1 and 3).

So the number of even s in 0..i is (i//2) +1.

The number of odd s in 0..i is (i+1) // 2.

So for each i, the total number of subarrays that include i and have odd length is:

(number of even s) * count_even_e + (number of odd s) * count_odd_e.

Where count_even_e is the number of even numbers in [i, n-1], and count_odd_e is the number of odd numbers in [i, n-1].

But how to compute count_even_e and count_odd_e?

As before, for the range [i, n-1], the count_even is ((n - i) + (i % 2 == 0)) // 2.

Similarly, count_odd is ((n - i) + (i % 2 == 1 )) // 2.

So for each i, the total contribution of the element at index i to the sum is:

( (i//2 +1) * count_even_e + ( (i+1)//2 ) * count_odd_e ) * value of the element.

Wait, no. Because for each such subarray that includes i and has odd length, the element at i is part of that subarray. So the contribution of the element to the total sum is the number of such subarrays multiplied by the element's value.

So for each i, the contribution is (number of subarrays that include i and have odd length) * arr[i].

So the total sum is the sum over all i of arr[i] * (number of such subarrays).

This seems promising. So the steps are:

For each element in the array, calculate the number of subarrays that include it and have odd length, multiply by the element's value, and sum all these.

So the code would be:

def odd_length_sum(arr):
    total = 0
    n = len(arr)
    for i in range(n):
        # compute count_even_e and count_odd_e for the range [i, n-1]
        a = i
        b = n - 1
        count_even_e = ((b - a + 1) + (a % 2 == 0)) // 2
        count_odd_e = ((b - a + 1) + (a % 2 == 1)) // 2
        # number of even s in 0..i is (i//2) +1
        even_s_count = (i // 2) + 1
        odd_s_count = (i + 1) // 2
        # compute the number of subarrays that include i and have odd length
        # for even s: count_even_e
        # for odd s: count_odd_e
        total += arr[i] * (even_s_count * count_even_e + odd_s_count * count_odd_e)
    return total

Wait, but wait. For each s in 0..i, the count_even_e is the number of e's in [i, n-1] that have the same parity as s. So for even s, the count is count_even_e. For odd s, the count is count_odd_e.

But the number of even s in 0..i is even_s_count, and the number of odd s is odd_s_count. So the total number of subarrays is even_s_count * count_even_e + odd_s_count * count_odd_e.

Yes.

Let me test this with the example.

Example: [1,2,4], n=3.

For i=0:

a =0, b=2.

count_even_e: (b -a +1) is 3. a is even (0), so (3 + 1) // 2 = 4//2=2. So count_even_e=2.

count_odd_e: (3 + 0) // 2 = 3//2=1 (since a is even, so (a%2 ==1 is false, so 3 + 0 =3, 3//2=1).

even_s_count = (0//2) +1 = 0 +1 =1.

odd_s_count = (0+1)//2 = 1//2=0.

So total for i=0 is 1*2 + 0*1 = 2. Multiply by arr[0] (1) → 2*1=2.

For i=1:

a=1, b=2.

count_even_e: (2-1+1)=2. a is 1 (odd). So (2 + 0) //2 = 2//2=1.

count_odd_e: (2 +1) //2 = 3//2=1.

even_s_count = (1//2) +1 = 0 +1=1.

odd_s_count = (1+1)//2 = 1.
```

</details>

**Code that ran:**

```python
def odd_length_sum(arr):
    total = 0
    n = len(arr)
    for i in range(n):
        a = i
        b = n - 1
        count_even_e = ((b - a + 1) + (a % 2 == 0)) // 2
        count_odd_e = ((b - a + 1) + (a % 2 == 1)) // 2
        even_s_count = (i // 2) + 1
        odd_s_count = (i + 1) // 2
        total += arr[i] * (even_s_count * count_even_e + odd_s_count * count_odd_e)
    return total
```

**Visible-test report:**

```text
PASS    assert odd_length_sum([1,2,4]) == 14
1 of 1 visible tests passed
```
