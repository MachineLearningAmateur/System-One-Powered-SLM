# Mbpp/61, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/61/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 7719. Answer tokens: 77.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where I have to count the number of substrings in a given string such that the sum of their digits equals the length of the substring. Let me think about how to approach this.

First, let me understand the problem with the example given. The input is '112112' and the output is 6. Let me check why. Let's list all possible substrings and see which ones meet the condition.

For example, the substring '1' (length 1) has sum 1, which equals the length. So that's valid. Similarly, each individual digit is a valid substring. But wait, the example says the answer is 6. Let's see:

Original string is '112112'. Let's list all substrings and check:

Possible substrings:

Length 1:
Each character. There are 6 of them. Each sum is the digit itself, which equals the length (1). So all 6 are valid. But the answer is 6. Wait, but the sample output is 6. So maybe that's the case. But wait, maybe there are other substrings that also meet the condition. Let me check.

Wait, maybe there are longer substrings that also meet the condition. For example, let's take the substring '11' (positions 0-1). The sum is 1+1=2. The length is 2. So sum equals length. So that's valid. So that's another substring. So in that case, the total would be more than 6. But according to the sample, the answer is 6. So perhaps my initial assumption is wrong. Wait, maybe the sample input is '112112' and the correct answer is 6. Let me check.

Wait, maybe there are other substrings. Let me think again. Let me list all possible substrings and check.

Original string is '1', '1', '2', '1', '1', '2'.

Let me think of all substrings:

For length 1: 6 substrings. All valid. So that's 6.

But the sample output is 6. So that suggests that there are no other substrings that meet the condition. But why? Let me check for longer substrings.

Take substring from index 0 to 1: '11' sum is 2, length is 2. Valid. So that's another one. So that would make the count 7. But sample says 6. So there's a contradiction here. Which means I must have misunderstood the problem.

Wait, maybe I made a mistake in the sample. Let me check the sample again. The sample says count_Substrings('112112') == 6. But according to my reasoning, there are at least 6 (from length 1) plus some others. So why is the answer 6?

Wait, perhaps I'm misunderstanding the problem. Let me re-read the problem statement.

The problem says: count the number of substrings where the sum of digits equals their length. So for a substring of length L, the sum of the digits in that substring must equal L.

So for example, the substring '11' has sum 2 and length 2. So that's valid. So that's one more. So the sample answer would be more than 6. But according to the sample, it's 6. So why?

Wait, maybe the sample is wrong? Or maybe I'm making a mistake here. Let me check the sample input again. Let me think of all possible substrings for '112112' and count how many meet the condition.

Let me list all possible substrings and check.

First, the string is '1','1','2','1','1','2' (indices 0 to 5).

Let me consider all possible substrings:

For length 1:

Each of the 6 characters. Sum is digit, length is 1. So sum equals length. So 6 substrings.

For length 2:

Check all substrings of length 2:

0-1: '11' sum 2, length 2 → valid.

0-1 is valid. So count +=1.

1-2: '12' sum 1+2=3, length 2 → 3 != 2 → invalid.

2-3: '21' sum 3, length 2 → invalid.

3-4: '11' sum 2 → valid. So count +=1.

4-5: '12' sum 3 → invalid.

So for length 2, there are 2 valid substrings. So total so far is 6 + 2 = 8.

Wait, but sample says 6. So something's wrong here. So maybe I'm missing something. Let me check again.

Wait, maybe the sample is wrong? Or maybe I have a misunderstanding.

Alternatively, perhaps the sample is correct, and I'm making a mistake here. Let me check again.

Wait, perhaps the sample input is '112112' and the correct answer is 6. So according to that, there are 6 substrings. Let me think again.

Let me check the sample input again. Let me think of all substrings.

Wait, maybe I made a mistake in the length 2 substrings.

Let me re-examine:

The string is '112112'.

Substrings of length 2:

Indices 0-1: '11' → sum 2 → length 2 → valid.

Indices 1-2: '12' → sum 1+2=3 → length 2 → 3 != 2 → invalid.

Indices 2-3: '21' → sum 2+1=3 → length 2 → invalid.

Indices 3-4: '11' → sum 2 → valid.

Indices 4-5: '12' → sum 3 → invalid.

So that's two more. So total is 6 + 2 = 8. But sample says 6. So this suggests that there's a mistake in my reasoning.

Wait, perhaps the sample is wrong? Or perhaps I'm misunderstanding the problem. Let me check the problem statement again.

The problem says: count the number of substrings with the sum of digits equal to their length. So the sum of digits in the substring equals the length of the substring.

Wait, perhaps the sample input is '112112' and the correct answer is 6. So why?

Let me think again. Maybe there are other substrings that are longer and meet the condition.

Let me check for length 3.

Substrings of length 3:

Indices 0-2: '112' → sum 1+1+2=4. Length 3 → 4 != 3 → invalid.

Indices 1-3: '121' → sum 1+2+1=4 → length 3 → invalid.

Indices 2-4: '211' → sum 2+1+1=4 → length 3 → invalid.

Indices 3-5: '112' → sum 1+1+2=4 → invalid.

So no valid substrings of length 3.

What about length 4?

Substrings of length 4:

Indices 0-3: '1121' sum 1+1+2+1 = 5. Length 4 → 5 !=4 → invalid.

Indices 1-4: '1211' sum 1+2+1+1=5 → length 4 → invalid.

Indices 2-5: '2112' sum 2+1+1+2=6 → length 4 → invalid.

No valid here.

Length 5:

Substrings of length 5:

Indices 0-4: '11211' sum 1+1+2+1+1=6. Length 5 → 6 !=5 → invalid.

Indices 1-5: '12112' sum 1+2+1+1+2=7 → invalid.

Length 6:

Sum is 1+1+2+1+1+2=8. Length 6 → 8 !=6 → invalid.

So for length 2, there are 2 valid substrings. So total is 6 + 2 = 8. But sample says 6. So there's a contradiction here. Which means that either I have a mistake in the reasoning, or the sample is wrong. But the sample says that count_Substrings('112112') == 6. So I must have made a mistake.

Wait, maybe I'm counting the substrings incorrectly. Let me recheck the sample input. Maybe the sample input is '112112' and the correct answer is 6. Let me think again. Let me think of all possible substrings that meet the condition.

Wait, maybe the substrings of length 1 are not all valid. Let me think. For example, the substring '1' has sum 1, which equals the length (1). So that's valid. So for each of the 6 digits, the substring is valid. So that's 6. But according to the sample, the answer is 6. Which suggests that there are no other substrings. But according to my previous analysis, there are 2 more substrings of length 2. So why is that?

Ah! Wait, maybe I made a mistake in the sum of the digits. Let me recheck the substrings of length 2.

For example, the substring '11' (indices 0-1) sum is 1 + 1 = 2, which equals the length (2). So that's valid. Similarly, the substring '11' at indices 3-4 (the third and fourth characters) is also sum 2. So that's two more. So total is 6 + 2 = 8. But sample says 6. So this suggests that there's a mistake in my analysis. What's going on?

Alternatively, perhaps the problem counts the substrings where the sum of digits is equal to the length of the substring. But maybe the problem is that the sum of the digits is equal to the length. So for example, the substring '11' (sum 2, length 2) is valid. So that's two more substrings. So why is the sample answer 6?

This suggests that either the sample is wrong, or I have a misunderstanding. Let me check the sample again. Maybe the sample is not correct. But the user says that the sample is correct. So I need to find why the sample output is 6.

Alternatively, maybe the problem is that the sum of digits is equal to the length of the substring. Wait, maybe I made a mistake in the sum of the digits for the substrings of length 2.

Wait, for the substring '11' (indices 0-1), sum is 1 + 1 = 2. Length is 2. So that's valid. So that's one. Similarly, the substring at indices 3-4 is '11' again. So sum 2, length 2. So that's two. So that's two more. So total is 6 + 2 = 8. But sample says 6. So why?

Wait, maybe the problem is that the substrings are counted in a different way. For example, maybe the problem counts the substrings where the sum of digits is equal to the length of the substring. But maybe the sum is not the sum of the digits, but something else. Or perhaps I have misread the problem.

Wait, the problem says: "sum of digits equal to their length". So the sum of the digits in the substring equals the length of the substring. So for example, the substring '11' has sum 2, length 2. So it's valid. So why is the sample output 6? Unless there's a mistake in the sample.

Alternatively, maybe I made a mistake in the sample input. Let me check the sample input again. The input is '112112'. Let me write down all the substrings and their sum and length.

Let me list all possible substrings:

For length 1:

Each single character. Sum is the digit. Length 1. So all valid. 6 substrings.

For length 2:

Check all possible substrings:

Indices 0-1: '11' sum 2 → valid.

Indices 1-2: '12' sum 3 → invalid.

Indices 2-3: '21' sum 3 → invalid.

Indices 3-4: '11' sum 2 → valid.

Indices 4-5: '12' sum 3 → invalid.

So two more substrings. Total 8.

Length 3:

Check all substrings of length 3.

Indices 0-2: '112' sum 1+1+2 =4. Length 3 → 4 !=3 → invalid.

Indices 1-3: '121' sum 1+2+1=4 → invalid.

Indices 2-4: '211' sum 2+1+1=4 → invalid.

Indices 3-5: '112' sum 4 → invalid.

No valid.

Length 4:

Indices 0-3: '1121' sum 1+1+2+1=5. Length 4 → invalid.

Indices 1-4: '1211' sum 1+2+1+1=5 → invalid.

Indices 2-5: '2112' sum 2+1+1+2=6 → invalid.

Length 5:

Indices 0-4: '11211' sum 1+1+2+1+1=6 → length 5 → invalid.

Indices 1-5: '12112' sum 1+2+1+1+2=7 → invalid.

Length 6:

sum 1+1+2+1+1+2=8 → length 6 → invalid.

So total valid substrings are 6 (from length 1) + 2 (from length 2) = 8. But according to the sample, it's 6. So why?

This suggests that there's a mistake in my analysis. But how?

Wait, maybe the sample is not correct. Or perhaps I'm missing something. Let me think again.

Wait, perhaps the problem counts the substrings where the sum of the digits is equal to the length of the substring. But in the case of the substring '11', the sum is 2, and the length is 2. So it's valid. So why is the sample answer 6?

Alternatively, maybe the problem counts the substrings where the sum of the digits equals the length of the substring, but the sum is calculated as the sum of the digits' numeric values. Wait, that's what I did. So why is the sample answer 6?

Alternatively, maybe the problem is that the substrings are not counted as per their length. Wait, perhaps the problem is that the sum of the digits is equal to the length of the substring. So for example, the substring '1' is length 1, sum is 1 → valid. But what about the substring '11' (length 2, sum 2) → valid. So that's two more. So why sample says 6?

This is confusing. Maybe there's a mistake in the sample. But the user says that the sample is correct. So I need to find out why the sample output is 6. Let me think of other possibilities.

Wait, perhaps I made a mistake in the sample input. Let me check the sample input again. The input is '112112'. Let me write it as a string: '112112'. Let me count the number of valid substrings again.

Wait, maybe I'm missing that some substrings are not valid. For example, the substring '1' is valid. But maybe there are some other substrings that are not counted. Let me re-examine.

Let me think of all possible substrings again.

Wait, perhaps I made a mistake in the length 1 substrings. For example, the string is '1', '1', '2', '1', '1', '2'. So for each of the 6 characters, the substring is valid. So 6. Then for length 2, there are two valid substrings. So total 8. But the sample says 6. So this suggests that the sample is wrong. Or perhaps I have a misunderstanding of the problem.

Alternatively, perhaps the problem counts substrings where the sum of the digits equals the length of the substring. But the sum is not the sum of the digits, but the sum of the digits multiplied by their positions or something else. But that's not what the problem says.

Alternatively, perhaps the problem is that the sum of the digits is equal to the length of the substring. But maybe the length is the length of the substring, which is the same as the number of digits. So for example, for a substring of length 2, the sum of digits is 2. Which is what I thought.

But then why the sample says 6?

Wait, maybe the sample is correct, and I'm making a mistake in the analysis. Let me think again.

Wait, perhaps the sample input is '112112' and the correct answer is 6. So maybe there are only 6 substrings that meet the condition. Let me think of what could be the case.

Let me think of all substrings again. Maybe there are no substrings of length 2 that are valid. How?

For example, the substring '11' (indices 0-1) sum is 2, length 2. Valid. So why is that not counted? Or perhaps the problem counts the sum of digits as the sum of their numeric values, but perhaps I made a mistake in calculating that.

Wait, let me recheck:

For the substring '11', the digits are 1 and 1. Sum is 1 + 1 = 2. Length is 2. So sum equals length. So it's valid.

So why is the sample output 6?

Unless the sample is wrong, but the user says that the sample is correct. So there must be a mistake in my analysis.

Alternatively, maybe the problem is that the sum of the digits is equal to the length of the substring. But for the substring '11' (sum 2), the length is 2. So it's valid. So the sample answer should be 8. But the sample says 6. So this is a problem.

Alternatively, maybe the problem is that the sum of the digits is equal to the length of the substring. But perhaps the sum is calculated as the sum of the digits, but the length is the length of the substring. So in the example, there are 6 substrings of length 1, and 0 of others. So how?

Wait, perhaps the sample input is '112112' and the correct answer is 6. Let me think of other possibilities.

Wait, perhaps I'm misunderstanding the problem. Maybe the problem is to find substrings where the sum of the digits is equal to the length of the substring. But for example, the substring '1' has sum 1, length 1. Valid. But what about substrings that have other lengths?

Wait, perhaps there are no other substrings. Let me think again. Maybe I made a mistake in the length of the substrings.

Wait, for the substring '11', length is 2. Sum is 2. So valid. So why is the sample answer 6?

This is confusing. Maybe I should try to think of another approach. Let me think of how to code this.

Let me think of the approach to solve the problem. For each possible substring, calculate the sum of its digits and compare it to the length of the substring. If equal, increment the count.

But for the sample input '112112', according to this approach, the count should be 8. But the sample says 6. So there's a contradiction. Therefore, I must have made a mistake in my analysis.

Alternatively, perhaps the sample is wrong. Or perhaps I'm missing something.

Wait, maybe the problem is that the sum of the digits is equal to the length of the substring. But the substring is a contiguous sequence of digits. So for example, the substring '11' is valid. But maybe the problem is that the sum of the digits is equal to the length of the substring. But in that case, the sample should have 8. So why is the sample answer 6?

Alternatively, perhaps the problem is that the sum of the digits is equal to the length of the substring. But in the sample input, the substrings of length 2 are not valid. How?

Wait, maybe I made a mistake in the sum calculation for the substrings of length 2. Let me recheck:

For the substring '11' (indices 0-1), digits are 1 and 1. Sum is 2. Length is 2. So valid.

For the substring at indices 3-4: digits are 1 and 1. Sum is 2. Length 2. Valid. So two substrings.

So total is 6 + 2 = 8.

But the sample says 6. So this is a problem.

Alternatively, maybe the problem counts the substrings where the sum of the digits is equal to the length of the substring, but the length is the length of the substring in terms of characters. But that's what I'm doing.

Wait, perhaps the sample is wrong. Or perhaps the problem is different. Maybe the sum of the digits is equal to the length of the substring, but the substring is considered as a number. For example, the substring '11' is the number 11, which has length 2. But the sum of digits is 2. So it's valid. So this doesn't change anything.

Alternatively, perhaps the problem is to find substrings where the sum of the digits is equal to the length of the substring, but the length is the number of characters, which is the same as the length of the substring. So that's what I'm doing.

Hmm. This is a puzzle. Let me think of another approach. Maybe I should write code to count the substrings for the sample input and see what it returns.

Let me write a small code snippet to calculate the count for the sample input.

For example:

s = '112112'

count = 0

for i in range(len(s)):

    for j in range(i, len(s)):

        substring = s[i:j+1]

        sum_digits = sum(int(c) for c in substring)

        if sum_digits == len(substring):

            count +=1

print(count)

Let me run this code in my mind for the sample input.

Let's see:

For i=0:

j=0 → substring '1', sum 1 → len 1 → valid → count +=1.

j=1 → substring '11', sum 2 → len 2 → valid → count +=1.

j=2 → substring '112', sum 1+1+2=4 → len 3 → 4 !=3 → no.

j=3 → substring '1121' sum 5 → len 4 → no.

j=4 → sum 1+1+2+1+1=6 → len 5 → no.

j=5 → sum 8 → len 6 → no.

So for i=0, count increases by 2.

i=1:

j=1 → substring '1' → valid → count +=1.

j=2 → '12' sum 3 → len 2 → no.

j=3 → '121' sum 4 → len 3 → no.

j=4 → '1211' sum 5 → len 4 → no.

j=5 → '12112' sum 7 → len 5 → no.

So for i=1, count increases by 1.

i=2:

j=2 → '2' → sum 2 → len 1 → 2 !=1 → no.

j=3 → '21' sum 3 → len 2 → no.

j=4 → '211' sum 4 → len 3 → no.

j=5 → '2112' sum 6 → len 4 → no.

So no additions here.

i=3:

j=3 → '1' → valid → count +=1.

j=4 → '11' sum 2 → len 2 → valid → count +=1.

j=5 → '112' sum 4 → len 3 → no.

So for i=3, count increases by 2.

i=4:

j=4 → '1' → valid → count +=1.

j=5 → '12' sum 3 → len 2 → no.

So for i=4, count increases by 1.

i=5:

j=5 → '2' → sum 2 → len 1 → no.

So total count is 2 (from i=0) + 1 (i=1) + 0 (i=2) + 2 (i=3) + 1 (i=4) + 0 (i=5) = 2+1+2+1=6? Wait, let me calculate:

i=0: 2 → count is 2.

i=1: 1 → total 3.

i=2: 0 → total 3.

i=3: 2 → total 5.

i=4: 1 → total 6.

i=5: 0 → total 6.

So the total count is 6. Which matches the sample! Oh! So why did I think there were 8 before? Because I forgot that for i=3, j=3 and j=4 are valid, and for i=1, j=1 is valid, and for i=0, j=0 and j=1 are valid. Let me recount:

Let me list all the valid substrings:

From the code:

When i=0, j=0 → valid (count 1).

i=0, j=1 → valid (count 2).

i=1, j=1 → valid (count 3).

i=3, j=3 → valid (count 4).

i=3, j=4 → valid (count 5).

i=4, j=4 → valid (count 6).

Wait, so there are 6 valid substrings. What about the other substrings of length 2?

Ah! I think I made a mistake earlier. Let me recheck:

For i=0, j=1: substring '11' → valid.

For i=3, j=4: substring '11' → valid.

But what about the other substrings of length 2? Like i=1, j=2: '12' sum 3 → len 2 → 3 !=2 → invalid.

i=2, j=3: '21' sum 3 → len 2 → invalid.

i=4, j=5: '12' sum 3 → invalid.

So only two substrings of length 2 are valid. But according to the code, the total count is 6. So how does that add up?

Let me list all the valid substrings:

1. i=0, j=0 → '1' → sum 1 → len 1.

2. i=0, j=1 → '11' → sum 2 → len 2.

3. i=1, j=1 → '1' → sum 1 → len 1.

4. i=3, j=3 → '1' → sum 1 → len 1.

5. i=3, j=4 → '11' → sum 2 → len 2.

6. i=4, j=4 → '1' → sum 1 → len 1.

So total of 6 valid substrings. Wait, what about the other '1's?

For example, i=2, j=2 → '2' → sum is 2, len is 1. So 2 !=1 → invalid.

i=5, j=5 → '2' → sum 2, len 1 → invalid.

So the other '1's are:

i=0, j=0 → valid.

i=1, j=1 → valid.

i=3, j=3 → valid.

i=4, j=4 → valid.

That's four substrings of length 1. Plus two substrings of length 2. So total 6.

Ah! I see my mistake earlier. I thought there were 6 substrings of length 1, but in reality, there are four of them. Because the other two are '2's (at positions 2 and 5), which have sum 2, but length 1 → 2 !=1 → invalid. So the valid substrings of length 1 are only those where the digit is 1. Let me recheck:

The string is '1','1','2','1','1','2'.

For each character:

- '1' (position 0): valid.

- '1' (position 1): valid.

- '2' (position 2): sum 2, len 1 → 2 !=1 → invalid.

- '1' (position 3): valid.

- '1' (position 4): valid.

- '2' (position 5): invalid.

So there are 4 valid substrings of length 1. Then two substrings of length 2 (positions 0-1 and 3-4). So total 4+2=6. Which matches the sample.

Ah! I see. Earlier, I thought that all 6 length 1 substrings are valid, but that's not the case. The '2's are not valid. So the mistake was in thinking that all single-digit substrings are valid. But no, because for a single-digit substring, the sum of digits is the digit itself, and the length is 1. So the condition is that digit == 1. So only the '1's are valid. So the number of valid substrings of length 1 is 4, not 6. That explains why the sample answer is 6.

So the initial mistake was thinking that all single-digit substrings are valid, but in reality, the sum of the digits must equal the length of the substring. For a single-digit substring, the sum is the digit, and the length is 1. So the digit must be 1. So the '2's are not counted.

So this explains why the sample answer is 6. So the code I wrote earlier would correctly count the 6 substrings.

So now, I need to write a Python function that does this.

The approach is to iterate over all possible substrings, calculate the sum of digits, and check if it equals the length of the substring. For each such case, increment the count.

But for large strings, this approach would be O(n^2), which may not be efficient. But given that the problem seems to have a sample input of length 6, it's acceptable for the problem.

So the code would be:

def count_Substrings(s):
    count = 0
    n = len(s)
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += int(s[j])
            if current_sum == (j - i + 1):
                count +=1
    return count

Let me test this code with the sample input.

For '112112', the code would:

i=0:

current_sum starts at 0.

j=0: current_sum +=1 → 1. j-i+1 is 1 → 1 ==1 → count +=1 → count=1.

j=1: current_sum +=1 → 2. j-i+1 is 2 → 2==2 → count=2.

j=2: current_sum +=2 → 4. j-i+1 is 3 → 4 !=3 → no.

j=3: current_sum +=1 →5. j-i+1 is 4 → 5 !=4 → no.

j=4: current_sum +=1 →6. j-i+1 is 5 → 6 !=5 → no.

j=5: current_sum +=2 →8. j-i+1 is 6 → 8 !=6 → no.

So for i=0, count increases by 2.

i=1:

current_sum starts at 0.

j=1: current_sum +=1 →1. j-i+1 is 1 → count=3.

j=2: current_sum +=2 →3. j-i+1 is 2 → 3 !=2 → no.

j=3: current_sum +=1 →4. j-i+1 is 3 → 4 !=3 → no.

j=4: current_sum +=1 →5. j-i+1 is 4 → 5 !=4 → no.

j=5: current_sum +=2 →7. j-i+1 is 5 → 7 !=5 → no.

So for i=1, count increases by 1 → total 3.

i=2:

current_sum starts at 0.

j=2: current_sum +=2 →2. j-i+1 is 1 → 2 !=1 → no.

j=3: current_sum +=1 →3. j-i+1 is 2 → 3 !=2 → no.

j=4: current_sum +=1 →4. j-i+1 is 3 → 4 !=3 → no.

j=5: current_sum +=2 →6. j-i+1 is 4 → 6 !=4 → no.

No increments.

i=3:

current_sum starts at 0.

j=3: current_sum +=1 →1. j-i+1 is 1 → count=4.

j=4: current_sum +=1 →2. j-i+1 is 2 → count=5.

j=5: current_sum +=2 →4. j-i+1 is 3 → 4 !=3 → no.

So for i=3, count increases by 2 → total 5.

i=4:

current_sum starts at 0.

j=4: current_sum +=1 →1 → j-i+1=1 → count=6.

j=5: current_sum +=2 →3 → j-i+1=2 → 3 !=2 → no.

So for i=4, count increases by 1 → total 6.

i=5:

current_sum starts at 0.

j=5: current_sum +=2 →2. j-i+1=1 → 2 !=1 → no.

So total count is 6. Which matches the sample.

So this code works.

So the code is as above. Now, I need to write this as a Python function, and include any necessary imports. Since there are no imports needed, the code is as follows.

Now, the function is called count_Substrings, and it takes a string as input. The code is as described.

So the final code would be:

def count_Substrings(s):
    count = 0
    n = len(s)
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += int(s[j])
            if current_sum == (j - i + 1):
                count += 1
    return count

Testing this function with '112112' returns 6, as required.

So this should be the correct solution.
```

</details>

**Code that ran:**

```python
def count_Substrings(s):
    count = 0
    n = len(s)
    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += int(s[j])
            if current_sum == (j - i + 1):
                count += 1
    return count
```

**Visible-test report:**

```text
PASS    assert count_Substrings('112112') == 6
1 of 1 visible tests passed
```
