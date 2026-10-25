# HumanEval/126, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/126/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 95.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_sorted that checks if a list of integers is sorted in ascending order. But there's a catch: if there are more than one duplicate of the same number, it should return False. Let me think about how to approach this.

First, the list needs to be in non-decreasing order. So each element should be less than or equal to the next. But wait, the problem says if there's more than one duplicate, return False. Wait, so if there are two same numbers in a row, that's a duplicate. For example, [1, 2, 2, 3] is allowed? Wait, the example given says is_sorted([1, 2, 2, 3, 3, 4]) returns True. Oh, right. Wait, the example says that [1,2,2,3,3,4] is True. But the second example says that [1,2,2,2,3,4] returns False. Oh, so if there's a number that appears more than once consecutively, but only once? Wait, no. Let me recheck the examples.

Looking at the examples:

The example is_sorted([1, 2, 2, 3, 3, 4]) returns True. So two 2s and two 3s are allowed. But in the case of [1, 2, 2, 2, 3, 4], it returns False. So that's three 2s. So the condition is that there can't be more than one occurrence of the same number? Or that consecutive duplicates are allowed only once?

Wait, the problem says: if the list has more than 1 duplicate of the same number, return False. Wait, maybe the wording is ambiguous. Let me re-read the problem statement.

The problem says: "If list has more than 1 duplicate of the same number, return False." So, for example, if the same number appears more than once, then it's invalid. Wait, but that's not possible. Because if the list is sorted, then duplicates would be consecutive. For example, if the list is [1, 2, 2, 3], then there are two 2s. So according to the problem's example, this is allowed. Wait, in the example given, is_sorted([1, 2, 2, 3, 3, 4]) returns True. So that's two 2s and two 3s. So the problem's condition is that the list is sorted, and there are no duplicates except for exactly one occurrence of the same number. Wait, no. Wait, the problem says that if the list has more than 1 duplicate of the same number, return False. So perhaps the condition is that the list must be strictly increasing, but with duplicates allowed only once? Or maybe the problem is that the list must be strictly increasing, but if there are duplicates (i.e., same numbers appearing more than once), then it's invalid. Wait, but the example shows that [1,2,2,3,3,4] is allowed. So that's two 2s and two 3s. So that's not allowed? But the example says it's True. Wait, that's confusing.

Wait, the problem says: "If list has more than 1 duplicate of the same number, return False." So maybe the problem is that if a number appears more than once, then it's considered a duplicate. So for example, if a number appears two times, that's one duplicate. But if it appears three times, that's two duplicates. So the condition is that each number can appear at most once. But that can't be, because the example [1,2,2,3,3,4] returns True. So that's two 2s and two 3s. So that's two duplicates. So the problem's wording is confusing. Wait, perhaps the problem is that the list must be strictly increasing. Because in the example given, [1,2,2,3,3,4] is considered True. But according to the problem's examples, that's allowed. Wait, but according to the problem's examples, that's allowed. So perhaps the problem's condition is that the list must be non-decreasing, but any duplicates are allowed as long as they are consecutive. But that's not the case. Let me check the examples again.

Wait, the example says is_sorted([1, 2, 2, 3, 3, 4]) returns True. So that's allowed. But the example is_sorted([1, 2, 2, 2, 3, 4]) returns False. So that's three 2s. So the condition is that each number can appear at most twice? Or that consecutive duplicates are allowed only once. Wait, perhaps the problem is that the list must be strictly increasing, but if there are any duplicates (i.e., same number appearing more than once), then it's invalid. But that contradicts the example given. So what's the correct interpretation?

Wait, the problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps the problem is that the list must be sorted in ascending order, and there are no duplicates. Wait, but the example [1,2,2,3,3,4] is allowed. So that's two duplicates of 2 and two of 3. So that's not possible. So maybe the problem's wording is incorrect, and the actual condition is that the list is sorted and has no duplicates. But that can't be because the example given [1,2,2,3,3,4] is allowed. So perhaps the problem's wording is that the list must be sorted in ascending order, and there are no duplicates except for exactly one occurrence. Wait, I'm confused.

Alternatively, perhaps the problem is that the list is sorted in ascending order, but if any number appears more than once, then it's invalid. But that's not the case. Because the example [1,2,2,3,3,4] is allowed. So that's two 2s and two 3s. So that's two duplicates. So the problem's wording must be different. Let me re-read the problem statement.

The problem says: "return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False."

Ah, maybe the problem is that the list must be sorted and have no duplicates. Because if there's more than one duplicate, then return False. Wait, but the example [1,2,2,3,3,4] is considered True. So that's two duplicates. So that's conflicting. So perhaps the problem's wording is that the list must be sorted in ascending order and have no duplicates. But that's not the case. So perhaps the problem is that the list is sorted, but if there are any duplicates (i.e., same number appearing more than once), then return False. But that's not the case. So the example [1,2,2,3,3,4] is allowed. So that's conflicting.

Wait, perhaps the problem's wording is that the list must be sorted in ascending order and have no consecutive duplicates. So, for example, [1,2,2,3] is allowed (no consecutive duplicates?), but [1,2,2,2] is not. Wait, but that's not the case. Let me look at the examples again.

The example is_sorted([1, 2, 2, 3, 3, 4]) returns True. So two 2s and two 3s. So that's allowed. But in the example is_sorted([1, 2, 2, 2, 3, 4]) returns False. So three 2s. So that's not allowed. So the condition is that each number can appear at most twice. But that's not possible. So the problem's condition is that the list is sorted, and that there are no duplicates except for exactly one occurrence. Or perhaps the problem is that the list must be strictly increasing. Wait, but the example [1,2,2,3,3,4] is allowed. So that's not strictly increasing.

Wait, perhaps the problem's condition is that the list is sorted in non-decreasing order, and that each element is unique. But then the example [1,2,2,3,3,4] would not be allowed. So that's conflicting. Therefore, I must have misunderstood the problem.

Let me re-examine the problem's examples and the sample input.

The sample input says:

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True

But according to the problem's condition, if there are more than 1 duplicate of the same number, return False. Wait, perhaps the problem is that the list must be sorted, and that there are no duplicates. But in that case, the example [1,2,2,3,3,4] would be invalid. But according to the sample, it's valid. So this suggests that the problem's condition is different.

Alternatively, maybe the problem is that the list must be sorted in ascending order, and that there are no duplicates. So the example [1,2,2,3,3,4] would not be allowed, but according to the sample it's allowed. So this is conflicting.

Alternatively, perhaps the problem's wording is that the list must be sorted in ascending order and that there are no consecutive duplicates. So for example, [1,2,2,3] is allowed (since duplicates are not consecutive?), but no, that's consecutive duplicates. Wait, no. If the list is sorted, then duplicates must be consecutive. So the problem's condition is that the list is sorted and that there are no duplicates. But that's not the case. So perhaps the problem's condition is that the list is sorted, and that there are no duplicates except for exactly one occurrence. But that's not clear.

Alternatively, perhaps the problem's wording is incorrect, and the actual condition is that the list is sorted in ascending order and that there are no duplicates. But the sample shows that [1,2,2,3,3,4] is allowed. So that's not possible.

Wait, perhaps the problem is that the list must be sorted in ascending order, and that each element is unique. But then the sample [1,2,2,3,3,4] would return False. But according to the sample, it returns True. So this is conflicting.

Hmm, perhaps I need to re-examine the problem statement again.

Problem statement:

"Given a list of numbers, return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False. Assume no negative numbers and only integers."

Wait, the wording is: if the list has more than 1 duplicate of the same number, return False. So, for example, if a number appears more than once, then it's considered a duplicate. So if a number appears two times, that's one duplicate. If it appears three times, that's two duplicates. So the condition is that each number can appear at most once. But that's not possible with the sample input.

But the sample input says that [1,2,2,3,3,4] returns True. Which has two 2s and two 3s. So that would have two duplicates of 2 and two of 3. So according to the problem's wording, that's more than one duplicate. So why is it allowed?

This suggests that the problem's wording is ambiguous, and perhaps the actual condition is that the list is sorted in non-decreasing order and that there are no consecutive duplicates. Or that the list is strictly increasing.

But the sample input [1,2,2,3,3,4] is considered True. So that's not strictly increasing. So the problem must have a different condition.

Wait, perhaps the problem's wording is that the list is sorted in ascending order, and that there are no duplicates. But that's not the case. Because in the sample input, [1,2,2,3,3,4] is allowed. So perhaps the problem's wording is wrong, and the actual condition is that the list is sorted and that there are no consecutive duplicates. Let me think.

If that's the case, then the function should check two things: the list is sorted in non-decreasing order, and that there are no consecutive duplicates. For example, [1,2,2,3] is allowed (since the duplicates are consecutive, but the list is sorted), but [1,2,2,2] would have consecutive duplicates, so it's invalid. Wait, but the sample input [1,2,2,3,3,4] is allowed. So that has two consecutive duplicates. So that would be allowed. But the sample input [1,2,2,2,3,4] returns False. So that's three consecutive duplicates. So the condition is that there are no consecutive duplicates. So the list must be strictly increasing.

But that would make the sample [1,2,2,3,3,4] invalid. So this is conflicting.

Alternatively, maybe the problem is that the list must be sorted and that each element is unique. But then the sample [1,2,2,3,3,4] would be invalid, but according to the sample it's valid. So this is not possible.

Hmm. This is confusing. Let me look at the sample inputs and outputs again.

Sample input 1: [5] returns True. That's a single element, so trivially sorted.

Sample input 2: [1,2,3,4,5] returns True. Strictly increasing.

Sample input 3: [1,3,2,4,5] returns False. Not sorted.

Sample input 4: [1,2,3,4,5,6] returns True. Strictly increasing.

Sample input 5: [1,3,2,4,5,6,7] returns False. Not sorted.

Sample input 6: [1,2,2,3,3,4] returns True. So here, the list is sorted, and there are duplicates. But according to the problem statement, this should return True. So the condition is that the list is sorted, and that there are no more than one duplicate of the same number. Wait, but how?

Wait, the problem says: if the list has more than 1 duplicate of the same number, return False. So for example, if a number appears twice, that's one duplicate. If it appears three times, that's two duplicates. So if the list has more than one duplicate of the same number, return False. So the condition is that each number can appear at most once. But that's not the case for the sample input [1,2,2,3,3,4]. So this suggests that the problem's wording is incorrect. Or perhaps the problem's wording is that the list is sorted and that there are no duplicates (i.e., all elements are unique). But the sample input [1,2,2,3,3,4] would then return False, but the sample says it returns True. So that's not possible.

Alternatively, perhaps the problem's wording is that the list must be sorted and that there are no duplicates except for exactly one occurrence. But that's not clear.

Alternatively, perhaps the problem's condition is that the list is sorted in non-decreasing order, and that there are no duplicates. But then the sample input [1,2,2,3,3,4] would return False, but the sample says it returns True. So this is not possible.

Wait, perhaps the problem's wording is that the list must be sorted, and that there are no consecutive duplicates. So for example, [1,2,2,3] is allowed (since the duplicates are consecutive, but not more than one occurrence). Wait, but that's not the case. The problem's example [1,2,2,3,3,4] would have consecutive duplicates, but the sample says it's allowed. So perhaps the condition is that the list is sorted, and that there are no more than one occurrence of any number. But that's not possible.

I'm stuck. Let me look at the sample inputs and outputs again.

Sample input [1,2,2,3,3,4] returns True. So the list is sorted, and the numbers 2 and 3 appear twice. So the problem's condition must be that the list is sorted in non-decreasing order, and that there are no duplicates. But that's not the case. So what is the correct condition?

Alternatively, perhaps the problem's condition is that the list is sorted in non-decreasing order, and that there are no duplicates except for exactly one occurrence. Wait, but that's not clear. Or perhaps the problem's wording is that the list is sorted, and that there are no duplicates. But that's not the case.

Alternatively, perhaps the problem's wording is incorrect, and the actual condition is that the list is sorted in non-decreasing order, and that there are no consecutive duplicates. So for example, [1,2,2,3] is allowed, but [1,2,2,2] is not. Let me check the sample inputs.

Sample input [1,2,2,3,3,4] would have consecutive duplicates, so it would be allowed. But according to this condition, it would be allowed. So the sample input [1,2,2,2,3,4] would return False, which matches the sample. So this seems to fit.

So the condition is that the list is sorted in non-decreasing order, and that there are no consecutive duplicates. So for example, if the list is sorted, and each element is strictly greater than the previous one, then it's allowed. But if there are two same elements in a row, then it's invalid. Wait, but the sample [1,2,2,3,3,4] would have consecutive duplicates, which would be invalid. But the sample says it returns True. So this is conflicting.

Wait, the sample input [1,2,2,3,3,4] returns True, but according to the condition that there are no consecutive duplicates, this would be invalid. So this suggests that the condition is not about consecutive duplicates.

This is very confusing. Maybe I should look at the examples again and try to derive the condition.

Let me look at the sample inputs and outputs:

Sample input [1, 2, 2, 3, 3, 4] returns True. So this list is sorted, and has duplicates. But the condition is not about consecutive duplicates, since the sample says it's allowed.

Sample input [1, 2, 2, 2, 3, 4] returns False. So this list has three 2s, which is more than one duplicate. So the condition is that each number can appear at most twice?

But then the first sample input has two 2s and two 3s, which is allowed. But the second sample input has three 2s, which is not allowed. So the condition is that each number can appear at most twice. But how to determine that.

But how can we check that? For example, if a number appears exactly twice, it's allowed. But if it appears more than twice, it's not allowed. But that's not clear.

Alternatively, perhaps the problem's condition is that the list is sorted in non-decreasing order and that there are no duplicates (i.e., all elements are unique). But that's not the case for the first sample input. So this is not possible.

Alternatively, perhaps the problem's condition is that the list is sorted and that there are no duplicates, except for exactly one occurrence. But that's not clear.

Alternatively, perhaps the problem's condition is that the list is sorted and that there are no duplicates. But the sample input [1,2,2,3,3,4] would return False, which contradicts the sample.

This suggests that there's a misunderstanding in the problem statement. Perhaps the problem is that the list must be sorted in ascending order, and that each number appears exactly once. But that's not the case for the sample.

Alternatively, perhaps the problem's wording is incorrect, and the actual condition is that the list is sorted and that there are no duplicates. But then the sample input [1,2,2,3,3,4] would return False, but according to the sample it returns True. So this is not possible.

Wait, perhaps the problem's wording is that the list must be sorted in ascending order, and that there are no duplicates. But the sample input [1,2,2,3,3,4] returns True, which suggests that this is not the case. So this is a contradiction.

Alternatively, perhaps the problem's wording is that the list must be sorted in ascending order, and that there are no duplicates except for exactly one occurrence. But this is not clear.

Alternatively, perhaps the problem's condition is that the list is sorted and that each element is strictly greater than the previous one. So the list must be strictly increasing. In that case, the sample input [1,2,2,3,3,4] would return False, but according to the sample it returns True. So that's not possible.

Hmm. I'm stuck. Maybe I should look at the sample inputs and outputs again and try to find a pattern.

Let me list the samples:

Sample 1: [5] → True. Single element, trivial.

Sample 2: [1,2,3,4,5] → True. Strictly increasing.

Sample 3: [1,3,2,4,5] → False. Not sorted.

Sample 4: [1,2,3,4,5,6] → True. Strictly increasing.

Sample 5: [1,3,2,4,5,6,7] → False. Not sorted.

Sample 6: [1,2,2,3,3,4] → True.

Sample 7: [1,2,2,2,3,4] → False.

So, for sample 6, the list is sorted, and has duplicates. But it returns True. For sample 7, the list is sorted, but has more than one duplicate (three 2s), returns False.

So the condition seems to be that the list is sorted in non-decreasing order, and that each number appears at most twice. But how to verify this.

Wait, sample 6 has two 2s and two 3s. So each number appears exactly twice. Sample 7 has three 2s, which is more than two. So the condition is that each number appears at most twice. But how to check this.

But then, what about a list like [1,2,2,3,3,3,4]? That would have three 3s, so it returns False. But how to implement this.

But how to determine that each number appears at most twice. So, for the list to be sorted, and that no number appears more than twice.

But how to check that. For example, for the list [1,2,2,3,3,4], the counts are 1, 2, 2, 1. So each number appears at most twice. So it's allowed.

But for [1,2,2,2,3,4], the count for 2 is 3, which is more than twice. So it returns False.

But how to check that. So the function needs to:

1. Check that the list is sorted in non-decreasing order.

2. Check that no number appears more than twice.

But how to do that.

But wait, the sample input [1,2,2,3,3,4] returns True, which suggests that the condition is that the list is sorted and that there are no duplicates (i.e., each number appears exactly once). But that's not the case.

Alternatively, perhaps the problem's condition is that the list is sorted in non-decreasing order, and that there are no duplicates. But that would make the sample input [1,2,2,3,3,4] return False, but the sample says it returns True. So this is not possible.

I think I need to re-examine the problem statement again.

The problem says: "If list has more than 1 duplicate of the same number, return False."

Ah! So, the wording is: if the list has more than one duplicate of the same number, return False. So, for example, if a number appears once, that's not a duplicate. If it appears twice, that's one duplicate. If it appears three times, that's two duplicates. So if the list has more than one duplicate of the same number, return False. So the condition is that each number can appear at most once. But that's not possible with the sample input.

Wait, but the sample input [1,2,2,3,3,4] has two duplicates of 2 and two of 3. So that's two duplicates for each, which is more than one. So why does it return True?

This suggests that the problem's wording is incorrect, and the actual condition is that the list is sorted and that there are no duplicates. But that's not the case.

Alternatively, perhaps the problem's wording is that if the list has more than one duplicate (i.e., if a number appears more than once), return False. So the list must be strictly increasing. But then the sample input [1,2,2,3,3,4] would return False, but the sample says it returns True. So this is not possible.

At this point, I think I need to look at the sample inputs and outputs to determine the correct condition.

Looking at the sample input [1,2,2,3,3,4] returns True. So it's sorted, and there are duplicates. So the condition must be that the list is sorted, and that the duplicates are allowed as long as they are not consecutive. But that's not the case.

Alternatively, perhaps the problem's condition is that the list is sorted, and that there are no duplicates. But the sample input [1,2,2,3,3,4] would return False. But the sample says it returns True. So this is conflicting.

I think I need to look for the correct interpretation based on the samples.

Sample input [1,2,2,3,3,4] returns True. So the list is sorted, and it has duplicates. So the condition is that the list is sorted, and that there are no duplicates. But that's not the case. So this suggests that the problem's wording is incorrect, and the actual condition is that the list is sorted, and that there are no consecutive duplicates. But how to check that.

Let me think: for the list [1,2,2,3,3,4], the consecutive elements are 1 and 2 (ok), 2 and 2 (duplicates), 2 and 3 (ok), 3 and 3 (duplicates), 3 and 4 (ok). So if the condition is that there are no consecutive duplicates, then this list would return False. But the sample says it returns True. So this is not the case.

Alternatively, perhaps the problem's condition is that the list is sorted, and that there are no duplicates except for exactly one occurrence. But this is not clear.

At this point, I think I need to look at the sample inputs and see what the correct condition is.

Let me look at the sample input [1,2,2,3,3,4] returns True. So the list is sorted, and has duplicates. So the condition is that the list is sorted and that there are no duplicates. But that's not the case.

Wait, perhaps the problem's condition is that the list is sorted and that each element is unique. But then the sample input [1,2,2,3,3,4] would return False. But the sample says it returns True. So this is not possible.

Alternatively, perhaps the problem's condition is that the list is sorted and that there are no more than one duplicate. So, for example, if a number appears twice, that's allowed. But if it appears three times, that's not allowed.

But how to determine that. Let's see:

In sample input [1,2,2,3,3,4], each number appears exactly twice. So that's allowed. But in sample input [1,2,2,2,3,4], the number 2 appears three times, which is more than one duplicate. So it returns False.

But how to check that. So the condition is that for each number in the list, its count is at most two.

So the function needs to:

- Check that the list is sorted in non-decreasing order.

- Check that no number appears more than twice.

But how to implement this.

So, for the list [1,2,2,3,3,4], the counts are 1, 2, 2, 1. So each number appears at most twice. So it's allowed.

For [1,2,2,2,3,4], the count of 2 is 3, which is more than two. So it's not allowed.

But how to check this.

So the steps for the function:

1. Check if the list is sorted in non-decreasing order. If not, return False.

2. Check if any number appears more than twice. If yes, return False.

Otherwise, return True.

But how to implement this.

Let me think about how to check if the list is sorted. For example, for a list lst, we can check if it is equal to its sorted version. But since the list may have duplicates, but the sorted version would have them in order. Wait, but the list is already sorted. So the check is to ensure that for all i, lst[i] <= lst[i+1]. So for i from 0 to len(lst)-2.

Then, for the second part, we need to count the occurrences of each number and ensure that no number appears more than twice.

So, for example, in the list [1,2,2,3,3,4], the counts are 1:1, 2:2, 3:2, 4:1. So all counts are <=2. So return True.

In the list [1,2,2,2,3,4], the count of 2 is 3, so return False.

So, the function would:

- First check if the list is sorted in non-decreasing order.

- Then, check that no element appears more than twice.

So, how to implement this.

Now, let's test this logic against the samples.

Sample input [1,2,2,3,3,4]: sorted, and counts are okay → True.

Sample input [1,2,2,2,3,4]: sorted, but count of 2 is 3 → False.

Sample input [1,2,3,4,5]: sorted, and all counts are 1 → True.

Sample input [5]: sorted, count is 1 → True.

Sample input [1,3,2,4,5]: not sorted → False.

Sample input [1,2,2,3,3,4]: True.

Sample input [1,2,2,2,3,4]: False.

This seems to fit the samples.

So the function should:

Check two conditions:

1. The list is sorted in non-decreasing order.

2. Each element appears at most twice.

Now, how to implement this.

First, check if the list is sorted.

We can do this by iterating through the list and ensuring that each element is less than or equal to the next.

For example:

for i in range(len(lst)-1):

    if lst[i] > lst[i+1]:

        return False

If this loop completes, the list is sorted.

Then, check for duplicates.

We can count the occurrences of each element. For example, using a frequency dictionary.

But since the list is sorted, we can also check for consecutive duplicates.

But for the frequency count, we can do:

from collections import Counter

counts = Counter(lst)

for v in counts.values():

    if v > 2:

        return False

But wait, the sample input [1,2,2,3,3,4] has counts of 2 for 2 and 3, which is allowed. So this would return True.

But the sample input [1,2,2,2,3,4] has a count of 3 for 2, which would return False.

So this logic works.

So the function would be:

def is_sorted(lst):

    # Check if the list is sorted in non-decreasing order

    for i in range(len(lst)-1):

        if lst[i] > lst[i+1]:

            return False

    # Check if any element appears more than twice

    from collections import Counter

    counts = Counter(lst)

    for v in counts.values():

        if v > 2:

            return False

    return True

But wait, what about the case where the list is [1,2,2,3,3,3,4]?

The first check would pass (sorted), and the counts would have 3 for 3, so it would return False.

So this seems to fit.

Let me check the sample inputs.

Sample input [1,2,2,3,3,4] → counts are 1, 2, 2, 1 → all <=2 → return True.

Sample input [1,2,2,2,3,4] → counts for 2 is 3 → return False.

Yes.

Now, let's check the sample input [1,2,2,3,3,4] returns True. Which is correct.

Now, what about a list like [1,1,2,2,3,3,4] → counts are 2 for each, so returns True.

Another case: [1,1,1] → counts is 3 → returns False.

So this logic seems to work.

Now, let's test the sample inputs.

Sample input 1: [5] → sorted, counts is 1 → True.

Sample input 2: [1,2,3,4,5] → sorted, counts all 1 → True.

Sample input 3: [1,3,2,4,5] → not sorted → False.

Sample input 4: [1,2,3,4,5,6] → sorted, counts all 1 → True.

Sample input 5: [1,3,2,4,5,6,7] → not sorted → False.

Sample input 6: [1,2,2,3,3,4] → sorted, counts 2 for 2 and 3 → True.

Sample input 7: [1,2,2,2,3,4] → sorted, counts 3 for 2 → False.

Yes, all samples pass.

Now, what about a list like [1,2,2,3,4,4,4] → sorted, but counts of 4 is 3 → returns False.

Yes.

So this logic works.

So the Python code should implement this.

Now, let's write the code.

But wait, the code needs to import Counter from collections. But the function may be called with a list, and the code must pass all the tests.

Now, the code:

def is_sorted(lst):

    # Check if the list is sorted in non-decreasing order

    for i in range(len(lst)-1):

        if lst[i] > lst[i+1]:

            return False

    # Check if any element appears more than twice

    from collections import Counter

    counts = Counter(lst)

    for v in counts.values():

        if v > 2:

            return False

    return True

Wait, but the code has to import Counter. However, the code may have to import it inside the function, but that's not allowed. Wait, no. In Python, you can't import inside the function in a way that would be allowed. Wait, no, you can import inside the function, but it's better to import at the top. However, the code must be self-contained.

But in the code, the function is_sorted is defined, and inside the function, it uses Counter. So, the code should import collections.Counter at the top.

But the problem says that the code should include any imports it needs. So the code should have the import statement.

So the complete code would be:

import collections

def is_sorted(lst):
    # Check if the list is sorted in non-decreasing order
    for i in range(len(lst)-1):
        if lst[i] > lst[i+1]:
            return False
    # Check if any element appears more than twice
    counts = collections.Counter(lst)
    for v in counts.values():
        if v > 2:
            return False
    return True

Wait, but the code must be in one code block, including any imports. So the code would be:

import collections

def is_sorted(lst):
    for i in range(len(lst)-1):
        if lst[i] > lst[i+1]:
            return False
    counts = collections.Counter(lst)
    for v in counts.values():
        if v > 2:
            return False
    return True

But wait, the sample input [1,2,2,3,3,4] would have counts of 2 for 2 and 3, which is allowed. So the code returns True.

Yes.

Now, let's test the code against the samples.

Sample 1: [5] → returns True.

Sample 2: [1,2,3,4,5] → returns True.

Sample 3: [1,3,2,4,5] → returns False.

Sample 6: [1,2,2,3,3,4] → returns True.

Sample 7: [1,2,2,2,3,4] → returns False.

Yes.

But what about the case where the list is [1,2,2,3,3,3,4] → returns False.

Yes.

So this code should work.

But wait,
```

</details>

**Code that ran:**

```python
import collections

def is_sorted(lst):
    # Check if the list is sorted in non-decreasing order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    # Check if any element appears more than twice
    counts = collections.Counter(lst)
    for v in counts.values():
        if v > 2:
            return False
    return True
```

**Visible-test report:**

```text
PASS    assert is_sorted([5]) == True
PASS    assert is_sorted([1, 2, 3, 4, 5]) == True
PASS    assert is_sorted([1, 3, 2, 4, 5]) == False
3 of 3 visible tests passed
```
