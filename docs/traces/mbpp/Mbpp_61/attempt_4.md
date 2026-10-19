# Mbpp/61, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/61/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 99.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that counts the number of substrings in a given string where the sum of the digits equals the length of the substring. The example given is '112112' which should return 6. Let me think about how to approach this.

First, let's understand the problem. For each possible substring, I need to check if the sum of its digits equals the length of the substring. For example, in the string '112112', let's look at some substrings.

Wait, the substring's sum of digits must equal its length. So for a substring of length n, the sum of its digits should be exactly n. So for example, a substring of length 2 with digits 1 and 1 would sum to 2, so that's valid. But a substring of length 3 with digits 1,1,2 would sum to 4, which is not equal to 3, so that's invalid.

The challenge is to find all such substrings efficiently. Let's think about how to approach this.

Brute force approach: generate all possible substrings, compute their sum, and check if it equals the length. But for a string of length n, there are O(n^2) substrings. For each substring, summing the digits would take O(n) time, leading to O(n^3) time. For n up to say 10^3, that's 1e9 operations, which is way too slow. But maybe the problem expects a more efficient approach.

But maybe the input is small. However, since the problem is given as a coding problem, perhaps there's a smarter way.

Let me think about the possible approaches.

Alternative approach: For each possible starting index, keep track of the cumulative sum of digits as we move the end index. For example, for each start index i, we can compute the sum of digits from i to j, and check if it equals j - i + 1. But how to do that efficiently?

Let me think. Let's consider the sum of digits from i to j. Let's denote the sum as sum_digits. The length of the substring is j - i + 1. So sum_digits == length. So sum_digits - (j - i + 1) == 0. But sum_digits is the sum of digits from i to j. Let me think of the sum as a running total.

Let me think of the sum of digits from i to j as sum[i..j]. Let's consider the prefix sum array. Let's define prefix_sum[0] = 0, prefix_sum[1] = digit[0], prefix_sum[2] = digit[0] + digit[1], etc. Then the sum from i to j is prefix_sum[j+1] - prefix_sum[i]. So for a substring from i to j (0-based), the sum is prefix_sum[j+1] - prefix_sum[i]. The length is j - i + 1. So the condition is:

prefix_sum[j+1] - prefix_sum[i] = (j - i + 1)

Rearranging:

prefix_sum[j+1] - prefix_sum[i] = j - i + 1

Adding prefix_sum[i] to both sides:

prefix_sum[j+1] = j - i + 1 + prefix_sum[i]

But j is the index of the end of the substring. Let me think of this as:

prefix_sum[j+1] - prefix_sum[i] = (j - i + 1)

Let me rearrange:

prefix_sum[j+1] - (j + 1) = prefix_sum[i] - i

Because:

prefix_sum[j+1] - (j+1) = (prefix_sum[j+1] - j - 1) 

and the right side is prefix_sum[i] - i.

So the equation becomes:

prefix_sum[j+1] - (j+1) = prefix_sum[i] - i 

So for each j, we can check for all i's where i <= j, whether the left side equals the right side. 

So for each j, we can compute the value (prefix_sum[j+1] - (j+1)), and then check how many times this value has occurred in the prefix_sum array up to index j.

Wait, because for each j, the left side is (prefix_sum[j+1] - (j+1)), and we need to find the number of i's where i <= j and prefix_sum[i] - i equals that value. 

So, for each j, we can compute the value (prefix_sum[j+1] - (j+1)), and then check how many times this value has occurred in the prefix_sum array up to index j. Because for each such i, the substring from i to j would satisfy the condition.

So the idea is:

- Precompute the prefix sum array.

- For each j (from 0 to n-1), compute the value (prefix_sum[j+1] - (j+1)).

- Then, check how many times this value has occurred in the prefix_sum array up to index j. 

Wait, but the prefix_sum array is built as follows. Let's say the original string is s of length n. Then prefix_sum is of length n+1, with prefix_sum[0] = 0, prefix_sum[1] = s[0], prefix_sum[2] = s[0] + s[1], etc.

So for each j (from 0 to n-1), the substring from i to j (inclusive) has length j - i + 1. So when we compute the value (prefix_sum[j+1] - (j+1)), which is the sum of digits from i to j (since prefix_sum[j+1] is sum of first j+1 digits, which is sum from 0 to j. Then subtract (j+1) gives the sum of digits from i to j (sum from 0 to j minus sum from 0 to i-1). So that's correct.

So for each j, the value (prefix_sum[j+1] - (j+1)) is the sum of digits from i to j minus (j - i + 1) ?

Wait, no. The sum of digits from i to j is prefix_sum[j+1] - prefix_sum[i]. And the length is j - i + 1. So the equation is:

prefix_sum[j+1] - prefix_sum[i] = j - i + 1 

Rearranged as:

prefix_sum[j+1] - (j+1) = prefix_sum[i] - i 

So for each j, the value (prefix_sum[j+1] - (j+1)) is equal to prefix_sum[i] - i for some i. So for each j, we can check how many times (prefix_sum[j+1] - (j+1)) has occurred in the prefix_sum array up to index j. 

So the approach is:

- Compute the prefix_sum array.

- For each j in 0..n-1:

   - compute current_val = prefix_sum[j+1] - (j+1)

   - check how many times current_val has occurred in the prefix_sum array up to index j.

   - add that count to the total.

But how to track the counts?

We can use a dictionary to keep track of the frequency of each value in the prefix_sum array up to the current index. For example, as we iterate j from 0 to n-1, for each j, we compute current_val, and then look up how many times current_val has occurred in the prefix_sum array up to index j. Then, we add that count to the total.

Wait, but the prefix_sum array is built as follows. Let's say for j=0, the prefix_sum is 0, s[0], s[0]+s[1], etc. So for j=0, the current_val is prefix_sum[1] - 1 = (s[0]) - 1. Then, we check how many times this value has occurred in the prefix_sum array up to index 0. But the prefix_sum array up to index 0 is [0]. So if current_val is 0, then it's counted once.

Wait, let's think again. The prefix_sum array is of length n+1. For each j in 0..n-1, we are considering the substring from i to j. So for each j, the current_val is prefix_sum[j+1] - (j+1). So for j=0, j+1 is 1. The current_val is prefix_sum[1] - 1. Which is s[0] - 1. Then, the number of times this current_val has occurred in the prefix_sum array up to index j (which is 0). So the prefix_sum array up to index 0 is [0], and the current_val is s[0] - 1. So if s[0] - 1 is 0, then the count is 1. So that would correspond to the substring from i=0 to j=0. Let's check that.

For example, if the substring is of length 1, then sum of digits is equal to the length. So sum is s[0] == 1. So if s[0] is 1, then the sum is 1, which equals the length 1. So that's valid. So in this case, the current_val is s[0] - 1 = 0. So the count would be 1. So that's correct.

So the idea is that for each j, we compute the current_val and check how many times it has occurred in the prefix_sum array up to index j (i.e., up to the current j). So the dictionary is built as we iterate through the prefix_sum array.

So the steps are:

Initialize a dictionary, say, count_map, which keeps track of the frequency of each value in the prefix_sum array up to the current index.

Initialize prefix_sum as 0 (prefix_sum[0] = 0).

Initialize the count_map with {0: 1} (since prefix_sum[0] is 0, and it's counted once).

Then, for each j from 0 to len(s) - 1:

   current_val = prefix_sum[j+1] - (j+1)

   add to the count the number of times current_val has been seen in the count_map.

   then, add the current prefix_sum[j+1] to the count_map (but wait, no, because the current_val is for j+1, and the next steps will check for j+1 in the prefix_sum array. Wait, no. Let me think again.

Wait, the count_map is supposed to track the values of prefix_sum[i] - i for i from 0 to j. Because for each j, when we compute current_val, which is prefix_sum[j+1] - (j+1), and we need to check how many times this value has occurred in the prefix_sum array up to index j. So the prefix_sum array is being built as we go. So for each j, when we process it, the count_map contains all the values of prefix_sum[0], prefix_sum[1], ..., prefix_sum[j]. Because for j=0, the count_map is {0:1} (prefix_sum[0] is 0). Then, after processing j=0, we add prefix_sum[1] to the count_map. Wait, no. Wait, the count_map is built as we process each j. Let me think again.

Let me think of the steps:

Initialize count_map as {0: 1} (since prefix_sum[0] is 0).

prefix_sum is 0.

Then, for each j from 0 to n-1:

   current_val = prefix_sum[j+1] - (j+1)

   the count for current_val is the number of times it's been seen in the count_map (so up to j, since the count_map contains prefix_sum[0] ... prefix_sum[j], since for each j, the count_map is built up to j).

   add that count to the total.

   then, we need to add the current prefix_sum[j+1] to the count_map. Wait, no. Because the next j's will need to check the prefix_sum up to j+1. Wait, the current j is the index in the original string. So for j=0, the prefix_sum[j+1] is prefix_sum[1], which is the sum of the first 1 digits. So when processing j=0, the current_val is prefix_sum[1] - 1. Then, we need to add the prefix_sum[1] to the count_map for future j's. Because for j=1, the next step, the current_val is prefix_sum[2] - 2, and we need to check how many times that value has occurred in the prefix_sum array up to index j=1 (so prefix_sum[0], prefix_sum[1]).

So the process is:

For each j in 0..n-1:

   compute current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add the current prefix_sum[j+1] to the count_map. Wait, no. Because the count_map is for the prefix_sum[i] - i for i up to j. So for j=0, the prefix_sum[0] is 0, and prefix_sum[1] is the sum of the first 1 digits. So when processing j=0, after checking current_val, we need to add the prefix_sum[1] to the count_map. Because for the next j's (like j=1), the prefix_sum[1] is part of the count_map.

Wait, no. Let me think again. The count_map is built as follows. For each j, the current_val is computed based on prefix_sum[j+1] - (j+1). The count_map is supposed to contain all the values of prefix_sum[0] - 0, prefix_sum[1] - 1, ..., prefix_sum[j] - j. Because when we process j, the current_val is prefix_sum[j+1] - (j+1), and we need to check how many times that value has occurred in the prefix_sum[0] - 0, prefix_sum[1] - 1, ..., prefix_sum[j] - j. So for each j, the count_map contains the values up to prefix_sum[j] - j.

So, after processing j, we need to add prefix_sum[j+1] - (j+1) to the count_map? Or wait, no. Because when j is processed, the next j is j+1. So for j, the current_val is prefix_sum[j+1] - (j+1). The count_map is for prefix_sum[0] - 0, ..., prefix_sum[j] - j. So when processing j, we need to add prefix_sum[j+1] - (j+1) to the count_map? No. Because the count_map is supposed to contain the values of prefix_sum[i] - i for i up to j. So for j, the prefix_sum[j+1] is not part of the count_map yet. Wait, no. The count_map is built for the prefix_sum[0] - 0, prefix_sum[1] - 1, ..., prefix_sum[j] - j. So when we process j, we need to add prefix_sum[j+1] - (j+1) to the count_map for the next steps. Because when j+1 is processed, the current_val is prefix_sum[j+2] - (j+2), and we need to check how many times that value has occurred in the prefix_sum array up to j+1 (i.e., up to prefix_sum[j+1] - (j+1)).

So the process is:

Initialize count_map with {0: 1} (prefix_sum[0] - 0 = 0).

Then, for j from 0 to n-1:

   current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add prefix_sum[j+1] - (j+1) to the count_map? No. Wait, no. Because the current_val is prefix_sum[j+1] - (j+1). But the count_map is supposed to track prefix_sum[i] - i for i up to j. So for j, after processing, we need to add prefix_sum[j+1] - (j+1) to the count_map. Wait, no. Because for the next j (j+1), the current_val is prefix_sum[j+2] - (j+2), and we need to check how many times that value has occurred in the prefix_sum array up to j+1. So the prefix_sum[j+1] - (j+1) is part of the count_map for the next steps. So when processing j, after checking the current_val, we need to add the prefix_sum[j+1] - (j+1) to the count_map? Or is it the prefix_sum[j+1] - (j+1) is not part of the count_map? Wait, no. The count_map is for the prefix_sum[i] - i for i up to j. So for j=0, the current_val is prefix_sum[1] - 1. The count_map contains prefix_sum[0] - 0. So after processing j=0, we need to add prefix_sum[1] - 1 to the count_map. Because for j=1, the current_val will be prefix_sum[2] - 2, and we need to check how many times that value has occurred in the prefix_sum array up to j=1 (i.e., up to prefix_sum[1] - 1). So the count_map after processing j=0 should have prefix_sum[0] - 0 and prefix_sum[1] - 1. So the steps are:

Initially, count_map has {0:1} (prefix_sum[0] - 0).

For each j in 0 to n-1:

   compute current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add prefix_sum[j+1] - (j+1) to the count_map? Wait, no. Because the current_val is for j+1, but the count_map is for the prefix_sum[i] - i up to j. So the prefix_sum[j+1] - (j+1) is the value that is being added to the count_map for the next steps. So after processing j, we need to add the current_val (prefix_sum[j+1] - (j+1)) to the count_map. Wait, no. Because for the next j (j+1), the current_val is prefix_sum[j+2] - (j+2), and the count_map needs to have prefix_sum[0] - 0, ..., prefix_sum[j+1] - (j+1). So when processing j, after checking the current_val, we need to add the current_val to the count_map. Wait, no. Because the current_val is prefix_sum[j+1] - (j+1). But the count_map is supposed to track prefix_sum[i] - i for i up to j. So for j, the current_val is prefix_sum[j+1] - (j+1), which is the value that is part of the prefix_sum array for i = j+1. So after processing j, we need to add this value to the count_map for future steps. So the steps are:

Initialize count_map with {0: 1} (prefix_sum[0] - 0).

prefix_sum is initialized as 0.

for j in 0 to len(s) - 1:

   current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add the current_val to the count_map? No. Because the current_val is for i = j+1. So when processing j, the current_val is the value of prefix_sum[j+1] - (j+1). But the count_map is for i up to j. So after processing j, we need to add the current_val to the count_map. Because when j+1 is processed, the current_val is part of the prefix_sum array up to j+1.

Wait, no. Let me think again. The count_map is for the prefix_sum[i] - i for i up to the current j. So for j=0, after processing, we need to add the prefix_sum[1] - 1 to the count_map. Because for j=1, the current_val is prefix_sum[2] - 2, and we need to check how many times that value has occurred in the prefix_sum array up to j=1 (i.e., up to prefix_sum[1] - 1).

So the process is:

Initially, the count_map contains {0:1} (prefix_sum[0] - 0).

Then, for each j in 0 to n-1:

   compute current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add the current_val to the count_map. Wait, no. Because the current_val is for i = j+1. So when j is 0, the current_val is prefix_sum[1] - 1. But the count_map is for prefix_sum[0] - 0, which is 0. So after processing j=0, we need to add the current_val (prefix_sum[1] - 1) to the count_map. Because for the next j (j=1), the current_val will be prefix_sum[2] - 2, and the count_map will have prefix_sum[0] - 0 and prefix_sum[1] - 1.

So the steps are:

For each j in 0 to n-1:

   compute current_val = prefix_sum[j+1] - (j+1)

   count += count_map.get(current_val, 0)

   then, add the current_val to the count_map (so that for the next j, it's available)

Wait, no. Because the current_val is for i = j+1. So when we add it to the count_map, we are adding it to the count_map for the next steps. So the count_map should contain the prefix_sum[i] - i for i from 0 to j+1. So after processing j, the count_map is updated with the current_val (prefix_sum[j+1] - (j+1)).

But how?

Let me think of the count_map as a dictionary that is built incrementally. Initially, it has prefix_sum[0] - 0. Then, for j=0, after processing, we add prefix_sum[1] - 1 to the count_map. Then, for j=1, the current_val is prefix_sum[2] - 2, and the count_map contains prefix_sum[0] - 0 and prefix_sum[1] - 1. So yes, the current_val is added to the count_map after processing j.

So the code would be:

Initialize prefix_sum = 0

count_map = {0: 1}

count = 0

for j in range(len(s)):

    current_val = prefix_sum + int(s[j]) - (j+1) ?

Wait, no. Wait, the prefix_sum is the sum up to j. Wait, the prefix_sum is built as follows. Let me think again.

The prefix_sum array is built as follows. Let's say s is the input string. Then, prefix_sum[0] = 0. For i from 1 to len(s), prefix_sum[i] = prefix_sum[i-1] + int(s[i-1]).

So for j in 0 to len(s)-1:

   the current j is the index in the string. So the prefix_sum[j+1] is the sum of the first j+1 digits (digits 0 to j).

So the current_val is prefix_sum[j+1] - (j+1) = (sum of digits 0 to j) - (j+1).

So for each j, the current_val is sum of digits from 0 to j minus (j+1). 

So in code, the prefix_sum is built as a list, but for efficiency, perhaps we can compute it on the fly.

So, in code, we can compute prefix_sum as a variable that is updated as we iterate through the string.

Let me think. Let's have a variable current_sum = 0. Then, for each j in 0 to len(s)-1:

   current_sum += int(s[j])

   current_val = current_sum - (j+1)

   then, check how many times current_val has occurred in the count_map (which contains the prefix_sum[0] - 0, prefix_sum[1] - 1, ..., prefix_sum[j] - j)

Wait, but in this case, the current_val is current_sum (which is sum of digits up to j) minus (j+1). So for j, the current_val is sum of digits up to j (current_sum) minus (j+1). 

But the count_map is for prefix_sum[i] - i for i up to j. So for the current j, the current_val is prefix_sum[j+1] - (j+1). But in this approach, the current_sum is the prefix_sum[j+1], because prefix_sum[0] = 0, prefix_sum[1] = s[0], prefix_sum[2] = s[0] + s[1], etc. So when j is 0, the current_sum is s[0], which is prefix_sum[1]. So for j=0, the current_val is prefix_sum[1] - 1 = s[0] - 1. 

So in code, the current_sum is built as the prefix_sum. So for each j, we can compute current_sum as the sum up to j, and then current_val is current_sum - (j+1). 

But then, the count_map is built as follows. Initially, it has {0:1} (prefix_sum[0] - 0). Then, for each j, after computing current_sum (prefix_sum[j+1]), we compute current_val = current_sum - (j+1). Then, we check how many times current_val has occurred in the count_map. Then, we add current_sum to the count_map? Or wait, no. Because the count_map is for prefix_sum[i] - i. So for the next steps, when j increases, the current_sum is prefix_sum[j+1], and we need to add it to the count_map. Wait, no. Because the current_sum is prefix_sum[j+1], and the count_map is for the prefix_sum[i] - i. So when j is processed, the current_val is prefix_sum[j+1] - (j+1). So after processing j, the count_map should include the current_val (prefix_sum[j+1] - (j+1)), so that for the next j, when we process j+1, the current_val is prefix_sum[j+2] - (j+2), and we can check against the count_map which includes prefix_sum[0] - 0, ..., prefix_sum[j+1] - (j+1).

So the steps are:

Initialize current_sum = 0

count_map = {0:1}

count = 0

for j in 0 to len(s)-1:

   current_sum += int(s[j])

   current_val = current_sum - (j+1)

   count += count_map.get(current_val, 0)

   # Now, add the current_val to the count_map? Or add current_sum - j ?

   # Wait, the count_map is for prefix_sum[i] - i, where i is up to j. So for the next j, we need to add the current_sum (prefix_sum[j+1]) - (j+1) to the count_map. But current_val is prefix_sum[j+1] - (j+1). So when we process j, the current_val is the value that we need to add to the count_map for future steps. So after processing j, we need to add the current_val to the count_map. Wait, no. Because the current_val is the value of prefix_sum[j+1] - (j+1). But the count_map is for prefix_sum[i] - i for i up to j. So after processing j, the current_val is for i = j+1. So we need to add it to the count_map for future steps. So in code, after computing current_val, we add it to the count_map. But how?

Wait, the count_map is supposed to contain the values of prefix_sum[i] - i for i up to j. So for j=0, after processing, the count_map should have prefix_sum[0] - 0 and prefix_sum[1] - 1. So for j=0, after processing, we need to add prefix_sum[1] - 1 to the count_map. But how?

Wait, the current_val is prefix_sum[j+1] - (j+1). So when j is 0, current_val is prefix_sum[1] - 1. So after processing j=0, we need to add this current_val to the count_map. Because for the next j (j=1), the current_val will be prefix_sum[2] - 2, and the count_map will have prefix_sum[0] - 0, prefix_sum[1] - 1.

So in code, after computing current_val, we add it to the count_map. But how?

Wait, the count_map is initially {0:1}. Then, for each j, after computing current_val, we add it to the count_map. So the code would be:

for j in range(len(s)):

    current_sum += int(s[j])

    current_val = current_sum - (j+1)

    count += count_map.get(current_val, 0)

    # Now, add current_val to the count_map?

    count_map[current_val] = count_map.get(current_val, 0) + 1

Wait, but that would add the current_val to the count_map. But the count_map is for prefix_sum[i] - i. So for the next j, when we process j+1, the current_val is prefix_sum[j+2] - (j+2), and the count_map includes prefix_sum[0] - 0, prefix_sum[1] - 1, ..., prefix_sum[j+1] - (j+1). So yes, adding current_val to the count_map after processing j.

But wait, in this code, for j=0, after processing, current_val is prefix_sum[1] - 1. We add that to the count_map. So the count_map now has {0:1, current_val:1}.

But for j=0, the current_val is prefix_sum[1] - 1. The count_map is for prefix_sum[i] - i up to j=0. So the count_map has prefix_sum[0] - 0 (0) and prefix_sum[1] - 1 (current_val). So for j=0, the count is incremented by count_map.get(current_val, 0). Which is 1 if current_val is in the count_map. But how does that work?

Wait, the code for j=0:

current_sum is 0 + int(s[0]) = sum up to j=0.

current_val is sum up to j=0 - (j+1) = sum up to j=0 - 1.

Then, count += count_map.get(current_val, 0). But the count_map has {0:1} (prefix_sum[0] - 0). So current_val is sum up to j=0 - 1. For example, if the string is '1', then current_sum is 1, current_val is 1 - 1 = 0. Then count_map.get(0, 0) is 1. So count increases by 1. Then, we add current_val (0) to the count_map. So count_map now has {0: 2}.

But for j=0, the current_val is 0, which is the same as prefix_sum[0] - 0. So when j=0 is processed, the count is increased by 1, which corresponds to the substring from i=0 to j=0. Because the current_val is prefix_sum[1] - 1 = sum up to j=0 (1) - 1 = 0. Which is equal to prefix_sum[0] - 0 (0). So that's the case where i=0, and the substring is from 0 to 0, which has sum 1, length 1. 1 == 1, so valid. So the code would count that.

So the code seems to work. Let me test with the example given.

Example: '112112' which is the input.

Let's compute the code step by step.

s = '112112' → len(s) = 6.

current_sum starts at 0.

count_map = {0:1}

count = 0

Processing j from 0 to 5:

j=0:

current_sum += int(s[0]) → 0 + 1 = 1.

current_val = 1 - (0+1) = 0.

count += count_map.get(0, 0) → count is 0 + 1 = 1.

Then, add current_val (0) to count_map. Now count_map is {0:2}.

j=1:

current_sum += int(s[1]) → 1 + 1 = 2.

current_val = 2 - (1+1) = 2 - 2 = 0.

count += count_map.get(0, 0) → count is 1 + 2 = 3.

Then, add current_val (0) to count_map. Now count_map is {0:3}.

j=2:

current_sum += int(s[2]) → 2 + 2 = 4.

current_val = 4 - (2+1) = 4 - 3 = 1.

count += count_map.get(1, 0) → count is 3 + 0 = 3.

Add current_val (1) to count_map → count_map {0:3, 1:1}.

j=3:

current_sum += int(s[3]) → 4 + 1 = 5.

current_val = 5 - (3+1) = 5 -4 = 1.

count += count_map.get(1, 0) → count is 3 + 1 = 4.

Add current_val (1) → count_map {0:3, 1:2}.

j=4:

current_sum += int(s[4]) → 5 + 1 = 6.

current_val = 6 - (4+1) = 6-5=1.

count += count_map.get(1, 0) → count is 4 + 2 = 6.

Add current_val (1) → count_map {0:3, 1:3}.

j=5:

current_sum += int(s[5]) → 6 + 2 = 8.

current_val = 8 - (5+1) = 8 -6 = 2.

count += count_map.get(2, 0) → count is 6 + 0 = 6.

Add current_val (2) → count_map {0:3, 1:3, 2:1}.

So total count is 6. Which matches the example.

So this approach works. So the code is:

Initialize current_sum = 0, count_map = {0:1}, count = 0.

Then, for each j in 0 to len(s)-1:

   current_sum += int(s[j])

   current_val = current_sum - (j+1)

   count += count_map.get(current_val, 0)

   count_map[current_val] = count_map.get(current_val, 0) + 1

So the code in Python would be:

def count_Substrings(s):
    current_sum = 0
    count_map = {0: 1}
    count = 0
    for j in range(len(s)):
        current_sum += int(s[j])
        current_val = current_sum - (j + 1)
        count += count_map.get(current_val, 0)
        count_map[current_val] = count_map.get(current_val, 0) + 1
    return count

Wait, but wait. Let's test the example again.

In the example, the code returns 6. Which is correct.

Another test case: let's take the string '1', the code would return 1.

Another test case: '11' → the substrings are:

'1' (sum 1, length 1 → valid)

'1' (sum 1, length 1 → valid)

'11' sum 2, length 2 → valid.

So total 3. Let's see what the code returns.

s = '11'

current_sum starts at 0.

count_map {0:1}

count = 0.

j=0:

current_sum = 1.

current_val = 1 - 1 = 0.

count += count_map.get(0, 0) → 1.

count becomes 1.

count_map now {0:2}.

j=1:

current_sum = 2.

current_val = 2 - 2 = 0.

count += count_map.get(0, 0) → 1 + 2 = 3.

count_map now {0:3}.

So total is 3. Which is correct.

Another test case: '12' → substrings:

'1' (sum 1, length 1 → valid)

'2' (sum 2, length 1 → no)

'
```

</details>

**Code that ran:**

```python
def count_Substrings(s):
    current_sum = 0
    count_map = {0: 1}
    count = 0
    for j in range(len(s)):
        current_sum += int(s[j])
        current_val = current_sum - (j + 1)
        count += count_map.get(current_val, 0)
        count_map[current_val] = count_map.get(current_val, 0) + 1
    return count
```

**Visible-test report:**

```text
PASS    assert count_Substrings('112112') == 6
1 of 1 visible tests passed
```
