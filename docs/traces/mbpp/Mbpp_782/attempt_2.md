# Mbpp/782, attempt 2

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`Mbpp/782/a2/r1`)

Visible tests: **pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 157.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that calculates the sum of all odd-length subarrays of a given array. The example given is that for [1,2,4], the sum is 14. Let me think about how to approach this.

First, what's a subarray? Oh right, a subarray is a contiguous part of the array. So for example, in [1,2,4], the subarrays of length 1 are [1], [2], [4], length 3 are [1,2,4], and length 5 isn't possible here. Wait, but the example says the sum is 14. Let me check that.

Wait, the example says [1,2,4] gives 14. Let me compute that. The odd-length subarrays are:

Length 1: 1 + 2 + 4 = 7.

Length 3: [1,2,4] sum is 7. So total is 7 +7 =14. Yes, that's correct.

So the problem is to find all subarrays of odd lengths and sum them up.

So the challenge is to find all possible subarrays of odd lengths and sum them.

But how to do that efficiently?

Let me think about the brute force approach first. For each possible starting index, and for each possible ending index (starting from start + 1, etc.), check if the length is odd. But for an array of size n, there are O(n^2) subarrays. For n up to say 10^4, that's 1e8 operations, which might be too slow. But maybe for the problem's constraints, it's acceptable. However, the problem might require a more efficient approach.

But let's think about the problem again. Let's think about the sum of all subarrays of odd length. How can we compute this efficiently?

An alternative approach is to find for each element, how many times it appears in odd-length subarrays, and then multiply by the element's value and sum all those.

So for each element at position i, find the number of odd-length subarrays that include this element, and then sum all elements multiplied by their count.

But how to compute that?

Let me think. For a given element at index i, the number of odd-length subarrays that include it depends on the number of possible positions where the subarray starts and ends such that the length is odd.

Alternatively, for each element, the number of odd-length subarrays that include it can be determined by considering the number of possible left and right boundaries.

But perhaps there's a smarter way. Let's think about the total sum of all subarrays of odd length. Let me think of the sum of all subarrays of odd length as the sum of all subarrays of even length, but that's not helpful. Wait, no. Wait, the problem is to find the sum of all odd-length subarrays. So perhaps we can find the sum of all subarrays of odd length by considering the sum of all subarrays of even length and subtracting from the total sum of all subarrays. But that's not directly helpful. Alternatively, maybe we can find the sum of all subarrays of odd length by considering their contribution.

Another approach: For each possible subarray, check if its length is odd. If it is, add it to the sum.

But for a large array, this approach would be O(n^2), which for n=1e4 would be 1e8 operations, which might be acceptable for Python if the code is optimized. But maybe there's a better way.

Let me think about the brute force approach first. Let's take the example array [1,2,4]. The subarrays of odd length are:

Length 1: [1], [2], [4] → sum 7.

Length 3: [1,2,4] → sum 7. Total 14.

So the brute force approach would generate all possible subarrays, check if their length is odd, and sum them.

So for each possible subarray, check if the length is odd. How to generate all subarrays?

The standard way is to loop over all possible start indices, and for each start index, loop over all possible end indices >= start. For each such subarray, check if (end - start + 1) is odd. If yes, add to the sum.

But for an array of size n, there are n*(n+1)/2 subarrays. For each subarray, check if the length is odd. So for each subarray, the time is O(1) to check, but the total time is O(n^2).

For n=1000, that's 1e6 operations. For n=1e4, 1e8 operations. Which might be acceptable in Python for small n, but perhaps not for larger n. However, the problem may not have such constraints, and the code is expected to handle it.

But let's proceed with this approach.

So the code would be something like:

def odd_length_sum(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        for j in range(i, n):
            if (j - i + 1) % 2 == 1:
                total += sum(arr[i:j+1])
    return total

Wait, but for the example [1,2,4], this code would compute:

i=0, j=0: length 1 → add 1.

i=0, j=1: length 2 → skip.

i=0, j=2: length 3 → add sum(1,2,4) =7.

i=1, j=1: length 1 → add 2.

i=1, j=2: length 2 → skip.

i=2, j=2: length 1 → add 4.

Then i=0, j=0, 0,1, 0,2, etc. So total is 1+7+2+4 = 14. Which matches the example.

Yes, that seems correct.

But for larger arrays, this approach would be O(n^2) time, which may be acceptable for small n. However, for n up to 1e4, this would be 1e8 operations. Which may be slow in Python.

But the problem says to write the correct code. So perhaps this approach is acceptable.

But perhaps there's a more efficient way. Let me think.

Alternative approach: For each element, find the number of times it appears in odd-length subarrays.

Let me think about the contribution of each element. For example, for an element at position i, how many times does it appear in odd-length subarrays?

Let me think. For each element, the number of odd-length subarrays that include it can be determined by the number of possible left and right boundaries.

Let me consider that the subarray must have an odd length. So for a given element at index i, the subarray can start at any position from left to i, and end at any position from i to right. But the length of the subarray must be odd.

Alternatively, for a given element at index i, the number of subarrays that include it and have odd length can be calculated as follows.

The number of subarrays that include i and have odd length is equal to the number of ways to choose a starting position (left) and ending position (right) such that left <= i <= right, and (right - left + 1) is odd.

But how to compute this?

Alternatively, for each element, the number of subarrays that include it and have odd length can be calculated as follows:

The total number of subarrays that include i is (i+1) * (n - i) → since for each left in 0..i, and right in i..n-1. But how many of these have odd length?

The length of the subarray is (right - left + 1). So for each subarray that includes i, the length is (right - left + 1). We need this to be odd.

But how to count that?

Let me think: For a given i, the number of subarrays that include i and have odd length is equal to the number of pairs (left, right) where left <= i <= right, and (right - left + 1) is odd.

But perhaps there's a way to compute this.

Let me think: For a given i, the number of subarrays that include i and have odd length can be found by considering the number of possible left and right positions such that the length is odd.

Let me think of the left and right positions. The length is (right - left + 1) = odd. So, right - left + 1 is odd → right - left is even → right - left is even → (right - left) is even → right and left have the same parity.

So for each subarray that includes i, the left and right must have the same parity.

But how to compute this?

Alternatively, for a given i, the number of subarrays that include i and have odd length is equal to the number of possible left positions (from 0 to i) and right positions (from i to n-1) such that (right - left + 1) is odd.

But perhaps there's a smarter way. Let me think of the left and right as follows.

For each i, the number of subarrays that include i and have odd length is equal to the number of pairs (left, right) where left <= i <= right and (right - left + 1) is odd.

But since the subarray must include i, left can be from 0 to i, and right can be from i to n-1.

Let me think of the possible left and right.

Let me consider that for each possible left (from 0 to i), and right (from i to n-1), the length is (right - left + 1). We need this to be odd.

But how to compute this?

Let me think of the parity of (right - left + 1). Since (right - left + 1) is odd if and only if (right - left) is even. So (right - left) is even → right and left have the same parity.

So for each left (from 0 to i) and right (from i to n-1), if left and right have the same parity, then the length is odd.

So for each i, the number of such pairs is equal to the number of lefts and rights where left and right have the same parity.

But how to compute that?

Let me think: For a given i, the left can be from 0 to i. The right can be from i to n-1.

The number of lefts with parity p and the number of rights with parity p.

Let me think: For each left in 0..i, the parity is (left % 2). For each right in i..n-1, the parity is (right % 2). The number of pairs where left and right have the same parity is equal to (number of lefts with even parity) * (number of rights with even parity) + (number of lefts with odd parity) * (number of rights with odd parity).

So for each i, we can compute the number of even and odd lefts and rights.

But how?

Let me think. Let's say for the lefts (0 to i):

number of even lefts = (i+1 + 1) // 2 if i is even, or (i+1) // 2 if i is odd? Wait, perhaps it's easier to compute the count.

The number of even numbers in 0 to i (inclusive) is (i//2) + 1 if i is even, or (i//2 + 1) if i is even? Wait, let me think:

For example, i=0: 0 is even. count is 1.

i=1: 0 is even, 1 is odd. count is 1.

i=2: 0,1,2 → even counts 2 (0,2).

So the count of even numbers in 0..i is (i//2) + 1 if i is even? Or perhaps (i+1)//2 if i is even?

Wait, for i even:

i = 2k → numbers 0 to 2k: there are 2k+1 numbers. The even numbers are 0, 2, ..., 2k → total k+1 numbers. So (i/2) + 1.

For i odd: i=2k+1. The numbers 0 to 2k+1: even numbers are 0, 2, ..., 2k → k+1 numbers. So again, (i+1)//2.

So for any i, the number of even lefts is (i+1) // 2.

Wait, let's check:

i=0 → (0+1)//2 = 0.5 → integer division gives 0? Wait, no. Wait, (i+1)//2 for i=0 is (0+1)//2 = 1//2 = 0. But the actual count is 1. So that's not correct.

Hmm, perhaps I need to find a better way. Let me think again.

The number of even numbers between 0 and i (inclusive) is equal to:

if i is even: (i/2) + 1.

if i is odd: (i+1)/2.

But in code, (i + 1) // 2 when i is even?

Wait, for i=0: (0+1)//2 = 0.5 → 0 in integer division. But the correct count is 1. So that's not right.

Alternatively, the number of even numbers from 0 to i is (i + 1) // 2 if i is even?

Wait, let me think for i=0:

i is even. (i+1) // 2 = (0+1)//2 = 0.5 → 0 in integer division. But the correct count is 1.

Hmm. Maybe I need to think of it as floor((i + 1)/2) ?

Wait, for i=0: (0+1)/2 = 0.5 → floor is 0. But the count is 1.

No. So perhaps the correct formula is (i//2) + 1 if i is even, and (i//2 + 1) if i is odd?

Wait, for i=0 (even): i//2 is 0, +1 is 1 → correct.

i=1 (odd): i//2 is 0, +1 is 1 → correct (0 is even, 1 is odd).

i=2 (even): i//2 is 1, +1 is 2 → correct (0, 2).

i=3 (odd): i//2 is 1, +1 is 2 → correct (0, 2).

Yes. So the number of even numbers in 0..i is (i//2) + 1 if i is even, and (i//2) + 1 if i is odd? Wait, no. Wait, for i=3 (odd), i//2 is 1, +1 is 2. Which is correct (0, 2). So for any i, the number of even numbers in 0..i is (i//2) + 1.

Wait, but for i=0, (0//2) +1 is 0 +1 =1, correct. So yes.

So the number of even numbers in 0..i is (i//2) + 1.

Similarly, the number of odd numbers in 0..i is i+1 - (i//2 +1) = (i+1) - (i//2 +1) = i - i//2.

But perhaps that's not necessary. Let me think again.

So for the lefts (0..i), the number of even lefts is (i//2) + 1, and the number of odd lefts is i - (i//2) + 1? Wait, no. Let me think: total numbers is i+1. The number of even is (i//2) + 1. Then the number of odd is (i+1) - (i//2 +1) = i - i//2.

But for i=0, (i//2) +1 = 0 +1 =1. So the number of even is 1, odd is 0. Which is correct.

So for the lefts, the number of even is (i//2) +1, and the number of odd is (i+1) - (i//2 +1) = i - (i//2) = (i - (i//2)).

Similarly for the rights, which are from i to n-1. So for the rights, the number of even rights is ( (n-1 - i) + 1 ) // 2 ?

Wait, for the rights, the numbers are from i to n-1. So the count is (n-1 - i +1) = n -i.

So the number of even rights is ( (n - i) + 1 ) // 2 ?

Wait, for example, if i=0, n=3 (so rights are 0,1,2). The number of even rights is 1 (0 and 2). So for n=3, i=0, the number of even rights is 2. Let's compute (n - i) is 3, so (3 +1)//2 = 2. Correct.

So the number of even rights is ( (n - i) + 1 ) // 2 ?

Wait, no. The number of even numbers in a range from a to b inclusive is equal to ( (b - a) // 2 ) + 1 if a and b are even, but maybe there's a better way. Alternatively, for the rights, the number of even numbers is:

count_even_rights = ( (n - i) + 1 ) // 2 if (n - i) is even? No, perhaps not. Let me think.

The number of even numbers in the range [i, n-1] is equal to:

if the first number (i) is even, then the count is ( (n -1 - i) // 2 ) + 1.

But perhaps there's a simpler way. Let me think of the number of even numbers in the range from a to b inclusive is ( (b - a) // 2 ) + 1 if a and b are even, but I'm not sure. Alternatively, the count is ( (b - a) // 2 ) + 1 if a is even and b is even, but this is getting complicated.

Alternatively, the number of even numbers in the range [i, n-1] is equal to ( (n - 1 - i) + 1 ) // 2 if (i is even) and (n-1 -i) is even? No, maybe not. Let me think of the number of even numbers in a range from a to b inclusive.

The formula is floor( (b - a) / 2 ) + 1 if a and b are even? Not sure. Let me think of a simple example.

For example, a=0, b=2: numbers 0,1,2. Even numbers: 0, 2 → count 2. (b -a) is 2. (2 / 2) + 1 = 1 + 1 = 2. Correct.

Another example: a=0, b=3 → numbers 0,1,2,3. Even numbers: 0,2 → count 2. (b -a) is 3. (3//2) + 1 = 1 +1=2. Correct.

Another example: a=1, b=3. Numbers 1,2,3. Even numbers: 2 → count 1. (3-1)/2 = 1 → 1 +1=2? No. Wait, (b -a) is 2. (2//2) +1 = 1 +1=2. But actual count is 1. So this formula is wrong.

Hmm. So perhaps the formula is ( (b - a) // 2 ) + 1 if the first number is even, but I'm not sure.

Alternatively, the number of even numbers in [a, b] is equal to ((b - (a % 2)) // 2) + 1 if a is even, but this is getting complicated.

Alternatively, the number of even numbers between a and b inclusive can be calculated as:

count_even = ((b - (a % 2)) // 2) + 1 if a is even else ((b - (a % 2)) // 2) + 1 ?

No, this isn't helpful.

Alternatively, since the parity of the numbers depends on their position, perhaps the number of even numbers in [i, n-1] is equal to ( (n -1 - i) + 1 ) // 2 if (i is even) or something like that. But this is getting too complicated.

Alternatively, for the rights, the number of even numbers is ( (n -1 - i) + 1 ) // 2 if (i is even) or (n -1 -i) is even? Not sure.

But maybe there's a better way. Let's think of the number of even numbers in the range [i, n-1] as follows:

The total number of numbers in the range is (n - i). The number of even numbers is equal to the ceiling of ( (n - i) / 2 ) if the first number is even, else the floor of ( (n - i) / 2 ) + 1 ?

Alternatively, the number of even numbers is ( (n - i) + ( (i % 2) == 0 ) ) // 2 ?

Not sure.

Alternatively, for the rights, since they are from i to n-1, the parity of the first element (i) and the last element (n-1) determines the count. But this is getting too complicated.

But perhaps for the purpose of this problem, we can compute the number of even and odd rights as follows:

The number of even rights is ( (n - i) + ( (i % 2) == 0 ) ) // 2 ?

No, perhaps not. Let me think of the number of even numbers in a range from a to b inclusive. The formula is:

count_even = ((b - a) // 2) + 1 if (a % 2 == 0 and b % 2 == 0) else ... ?

No, that's not helpful.

Alternatively, the number of even numbers in the range [a, b] is equal to ( (b - a) // 2 ) + 1 if a is even, else ( (b - a) // 2 ) + 1 if a is even? No.

Alternatively, for any range, the number of even numbers is ( (b - a) // 2 ) + 1 if a is even, else ( (b - a) // 2 ) if a is odd.

Wait, let's take an example. a=1, b=3. The numbers are 1,2,3. The even numbers are 2 → count 1. (b - a) is 2. (2//2) =1. So if a is odd (1), then the count is 1. Which is correct.

Another example: a=0, b=3. Numbers 0,1,2,3. Even numbers 0,2 → count 2. (3-0) =3. 3//2 =1. So if a is even (0), then count is 1+1=2. Which is correct.

Another example: a=0, b=2. Numbers 0,1,2. Even count is 2. (2-0) is 2. 2//2 is 1. So if a is even, count is 1 +1=2. Correct.

So the formula for the number of even numbers in [a, b] is:

if a is even:

count_even = ((b - a) // 2) + 1

else:

count_even = ((b - a) // 2)

But how to compute this in code?

Well, in code, for the rights (from i to n-1), the number of even rights is:

if i is even:

count_even = ( ( (n - 1) - i ) // 2 ) + 1

else:

count_even = ( ( (n - 1) - i ) // 2 )

But (n-1 - i) is the number of elements in the range. Let me see.

But for the rights, the count is ( (n-1 - i) + 1 ) // 2 if i is even, else ( (n-1 - i) ) // 2 ?

No, perhaps the formula is:

count_even_rights = ( (n - 1 - i) + 1 ) // 2 if i is even else ( (n - 1 - i) ) // 2 ?

Wait, for example, when i is even:

a = i, b = n-1.

The number of even numbers is ((b - a) // 2) + 1 if a is even and b is even?

No, but the formula I derived earlier is:

count_even = ((b - a) // 2) + 1 if a is even.

But for a=0, b=3 (even numbers 0,2 → count 2). (b - a) is 3. 3//2 is 1. 1 +1=2. Correct.

So in code, for the rights, the number of even numbers is:

if i is even:

count_even = ((n -1 - i) // 2) + 1

else:

count_even = ((n -1 - i) // 2)

But wait, (n -1 - i) is the number of elements in the range from i to n-1. So the length is (n - i).

So for example, if i is even, the count_even is ( (n - i - 1) // 2 ) + 1 ?

Wait, (n -1 - i) is (n -i -1). So for example, when i=0, n=3, n-1 -i = 3-1 -0 = 2. 2//2 +1 = 1 +1=2. Correct.

Yes.

So for the rights, the number of even rights is:

if i is even:

count_even_rights = ( (n -1 - i) // 2 ) + 1

else:

count_even_rights = ( (n -1 - i) // 2 )

But (n -1 -i) is (n - i - 1). So in code, it's (n - i - 1) // 2 + 1 if i is even, else (n -i -1) // 2.

But how to compute that in code?

Alternatively, the number of even rights is ( ( (n - i) - ( (i % 2) == 0 ) ) // 2 ) + 1 ?

Not sure.

But perhaps this is getting too complicated. Let me think of another way.

For each element at position i, the number of odd-length subarrays that include it is equal to the number of pairs (left, right) where left <= i <= right and (right - left + 1) is odd.

But since the length is odd, right - left + 1 is odd → right - left is even → right and left have the same parity.

So for each i, the number of such pairs is equal to the number of lefts with parity same as rights.

So for the lefts (from 0 to i), and rights (from i to n-1), the number of pairs where left and right have the same parity.

So the total for the element is (number of even lefts * number of even rights) + (number of odd lefts * number of odd rights).

So for each i, compute:

even_lefts = (i//2) + 1

odd_lefts = (i+1) - even_lefts

even_rights = ?

odd_rights = ?

But how to compute even_rights and odd_rights?

For the rights, the number of even rights is:

if i is even:

even_rights = ( (n - 1 - i) // 2 ) + 1

else:

even_rights = ( (n -1 - i) // 2 )

But perhaps it's easier to compute for the rights:

even_rights = ((n - i) + ( (i % 2) == 0 )) // 2 ?

No, not sure.

Alternatively, the number of even rights is ( (n - i) + 1 ) // 2 if i is even, else (n - i) // 2 ?

Wait, for example:

i=0, n=3. rights are 0,1,2. n - i = 3. (3 +1 )//2 = 2 → which is correct (0 and 2 are even).

If i is even, then even_rights is (n -i +1 ) // 2 ?

Yes. For i=0, n=3: (3+1)/2 = 2. Correct.

For i=0, n=4: rights are 0,1,2,3. even_rights are 0,2 → count 2. (4 - 0) is 4. (4 +1 )//2 = 2.5 → 2. Correct.

So yes, for even i, even_rights = (n -i + 1 ) // 2.

For odd i, even_rights = (n -i ) // 2.

So in code:

if i is even:

even_rights = (n - i + 1) // 2

else:

even_rights = (n - i) // 2

Similarly for odd_rights.

But how to compute odd_rights?

For odd_rights, it's (n -i) - even_rights.

So for the rights, the number of odd_rights is (n -i) - even_rights.

But for the code, perhaps it's easier to compute the number of even and odd rights for the given i.

Once we have the number of even_lefts and even_rights, and odd_lefts and odd_rights, then the total number of pairs is even_lefts * even_rights + odd_lefts * odd_rights.

But then, for each such pair (left, right), the subarray from left to right includes the element at i, and has odd length. So the contribution of the element arr[i] to the total sum is arr[i] * (number of such pairs).

So the total sum is sum over all i of arr[i] * (number of pairs for i).

So the code would be:

def odd_length_sum(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        # compute number of even_lefts and odd_lefts
        even_lefts = (i // 2) + 1
        odd_lefts = i + 1 - even_lefts
        # compute number of even_rights and odd_rights
        if i % 2 == 0:
            even_rights = (n - i + 1) // 2
            odd_rights = (n - i) - even_rights
        else:
            even_rights = (n - i) // 2
            odd_rights = (n - i) - even_rights
        # compute the number of pairs
        count = even_lefts * even_rights + odd_lefts * odd_rights
        total += arr[i] * count
    return total

Wait, but this is for the number of subarrays that include i and have odd length. So the sum of all such subarrays would be arr[i] multiplied by count. So this would give the total sum of all odd-length subarrays.

Let me test this with the example [1,2,4].

n=3.

For i=0:

i=0 is even.

even_lefts = (0//2) +1 = 0 +1 =1.

odd_lefts = 0 +1 - 1 = 0.

For rights:

i=0 is even. even_rights = (3-0 +1)//2 = (3+1)//2 = 2. odd_rights = 3 -0 - 2 = 1.

count = 1 * 2 + 0 * 1 = 2.

so contribution is 1 * 2 = 2.

For i=1:

i=1 is odd.

even_lefts = (1//2) +1 = 0 +1 =1.

odd_lefts = 1 +1 -1 = 1.

rights: i=1 is odd. even_rights = (3-1)//2 = 2//2=1. odd_rights = 3-1 -1 = 1.

count = 1 * 1 + 1 * 1 = 2. contribution is 2 * 2 =4.

For i=2:

i=2 is even.

even_lefts = (2//2) +1 = 1 +1 =2.

odd_lefts = 2 +1 -2 = 1.

rights: even_rights = (3-2 +1)//2 = (2)//2 =1. odd_rights = 3-2 -1 = 0.

count = 2*1 + 1*0 = 2. contribution is 4 *2=8.

Total sum is 2+4+8=14. Which matches the example. So this code works.

So this approach is O(n) time, which is much better than O(n^2) time. So this is the correct approach.

So the code is:

def odd_length_sum(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        even_lefts = (i // 2) + 1
        odd_lefts = i + 1 - even_lefts
        if i % 2 == 0:
            even_rights = (n - i + 1) // 2
            odd_rights = (n - i) - even_rights
        else:
            even_rights = (n - i) // 2
            odd_rights = (n - i) - even_rights
        count = even_lefts * even_rights + odd_lefts * odd_rights
        total += arr[i] * count
    return total

But wait, let me check for i=0 in the example.

i=0:

even_lefts = 1, odd_lefts = 0.

rights: even_rights = (3-0+1)//2 = 4//2=2. odd_rights = 3-0 - 2 = 1.

count = 1*2 + 0*1 = 2. So contribution 1*2=2.

Yes.

Another test case: [1,2,4], which gives 14. So the code returns 14.

Another test case: let's take [1]. The only subarray is length 1, sum is 1. The code:

n=1.

i=0.

even_lefts = (0//2) +1 = 0+1=1.

odd_lefts = 0+1 -1 =0.

rights: i is even. even_rights = (1-0 +1)//2 = 2//2=1. odd_rights = 1-0 -1 =0.

count = 1*1 + 0*0 =1. total += 1*1=1. Correct.

Another test case: [1, 2]. The odd-length subarrays are [1], [2], [1,2] (length 3). Wait, no. Wait, the subarrays of odd length are:

length 1: [1], [2] → sum 3.

length 3: [1,2] is length 2, no. So sum is 3. So the code should return 3.

Let's compute:

n=2.

i=0:

even_lefts = (0//2) +1 = 1.

odd_lefts = 0+1 -1 =0.

rights: i is even. even_rights = (2-0 +1)//2 =3//2=1. odd_rights = 2-0 -1=1.

count = 1*1 + 0*1 =1 → contribution 1*1=1.

i=1:

i is odd.

even_lefts = (1//2) +1 = 0 +1=1.

odd_lefts = 1+1 -1=1.

rights: i is odd. even_rights = (2-1)//2 =1//2=0. odd_rights = 2-1 -0=1.

count = 1*0 +1*1=1. contribution 2*1=2.

total is 1+2=3. Correct.

So the code works.

Therefore, this approach is correct and efficient.

So the code is as above.

Now, the code needs to be written in Python, with the necessary imports. But since there are no imports needed, the code is as follows.

But wait, the code may need to handle the case when the array is empty. But the problem says that the input is a list, and the function is to be written for any input. However, the code handles it as per the logic.

So the final code is:

def odd_length_sum(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        even_lefts = (i // 2) + 1
        odd_lefts = i + 1 - even_lefts
        if i % 2 ==
```

</details>

**Code that ran:**

```python
def odd_length_sum(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        even_lefts = (i // 2) + 1
        odd_lefts = i + 1 - even_lefts
        if i % 2 == 0:
            even_rights = (n - i + 1) // 2
            odd_rights = (n - i) - even_rights
        else:
            even_rights = (n - i) // 2
            odd_rights = (n - i) - even_rights
        count = even_lefts * even_rights + odd_lefts * odd_rights
        total += arr[i] * count
    return total
```

**Visible-test report:**

```text
PASS    assert odd_length_sum([1,2,4]) == 14
1 of 1 visible tests passed
```
