# Mbpp/782, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/782/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 319.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that calculates the sum of all odd-length subarrays of a given array. The example given is that for [1,2,4], the sum is 14. Let me think about how to approach this.

First, I need to understand what a subarray is. A subarray is a contiguous part of an array. So for example, in [1,2,4], the subarrays of length 1 are [1], [2], [4]. Length 3 is [1,2,4]. So the odd-length subarrays here are of lengths 1 and 3. Their sum is 1 + 2 + 4 + (1+2+4) = 1 + 2 + 4 + 7 = 14. Which matches the example.

So the task is to find all possible subarrays of odd lengths and sum them up.

The brute force approach would be to generate all possible subarrays of odd lengths, sum them. But for larger arrays, this could be inefficient. However, given that the problem is for a coding challenge, maybe the constraints are manageable.

But let's think about how to do this efficiently.

Let me think about the possible approach. For each possible starting index, and for each possible ending index, check if the length is odd. But that's O(n^2) time, which is acceptable for small n. But for larger n, maybe there's a smarter way.

Alternatively, for each possible center of the subarray, and expand outward. But I'm not sure.

Wait, the problem is to find the sum of all odd-length subarrays. Let's think about the sum for each possible length. For example, for each possible odd length l (like 1,3,5,...), compute the sum of all subarrays of length l, and add them all.

But how to compute the sum of all subarrays of length l?

For example, for l=1, the sum is the sum of all elements. For l=3, the sum is sum of elements at positions 0-2, 1-3, 2-4, etc. So for each l, the sum can be calculated by sliding window.

But for each l, the number of subarrays is n - l + 1. So for each l, we can compute the sum of all subarrays of length l, and add them all.

But the problem is that for l to be odd, we need to iterate over all possible l's that are odd. So for example, for an array of length n, the possible l's are 1,3,..., up to n if n is odd, or n-1 if n is even.

But how to compute the sum for each l?

Let me think. For each possible l (odd), compute the sum of all subarrays of length l.

But for each l, the sum can be calculated by:

sum = 0

for i in 0 to n - l:

    sum += sum of elements from i to i + l - 1

But for each l, this would take O(n) time. So overall, the time complexity would be O(n^2) for all possible l's. But for n up to say 1e4, this would be O(1e8) which is too slow. But perhaps for the problem's constraints, this is acceptable. However, the problem may require a more efficient approach.

But given that the problem is to find the sum for all odd-length subarrays, perhaps there's a smarter way.

Let me think about the sum of all subarrays of odd length. Let me think about the contribution of each element to the total sum.

For example, each element is part of some subarrays. The question is, for each element, how many times does it contribute to the sum of odd-length subarrays.

So, for each element at position i, we can find the number of odd-length subarrays that include this element, and then multiply by the element's value and sum all these.

But how to compute that?

Let me think. For a given element at index i, how many odd-length subarrays include it?

The subarrays that include i can be of any odd length. But the subarrays that include i must have length odd. So for each element, we need to find the number of subarrays that include it and have odd length.

But how to compute that?

Let me think. For a given element at index i, the number of subarrays that include it and have odd length can be calculated as follows.

The number of subarrays that include i and have odd length is equal to the number of possible left and right boundaries such that the subarray is of odd length.

Alternatively, for each element, the number of subarrays that include it and have odd length can be calculated by considering the number of possible positions to the left and right of i where the subarray can be formed.

But perhaps there's a formula here.

Let me think. For a given element at index i, the number of subarrays that include i and have odd length can be calculated as:

The number of possible subarrays that start at some position <= i and end at some position >= i, such that the length is odd.

Let me think of the left and right boundaries.

For a subarray to include i, the left boundary can be from 0 to i, and the right boundary can be from i to n-1. So the length of the subarray is (right - left + 1). For this to be odd, (right - left + 1) must be odd. Which implies that (right - left) is even. So right - left is even.

So for each i, the number of possible (left, right) pairs where left <= i <= right, and right - left is even.

But how to compute this?

Alternatively, for each element at position i, the number of subarrays that include it and have odd length can be found by considering the number of possible subarrays that include i and have odd length.

Let me think of the possible subarrays that include i. For example, the subarray can start at any position from 0 to i, and end at any position from i to n-1. But the length must be odd.

So for each possible start and end, the length is (end - start + 1) must be odd. So end - start + 1 is odd => end - start is even => end and start have the same parity.

So for each i, the number of subarrays that include i is the number of pairs (start, end) where start <= i <= end, and start and end have the same parity.

But how to compute this?

Alternatively, for each i, the number of subarrays that include i and have odd length is equal to the number of possible left positions (from 0 to i) and right positions (from i to n-1) such that (right - left + 1) is odd.

But perhaps there's a way to compute this using the number of possible left and right positions.

Let me think. For a given i, the number of subarrays that include i and have odd length can be calculated as follows:

The number of subarrays that start at some position <= i and end at some position >= i, and the length is odd.

Let me think of the number of subarrays that include i and have length odd.

Let me think of the left side of i. Let's say the left side can be from 0 to i. For each possible left, the right side can be from i to n-1. The length is (right - left + 1). For this to be odd, (right - left + 1) must be odd. Which is equivalent to (right - left) is even. So (right - left) is even => right and left have the same parity.

So for each left (from 0 to i), the number of right positions (from i to n-1) where right has the same parity as left.

But how to compute this?

Alternatively, for each i, the number of subarrays that include i and have odd length is equal to the number of possible left positions (from 0 to i) multiplied by the number of possible right positions (from i to n-1) where right and left have same parity.

But how to compute that?

Alternatively, for each i, the number of subarrays that include i and have odd length is equal to the number of possible left positions (from 0 to i) multiplied by the number of possible right positions (from i to n-1) where (right - left) is even.

But perhaps this is getting too complicated.

Alternatively, for each i, the number of subarrays that include i and have odd length can be calculated as follows:

Let's consider the left part. The left can be from 0 to i. The right can be from i to n-1. For each left, the number of right positions where (right - left) is even.

But since left is fixed, and right varies from i to n-1, the parity of right and left must be same.

Let me think. For a given left, the parity of left is fixed. So for each right in i to n-1, the parity of right must be same as left's parity.

So the number of right positions for a given left is equal to the number of elements in the range [i, n-1] that have the same parity as left.

But how to compute this?

Let me think. For a given left (say, left = l), the parity of l is fixed. The number of right positions (r) in [i, n-1] where r has the same parity as l.

So for each l in 0..i, the number of r in [i, n-1] with r's parity same as l.

But since l can be from 0 to i, and for each l, the number of r's is the count of numbers in the range [i, n-1] with the same parity as l.

But perhaps this can be calculated as follows:

The total number of elements in [i, n-1] is (n - i). Let's call this m.

The number of elements with parity same as l is:

If the parity of l is even, then the count is (number of even numbers in [i, n-1]).

Similarly for odd.

But how to compute that?

Alternatively, the number of elements in [i, n-1] with parity same as l is ( (n - i) + ( ( (n - i) % 2) - ( (l % 2) - ( (n - i) % 2 )) )) ) / 2 ?

Not sure. Maybe there's a better way.

Alternatively, for the range [i, n-1], the number of elements with parity same as l is:

Let's say the total elements in the range is m = n - i.

The number of elements with parity same as l is:

If m is even, then if the parity of l is even, then m/2 elements. If l is odd, then m/2 elements.

If m is odd, then if l is even, then (m + 1)/2 elements. Wait, no. Let me think. For example, if m is 3, and l is even. The numbers in the range [i, n-1] have 2 even numbers and 1 odd. So the count is 2. Which is (m + 1) // 2 if l is even? Wait, no. Let me think again.

The number of even numbers in a range can be calculated as:

The first number in the range is i, the last is n-1.

The number of even numbers is ((last - first) // 2) + 1 if first and last are even, or something like that. But perhaps there's a formula.

But maybe for the purpose of this problem, we can calculate the count as follows:

For the range [i, n-1], the number of elements with parity same as l is:

count = ( ( (n-1 - i) // 2 ) + 1 ) if (i % 2 == l % 2) else ( (n - i - 1) // 2 + 1 )

Wait, no. Let's think of the number of elements in [i, n-1] with parity same as l.

Let me think of the parity of i and the parity of l.

If the parity of i is same as l, then the count is ( (n - i) + 1 ) // 2 ?

No. Let me take an example. Suppose i is even, and the range is from i to n-1. Let's say n-1 is even. Then the count is (n - i) / 2 + 1? Or (n - i) / 2 ?

Wait, for example, if the range is [0, 2], which is 3 elements (0,1,2). The even numbers are 0, 2. So count is 2. Which is (3 + 1) // 2 = 2. If the range is [0, 3], then the even numbers are 0, 2. Count is 2. (3 + 1) // 2 = 2. So yes.

Another example: range [1, 3], which has 3 elements. The even numbers are 2. So count is 1. (3 + 1) // 2 is 2, but the actual count is 1. So that formula is not correct.

Hmm, so perhaps the formula is ( ( (n - i) + 1 ) // 2 ) if the parity of i is same as l. Wait, but in the previous example, when the range is [1,3], which has 3 elements. i is 1 (odd). l is odd. So the count is 1 (element 3 is odd). So (3 + 1) // 2 is 2, but actual count is 1. So that formula is not correct.

Hmm. So perhaps I need to find a way to compute the number of elements in [i, n-1] with the same parity as l.

Let me think of the number of elements in the range [a, b] with parity p. Where a = i, b = n-1.

The number of elements with parity p is:

If a and b have the same parity, then (b - a) // 2 + 1.

Else, (b - a + 1) // 2.

Wait, let's test this.

Case 1: a = 0, b = 2 (even). So same parity. (2-0)/2 +1 = 1 +1 = 2. Correct.

Case 2: a = 1, b = 3 (odd). Same parity. (3-1)/2 +1 = 1 +1 = 2. But the actual count is 2 (elements 1 and 3). Correct.

Case 3: a = 1, b = 4 (odd). Then (4-1)/2 +1 = 1.5? No. Wait, (4-1) is 3, which is odd. So the formula is (b - a) // 2 + 1 if same parity. But (b - a) is 3, which is odd. So (3//2) is 1, plus 1 is 2. But the elements are 1, 3, 4 (wait, no, a=1, b=4. So elements are 1,2,3,4. The odd numbers are 1,3. So count is 2. Which is correct. So the formula works.

Another example: a=0, b=1 (even and odd). So different parity. (b - a + 1) // 2 = (2) // 2 = 1. Which is correct (only 0 is even). So yes.

So the formula for the number of elements in [a, b] with parity p is:

if (a % 2 == b % 2):

    count = (b - a) // 2 + 1

else:

    count = (b - a + 1) // 2

But how to compute this in code?

Alternatively, the number of elements with parity same as l is:

count = ( (n - i) + ( ( (n - i) % 2 ) - ( (l % 2) - ( (n - i) % 2 )) )) ) // 2 ?

Not sure. But perhaps the formula can be simplified as:

count = ((n - i) + 1) // 2 if (i % 2 == l % 2) else (n - i) // 2

Wait, let's test:

For example, if i is 0, l is 0 (same parity). The range is [0, n-1], which has length n. So count is (n + 1) // 2. Which is correct.

If i is 0, l is 1 (different parity). The range is [0, n-1]. The count is (n) // 2. Which is correct.

But how to compute this in code?

Alternatively, for the range [i, n-1], the number of elements with parity same as l is:

if (i % 2) == (l % 2):

    count = ( (n - 1 - i) + 1 ) // 2 + 1 ?

Wait, no. Wait, the length of the range is (n - i). So the number of elements with same parity is:

if the parity of i is same as l, then the number is ((n - i) + 1) // 2 ?

Wait, let me think again. For example, when i is 0, and the range is from 0 to n-1 (length n). The number of elements with same parity as i (0) is (n + 1) // 2 if n is even? No, that's not correct.

Wait, the formula for the number of elements in the range [i, n-1] with parity same as l is:

if (i % 2 == l % 2):

    count = ( (n - i) + 1 ) // 2

else:

    count = ( (n - i) ) // 2

Wait, let's test for i=0, l=0 (same parity). The range is [0, n-1], which has length n. So count is (n + 1) // 2. Which is correct for even and odd n?

For example, n=3 (i=0, range [0,2], length 3). (3+1)/2 = 2. Which is correct (0,2).

n=4: (4+1)/2= 2.5 → 2.5? No, integer division. (n - i) is 4. (4 + 1) // 2 = 2.5 → 2. But in reality, for range [0,3], the count is 2 (0 and 2). So yes.

Another example: i=1, l=1. The range is [1, n-1], length is n - 1. If n is 4, then the range is [1,3], length 3. (3 + 1) // 2 = 2. Which is correct (1 and 3).

So yes, the formula is:

if (i % 2 == l % 2):

    count = (n - i + 1) // 2

else:

    count = (n - i) // 2

But how to compute this?

But for each i, l is fixed (the parity of i). So for each i, the number of right positions (r) in [i, n-1] where r has the same parity as i is:

count = ( (n - i) + 1 ) // 2 if i's parity is same as l's parity (which is the same as i's parity, since l is i's parity).

Wait, no. Because l is the parity of i. So for each i, the parity of l is the same as i's parity. So the count is (n - i + 1) // 2.

Wait, no. Because the parity of l is the same as i's. So for the range [i, n-1], the number of elements with same parity as i is (n - i + 1) // 2.

But wait, the formula for the count is:

count = ( (n - i) + 1 ) // 2 ?

Wait, the length of the range is (n - i). So the formula is ( (n - i) + 1 ) // 2 ?

Yes. For example, when the length is 3, (3 + 1) // 2 = 2. Which is correct.

So for each i, the number of right positions (r) in [i, n-1] with same parity as i is (n - i + 1) // 2.

But then, for each i, the number of subarrays that include i and have odd length is the number of left positions (from 0 to i) with same parity as i, multiplied by the number of right positions (from i to n-1) with same parity as i.

Wait, no. Because for each left position l (from 0 to i), the right positions r (from i to n-1) must have same parity as l. But that's not the case. Because for each left position l, the parity of l is fixed. So for each l, the number of r's with same parity as l is (n - i + 1) // 2. But that's only if l has the same parity as i.

Wait, no. For each left position l (from 0 to i), the parity of l is fixed. For example, if l is even, then the number of r's in [i, n-1] with same parity as l is (n - i + 1) // 2. But that's only if l's parity is same as i's parity.

Wait, no. For each left position l, the parity of l is fixed. So for each l, the number of r's in [i, n-1] with same parity as l is (n - i + 1) // 2 if l's parity is same as i's parity? No. Wait, the parity of l is fixed. So for example, if l is even, then the number of r's in [i, n-1] with same parity as l is (n - i + 1) // 2. But this is only if the parity of l is same as i's parity. Wait, no. Because l is varying from 0 to i. So for each l in 0 to i, the parity of l is fixed. So for example, if i is even, then l can be even or odd. So the number of r's for each l depends on the parity of l.

This seems complicated. Maybe this approach is not the best.

Alternative approach: Let's think about the total number of subarrays of odd length. For each element, how many times does it contribute to the sum?

Let me think of the following. For each element at position i, the number of subarrays that include it and have odd length is equal to the number of subarrays that start at some position <= i and end at some position >= i, and the length is odd.

But how to compute this?

Let me think of the number of subarrays that include i and have odd length. Let me consider that for a subarray to include i, the start can be from 0 to i, and the end can be from i to n-1. The length is (end - start + 1) must be odd.

Which is equivalent to (end - start) is even.

So for each start in 0 to i, and end in i to n-1, such that end - start is even.

But how to count this?

For each start, the end must be such that end is congruent to start mod 2.

So for a given start, the number of ends in [i, n-1] that are congruent to start mod 2 is equal to the number of elements in [i, n-1] with same parity as start.

So for each start in 0 to i, the count is the number of ends in [i, n-1] with same parity as start.

But since the start can vary from 0 to i, and for each start, the count depends on the parity of the start.

But this seems complicated. However, perhaps we can find that for each i, the total number of subarrays that include i and have odd length is equal to the number of possible start positions (from 0 to i) multiplied by the number of possible end positions (from i to n-1) with same parity as start.

But how to compute this?

Alternatively, for each i, the total number of subarrays that include i and have odd length is equal to the number of possible (start, end) pairs where start <= i, end >= i, and end - start is even.

But how to compute this?

Another idea: the number of such subarrays is equal to the number of subarrays that include i and have odd length. Let's think of the subarrays that include i and have odd length. For each such subarray, the start can be from 0 to i, and the end can be from i to n-1. The length is odd.

Let me think of the start and end as follows: the start can be any value from 0 to i, and the end can be any value from i to n-1. The length is (end - start + 1) must be odd. So end - start is even.

So for a given i, the number of such pairs is the number of (start, end) pairs where start <= i, end >= i, and end - start is even.

But how to compute this?

Let me think of the start and end as follows. For each start, the end must be such that end is congruent to start mod 2. So for each start, the number of ends in [i, n-1] with the same parity as start is the same as the count we discussed earlier.

So for each start, the number of ends is ( (n - i) + 1 ) // 2 if the start's parity is same as i's parity?

No, that's not right. Because the start can have any parity. So for each start, the number of ends with same parity as start is:

if the start's parity is same as the parity of i, then the count is (n - i + 1) // 2 ?

No. Wait, the start's parity is fixed. For example, if the start is even, then the number of ends in [i, n-1] with even parity is (n - i + 1) // 2 if the parity of i is even?

No, that's not correct. Because the parity of the start is fixed, and the parity of the end is fixed. So for example, if the start is even, then the number of ends in [i, n-1] with even parity is ( (n - i) + 1 ) // 2 if the parity of i is even?

No, that depends on the parity of the start and the parity of the range.

This seems too complicated. Maybe there's a better way.

Let me think of the total number of subarrays of odd length. For each i, the number of subarrays that include i and have odd length is equal to the number of possible subarrays that include i and have odd length.

But for a subarray to include i, the start can be from 0 to i, and the end can be from i to n-1. The length is (end - start + 1) must be odd. Which is equivalent to (end - start) is even.

So for each i, the total number of subarrays that include i and have odd length is equal to the number of (start, end) pairs where start is in [0, i], end is in [i, n-1], and end - start is even.

But how to compute this?

Let me think of the number of possible (start, end) pairs where start is in [0, i], end is in [i, n-1], and end - start is even.

Let me think of the start and end as variables. For each start, the end must be in the range [i, n-1] and have the same parity as start.

So for each start, the number of ends is the number of elements in [i, n-1] with the same parity as start.

So the total number is the sum over all start in [0, i] of the number of ends in [i, n-1] with same parity as start.

But since the start can be any value from 0 to i, and for each start, the number of ends is the same as the count we discussed earlier.

But how to compute this sum?

Let me think. For the start in 0 to i, the number of ends with same parity as start is:

If the start's parity is even, then the number of ends in [i, n-1] with even parity is ( (n - i) + 1 ) // 2 if the parity of i is even?

No, that's not correct. It depends on the parity of the start and the parity of the range.

But maybe for all start in 0 to i, the sum of the number of ends with same parity as start is equal to the number of possible (start, end) pairs where start is in 0..i and end is in i..n-1 and end - start is even.

But how to compute this sum?

Let me think of the sum as follows:

For each start in 0..i, the number of ends in [i, n-1] with same parity as start is:

If the parity of start is same as the parity of i, then the count is (n - i + 1) // 2.

If the parity of start is different from i's parity, then the count is (n - i) // 2.

But how to compute this?

For example, the number of starts with even parity in [0, i] is:

if i is even: (i + 1) // 2

if i is odd: (i) // 2

Similarly for odd parity.

But this seems complicated. However, for the sum over all starts in 0..i of the number of ends with same parity as start, it's equal to the number of ends in [i, n-1] with same parity as start for each start.

But this is equal to the total number of (start, end) pairs where start is in 0..i and end is in i..n-1 and end has same parity as start.

But this is equal to the number of pairs where end has same parity as start, and start is in 0..i, end is in i..n-1.

But this is equal to the number of pairs (start, end) where start is in 0..i, end is in i..n-1, and end has same parity as start.

But how to compute this?

Let me think of the total number of such pairs as follows:

Let me consider that for each start, the number of ends with same parity as start is:

If the start's parity is even, then the number is ( (n - i) + 1 ) // 2 if the parity of i is even, or ( (n - i) // 2 ) if the parity of i is odd.

Wait, no. For example, if the parity of i is even, then the number of ends in [i, n-1] with even parity is (n - i + 1) // 2. Because the range is [i, n-1], which has length (n - i). So the number of even numbers in this range is ( (n - i) + 1 ) // 2 if the parity of i is even.

But this is only true if the parity of i is even. So for each start, the number of ends depends on the parity of start and i.

This seems very complex. Perhaps there's a simpler way.

Another idea: For the entire array, the number of odd-length subarrays is equal to the sum over all possible odd lengths l (1, 3, ..., up to n if odd) of (n - l + 1) * (sum of elements in the subarray of length l).

But how to compute this sum for all odd l.

But for the example [1,2,4], the odd lengths are 1 and 3.

For l=1: sum is 1 + 2 + 4 = 7.

For l=3: sum is 1+2+4 = 7.

Total sum is 7 + 7 = 14, which matches the example.

So the problem can be approached by calculating for each odd l, the sum of all subarrays of length l, and summing them.

Now, how to compute the sum of all subarrays of length l.

For each l, the sum of subarrays of length l can be calculated using the sliding window technique. For example, for l=1, it's the sum of all elements. For l=3, it's sum of elements 0-2, 1-3, 2-4, etc.

So the total sum is the sum for all odd l of the sum of all subarrays of length l.

But how to compute this efficiently.

For example, for l=1, the sum is sum(arr).

For l=3, it's sum(arr[0:3], arr[1:4], ...).

So for each l, the sum can be computed as follows:

sum_subarrays = 0

for i in range(0, len(arr) - l + 1):

    sum_subarrays += sum(arr[i:i+l])

But this is O(n^2) time, which is acceptable for small n.

But for larger n, it's O(n^2) time, which may be acceptable for the problem's constraints.

But the problem says to write a correct Python function, and the example given is [1,2,4], which is small.

So perhaps the brute force approach is acceptable here.

Let's proceed with this approach.

So, the steps for the function:

1. Iterate over all possible odd lengths l.

2. For each l, compute the sum of all subarrays of length l.

3. Add all these sums together.

Now, the code:

def odd_length_sum(arr):

    n = len(arr)

    total = 0

    for l in range(1, n + 1):

        if l % 2 == 1:

            # compute sum of all subarrays of length l

            for i in range(0, n - l + 1):

                total += sum(arr[i:i+l])

    return total

But wait, for l=1, the loop runs from i=0 to n - 1, which is correct.

But for l=3, it runs for i=0 to n - 3, etc.

But this code would work for small arrays.

Let's test it with the example.

Example: [1,2,4]

n = 3.

l ranges from 1 to 3.

For l=1: 3 subarrays, sum 1+2+4=7.

For l=3: 1 subarray, sum 7.

Total is 7 + 7 =14. Which matches.

But what about for a larger array?

For example, [1,2,3,4].

Odd lengths are 1,3.

For l=1: sum of all elements 1+2+3+4=10.

For l=3: sum of [1,2,3] + [2,3,4] = 6 + 9 = 15.

Total is 10 + 15 = 25.

But let's compute manually:

All odd-length subarrays:

Length 1: 1,2,3,4 → sum 10.

Length 3: [1,2,3], [2,3,4] → sum 6 + 9 = 15.

Total 25. Correct.

So the code works.

But what about for l=5 in an array of length 5?

Yes, it would compute it.

But for larger arrays, this code may be slow. However, for the problem's purposes, it's acceptable.

But the code may be optimized. For example, precomputing prefix sums.

Let me think about how to optimize this.

The sum of subarrays of length l can be computed using prefix sums.

For example, the sum of arr[i:i+l] is equal to prefix[i + l] - prefix[i].

So, for each l, the sum of all subarrays of length l is sum_{i=0}^{n - l} (prefix[i + l] - prefix[i]).

But how to compute this efficiently.

The prefix sum array can be precomputed once.

So, the code can be optimized as follows:

Compute prefix sums, then for each odd l, compute the sum of all subarrays of length l.

Let me write this code.

First, compute prefix sum:

prefix = [0] * (n + 1)

for i in range(n):

    prefix[i+1] = prefix[i] + arr[i]

Then, for a subarray from i to i + l - 1, the sum is prefix[i + l] - prefix[i].

So, for each odd l:

sum_subarrays = 0

for i in range(0, n - l + 1):

    sum_subarrays += prefix[i + l] - prefix[i]

So, the total sum is the sum of all these for each odd l.

This approach is O
```

</details>

**Code that ran:**

```python
def odd_length_sum(arr):
    n = len(arr)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    total = 0
    for l in range(1, n + 1):
        if l % 2 == 1:
            for i in range(n - l + 1):
                total += prefix[i + l] - prefix[i]
    return total
```

**Visible-test report:**

```text
PASS    assert odd_length_sum([1,2,4]) == 14
1 of 1 visible tests passed
```
