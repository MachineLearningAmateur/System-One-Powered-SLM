# Mbpp/239, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/239/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 753.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to find the number of possible sequences of length n. Each element in the sequence has to be a positive integer. The condition is that each element is at least twice the previous one, and also not exceeding m. Let's think about how to approach this.

Let me start by understanding the example given. The assertion says that get_total_number_of_sequences(10,4) equals 4. Let's see why. For sequences of length 4, each element must be >= twice the previous and <=10.

Let me list all possible sequences. Let's think for the first element. Let's say the first element is a, then the second must be at least 2a, then third at least 2*(second), and so on. So for the first element, possible values are from 1 up to some maximum. Let's think for the example.

For n=4, m=10. Let's think of possible sequences:

Let me think of the first element. Let's see:

The first element can be as big as possible such that even if each next element is twice the previous, the last element is <= m.

For example, for a sequence of length 4, the first element a must satisfy a * 2^3 <= m. Because each step is multiplied by 2. So a * 8 <= 10. So a can be 1 (since 1*8=8 <=10), 2 (2*8=16>10, so no). So only a=1 is possible for the first element. Wait, but then the second element is 2a, which is 2, then third is 4, fourth is 8. So that's one sequence: 1,2,4,8. But the example says the answer is 4. So there must be other sequences.

Wait, maybe there are sequences where the elements are not strictly increasing by doubling each time. For example, maybe the first element is 1, second is 2, third is 4, fourth can be 8 or 9 or 10. Wait, but the third element is 4, so the fourth must be >= 8 (twice 4), but <=10. So possible values for fourth element are 8,9,10. So that would be three possibilities here. Then the sequence could be 1,2,4,8; 1,2,4,9; 1,2,4,10. So that's three sequences. But then there's also sequences where the third element is larger than 4. For example, maybe the first element is 1, second is 2, third is 5 (since 5 is >= 2*2=4), then the fourth element must be >= 10. But since m is 10, the fourth element can be 10. So that's another sequence: 1,2,5,10. So that's another one. So that's four sequences. So the example's answer is 4. So that makes sense.

So the problem is to count all such sequences. How can I model this?

This seems like a dynamic programming problem. Let's think recursively. For a given position in the sequence, and a current value, how many sequences can be formed from there.

Let me think of the approach. Let's say we have a function that, given the current position (say, position k) and the previous value (prev), returns the number of sequences that can be formed from there. For example, for position k, the next element must be >= 2*prev and <=m. Then for each possible next value, we can proceed to the next position.

But since the sequence is of length n, and for each step, the choices depend on the previous value, we can model this with memoization. Let's think of the parameters for the DP. The parameters would be the current position (like, how many elements have been chosen so far) and the previous value. The base case is when the position is n, then there's one sequence (the empty sequence, but perhaps the base case is when we have filled all elements). Wait, the base case would be when we have selected all n elements. So for example, if we are at position n, then there's exactly 1 way (the sequence is complete). So the DP function would be something like dp(pos, prev) = number of sequences starting from position pos, given that the previous element is prev.

But for the first position, the previous value is 0 (since there's no previous element). Wait, maybe for the first element, we can choose any value from 1 to m, but then for the next elements, they have to be at least twice the previous.

Alternatively, for the first element, the previous is 0. So the first element can be any value between 1 and m. Then, for the next elements, each must be >= twice the previous value, and <= m.

So the DP approach would be to compute for each position and previous value, the number of sequences. Let's think of memoization. Let's define dp(pos, prev) as the number of sequences starting from position pos, given that the previous element is prev. For example, for pos=1, prev is 0 (since it's the first element). For pos=1, the possible values are from 1 to m, but then for each choice, we move to pos=2 with prev being that value. For pos=2, the next value must be >= 2*prev, etc.

Wait, but for the first position, pos is 1. For pos=1, the previous value is 0. So the first element can be any value from 1 to m. Then, for each such value, we move to pos=2 with prev being that value. For pos=2, the next element must be >= 2*prev and <= m. So for each possible next value, we proceed to pos=3, etc.

So the recurrence would be:

dp(pos, prev) = sum over all possible next values (next_val) where next_val >= 2*prev and next_val <= m of dp(pos+1, next_val)

The base case is when pos == n. Then, there's exactly 1 way (the sequence is complete).

But for the first call, we need to consider all possible first elements. So the total number of sequences is the sum over all possible first elements (from 1 to m) of dp(2, first_element).

But how to implement this? Let's think about memoization. Since m can be up to some value, but for the constraints of the problem, perhaps m can be up to 1e5 or something, but for Python, memoization with a cache can be feasible if the parameters are manageable.

But for the given example, m=10, n=4. Let's think of how the DP would work.

For pos=4, the base case is 1. So for pos=4, any prev value (as long as the previous steps are valid) would contribute 1. But how?

Wait, for pos=4, the current position is 4. Since the sequence length is 4, that's the last element. So when we are at pos=4, the previous value is the third element. So the fourth element must be >= 2*third and <= m. But since pos=4 is the last element, the number of sequences is 1, because once we have chosen the third element, the fourth element can be any value that meets the condition. Wait, no. Wait, the DP function dp(pos, prev) represents the number of sequences starting from pos, given that the previous element is prev. So when pos is n, we have already filled n elements. Wait, no. Let's think again.

Let me rephrase: pos represents how many elements have been chosen so far. For example, if pos is 1, we have chosen the first element. Then, for pos=2, we have chosen the first and second elements. So the base case is when pos equals n, which means that we have filled all elements. So for that case, the number of sequences is 1.

Wait, but how does that work? Let's think of the initial call. For the first element, we have pos=1. We choose a value, then proceed to pos=2, etc. So for pos=1, the number of sequences is the sum over all possible first elements (each of which contributes the number of sequences starting from pos=2 with that first element as the previous value).

So for the base case, when pos == n, the number of sequences is 1. Because once you have chosen the first n-1 elements, the nth element is determined? No, no. Wait, the pos is the number of elements that have been chosen. So when pos is n, that means that the sequence has exactly n elements. So the function dp(pos, prev) is the number of sequences starting from pos, given that the previous element is prev. So when pos is n, we have already selected n elements. So the function returns 1.

Wait, maybe the parameters are pos (the number of elements already selected), and prev is the last element. So for example, when pos is 0, we have selected 0 elements, and we need to select n elements. But that might complicate. Alternatively, perhaps the pos represents the current step, and the number of elements to choose is (n - pos). So for example, pos=0: we need to choose n elements. pos=1: we have already chosen 1 element, and need to choose n-1 more. So the base case is when pos == n, which means that all elements are chosen, and returns 1.

So, the recurrence is:

For each position pos (from 1 to n), and for each possible previous value, we can compute the number of sequences.

So, for the DP function, for a given pos and prev, the number of sequences is the sum over all next_val >= 2*prev, next_val <=m, of the number of sequences starting from pos+1 with next_val as the previous value.

So the base case is when pos == n: return 1.

But how do we compute this efficiently?

For the given example, let's think of the DP steps.

For m=10, n=4.

The initial call is for pos=1, and prev=0 (since there's no previous element yet). Wait, but for the first element, the previous is 0. So the first element can be any value between 1 and m. So for the first element, the next_val is the first element. Then, for pos=1, prev=0, the next_val can be any value between 1 and m, and then for each such value, we call dp(2, next_val).

So the DP function needs to handle pos from 1 to n.

But how to implement this in Python? Using memoization with lru_cache, but since m can be large, perhaps we need to memoize based on pos and prev.

But for the problem, m can be up to some value, but for the given example, it's manageable.

But for larger m and n, this approach may have high time complexity. Let's think about the time complexity. The number of possible states is O(n * m). For each state, the transitions are O(m) in the worst case. So for m up to say 1e4 and n up to 1e3, this could be O(1e7) operations, which is acceptable.

But perhaps there's a way to optimize.

But for the problem, let's proceed with the DP approach.

So, the plan is:

- Implement a recursive function with memoization, where the parameters are pos and prev.

- For each call, if pos == n, return 1.

- Else, for the current pos, the next element must be >= 2*prev, and <=m. So for all possible next_val in that range, we sum the number of sequences from pos+1 with prev = next_val.

But how to handle the first element? For the first element, prev is 0, so the next_val must be >= 2*0 = 0, but since next_val is a positive integer, it's >=1. So the first element can be any value from 1 to m.

So the initial call is dp(1, 0), and the total number of sequences is the sum over all possible first elements (1 to m) of dp(2, first_element). Wait, no. Because for the first element, the pos is 1, and the previous is 0. So the function would be called with pos=1 and prev=0. Then, for each possible next_val (the first element) that is >= 2*prev (which is 0) and <=m, we add dp(2, next_val). So the initial call is dp(1, 0), which would return the total number of sequences.

Wait, perhaps the DP function is called with pos and prev, where pos is the number of elements already selected, and prev is the last element selected. Then, for the first call, pos is 0, and prev is 0 (but that's not correct). Alternatively, perhaps the function is called with pos as the number of elements that have been chosen, and the next element to choose is the (pos+1)th element. So for example, when pos is 0, we need to choose the first element. So for pos=0, prev is 0, and the next element must be >= 2*prev (which is 0), but since it's a positive integer, it's >=1. So for each possible next_val, we proceed to pos=1 with prev = next_val.

But maybe it's easier to think of the DP as follows: for the current position (the next element to choose), and the previous value. For example, when you have selected k elements, and the last element is prev, then you need to select the (k+1)th element. So for the initial call, k=0, and the previous value is 0. Then, the first element can be any value between 1 and m. Then, for each of these, you call the function for k=1, prev = that value.

So the base case is when k == n, which means that we have selected all elements. So the function returns 1.

So the recursive function is:

def dp(k, prev):

    if k == n:

        return 1

    total = 0

    for next_val in range(2*prev, m+1):

        total += dp(k+1, next_val)

    return total

But wait, the next_val must be >= 2*prev. But when prev is 0 (for the first call), 2*prev is 0. So the next_val can be from 1 to m. So the initial call is dp(0, 0), and then for each next_val in 1 to m, we call dp(1, next_val). Then, for k=1, prev is the first element, and next_val must be >= 2*prev, etc.

But this approach would work. However, for large m and n, this could be very slow. For example, if m is 1e5 and n is 10, then the number of states is O(n*m), but for each state, we might have O(m) operations. So for m=1e5 and n=10, that's 1e6 * 1e5 = 1e11 operations, which is way too slow.

But for the given example, it's manageable. But for larger inputs, this approach would not be efficient. So perhaps we need to optimize.

Wait, but for the problem, the constraints are not given. So maybe we can proceed with memoization and see. But in practice, for the problem, the test cases may not be too big. However, for the code submission, perhaps the code needs to handle larger inputs. So perhaps we need to find a way to optimize the DP.

Let me think about the recurrence again. For a given pos and prev, the next_val can be from 2*prev to m. Let's think about how to compute the number of sequences for each possible next_val. For each next_val, the number of sequences is dp(pos+1, next_val). So for the current pos and prev, the total is the sum over next_val in [2*prev, m] of dp(pos+1, next_val).

But how to compute this sum efficiently. Let's think of memoizing the DP and using memoization. Also, for each (pos, prev), we can compute the sum once and store it.

But for the code, perhaps we can use memoization with lru_cache, but since m can be up to some value, but for Python, the recursion depth may be an issue. For example, if n is 100, then recursion depth is 100, which is acceptable.

But for the problem, the given example is small, but the code needs to handle all possible m and n.

So, let's proceed with the DP approach, using memoization.

But for the code, how to implement this? Let's think of writing a memoized recursive function. But since Python has a maximum recursion depth, perhaps for n up to 1000, it's not feasible. However, for the problem, the code may need to handle that. Alternatively, we can use memoization with a memo table, perhaps using a memo dictionary, and using a bottom-up approach.

Alternatively, memoization with lru_cache, but with parameters pos and prev. Let's try to code it.

But first, the function needs to take m and n as parameters, but in the code, the DP function would need to have access to m and n. So perhaps the code would be structured as follows:

def get_total_number_of_sequences(m, n):

    from functools import lru_cache

    @lru_cache(maxsize=None)

    def dp(pos, prev):

        if pos == n:

            return 1

        total = 0

        start = 2 * prev

        # next_val must be >= start and <= m

        # but also, since next_val is a positive integer, start must be at least 1?

        # for example, if prev is 0, start is 0. So next_val can be from 1 to m.

        # So, the lower bound is max(1, start)

        # Wait, no. Because prev is the previous value. For the first call, prev is 0, and the next_val is the first element, which must be >= 1 (since it's a positive integer). But according to the problem statement, each element is a positive integer.

        # So, the next_val must be >= 2*prev, but also >=1.

        # Wait, the problem says that each element is a positive integer. So for the first element, it's >=1. For the second element, it's >= 2*prev (the first element), which is >= 2*1=2. So for the next_val, it's allowed to be >= 2*prev, but also >=1. But since 2*prev is >= 0 (since prev is a positive integer), but for the first call, prev is 0. So for the first call, the next_val must be >= 1 (since it's the first element) and >= 2*prev (which is 0). So the lower bound is max(2*prev, 1). Wait, no. Because the next_val must be >= 2*prev, but also must be a positive integer. So for example, if prev is 0, then 2*prev is 0. So next_val must be >=0, but since it's a positive integer, next_val >=1. So the lower bound is max(2*prev, 1). So in code, the start is max(2*prev, 1). But wait, for the first element, prev is 0, so start is max(0, 1) = 1. So the next_val starts from 1. For the second element, prev is the first element (say, 1), then next_val must be >= 2*1=2. So that's correct.

        # So the code for the lower bound is start = max(2*prev, 1)

        # But wait, the next_val can be any value >= 2*prev, but also must be a positive integer. However, 2*prev can be zero (if prev is 0), but the next_val is a positive integer. So the lower bound is max(2*prev, 1). But in the case where prev is zero (the first element), then the next_val must be >= 1. So the code for the lower bound is:

        lower = 2 * prev

        if lower < 1:

            lower = 1

        # So the next_val starts from lower to m.

        # Wait, but for the first element, prev is 0. So lower is 0, but next_val must be >=1. So the lower is max(2*prev, 1). So the code can be written as:

        lower = max(2 * prev, 1)

        # So for each next_val in lower to m:

        for next_val in range(lower, m+1):

            total += dp(pos + 1, next_val)

        return total

    # The initial call is pos=0, prev=0, since we have selected 0 elements, and the previous value is 0 (so the first element can be chosen as any value >= 1).

    # Wait, no. For pos=0, we need to choose the first element. The previous value is 0, so the next_val must be >= 2*prev (which is 0), but since it's the first element, it must be a positive integer. So the lower bound is 1.

    # So the initial call is dp(0, 0). But then, in the first call, pos is 0. So for pos=0, the function will compute the sum for next_val from 1 to m, and then call dp(1, next_val). Then, for each of those, the next steps.

    # Wait, but the pos is the number of elements already selected. For example, when pos=0, we need to select the first element (so after selecting it, pos becomes 1). So the initial call is dp(0, 0), which returns the total number of sequences.

    # However, in the code above, the function is called with pos and prev. So for pos=0, the function will check if pos == n (which is 4 in the example). If not, it will compute the sum for next_val from lower to m. So for the example, the initial call is dp(0, 0), which returns the total number of sequences.

    # Wait, but in the code, the function is called with pos and prev. So for the first call, pos=0, prev=0. Then, the code will compute lower = max(2*0, 1) = 1. So next_val ranges from 1 to m. For each next_val, we call dp(1, next_val). Then, for each of these, the function proceeds.

    # But in the code above, the base case is when pos == n. So for example, if n=4, then when pos=4, we return 1. So the initial call is dp(0, 0), which for pos=0, will generate all possible first elements, and so on.

    # So the code for the function is:

    # return dp(0, 0)

    # Wait, but in the code, the initial call would be dp(0, 0). But in the code above, the function dp is defined as taking pos and prev. So for the first element, pos=0, prev=0. Then, the next_val is in range(1, m+1). So the code would return the sum for all possible first elements, and then proceed recursively.

    # So the code for the function would be:

    return dp(0, 0)

Wait, but let's test this with the example. For m=10, n=4.

Let's see what dp(0, 0) returns.

In the first call, pos=0, prev=0. lower is max(0*2, 1) = 1. So next_val ranges from 1 to 10. For each next_val, we call dp(1, next_val).

So for each of these next_val, we have to compute dp(1, next_val). Let's take next_val=1. Then, pos=1, prev=1. Now, for this call, lower is max(2*1, 1) = 2. So next_val ranges from 2 to 10. For each of those, we call dp(2, next_val). For example, next_val=2, then dp(2,2) would have lower = 4. So next_val ranges from 4 to 10. For each of these, call dp(3, next_val). Then, for dp(3, next_val), lower is 2*next_val. For example, if next_val is 4, then lower is 8. So next_val ranges from 8 to 10. Then, for dp(4, next_val), which is pos=4, which is equal to n=4, so returns 1. So that's one sequence. So for the first path, 1,2,4,8 is counted once. Similarly, for next_val=4 in the third step, the next_val could be 8,9,10. So for each of those, dp(4, ...) returns 1. So that's three sequences. Then, for the third step, if the previous value is 5, then lower is 10. So next_val can be 10. So that's one sequence. So for the example, the total is 4.

So the code should return 4 for the example. So the code seems correct.

But what about the memoization? The function dp is memoized with pos and prev. So for each (pos, prev), the function returns the same value. So for the example, the code should work.

But let's check for the initial call. For example, when m=10, n=4, the code returns dp(0,0). Let's see.

But in the code, the function dp is called with pos=0 and prev=0. Let's think of the code.

But what about when prev is 0 and pos is 0, and the next_val is 1. Then, in the next step, pos is 1, prev is 1. So the code seems to handle it.

So the code should work.

Now, the problem is that for large m and n, this approach may be too slow. But for the problem, perhaps it's acceptable.

Now, the code needs to be written in Python. So the function get_total_number_of_sequences(m, n) would use memoization via lru_cache.

But there's a problem: the parameters to the dp function are pos and prev. However, for the initial call, prev is 0, and for the first step, the next_val is from 1 to m. But in Python, when using lru_cache, the parameters must be hashable. Since pos is an integer and prev is an integer, that's okay.

But what about when m is very large, say 1e5, and n is 10? The number of possible (pos, prev) pairs is O(n*m). For n=10, m=1e5, that's 1e6 possible states. For each state, the number of transitions is O(m) in the worst case. But in practice, for each state, the range of next_val is from 2*prev to m, which could be O(m) steps. So the total time complexity is O(n * m^2), which is not feasible for large m.

But perhaps there's a way to optimize the code. Let's think about the recurrence. For each (pos, prev), the total is the sum of dp(pos+1, next_val) for next_val in [2*prev, m]. So if we can compute this sum efficiently.

But how? For example, for a given pos and prev, the sum can be computed as the sum of dp(pos+1, next_val) for next_val in [a, m], where a = 2*prev. So if we can precompute the sum for ranges, perhaps using memoization and some pre-processing.

But perhaps we can memoize the dp function and for each (pos, prev), compute the sum over next_val from a to m. But even with memoization, for large m, this could be slow.

Alternative approach: for each pos, we can compute the number of sequences for all possible prev values. Let's think of it as a dynamic programming table. Let's define dp[pos][prev] as the number of sequences starting from pos, given that the previous value is prev. Then, for each pos and prev, dp[pos][prev] = sum_{next_val >= 2*prev} dp[pos+1][next_val].

But how to compute this efficiently.

Let's think of the problem in terms of bottom-up DP. Starting from pos = n, then pos = n-1, etc.

For pos = n, dp[n][prev] = 1 for any prev (since we have already selected all elements).

For pos = n-1, dp[n-1][prev] is the number of next_val >= 2*prev and <= m. So for each prev, the number of possible next_val is max(0, m - 2*prev + 1). But wait, no. Because for pos = n-1, the next_val is the nth element, which must be >= 2*prev and <= m. So the number of possible next_val is max(0, m - 2*prev + 1) if 2*prev <= m. Otherwise 0. So for pos = n-1, dp[pos][prev] is the count of next_val.

But this is only true if the next_val is allowed. So for pos = n-1, dp[pos][prev] is the number of valid next_val (each of which contributes 1, because once you choose it, you have a valid sequence).

But for pos = n-2, dp[pos][prev] is the sum over all next_val >= 2*prev of dp[pos+1][next_val], which is the sum over next_val of the number of sequences starting from pos+1.

So, for each pos, and for each possible prev, we can compute the sum.

But how to compute this sum efficiently. For example, for a given pos, and prev, the sum is over next_val in [a, m], where a = 2*prev. So if we can precompute the sum for each pos and a, then we can compute it quickly.

But how?

Let me think of the bottom-up approach. For each pos from n-1 down to 0, and for each possible prev, compute dp[pos][prev].

For example, for pos = n, dp[pos][prev] = 1 for any prev.

For pos = n-1, dp[pos][prev] = number of next_val >= 2*prev and <= m. So for each prev, it's max(0, m - 2*prev + 1) if 2*prev <= m, else 0.

For pos = n-2, dp[pos][prev] is the sum over next_val >= 2*prev of dp[pos+1][next_val].

But how to compute this sum efficiently.

If we can precompute for each pos and a (the lower bound), the sum from a to m of dp[pos+1][x], then it's possible.

This suggests that for each pos, we can precompute a prefix sum array.

Let me think. For each pos, we can compute a prefix sum array S where S[x] is the sum of dp[pos][y] for y from 1 to x. Then, the sum from a to m is S[m] - S[a-1].

But for this, we need to know for each pos, the sum of dp[pos][x] from x = a to m.

So, for each pos, we can compute the sum for all possible ranges.

But how to implement this.

Let me think for each pos, we can compute a prefix sum array.

But for the bottom-up approach, let's proceed.

Let's assume that m is up to some maximum value. For example, for the given problem, m can be up to say 1e5. But for the code, we need to handle any m.

So, the steps for bottom-up DP:

Initialize a 2D array dp[pos][prev], but since pos can be up to n and prev can be up to m, this could be memory-intensive. However, for Python, it's manageable for small m and n.

But for larger m, like 1e5, and n up to 100, it's possible that the memory usage is O(n * m), which could be 1e7 for m=1e5 and n=100, which is acceptable.

But for the code, perhaps it's better to use a 2D array and compute the sums.

Alternatively, since for each pos, we only need the previous pos+1's values, we can use two 1D arrays: current and next.

But let's think of the steps:

Initialize for pos = n: for any prev, dp[pos][prev] = 1.

Then, for pos from n-1 down to 0:

   for each possible prev:

       compute the sum of dp[pos+1][next_val] for next_val >= 2*prev and <=m.

But how to compute this sum efficiently.

For example, for each prev, the sum is the number of sequences starting from pos+1 with next_val >= 2*prev.

So, for each pos, we can compute a prefix sum array, which allows us to compute the sum from a to m quickly.

Let me think: for each pos, we can precompute a prefix sum array where prefix_sum[x] is the sum of dp[pos][y] for y from 1 to x. Then, the sum from a to m is prefix_sum[m] - prefix_sum[a-1].

But in this case, for each pos, we can compute this prefix sum array once.

So, the steps for bottom-up DP:

Initialize a 2D array dp, where dp[pos][prev] is the number of sequences.

But for space optimization, since we only need the current and next pos, we can use two 1D arrays.

But let's proceed with the bottom-up approach.

Let's think of for each pos in reverse order (from n down to 0).

For pos = n, the dp is 1 for all prev.

But what's the maximum possible prev for each pos? For pos = 0, the prev can be up to m, but for pos = 1, the prev can be up to m, and so on.

But for the bottom-up approach, we can precompute for each pos, the maximum possible prev that can be considered. For example, for pos=0, the prev is 0, but for pos=1, the prev is the first element, which can be up to m. So for each pos, the prev can be up to m.

So, for the code, the maximum prev is m.

So, for the bottom-up approach, we can have a 2D array of size (n+1) x (m+1), where dp[pos][prev] represents the number of sequences for that pos and prev.

But for large m, this could be memory-intensive. For example, if m is 1e5 and n is 10, then the array is 11 * 1e5 = 1.1e6 elements, which is manageable.

But for Python, perhaps it's better to use a list of dictionaries or something else. However, for simplicity, let's proceed with the 2D array.

Let's proceed with the code:

def get_total_number_of_sequences(m, n):

    # Initialize dp as a 2D array of size (n+1) x (m+1)

    # Since for pos from 0 to n, and prev from 0 to m.

    # But for prev, the maximum possible value is m.

    # However, for pos=0, the prev is 0, but for other pos, prev can be up to m.

    # So, let's create a 2D array.

    # But since m can be up to a large value, perhaps we need to use a list of lists.

    # However, for the given example, it's manageable.

    # But in Python, for large m, this may not be feasible. So perhaps we need to find a way to optimize.

    # Let's proceed.

    # First, handle the case where n=0. But the problem says n is a positive integer.

    # Assuming n >= 1.

    # Initialize dp as a list of lists.

    # Since for pos in 0 to n, and prev in 0 to m.

    # But for the problem, the prev can be up to m.

    # So, for each pos in 0 to n, and for each prev in 0 to m.

    # But for the initial case, pos = n, dp[n][prev] = 1 for any prev.

    # However, for the bottom-up approach, we can proceed as follows.

    # Let's create a 2D array dp with (n+1) rows and (m+1) columns.

    # Initialize dp[pos][prev] for all pos and prev.

    # But for pos = n, dp[n][prev] = 1 for any prev.

    # Then, for pos
```

</details>

**Code that ran:**

```python
from functools import lru_cache

def get_total_number_of_sequences(m, n):
    @lru_cache(maxsize=None)
    def dp(pos, prev):
        if pos == n:
            return 1
        lower = max(2 * prev, 1)
        total = 0
        for next_val in range(lower, m + 1):
            total += dp(pos + 1, next_val)
        return total

    return dp(0, 0)
```

**Visible-test report:**

```text
PASS    assert get_total_number_of_sequences(10, 4) == 4
1 of 1 visible tests passed
```
