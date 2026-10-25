# Mbpp/61, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/61/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 7778. Answer tokens: 102.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to count the number of substrings in a given string such that the sum of their digits equals the length of the substring. Let me think about how to approach this.

First, let me understand the problem with the example given. The input is '112112' and the output is 6. Let me check why. For each substring, the sum of its digits should be equal to its length. Let's take some examples.

For example, take the substring '1' (the first character). The sum is 1, and the length is 1. So that's valid. Similarly, the second '1' is also valid. Then, maybe substrings like '11' (sum 2, length 2) would count. Let me check the example.

Let me list all possible substrings and check which ones satisfy the condition. But that might take time. However, the example says the answer is 6. Let me think of possible substrings that meet the criteria.

For the string '112112', let's consider all possible substrings:

- All single characters: each is a substring. The sum is the digit itself, and length is 1. So for each '1' or '2', the sum is equal to length. So for the string, there are 4 '1's and 2 '2's. Wait, the string is '1','1','2','1','1','2'. So single characters: each is valid. That's 6 substrings. But the answer is 6. Wait, but maybe there are more substrings that also meet the condition. Wait, but according to the example, the answer is 6. So maybe the single characters are the only ones. But that can't be right. Let me check.

Wait, for example, the substring '11' (positions 0-1). Sum is 1+1=2, length is 2. So that's valid. So that's another substring. So why does the example have 6?

Wait, maybe the example includes some other substrings. Let me think again.

Original example: '112112' gives 6. Let me count:

Single characters: 6 substrings (each individual digit). But according to the example, the answer is 6. But that would imply that there are no longer substrings that satisfy the condition. But maybe that's the case. Let me check.

Wait, let's take the substring '12' (positions 0-1). Sum is 1+2=3, length is 2. 3 != 2. Not valid. What about '112'? Sum is 1+1+2=4, length is 3. 4 !=3. Not valid. How about '121'? Sum is 1+2+1=4, length 3. Not valid. How about '211'? Sum 2+1+1=4, length 3. Not valid. How about '1121'? Sum 1+1+2+1=5, length 4. 5 !=4. Not valid. What about '1211'? Sum 1+2+1+1=5, length 4. 5 !=4. Hmm.

Wait, perhaps the substrings that are valid are only the single digits. But then why the example says 6? Because the string is 6 characters long, so there are 6 single-digit substrings. So that would be the answer. But maybe there are other substrings. Let me check again.

Wait, maybe there are substrings longer than 1 that also meet the condition. Let's see. For example, the substring '112112' (the entire string). Sum is 1+1+2+1+1+2 = 8. Length is 6. 8 !=6. Not valid. How about substrings of length 2?

Check each possible substring of length 2:

- '11': sum 2, length 2 → valid. So that's one.
- '12': sum 3, length 2 → no.
- '21': sum 3, length 2 → no.
- '11': sum 2 → valid.
- '12': sum 3 → no.
So there are two substrings of length 2 that are valid. So adding that to the 6 single digits would make 8. But the example says 6. So that's conflicting. Therefore, perhaps my initial assumption is wrong.

Wait, maybe the example is not that. Let me recheck the example. The sample input is '112112' and the expected output is 6. So according to that, there are 6 substrings. So maybe the single digits are 6, but some of them are not valid. Wait, no. Wait, for each single digit, the sum is the digit itself, and the length is 1. So for example, the first '1' is valid. The second '1' is valid. The '2' is valid. Then the third '1' is valid. Fourth '1', fifth '1', sixth '2' — all of them. So that's 6 substrings. So the answer is 6. So perhaps there are no other substrings that meet the condition. Therefore, the function should count all single-digit substrings. But why?

Wait, maybe there are other substrings. Let me check again. For example, the substring '1' (the third character). Sum is 1, length 1. Valid. So that's one. What about substrings of length 3?

Let me check for substrings of length 3. For example, the first three characters: '112' sum is 1+1+2=4, length 3. 4 !=3. Not valid. Next substring: '121' (positions 1-3). Sum is 1+2+1=4. Length 3. No. Then '211' (positions 2-4): sum 2+1+1=4, length 3. No. Then '112' (positions 3-5): sum 1+1+2=4, length 3. No. So none of the substrings of length 3 are valid.

What about substrings of length 4? Let's take the first four characters: sum is 1+1+2+1=5. Length 4. 5 !=4. No. Next substring of length 4: 1+2+1+1=5. Length 4. No. Then 2+1+1+2=6. Length 4. No. So none.

So perhaps the only valid substrings are the single digits. So the answer is 6. Which matches the sample. So the function needs to count all substrings where the sum of digits equals the length of the substring.

So how to approach this?

The problem is to find all substrings where sum of digits equals the length of the substring.

So for each possible substring, we can compute the sum of digits and check if it equals the length.

But for a string of length n, there are O(n^2) possible substrings, which could be up to 1e4 or 1e5, which is manageable for small n.

But for the problem, perhaps the solution is to iterate through all possible substrings, calculate the sum of digits, and check if it equals the length.

But for each substring, how to calculate the sum of digits efficiently?

For example, for a substring from index i to j (inclusive), the length is j - i + 1. The sum of digits is sum of the digits in the substring.

So, for each possible i and j, where i <= j, compute the sum of digits from i to j, and check if it equals (j - i + 1).

But calculating the sum for each substring naively would take O(n^3) time, which for large n (like 1e4) would be too slow.

But perhaps the constraints for the problem are small. Let's think about the possible input size. Since the sample input is 6 characters, but for a code submission, the code needs to handle larger inputs. So we need an efficient approach.

Wait, but for the problem, perhaps the constraints are not given. So maybe the code can be written with O(n^2) time and O(n) space, using prefix sums.

Let me think. Let's precompute a prefix sum array. Let prefix_sum[i] be the sum of the first i digits. For example, prefix_sum[0] = 0, prefix_sum[1] = first digit, prefix_sum[2] = sum of first two digits, etc.

Then, for a substring from index i to j (0-based), the sum of digits is prefix_sum[j+1] - prefix_sum[i]. The length of the substring is (j - i + 1). So we need:

prefix_sum[j+1] - prefix_sum[i] == (j - i + 1)

Which can be rewritten as:

prefix_sum[j+1] - (j+1) == prefix_sum[i] - i

Because:

prefix_sum[j+1] - prefix_sum[i] = (j - i + 1) → rearranged:

prefix_sum[j+1] - (j+1) = prefix_sum[i] - i

So, for each j, we can compute the value of (prefix_sum[j+1] - (j+1)), and then check how many times this value has occurred in the previous prefix_sum[i] - i for i <= j.

So, the idea is to compute for each position, the value of (prefix_sum[i] - i), and for each j, we look for how many times the current value (prefix_sum[j+1] - (j+1)) has occurred before. That would give the count of substrings ending at j that satisfy the condition.

This is similar to the approach used in the problem of finding subarrays with sum equal to k. So, using a hash map to track the counts of the prefix values.

So, here's the plan:

- Precompute the prefix_sum array.

- For each index i, compute the value of prefix_sum[i] - i.

- Use a hash map (like a dictionary) to keep track of the frequency of these values.

- For each j, compute current_value = prefix_sum[j+1] - (j+1). The number of times this current_value has occurred before (in the map) is added to the count.

- Initialize the map with the value for i=0 (prefix_sum[0] - 0 = 0 - 0 = 0). Because when j is 0, the prefix_sum[j+1] is prefix_sum[1], which is the first digit. Then, current_value is prefix_sum[1] - 1. The initial value in the map is for i=0 (prefix_sum[0] - 0 = 0). So for each j, the current_value is checked against the map, and the count is incremented by the frequency of current_value in the map.

Wait, let me think again. Let me think about the formula.

Let me rephrase:

For a substring from i to j (inclusive), the sum of digits is sum = prefix_sum[j+1] - prefix_sum[i].

The length is (j - i + 1).

We need sum == length → prefix_sum[j+1] - prefix_sum[i] = j - i + 1 → prefix_sum[j+1] - (j+1) = prefix_sum[i] - i.

So for each j, we can compute the current value (prefix_sum[j+1] - (j+1)), and look for how many previous i's (from 0 to j) have prefix_sum[i] - i equal to this current value. Because each such i corresponds to a substring from i to j.

So the approach is:

Initialize a dictionary with the initial value (for i=0, prefix_sum[0] - 0 = 0). Then for each j in 0 to n-1:

Compute current_value = prefix_sum[j+1] - (j+1). Then, the count += the number of times this current_value has been seen before. Then, we add the current_value (for i = j+1) to the dictionary.

Wait, no. Wait, for each j (the end of the substring), we need to consider all possible starting positions i (from 0 to j). So, for j, we compute the current_value (prefix_sum[j+1] - (j+1)), and then check how many times this value has appeared in the prefix_sum[i] - i for i from 0 to j. Because for each such i, the substring from i to j is valid.

So, the process is:

Initialize a dictionary, say count_map, with {0: 1} (since prefix_sum[0] - 0 = 0, and we have one occurrence of it).

Then, for each index j from 0 to len(s)-1:

Compute the current prefix_sum up to j+1, then compute current_value = prefix_sum[j+1] - (j+1).

Then, the number of times this current_value has been seen in count_map is added to the total count.

Then, we update the count_map by adding the value (prefix_sum[j+1] - (j+1)) to the map (for the next j's).

Wait, no. Because for the next j's, the i's would be up to j. So for the current j, when we compute current_value, we need to check how many times it has appeared before (i.e., for i from 0 to j). So, the current_value is for the j+1-th prefix sum. So, for the j-th index (the end of the substring), we need to check the count_map which contains the values for prefix_sum[0] - 0, prefix_sum[1] -1, ..., prefix_sum[j] - j. So the steps would be:

Initialize count_map with {0:1} (for prefix_sum[0] - 0 = 0).

Initialize prefix_sum as 0.

Then, for each character in the string:

prefix_sum += int(char)

current_value = prefix_sum - (current_position + 1) ?

Wait, let me think again.

Let me think of the prefix_sum array. Let's say the string is s of length n. Let prefix_sum be an array where prefix_sum[0] = 0, prefix_sum[1] = s[0], prefix_sum[2] = s[0] + s[1], etc.

So for j in 0 to n-1, the substring from i to j (inclusive) has length (j - i + 1). The sum is prefix_sum[j+1] - prefix_sum[i].

So, for each j, we compute the current_value = prefix_sum[j+1] - (j+1). Then, the number of times this current_value has occurred in the count_map (which contains the values of prefix_sum[i] - i for i from 0 to j) is the number of valid substrings ending at j.

So the steps would be:

Initialize prefix_sum = 0.

Initialize count_map with {0: 1}.

Initialize total_count = 0.

For each index j from 0 to len(s)-1:

current_char = s[j]

prefix_sum += int(current_char)

current_value = prefix_sum - (j + 1)

total_count += count_map.get(current_value, 0)

Then, we need to add the current_value (prefix_sum - (j + 1)) to the count_map for future j's. Wait, no. Because for the next j's, the i can be up to j+1. So, for the current j, after processing, we need to add the value (prefix_sum - (j+1)) to the count_map. Wait, no. Because for the next j, when we compute current_value, we need to have the prefix_sum[i] - i for i up to j. So, when we process j-th character (the current j), after calculating current_value, we add the value (prefix_sum - (j + 1)) to the count_map? Or wait, the prefix_sum for the current j is prefix_sum[j+1]. So for the next steps, when we process the next j, we need to have the prefix_sum[i] - i for i up to j.

Wait, the count_map is supposed to track prefix_sum[i] - i for i from 0 to current j. So, when we process j-th character (the current j), the prefix_sum is prefix_sum[j+1]. So, the current_value for j is prefix_sum[j+1] - (j+1). But this is for i = j+1? Or for i = ?

Wait, perhaps I'm getting confused. Let me think again.

The current_value is prefix_sum[j+1] - (j+1). This is the value that we want to find in the count_map. The count_map contains the values of prefix_sum[i] - i for i from 0 to j. Because for each i, when we process the j-th character, we have already added the prefix_sum[i] - i for i up to j. Wait, no. Let me think of the loop:

Initially, count_map has {0:1} (prefix_sum[0] - 0 = 0).

Then, for j=0 (the first character):

prefix_sum is 0 + s[0] (i.e., prefix_sum[1]).

current_value is prefix_sum[1] - (0 + 1) = prefix_sum[1] -1.

We check how many times this current_value has been in the count_map (which is {0:1}).

Then, we add the value (prefix_sum[1] - (0 + 1)) to the count_map? Or is that the value for i=1?

Wait, the count_map is supposed to track prefix_sum[i] - i for i from 0 to current j. Because for the next j's, when we process them, we need to have all the previous i's.

So, after processing j-th character, we need to add the value for i = j+1 (i.e., prefix_sum[j+1] - (j+1)) into the count_map. Because for the next j, when processing j+1, the i can be up to j+1.

So the steps would be:

Initialize prefix_sum = 0.

count_map = {0:1}

total_count = 0

for j in 0 to len(s)-1:

    prefix_sum += int(s[j])

    current_value = prefix_sum - (j+1)

    total_count += count_map.get(current_value, 0)

    # Now, add the current_value (prefix_sum - (j+1)) to the count_map for the next steps.

    # Wait, no. Because the current_value is prefix_sum[j+1] - (j+1) = (prefix_sum up to j+1) - (j+1). Which is the value for i = j+1. So, for the next j's, when they process, they need to check for this i.

    # So, after processing j, we add this current_value to the count_map.

    # Wait, no. Because for the next j, the i can be up to j+1. So, after processing j, the current_value is for i = j+1. So we need to add this to the count_map for future steps.

    # So, we add current_value to the count_map.

    count_map[current_value] = count_map.get(current_value, 0) + 1

Wait, but that's not right. Because for j-th iteration, the current_value is prefix_sum[j+1] - (j+1), which is for i = j+1. So when we add this to the count_map, it's for the next steps. Because in the next steps, when j is incremented, the current_value will be for prefix_sum[j+1] - (j+1), and we need to check against the count_map which contains all previous i's (from 0 to j+1).

So the code would be:

Initialize prefix_sum = 0.

count_map = {0:1}

total_count = 0

for j in range(len(s)):

    prefix_sum += int(s[j])

    current_value = prefix_sum - (j+1)

    total_count += count_map.get(current_value, 0)

    # Now, we need to add the current_value to the count_map for future use.

    # Wait, but current_value is the value for i = j+1. Because prefix_sum is now prefix_sum[j+1], and current_value is prefix_sum[j+1] - (j+1). So, this value is for the i = j+1. So when the next j is processed, the count_map will include this value.

    # So, we need to add this current_value to the count_map.

    count_map[current_value] = count_map.get(current_value, 0) + 1

Wait, but when j is 0, the current_value is prefix_sum[1] - 1. Then, we add this value to the count_map. So for the next j (j=1), when we compute current_value, the count_map includes this value. So the code is correct.

Let me test this approach with the sample input '112112'.

Let's walk through the sample step by step.

Sample input: '112112' → s = ['1','1','2','1','1','2']

n = 6.

Initialize prefix_sum = 0.

count_map = {0:1}

total_count = 0.

Processing j from 0 to 5:

j=0:

s[j] = '1'

prefix_sum = 0 + 1 = 1.

current_value = 1 - (0+1) = 1-1 = 0.

total_count += count_map.get(0,0) → 1 → total_count is 1.

Then, add current_value (0) to count_map. count_map[0] becomes 2.

count_map is {0:2}.

j=1:

s[j] = '1'

prefix_sum = 1 + 1 = 2.

current_value = 2 - (1+1) = 2-2=0.

total_count += count_map.get(0) → 2 → total_count becomes 1+2=3.

Then, add current_value 0 to count_map. Now count_map[0] is 3.

j=2:

s[j] = '2' → prefix_sum = 2 + 2 =4.

current_value = 4 - (2+1) = 4-3=1.

count_map has 0:3. So current_value is 1. count_map.get(1,0) is 0. So total_count remains 3.

Then add current_value 1 to count_map. count_map now has {0:3, 1:1}.

j=3:

s[j] = '1' → prefix_sum =4 +1=5.

current_value =5 - (3+1) =5-4=1.

count_map.get(1) is 1 → total_count +=1 → total becomes 4.

Then add current_value 1 → count_map[1] becomes 2.

j=4:

s[j] = '1' → prefix_sum =5+1=6.

current_value =6 - (4+1) =6-5=1.

count_map.get(1) is 2 → total_count +=2 → total becomes 4+2=6.

Then add current_value 1 → count_map[1] becomes 3.

j=5:

s[j] = '2' → prefix_sum =6+2=8.

current_value =8 - (5+1) =8-6=2.

count_map has 0:3, 1:3. So get(2) is 0. total_count remains 6.

Then add current_value 2 to count_map.

So the total_count is 6, which matches the sample. So this approach works.

So the code should implement this logic.

Now, the code steps:

We need to read the string, process each character, keep track of prefix_sum, and use a dictionary to count the occurrences of (prefix_sum - i) for each i.

Now, code:

We can write the function as follows.

First, import nothing, since it's not needed.

The function count_Substrings(s):

Initialize prefix_sum = 0

count_map = {0:1}

total_count = 0

for j in range(len(s)):

    prefix_sum += int(s[j])

    current_value = prefix_sum - (j + 1)

    total_count += count_map.get(current_value, 0)

    count_map[current_value] = count_map.get(current_value, 0) + 1

return total_count

Wait, but let me check for the sample. Let me run through the steps again.

Yes, the code for the sample gives 6, which is correct.

So this code should work.

Now, let's test another case. For example, the string '1' → expected count is 1.

Processing j=0:

prefix_sum is 1. current_value =1 -1=0. count_map has 0:1. So total_count +=1. Then count_map[0] becomes 2. So returns 1. Correct.

Another test case: '11' → expected count is 2 (each single '1' and the substring '11' (sum 2, length 2).

Let me see:

prefix_sum starts at 0.

count_map {0:1}

j=0:

prefix_sum =1. current_value =1-1=0. total_count +=1. count_map[0] becomes 2.

j=1:

prefix_sum =2. current_value =2 - 2 =0. total_count +=2 → total_count is 1+2=3. Then count_map[0] becomes 3.

But the expected answer is 3?

Wait, the substrings are:

For '11', the valid substrings are:

- '1' (0), sum 1, length 1.

- '1' (1), sum 1, length 1.

- '11' (sum 2, length 2). So total 3. So the code returns 3, which is correct. So the code works here.

Another test case: '12' → expected count?

Single digits: 1 and 2. Both are valid (sum 1 and 2, length 1 each). Then check substrings of length 2: sum 1+2=3, length 2 → no. So total 2. Let's see code:

prefix_sum starts at 0.

count_map {0:1}

j=0:

prefix_sum =1. current_value =1-1=0. total_count +=1 → 1. count_map[0] is 2.

j=1:

prefix_sum =1+2=3. current_value =3 - 2 =1. count_map has 0:2. So total_count +=0. So total is 1. Then add 1 to count_map. So returns 1? But expected is 2. Wait, what's wrong here?

Wait, the code returns 1, but the correct answer is 2. What's wrong?

Wait, let me re-examine the code.

For the string '12', the code steps:

j=0:

prefix_sum =1.

current_value =1 - (0+1) = 0.

count_map has 0:1. So total_count +=1 → total_count is 1.

Then, count_map[0] becomes 2.

j=1:

prefix_sum =1 + 2 =3.

current_value =3 - (1+1) = 3 - 2 =1.

count_map has 0:2. So count_map.get(1) is 0. So total_count remains 1.

Then, add 1 to count_map. So count_map has 0:2, 1:1.

So the code returns 1. But the correct answer is 2. So why is there a discrepancy?

Ah! Because the code is missing something. Let me think again.

Wait, what is the code counting?

The code counts the number of substrings where sum of digits equals the length. For the string '12', the valid substrings are:

- '1' (sum 1, length 1)

- '2' (sum 2, length 1)

So that's 2. But according to the code, it's returning 1. So there's a problem. So why?

Let me re-examine the logic.

In the code, for j=0 (the first character), the code adds 1 to total_count. That's the substring from i=0 to j=0 (the first '1').

Then, for j=1 (the second character), the code checks current_value = prefix_sum - (j+1) = 3 - 2 =1. Then, the count_map has 0:2. So no addition. But what about the substring from i=1 to j=1 (the second '2')?

Ah! Because in the code, the current_value for j=1 is 1. But the count_map contains the previous values. Let me think about what's the current_value for the substring from i=1 to j=1.

For the substring from i=1 to j=1, the sum is 2. The length is 1. So sum equals length. So it should be counted.

But according to the code, when j=1, the current_value is prefix_sum[j+1] - (j+1) =3 - 2 =1. We need to find the number of previous i's where prefix_sum[i] - i equals 1.

The previous i's are 0 and 1 (since for j=1, the code is processing the current j=1, and the count_map contains prefix_sum[i] - i for i from 0 to j (i=0 and i=1? Or not? Let me think again.

Wait, the code for j=1:

At this point, the code has processed j=0 and added the current_value (0) to the count_map. So count_map contains 0:2.

Then, for j=1, the code computes current_value =3-2=1. The count_map has entries for prefix_sum[i] - i where i ranges from 0 to j (i=0 and i=1? Or i=0 to j=1? Or i=0 to j=0? Let me think.

Wait, the code for j=1:

The prefix_sum is updated to include the current character (s[1] = '2'). So prefix_sum is now the sum of the first j+1 = 2 characters.

Then, current_value is prefix_sum[j+1] - (j+1) = prefix_sum[2] - 2.

This is the value that we are looking for in the count_map, which contains all prefix_sum[i] - i for i from 0 to j (i=0 and i=1? Or i=0 to j=1? Because for j=1, the code is processing the second character, and the count_map should have the entries for i=0 and i=1?

Wait, the count_map is initially {0:1} (i=0).

Then, for j=0:

current_value is prefix_sum[1] -1. Then, after processing, the code adds this current_value to the count_map. So the count_map now has entries for i=0 and i=1? Or for i=1?

Wait, the count_map is supposed to track prefix_sum[i] - i for i from 0 to current j. Because when processing j, the current_value is for prefix_sum[j+1] - (j+1), which is the value for i = j+1. But when we add it to the count_map, it's for the next steps.

So, during the processing of j=0, after adding the current_value, the count_map contains entries for i=0 and i=1?

No. Because the count_map is for prefix_sum[i] - i for i=0 to j. For j=0, after processing, the current_value is for i=1 (prefix_sum[1] - 1). So during the processing of j=0, the code adds this value to the count_map. So for the next steps, the count_map contains entries for i=0 and i=1.

So when processing j=1, the code is looking for current_value (prefix_sum[2] - 2) and checking how many times this value has occurred in the count_map, which includes i=0 and i=1.

But for the substring from i=1 to j=1, which is the second character, the sum is 2, length is 1. So sum equals length. How does this fit into the formula?

Let me compute the formula for this substring.

i=1, j=1.

sum = prefix_sum[j+1] - prefix_sum[i] = prefix_sum[2] - prefix_sum[1] = 3 - 1 = 2.

length = j - i + 1 = 1-1+1=1.

So 2 = 1? No. Wait, this is not valid. Wait, why?

Wait, the substring is from i=1 to j=1 (the second character). The sum is 2, length is 1. So 2 !=1. So this is not a valid substring. So why did I think it was valid?

Oh! I made a mistake here. The substring is '2', sum is 2, length is 1. So sum is not equal to length. So it's not valid. So the code is correct in not counting it. But then why does the code return 1 for the string '12'? Because the only valid substring is the first '1' (counted in j=0) and the second '2' is not valid. But then what about the substring '1' (second character)? Wait, the code is counting all substrings where sum equals length. So the second '2' is a substring of length 1, sum is 2. So 2 !=1. So it's not valid. So the correct answer for '12' is 1. But earlier I thought it would be 2. So I made a mistake in the previous analysis.

So the code is correct. For the string '12', the valid substrings are only the first '1' (sum 1, length 1). The second '2' is not valid. So the code returns 1, which is correct.

So my earlier analysis was wrong. So the code works.

Another example: '2' → returns 1, which is correct.

Another example: '11' → returns 3. Which includes:

- first '1' (sum 1, length 1)

- second '1' (sum 1, length 1)

- '11' (sum 2, length 2)

Yes, which is correct.

So the code seems correct.

Therefore, the Python function can be written as follows.

Now, code:

def count_Substrings(s):
    prefix_sum = 0
    count_map = {0: 1}
    total_count = 0
    for j in range(len(s)):
        prefix_sum += int(s[j])
        current_value = prefix_sum - (j + 1)
        total_count += count_map.get(current_value, 0)
        count_map[current_value] = count_map.get(current_value, 0) + 1
    return total_count

Testing this with the sample input '112112' returns 6, which is correct.

So this should be the solution.
```

</details>

**Code that ran:**

```python
def count_Substrings(s):
    prefix_sum = 0
    count_map = {0: 1}
    total_count = 0
    for j in range(len(s)):
        prefix_sum += int(s[j])
        current_value = prefix_sum - (j + 1)
        total_count += count_map.get(current_value, 0)
        count_map[current_value] = count_map.get(current_value, 0) + 1
    return total_count
```

**Visible-test report:**

```text
PASS    assert count_Substrings('112112') == 6
1 of 1 visible tests passed
```
