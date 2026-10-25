# HumanEval/126, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/126/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8173. Answer tokens: 95.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_sorted that checks if a list of numbers is sorted in ascending order. But there's an extra condition: if there are more than one duplicate of the same number, it should return False. Let me think about how to approach this.

First, let me understand the problem. The list should be in non-decreasing order, but duplicates are allowed only once. Wait, no. Wait the problem says if there's more than one duplicate, return False. So for example, [1,2,2,3] is allowed because there are exactly two 2s? Wait no, wait the example given says is_sorted([1,2,2,3,3,4]) returns True. Oh, wait the example says that. Let me check the examples again.

Looking at the examples:

The example is_sorted([1, 2, 2, 3, 3, 4]) returns True. Wait, but according to the problem statement, if there's more than one duplicate, return False. Wait, but in this example, there are two 2s and two 3s. So why is it returning True? Wait maybe I misunderstood the problem.

Wait the problem says: If the list has more than 1 duplicate of the same number, return False. Wait, maybe the wording is confusing. Let me read the problem statement again.

The problem says: "If list has more than 1 duplicate of the same number, return False." So, for example, if a number appears more than once, but only once? Wait, maybe the problem is that if there are duplicates, but they are consecutive? Or maybe the problem is that if there are duplicates, but not consecutive? Or maybe the problem is that if there are duplicates in the list, but not exactly once?

Wait, let me look at the examples given. For example, the example is_sorted([1, 2, 2, 3, 3, 4]) returns True. So that list has two 2s and two 3s. But according to the problem statement, that should return True. So that suggests that the problem allows duplicates as long as they are consecutive? Or maybe the problem is that the list is sorted in ascending order, but if there are duplicates, they must be consecutive. Wait, but the problem says that if there are more than one duplicate of the same number, return False. Wait, perhaps the problem is that if a number appears more than once, then it's considered a duplicate. But the example shows that [1,2,2,3,3,4] is considered valid. So that suggests that having duplicates is allowed as long as they are consecutive. Wait, but the problem says that if there's more than one duplicate, return False. Wait maybe the problem is that the list must be strictly increasing, but that's not the case. Because the first example is [5], which is True. Then [1,2,3,4,5] is True. But then in the example [1,2,2,3,3,4], the list is considered True. So that implies that the list can have duplicates, but only if they are consecutive. But how does that fit with the problem statement?

Wait the problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps the problem is that if there are any duplicates (i.e., if a number appears more than once in the list), then it's considered invalid. Wait but that's not the case. Because the example [1,2,2,3,3,4] returns True. So that's conflicting. So perhaps the problem is that the list must be sorted in non-decreasing order, but with the condition that there are no duplicates. Wait but that's not the case. Because the example [1,2,2,3,3,4] returns True. So maybe the problem is that the list is sorted in non-decreasing order, but if there are duplicates, they must be consecutive. Wait, but how does that fit with the problem statement?

Alternatively, perhaps the problem's wording is incorrect. Let me recheck the problem statement.

The problem says: "return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False."

Wait, perhaps the problem is that the list must be sorted in ascending order, and also have no duplicates. Because if there's more than one duplicate, then it's invalid. But in the example [1,2,2,3,3,4], there are two duplicates (the 2 and 3), but the function returns True. So that contradicts that.

Wait, perhaps the problem is that the list is sorted in ascending order, and there are no duplicates. So the list must be strictly increasing. But then the example [1,2,2,3,3,4] would return False, but according to the given example, it returns True. So that's conflicting.

Wait looking back at the examples given in the problem:

Sample input is_sorted([1, 2, 2, 3, 3, 4]) returns True. So according to that, duplicates are allowed. So the problem must not be about duplicates. Then perhaps the problem is that the list is sorted in ascending order, but if there are consecutive duplicates, then it's allowed. But then why the sample [1,2,2,3,3,4] is considered True. But the other sample is [1,2,2,2,3,4] returns False. So that suggests that if a number appears more than once, but not consecutive, then it's invalid. Wait, no. Let me look at the example:

The example says is_sorted([1,2,2,2,3,4]) returns False. So the list is [1,2,2,2,3,4]. So the 2 appears three times. So the problem says that if there's more than one duplicate, return False. Wait, but in this case, the 2 appears three times, which is more than one. So the function returns False. But in the example [1,2,2,3,3,4], the 2 appears twice and 3 appears twice. So why is that allowed?

This is confusing. Let me recheck the problem statement again.

The problem says: "If list has more than 1 duplicate of the same number, return False."

Wait, perhaps the wording is that if there are any duplicates (i.e., if a number appears more than once), then return False. But that can't be because the example [1,2,2,3,3,4] returns True. So that's not possible.

Alternatively, perhaps the problem is that the list must be strictly increasing. So that duplicates are not allowed. But then the example [1,2,2,3,3,4] would return False, but according to the given example, it returns True. So that's not the case.

Wait perhaps the problem's wording is that if there are any duplicates (i.e., if the list has more than one occurrence of a number), then return False. But then the example [1,2,2,3,3,4] would return False, but according to the problem's example, it returns True. So that's conflicting.

Wait maybe the problem statement is that the list must be sorted in ascending order, and if there are any duplicates (i.e., if a number appears more than once), then return False. But the sample [1,2,2,3,3,4] returns True. Which contradicts that. So there's something wrong here.

Alternatively, perhaps the problem statement is that the list must be sorted in ascending order, and also that there are no duplicates. But the sample [1,2,2,3,3,4] returns True. Which would not fit that.

Wait, maybe the problem statement's wording is incorrect. Let me look at the sample input and output again.

The sample input is:

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True

is_sorted([1, 2, 2, 2, 3, 4]) ➞ False

So the first case has two 2s and two 3s. The second case has three 2s. So the problem is that the list must be sorted, and if any number appears more than once (i.e., duplicates), then return False. But in the first case, the 2 appears twice. So why is that allowed?

Ah, maybe the problem is that the list must be sorted and have no duplicates. But in that case, the first example would be invalid. So that's not possible.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order, but if any number appears more than once, then it's invalid. But that's not the case.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order, and there are no consecutive duplicates. So, for example, [1,2,2,3] is allowed (no consecutive duplicates?), but [1,2,2,2] is not allowed. Wait, but that's not the case. Because the first example [1,2,2,3,3,4] is allowed. So in that case, the list has consecutive duplicates. So that's not the case.

Wait maybe the problem is that the list is sorted, and if there are any duplicates (i.e., any occurrence of the same number more than once), then return False. But in that case, the first example would return False. But according to the problem, it returns True. So that's not possible.

I'm confused. Let me re-examine the problem statement again.

The problem says: "return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False."

Ah, perhaps the wording is that if there are more than one occurrence of the same number, then return False. So, for example, if a number appears two or more times, return False. But then the sample [1,2,2,3,3,4] would return False, but according to the problem's example, it returns True. So that's conflicting.

Alternatively, maybe the problem is that the list must be sorted in ascending order and have no duplicates. So the list must be strictly increasing. But in that case, the sample [1,2,2,3,3,4] would return False. But according to the example, it returns True. So that's not possible.

Wait, perhaps the problem's wording is that if the list has more than one duplicate of the same number, meaning that the same number appears more than once. So for example, if a number appears exactly once, it's okay. If it appears two or more times, then it's invalid. But that would mean that the sample [1,2,2,3,3,4] is invalid, but according to the problem, it's valid. So this is conflicting.

Alternatively, perhaps the problem's wording is that if there are consecutive duplicates. For example, [1,2,2,3] is allowed, but [1,2,2,2] is not. But then the sample [1,2,2,3,3,4] is allowed, and [1,2,2,2,3,4] is not. Which matches the examples. So that's possible.

So the problem is that the list must be sorted in ascending order, and also have no consecutive duplicates. So, for example, [1,2,2,3] is allowed, but [1,2,2,2] is not. But how does that fit with the sample [1,2,2,3,3,4] returning True? Because in that case, the 2 and 3 are consecutive duplicates. So that's allowed. So the problem is that the list is sorted in non-decreasing order, and there are no consecutive duplicates. So, the list must be strictly increasing. Wait, but that would mean that the sample [1,2,2,3,3,4] is invalid. But according to the example, it's valid. So that's not possible.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order, and if there are any duplicates (not necessarily consecutive), then return False. But that can't be because the sample [1,2,2,3,3,4] would have duplicates, so it should return False. But according to the example, it returns True. So that's not possible.

This is really confusing. Let me look at the sample inputs and outputs again.

Sample 1: is_sorted([5]) returns True. That's trivial.

Sample 2: [1,2,3,4,5] returns True. That's strictly increasing.

Sample 3: [1,3,2,4,5] returns False. Because it's not sorted.

Sample 4: [1,2,3,4,5,6] returns True.

Sample 5: [1,3,2,4,5,6,7] returns False.

Sample 6: [1,2,2,3,3,4] returns True.

Sample 7: [1,2,2,2,3,4] returns False.

So the sample 6 and 7 show that if there are two duplicates, it's allowed, but if three, it's not. So the condition is that a number can appear at most twice in the list. Wait, but sample 6 has two 2s and two 3s. So that's allowed, but sample 7 has three 2s, which is not allowed. So the condition is that no number appears more than twice. But why?

But how does that fit with the problem statement? The problem says "If list has more than 1 duplicate of the same number, return False." So perhaps the wording is that if a number appears more than once (i.e., at least two times), then return False. But sample 6 has two 2s and two 3s, which would be invalid, but according to the example, it's valid. So that's conflicting.

Alternatively, maybe the problem is that the list must be sorted and have no duplicates except for exactly one occurrence of a number. Wait, but that doesn't fit either.

Alternatively, perhaps the problem statement is incorrect and the actual condition is that the list is sorted in non-decreasing order and has no consecutive duplicates. That is, the list is strictly increasing. But that would make the sample 6 invalid, which it isn't.

Wait, maybe the problem is that the list must be sorted in non-decreasing order and there are no duplicates. So the list must be strictly increasing. But then sample 6 would be invalid, but according to the example, it is valid. So that's not possible.

Alternatively, maybe the problem is that the list is sorted in non-decreasing order and there are no duplicates except for exactly one pair of duplicates. But that's not clear.

Alternatively, perhaps the problem statement has a typo. Maybe it's supposed to say that if there are more than one consecutive duplicates, return False. For example, in sample 6, the list is [1,2,2,3,3,4]. The 2 and 3 appear twice consecutively. So maybe the condition is that there are no consecutive duplicates. So the list must be strictly increasing. But then sample 6 would return False, which it doesn't.

But the sample 6 returns True. So that's not the case.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order and there are no duplicates. But that would mean that the sample 6 is invalid. So that's not possible.

Hmm. Maybe I should look at the sample inputs and outputs again, and think about what the actual condition is.

Let me think about the sample 6 and 7:

Sample 6: [1,2,2,3,3,4] → True.

Sample 7: [1,2,2,2,3,4] → False.

So what's the difference between these two? In sample 6, the duplicates are consecutive. So the list is sorted and has consecutive duplicates. But sample 7 has three 2s, which is more than two consecutive duplicates. So perhaps the condition is that there can be at most one duplicate (i.e., exactly one pair of duplicates), but that doesn't fit with the sample 6.

Alternatively, perhaps the problem is that the list is sorted, and there are no duplicates. But sample 6 has duplicates, so that's not possible.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order and has no duplicates except for exactly one pair. But that's not clear.

Alternatively, perhaps the problem statement's wording is incorrect, and the actual condition is that the list is sorted and has no duplicates. But then sample 6 would return False, which it doesn't. So that's not possible.

Alternatively, perhaps the problem statement is that the list is sorted in non-decreasing order, and any duplicates must be consecutive. So, for example, [1,2,2,3] is allowed, but [1,2,3,2] is not. But then sample 6 is allowed, sample 7 is not. But how does that fit with the sample 6?

Wait, the sample 6 is [1,2,2,3,3,4]. This is sorted, and the duplicates are consecutive. So that's allowed. But the sample 7 has three 2s, which are consecutive. So why is that not allowed? According to the sample, it returns False. So perhaps the condition is that there can be at most one pair of duplicates. So if a number appears more than two times, it's invalid. But that's not clear.

Alternatively, maybe the problem is that the list must be strictly increasing. But sample 6 is not strictly increasing. So that's not possible.

At this point, I think I need to find a way to interpret the sample inputs and outputs to determine the correct condition.

Let me think about the sample 6 and 7 again.

Sample 6: [1,2,2,3,3,4] → True.

Sample 7: [1,2,2,2,3,4] → False.

So what is the difference between these two? In sample 6, the duplicates are two times, and in sample 7, three times. So the condition seems to be that a number can appear at most two times in the list. So, if any number appears three or more times, return False. But how does that fit with the sample 6?

Wait, in sample 6, the 2 appears twice and the 3 appears twice. So that's allowed. But the problem says "if list has more than 1 duplicate of the same number, return False." So perhaps the problem is that if a number appears more than once (i.e., at least two times), then return False. But sample 6 has two 2s and two 3s, which would return False. But according to the sample, it returns True. So that's conflicting.

This is very confusing. Maybe I should look at the problem's examples again.

The problem says:

Examples:

is_sorted([5]) ➞ True → trivial case.

is_sorted([1, 2, 3, 4, 5]) ➞ True → strictly increasing.

is_sorted([1, 3, 2, 4, 5]) ➞ False → not sorted.

is_sorted([1, 2, 3, 4, 5, 6]) ➞ True → strictly increasing.

is_sorted([1, 3, 2, 4, 5, 6, 7]) ➞ False → not sorted.

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True → sorted, but with duplicates.

is_sorted([1, 2, 2, 2, 3, 4]) ➞ False → sorted, but with three 2s.

So the key is that the list must be sorted in non-decreasing order, and if any number appears more than once, then it's allowed only if it appears exactly once. Or wait, no. Because in sample 6, the 2 appears twice and 3 appears twice. So that's allowed.

Wait, but how can that be? If the list is sorted, and has duplicates, but the duplicates are not consecutive? For example, [1,2,3,2,4], which is not sorted. But the sample 6 is sorted and has consecutive duplicates.

So perhaps the problem is that the list is sorted in non-decreasing order, and there are no duplicates. But sample 6 has duplicates. So that's not possible.

Alternatively, maybe the problem is that the list is sorted in non-decreasing order, and any duplicates must be consecutive. So for example, the list [1,2,2,3,3,4] is allowed, but [1,2,3,2,4] is not. But how does that fit with the sample 7?

Sample 7 is [1,2,2,2,3,4]. This is sorted and has consecutive duplicates. But the sample returns False. So why?

Maybe the condition is that the list is sorted and has no duplicates. But sample 6 has duplicates, so that's not possible.

At this point, I'm stuck. Maybe I should try to find a pattern in the samples.

Let me think: what is the condition that the samples are passing?

Sample 6: [1,2,2,3,3,4] → True.

Sample 7: [1,2,2,2,3,4] → False.

What's the difference between these two? In sample 6, each number appears at most twice. In sample 7, the 2 appears three times. So perhaps the condition is that no number appears more than twice. But then why sample 6 is allowed. But how does that fit with the problem statement?

The problem says: "If list has more than 1 duplicate of the same number, return False."

Wait, perhaps the wording is that if a number appears more than once (i.e., two or more times), then return False. But sample 6 has numbers that appear twice, and it returns True. So that's conflicting.

Alternatively, maybe the problem's wording is that if a number appears more than once (i.e., two or more times), then it's considered a duplicate. But the function should return False if there are any such duplicates. But sample 6 would return False, but according to the example, it returns True.

This is very confusing. Maybe I should look for the actual condition that the sample is passing.

Let me think about what the function should return for the sample 6 and 7.

Sample 6: [1,2,2,3,3,4] → True. So the list is sorted, and the duplicates are allowed. So the condition is not about duplicates at all. So perhaps the problem statement is incorrect, and the actual condition is that the list is sorted in non-decreasing order and has no duplicates. But that's not the case.

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order, and there are no duplicates. So the function should return True only if the list is strictly increasing. But sample 6 would return False, but according to the example, it returns True. So that's not possible.

At this point, I think I need to look for the correct condition that would make the samples pass. Let's think about what the samples are testing.

Sample 6: [1,2,2,3,3,4] returns True. So the list is sorted, and there are duplicates. So the condition is not about duplicates.

Sample 7: [1,2,2,2,3,4] returns False. So the list is sorted, but has three 2s. So what is the difference between sample 6 and 7?

Maybe the condition is that the list is sorted, and there are no consecutive duplicates. So, for example, [1,2,2,3] is not allowed, but [1,2,3,4] is allowed. But sample 6 has consecutive duplicates and returns True, so that's not possible.

Alternatively, the condition is that the list is sorted and has no duplicates except for exactly one pair of duplicates. But sample 6 has two pairs, which would be allowed. But sample 7 has three duplicates, which is not allowed. So that's possible.

But how to implement that?

Alternatively, perhaps the problem is that the list is sorted in non-decreasing order and has no duplicates. But sample 6 has duplicates, so that's not possible.

Alternatively, maybe the problem statement is incorrect, and the actual condition is that the list is sorted and has no duplicates. So, the function should return True only if the list is strictly increasing. But in that case, sample 6 would return False, which it doesn't. So that's not possible.

Alternatively, perhaps the problem statement is that the list is sorted in non-decreasing order and has no duplicates. So the function should return True if the list is sorted and all elements are unique. But sample 6 has duplicates, so it returns False. But according to the example, it returns True. So that's not possible.

At this point, I think I need to find a way to write the function that passes the given samples, even if I don't fully understand the problem statement.

Let me think about what the samples are requiring.

Sample 6: [1,2,2,3,3,4] returns True. So the list is sorted, and has duplicates. Sample 7: [1,2,2,2,3,4] returns False. So the list is sorted, but has three 2s. So the difference between the two is the number of duplicates.

So perhaps the condition is that the list is sorted in non-decreasing order, and any number can appear at most twice.

If that's the case, then for sample 6, each number appears at most twice (2 appears twice, 3 appears twice), so it's allowed. For sample 7, 2 appears three times, which is not allowed.

But how does this fit with the problem statement? The problem says "If list has more than 1 duplicate of the same number, return False." So perhaps the wording is that if a number appears more than once (i.e., at least two times), then return False. But that would mean sample 6 returns False, which it doesn't. So that's not possible.

Alternatively, the problem statement may have a typo, and the actual condition is that the list is sorted and has no duplicates. But sample 6 would return False, which it doesn't. So that's not possible.

Alternatively, perhaps the problem statement is that the list is sorted in non-decreasing order, and there are no consecutive duplicates. So, the list must be strictly increasing. But sample 6 has consecutive duplicates, so it would return False, but according to the example, it returns True. So that's not possible.

At this point, I think the only way to proceed is to find a pattern that fits all the samples.

Let me think about the samples:

Sample 6: [1,2,2,3,3,4] → True.

Sample 7: [1,2,2,2,3,4] → False.

So the difference between these two is the number of occurrences of 2. In sample 6, 2 occurs twice, in sample 7, three times. So the condition might be that each number can appear at most twice.

But how to verify this with other samples.

Another sample: [1,2,3,4,5,6] → True. All numbers appear once. So allowed.

Another sample: [1,2,2,3,4] → allowed? If the condition is that each number can appear at most twice, then yes. But the problem statement says that [1,2,2,3,3,4] is allowed. So that's allowed.

But what about [1,2,3,2,4] → not sorted, so returns False.

So the function needs to check two things: the list is sorted in non-decreasing order, and no number appears more than twice.

But how to implement this.

So the steps for the function would be:

1. Check if the list is sorted in non-decreasing order.

2. Check that no number appears more than twice.

If both conditions are met, return True; else, False.

Let me test this against the samples.

Sample 6: [1,2,2,3,3,4] → sorted, and each number appears at most twice → True.

Sample 7: [1,2,2,2,3,4] → sorted, but 2 appears three times → False.

Sample 2: [1,2,3,4,5] → sorted, no duplicates → True.

Sample 1: [5] → sorted, no duplicates → True.

Sample 3: [1,3,2,4,5] → not sorted → False.

Sample 4: [1,2,3,4,5,6] → sorted, no duplicates → True.

Sample 5: [1,3,2,4,5,6,7] → not sorted → False.

So this seems to fit all the samples.

So the problem statement's wording is possibly incorrect, and the actual condition is that the list is sorted in non-decreasing order, and no number appears more than twice.

But how to explain the problem statement's wording: "If list has more than 1 duplicate of the same number, return False."

Maybe the wording is incorrect, and it should say "If list has more than two occurrences of the same number, return False."

In that case, the function should check for that.

So the approach is:

- Check if the list is sorted in non-decreasing order.

- Check that each number appears at most twice.

But how to implement this.

So, the code would:

First, check if the list is sorted. How to do that? For example, compare each element with the next one. If any element is greater than the next, return False.

Then, check for duplicates. For this, we can count the occurrences of each number. If any number appears more than twice, return False.

So the code would be:

def is_sorted(lst):
    # Check if the list is sorted in non-decreasing order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    # Check for duplicates
    from collections import Counter
    counts = Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
    return True

Wait, but let's test this against the samples.

Sample 6: [1,2,2,3,3,4] → counts are {1:1, 2:2, 3:2, 4:1} → all counts ≤ 2 → returns True. Correct.

Sample 7: [1,2,2,2,3,4] → counts for 2 is 3 → returns False. Correct.

Sample 2: [1,2,3,4,5] → all counts 1 → returns True. Correct.

Sample 1: [5] → count is 1 → returns True.

Sample 3: [1,3,2,4,5] → not sorted → returns False. Correct.

Sample 4: [1,2,3,4,5,6] → sorted, counts all 1 → returns True.

Sample 5: [1,3,2,4,5,6,7] → not sorted → returns False.

This seems to fit all the samples.

But the problem statement says that the function should return False if there are more than one duplicate of the same number. So the wording is confusing, but this approach passes the samples.

So this must be the correct approach.

Now, I need to implement this in Python.

But wait, the problem says "if list has more than 1 duplicate of the same number, return False." So perhaps the wording is that if a number appears more than once, return False. But in that case, the sample 6 would return False, which it doesn't. So the problem statement's wording is likely incorrect, and the actual condition is that no number appears more than twice.

Thus, the code as described above would be correct.

Now, the code:

Implement the two checks.

But wait, for the first check, the list is sorted in non-decreasing order. So for example, [1,2,2,3] is sorted, and the counts are okay.

But what about [1,2,2,2] → counts are 3 → returns False.

So the code would work.

Now, the code.

But for the first check, we can iterate through the list and check if each element is <= the next.

Then, for the counts, we can use a Counter.

But in Python, for small lists, this is acceptable.

Now, code:

def is_sorted(lst):
    # Check if the list is sorted in non-decreasing order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    # Check for duplicates (each number appears at most twice)
    from collections import Counter
    counts = Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
    return True

Wait, but in the sample [1,2,2,3,3,4], the counts are 1, 2, 2, 1. So all counts are <= 2. So returns True.

Yes.

But what about [1,2,2,3,3,3]? Then counts for 3 is 3 → returns False.

Yes.

Now, the code would pass all the samples.

But the problem statement says that the function should return False if there are more than one duplicate of the same number. But this code returns True for [1,2,2,3,3,4], which has two duplicates. So the problem statement's wording is likely incorrect, and the actual condition is that each number can appear at most twice.

But given the samples, this code is correct.

Now, let's test the code against the samples.

Sample 1: [5] → returns True. Correct.

Sample 2: [1,2,3,4,5] → returns True. Correct.

Sample 3: [1,3,2,4,5] → not sorted → returns False. Correct.

Sample 6: [1,2,2,3,3,4] → returns True. Correct.

Sample 7: [1,2,2,2,3,4] → returns False. Correct.

Yes.

Now, the code should be correct.

But what about the case where the list is sorted, but has a number appearing exactly twice? Like [1,2,2,3]. This would return True.

Yes, which is correct according to the samples.

So the code is correct.

Now, the code needs to be written.

But the code uses the Counter from collections. So we need to import it.

But in the code, the function is_sorted is defined, and the imports should be inside the function? No, the imports should be at the top. But in Python, the code can't have import inside the function. So the code should import collections.Counter.

But the code is written as:

def is_sorted(lst):
    ...
    from collections import Counter
    ...

But that's not allowed. Because the import statement is inside the function. So that's invalid.

So the code should import Counter at the top.

But the user's code must be self-contained. So the code should include the necessary imports.

So the complete code would be:

import collections

def is_sorted(lst):
    # Check if the list is sorted in non-decreasing order
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    # Check for duplicates (each number appears at most twice)
    counts = collections.Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
    return True

But wait, what about the case where the list is empty? Well, the problem says that the list has no negative numbers and only integers. But the sample includes [5], which is allowed.

But the function should handle empty lists? Well, the problem says nothing about it. But the code would return True for an empty list, since it's trivially sorted and has no duplicates. But the problem examples don't cover that.

But the code should work as per the problem's examples.

Now, let's check the sample [1,2,2,3,3,4]. The code would return True.

Yes.

So this should be the correct solution.

But let me check the sample [1,2,2,3,3,3]. The code would return False, which is correct.

Another sample: [1,2,2,3,3,4,4,4] → counts for 4 is 3 → returns False.

Yes.

So the code is correct.

Now, the code needs to be written, including any imports.

So the complete code would be:

import collections

def is_sorted(lst):
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    counts = collections.Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
    return True

But wait, the problem says that the list has no negative numbers and only integers. But that doesn't affect the code.

Now, let's test the code against the sample inputs.

Sample 6: [1,2,2,3,3,4] → returns True. Correct.

Sample 7: [1,2,2,2,3,4] → returns False. Correct.

Yes.

So this should be the correct solution.
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
    # Check that no number appears more than twice
    counts = collections.Counter(lst)
    for count in counts.values():
        if count > 2:
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
