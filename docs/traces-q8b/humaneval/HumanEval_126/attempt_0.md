# HumanEval/126, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/126/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 7386. Answer tokens: 91.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called is_sorted that checks if a list of numbers is sorted in ascending order. But there's an extra condition: if there are more than one duplicate of the same number, it should return False. Let me think about how to approach this.

First, the list must be in non-decreasing order. But wait, the problem says "ascending order", but the examples include duplicates. Wait, looking at the examples: for instance, [1,2,2,3,3,4] returns True. Oh, right, because the duplicates are allowed as long as they are consecutive. Wait, but the second condition says if there are more than one duplicate of the same number, return False. Wait, maybe I need to clarify the problem.

Wait the problem says: If the list has more than 1 duplicate of the same number, return False. Wait, what's considered a duplicate here? For example, in the example [1,2,2,3,3,4], it returns True. So that's two 2s and two 3s. But according to the problem statement, that's allowed? Wait, the problem says that if there are more than one duplicate of the same number, return False. Wait, maybe the wording is confusing. Let me read the problem again.

The problem says: "If list has more than 1 duplicate of the same number, return False." So, for example, if a number appears more than once, but only once? Wait, maybe the problem is that if there are duplicates, but more than one occurrence. Wait, maybe the condition is that the list must be strictly increasing. Because if there's any duplicate, then it's not allowed. But wait the example [1,2,2,3,3,4] returns True. Wait that's conflicting. Let me check the example again.

Looking at the examples:

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True

But according to the problem's condition, if there are more than one duplicate of the same number, return False. Wait, but in this example, there are two 2s and two 3s. So according to the problem statement, this should return False. But the example says it returns True. So there's a contradiction here. Wait, perhaps I misunderstood the problem statement.

Wait the problem says: "If list has more than 1 duplicate of the same number, return False." So maybe the condition is that the list must not have any duplicates. Wait, but that would make the example [1,2,2,3,3,4] return False, but according to the sample input, it returns True. So that's conflicting. Therefore, I must have misunderstood the problem.

Wait looking back at the examples:

The example is_sorted([1,2,2,3,3,4]) returns True. So according to the problem's conditions, this is allowed. So the problem's condition must be that the list is sorted in ascending order, but there can be duplicates as long as they are consecutive. Wait but the problem says "if list has more than 1 duplicate of the same number, return False." Wait maybe the problem is that if a number appears more than once, but not consecutively. Wait, perhaps the problem is that the list must be strictly increasing. But the sample input [1,2,2,3,3,4] is not strictly increasing. So that's confusing.

Wait maybe the problem's wording is incorrect. Let me re-examine the problem statement.

The problem says: return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False. So, perhaps the problem is that the list must be sorted in ascending order, and also that all elements are unique. Wait, but then the sample input [1,2,2,3,3,4] would return False, but the example says it returns True. So that's not possible.

Alternatively, perhaps the problem's wording is that if there are multiple duplicates (i.e., more than one occurrence of the same number), then return False. But that would mean that the list must have all unique elements. But in the example [1,2,2,3,3,4], there are duplicates, so the function should return False, but according to the sample input, it returns True. So that's conflicting.

Wait perhaps the problem statement is that the list must be sorted in ascending order and have no duplicates. But that's not the case. Because the sample input [1,2,2,3,3,4] returns True. So that's not possible. Therefore, I must have misunderstood the problem statement.

Wait let me re-read the problem statement again.

Problem statement:

"Given a list of numbers, return whether or not they are sorted in ascending order. If list has more than 1 duplicate of the same number, return False. Assume no negative numbers and only integers."

Wait, perhaps the problem is that the list must be sorted in ascending order, and also that there are no duplicates. Because if there are duplicates, then that's considered as having more than one occurrence. But the sample input [1,2,2,3,3,4] returns True, which would not fit that. Therefore, perhaps the problem statement is that the list must be sorted in ascending order and strictly increasing. But that's not possible because the sample input [1,2,2,3,3,4] would return False, but according to the example, it returns True. So this is confusing.

Alternatively, perhaps the problem statement is that the list is sorted in ascending order, and there are no consecutive duplicates. So, for example, if a number appears more than once, but not consecutively, then it's allowed. But that's not clear.

Wait looking at the sample input:

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True

But according to the problem's condition, if there are more than one duplicate of the same number, return False. So in this case, the list has two 2s and two 3s. So according to the problem statement, this should return False. But the sample says it returns True. Therefore, the problem statement's wording must be different. So perhaps the problem is that the list is sorted in ascending order, and there are no duplicates. But then the sample input [1,2,2,3,3,4] would return False. But the sample says it returns True. Therefore, there's a contradiction here.

Alternatively, perhaps the problem statement is that the list is sorted in ascending order, and each element is unique. But that's not the case. Because the sample input [1,2,2,3,3,4] returns True, but there are duplicates.

Wait maybe the problem statement's wording is incorrect. Let me check the sample inputs again.

Looking at the sample input:

is_sorted([1, 2, 2, 3, 3, 4]) ➞ True

is_sorted([1, 2, 2, 2, 3, 4]) ➞ False

So in the first case, there are two duplicates (2 and 3), but the function returns True. In the second case, there are three 2s, and returns False. So the condition seems to be that if a number appears more than once, but not consecutively, then it's allowed. Wait no. Because in the first case, the duplicates are consecutive. So perhaps the problem is that the list must be sorted, and there are no consecutive duplicates. Wait that would make sense.

Wait for example, in the first case, the list [1,2,2,3,3,4] has consecutive duplicates. But according to the sample input, it returns True. So that's not possible. So what's the pattern here?

Looking at the sample inputs:

The sample input [1,2,2,3,3,4] returns True. But [1,2,2,2,3,4] returns False. So the condition seems to be that each number can appear at most twice. But that's not the case. Because the first case has two 2s and two 3s, and returns True. The second case has three 2s and returns False. So the condition is that each number can appear at most two times. But that's not what the problem says. The problem says "if list has more than 1 duplicate of the same number, return False." So perhaps the problem is that if a number appears more than once, then it's considered as having duplicates. But that would mean that the list must have all unique elements. Which contradicts the sample input.

So I think there's a misunderstanding here. Let me read the problem statement again.

The problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps the wording is that if there are two or more duplicates of the same number. For example, if a number appears two times, that's considered as having more than one duplicate. But that would mean that the list must have all unique elements. But the sample input [1,2,2,3,3,4] returns True, which contradicts that.

Alternatively, maybe the problem is that if there are multiple duplicates (i.e., the same number appears more than once), but not in a consecutive way. For example, [1,2,2,3,4,4] would be allowed, but [1,2,2,2,3,4] would not. But how to determine that.

Alternatively, perhaps the problem is that the list must be sorted in ascending order, and there are no duplicates. But then the sample input [1,2,2,3,3,4] would return False, which is not the case.

This is very confusing. Let me look at the examples again.

Let me look at the examples:

Sample 1: [5] returns True. That's a single element, so no duplicates.

Sample 2: [1,2,3,4,5] returns True. All unique.

Sample 3: [1,3,2,4,5] returns False. Because it's not sorted.

Sample 4: [1,2,3,4,5,6] returns True. All unique.

Sample 5: [1,3,2,4,5,6,7] returns False. Not sorted.

Sample 6: [1,2,2,3,3,4] returns True. So here, the list is sorted, and there are duplicates. But the function returns True.

Sample 7: [1,2,2,2,3,4] returns False. So here, there are three 2s. So the function returns False.

So the condition seems to be that the list is sorted in ascending order, and each number can appear at most two times. But how does that fit with the problem statement?

The problem statement says: "If list has more than 1 duplicate of the same number, return False." So maybe "more than one duplicate" refers to more than one occurrence of the same number. For example, if a number appears two times, that's one duplicate. If it appears three times, that's two duplicates. So the problem is that if a number appears more than once (i.e., two or more times), then return False. But that would make the sample input [1,2,2,3,3,4] return False, but the sample says it returns True. So that's not possible.

Alternatively, perhaps the problem is that the list is sorted, and there are no duplicates. But sample input 6 returns True. So that's not possible.

Alternatively, maybe the problem is that the list is sorted, and there are no consecutive duplicates. Wait, but sample input 6 has consecutive duplicates. Let me see:

In sample input 6: [1,2,2,3,3,4]. The duplicates are consecutive. So if the condition is that there are no consecutive duplicates, then this sample would return False, but the sample says it returns True. So that's not possible.

Alternatively, maybe the problem is that the list is sorted, and there are no duplicates. But sample input 6 returns True. So that's not possible.

This is very confusing. Let me look at the sample inputs again and try to find a pattern.

Sample 6: [1,2,2,3,3,4] returns True. So the list is sorted, and there are duplicates, but the function returns True.

Sample 7: [1,2,2,2,3,4] returns False. So the list is sorted, but has three 2s, and returns False.

So the condition seems to be that the list is sorted in ascending order, and each number can appear at most twice. But how does that fit with the problem statement's wording?

The problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps "more than one duplicate" means that the same number appears more than once. So if a number appears two times, it's considered as one duplicate. But the problem says that if there are more than one duplicate, then return False. So that would mean that if a number appears more than once, then return False. But that contradicts the sample input 6.

Alternatively, perhaps the problem statement is written incorrectly, and the actual condition is that the list must be sorted and strictly increasing (i.e., no duplicates). But then sample input 6 would return False. But the sample says it returns True. So that's not possible.

Alternatively, perhaps the problem statement is that the list is sorted, and there are no consecutive duplicates. So the list must be strictly increasing. But sample input 6 has consecutive duplicates, but returns True. So that's not possible.

Hmm. Maybe I should look at the sample inputs and try to find what the actual condition is. Let me think:

Sample 6: [1,2,2,3,3,4] returns True. So the list is sorted, and the duplicates are allowed. But in sample 7, [1,2,2,2,3,4] returns False. So the difference between sample 6 and 7 is that sample 6 has two duplicates (two 2s and two 3s), and sample 7 has three 2s. So perhaps the condition is that each number can appear at most twice. But how to determine that from the problem statement.

The problem statement says: "If list has more than 1 duplicate of the same number, return False." So maybe the wording is that if a number appears more than once (i.e., two or more times), then return False. But that would make sample 6 return False, which is not the case. So there's a contradiction here.

Alternatively, perhaps the problem statement is that if there are multiple duplicates (i.e., more than one occurrence of the same number), then return False. But this is not possible. 

Alternatively, perhaps the problem statement's wording is incorrect, and the actual condition is that the list must be sorted, and there are no duplicates. But then sample input 6 would return False. But according to the sample, it returns True. So that's not possible.

This is very confusing. Let me try to think of what the actual condition is based on the samples.

The samples that return True are:

- [5] → True (single element)
- [1,2,3,4,5] → True (all unique)
- [1,2,2,3,3,4] → True (duplicates allowed?)
- [1,2,3,4,5,6] → True (all unique)
- [1,2,2,3,3,4] → True
- [1,2,2,2,3,4] → False

So the difference between sample 6 and 7 is that sample 6 has two 2s and two 3s, but sample 7 has three 2s. So the condition seems to be that each number can appear at most twice. But how to derive this from the problem statement.

The problem says: "If list has more than 1 duplicate of the same number, return False." So maybe the wording is that if a number appears more than once (i.e., two or more times), then return False. But in that case, sample 6 would return False, but according to the sample it returns True. So this is not possible.

Alternatively, perhaps the problem statement means that if a number appears more than once, but not consecutively. But that would not fit with the sample.

Alternatively, maybe the problem statement is that the list must be sorted, and there are no duplicates. But the sample input 6 contradicts this.

Alternatively, perhaps the problem statement is that the list is sorted and has no consecutive duplicates. For example, [1,2,2,3,3,4] has consecutive duplicates, so returns True. But that's not possible because the sample input 6 returns True.

Wait, maybe the problem statement is that the list is sorted, and there are no duplicates. But sample input 6 returns True, which would be a contradiction. 

Alternatively, perhaps the problem statement is that the list is sorted in ascending order, and there are no duplicates. But the sample input 6 returns True, which would be a contradiction.

At this point, I think the problem statement may have a mistake in the wording. Let's look at the sample input 6 and 7 again.

Sample 6: [1,2,2,3,3,4] returns True. So the list is sorted and has duplicates. But sample 7: [1,2,2,2,3,4] returns False. So the difference is that in sample 6, the duplicates are in pairs, but in sample 7, there are three 2s. So the condition may be that each number can appear at most twice. So the function should return True if the list is sorted and each number appears at most twice.

But how to reconcile this with the problem statement's wording. The problem says: "If list has more than 1 duplicate of the same number, return False." So if a number appears two times, that's one duplicate. If it appears three times, that's two duplicates. So the condition would be that if a number appears more than one time (i.e., two or more), then return False. But that would make sample 6 return False, which contradicts the sample.

So this is very confusing. Maybe the problem statement is that the list is sorted and has no duplicates. But then sample 6 would return False, but according to the sample it returns True. So this is not possible.

Alternatively, maybe the problem statement is that the list is sorted and has no consecutive duplicates. So the list must be strictly increasing. But sample input 6 has consecutive duplicates and returns True. So that's not possible.

Hmm. Maybe the problem statement's wording is incorrect. Perhaps the actual condition is that the list is sorted in ascending order and has no duplicates. But then sample 6 would return False, but according to the sample it returns True. So that's not possible.

Alternatively, perhaps the problem statement is that the list is sorted, and there are no duplicates. But sample 6 is allowed. So I'm stuck.

Maybe I should look for the pattern in the samples and try to find what the actual condition is.

The samples that return True are:

- [5] → True
- [1,2,3,4,5] → True
- [1,2,2,3,3,4] → True
- [1,2,3,4,5,6] → True
- [1,2,2,3,3,4] → True (again)
- [1,3,2,4,5] → False (not sorted)
- [1,2,2,2,3,4] → False

So the only condition that seems to be checked is whether the list is sorted in ascending order. But in sample 6, the list is sorted but has duplicates. So why is it allowed? And in sample 7, the list is sorted but has three 2s, so it's not allowed. So what's the difference between sample 6 and 7?

Ah! Wait, in sample 6, the duplicates are consecutive. So maybe the problem is that the list must be strictly increasing, but the samples are conflicting. But sample 6 is [1,2,2,3,3,4], which is not strictly increasing. So why does it return True?

Wait this is very confusing. Let me think of the possible conditions that would make the sample inputs correct.

Let me think of the sample input 6: [1,2,2,3,3,4] returns True. So the function must return True for this case. So what is the condition that allows this?

Maybe the function is supposed to return True if the list is sorted in non-decreasing order, but with each number appearing at most twice. So, for example, in sample 6, each number appears exactly twice (except 1 and 4). Wait no, 1 appears once, 2 appears twice, 3 appears twice, 4 appears once. So the condition is that each number appears at most twice.

But how to determine this from the problem statement.

The problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps the wording is that if a number appears more than once, it's considered as having one duplicate. And if it appears more than once (i.e., at least two times), then it's considered as having one duplicate. But the condition says to return False if there are more than one duplicate. So perhaps the wording is that if a number appears more than two times, then return False.

But how to interpret the wording. Let me think:

"more than 1 duplicate of the same number" → perhaps this means that the number appears more than once (i.e., two or more times). So if a number appears two times, that's one duplicate. If it appears three times, that's two duplicates. So the condition is that if there are more than one duplicates (i.e., two or more), return False. But that would mean that any list with duplicates would return False, which contradicts the sample input 6.

So this is very confusing. Perhaps the problem statement has a typo, and the actual condition is that the list is sorted in ascending order and has no consecutive duplicates. So the list must be strictly increasing. But sample input 6 is [1,2,2,3,3,4], which is not strictly increasing. So why does it return True?

Alternatively, perhaps the problem statement is that the list is sorted in ascending order and has no duplicates. But sample input 6 returns True, which would not fit.

At this point, I think the best approach is to look at the sample inputs and try to derive the actual condition.

Looking at the samples:

The function returns True if the list is sorted in ascending order and each number appears at most twice. For example:

- [1,2,2,3,3,4] → each number appears at most twice → True
- [1,2,2,2,3,4] → 2 appears three times → False
- [1,2,3,4,5] → all unique → True
- [5] → True

So the condition is that the list is sorted in non-decreasing order, and no element appears more than twice.

But how to reconcile this with the problem statement's wording. The problem says: "If list has more than 1 duplicate of the same number, return False." So perhaps "more than 1 duplicate" means that the number appears more than two times. So if a number appears two times, it's allowed. But if it appears three or more times, it's not allowed.

But this is just a guess. Let me see the sample input 6: [1,2,2,3,3,4] has two 2s and two 3s. So it's allowed. Sample input 7 has three 2s, so it's not allowed. So the condition is that each number appears at most twice.

But how to interpret the problem statement's wording. It says "more than 1 duplicate of the same number". So perhaps "duplicate" means that the number appears more than once. So if a number appears two times, it's considered as having one duplicate. If it appears three times, it's two duplicates. So the condition is that if there are more than one duplicates (i.e., two or more), return False. But that would make sample input 6 return False, which is not the case.

So I think the problem statement's wording is incorrect, and the actual condition is that the list is sorted in non-decreasing order, and each number appears at most twice.

Assuming that, how to implement the function.

So the steps to solve the problem:

1. Check if the list is sorted in non-decreasing order. If not, return False.
2. Check if any number appears more than two times. If yes, return False.
3. Otherwise, return True.

Let me test this with the samples:

Sample 6: [1,2,2,3,3,4] → sorted and each number appears at most twice → True.

Sample 7: [1,2,2,2,3,4] → sorted, but 2 appears three times → False.

Sample 2: [1,2,3,4,5] → sorted and all unique → True.

Sample 1: [5] → sorted and unique → True.

Sample 3: [1,3,2,4,5] → not sorted → False.

Sample 4: [1,2,3,4,5,6] → sorted and unique → True.

Sample 5: [1,3,2,4,5,6,7] → not sorted → False.

So this seems to fit.

So the function needs to:

- Check if the list is sorted in non-decreasing order.
- Check if any element appears more than two times.

But how to implement this.

So first, to check if the list is sorted in non-decreasing order. That can be done by comparing each element to the next. For example, for i in range(len(lst)-1), check if lst[i] <= lst[i+1]. If any of these is not true, return False.

Then, check for duplicates. How to check if any element appears more than two times.

We can count the frequency of each element. For example, using a dictionary or Counter.

If any element has a count > 2, return False.

So the steps for the function:

def is_sorted(lst):

   if not lst: return True (but the problem says no negative numbers, but the list can be empty? The examples include [5], so maybe the function can handle empty lists, but the problem says "list of numbers", but the examples don't cover that. But the problem says to assume no negative numbers and only integers, but not about empty lists. However, the sample inputs include [5], which is a single element.

So for the empty list, perhaps it's considered as sorted, but the problem may not cover it. But since the problem's examples don't include it, we can assume that the input is a non-empty list.

So first, check if the list is sorted in non-decreasing order.

Then, check if any element appears more than two times.

So, code steps:

- Check if the list is sorted in non-decreasing order.

- If not, return False.

- Else, check for any element that appears more than two times.

- If found, return False.

- Else, return True.

So for example, in sample 6, the list is sorted, and the counts are:

1: 1

2: 2

3: 2

4: 1 → all counts <= 2 → return True.

In sample 7, 2 appears three times → return False.

Now, how to implement this in Python.

Let's write code for that.

First, check if the list is sorted.

def is_sorted(lst):
    # Check if the list is non-decreasing
    for i in range(len(lst)-1):
        if lst[i] > lst[i+1]:
            return False
    # Now check for duplicates
    from collections import Counter
    counts = Counter(lst)
    for key, val in counts.items():
        if val > 2:
            return False
    return True

Wait, but what about the case where the list has multiple duplicates but not more than two? For example, [1,2,2,3,3,4], which is allowed. The code would return True.

But what about the case where the list is sorted, but has two duplicates, like [1,2,2,3]. That would return True.

But the problem's sample input 6 is [1,2,2,3,3,4], which returns True.

So this code should work.

Let's test the sample inputs.

Sample 6: [1,2,2,3,3,4] → sorted and counts are 1,2,2,1 → returns True.

Sample 7: [1,2,2,2,3,4] → counts for 2 is 3 → returns False.

Sample 2: [1,2,3,4,5] → counts are all 1 → returns True.

Sample 1: [5] → counts is 1 → returns True.

Sample 3: [1,3,2,4,5] → not sorted → returns False.

Sample 4: [1,2,3,4,5,6] → sorted and all unique → returns True.

Sample 5: [1,3,2,4,5,6,7] → not sorted → returns False.

So this code should pass the samples.

But what about the case where the list is sorted, but has two duplicates, but not consecutive? Like [1,2,3,2,4]. Wait, no, because the list is not sorted. So the first check would fail.

Another example: [1,2,2,3,2,4]. This list is not sorted, so the first check would fail.

So the code seems to handle that.

Now, what about the case where the list is sorted, and has two duplicates, but not consecutive? Like [1,2,3,3,4,3]. Wait, no, this list is not sorted. Because 4 is followed by 3. So the first check would fail.

So the code is correct.

But what about the case where the list is sorted, and has two duplicates, like [1,2,2,3,3,4]. The code returns True.

But according to the problem statement, this should be allowed. So the code works.

Now, the problem statement says that the list has no negative numbers and only integers. But the code doesn't need to handle that, as the input is assumed to be correct.

So the code seems to handle the samples correctly.

Now, let's test the sample input [1,2,2,3,3,4], which returns True. The code returns True.

The sample input [1,2,2,2,3,4] returns False, which the code returns False.

So this code should work.

Now, the problem says to write the function. So the code would be:

import collections

def is_sorted(lst):
    # Check if the list is non-decreasing
    for i in range(len(lst) - 1):
        if lst[i] > lst[i+1]:
            return False
    # Check for duplicates
    counts = collections.Counter(lst)
    for count in counts.values():
        if count > 2:
            return False
    return True

But wait, what about the case where the list is empty? The problem says to assume no negative numbers and only integers, but the code may need to handle empty list. However, the sample inputs don't include that. For example, if lst is empty, the code returns True. But according to the problem's examples, it's not specified. But since the problem says to assume no negative numbers, but the code may not need to handle empty lists. However, the code will handle it.

But the problem's examples include [5], which is a single element, so the code should handle that.

Now, the code uses the collections.Counter, which is imported. So the code needs to import it.

But the problem says to include any imports it needs. So the code should import collections.

But in the code block, the user may need to include the import.

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

But wait, the sample input [1,2,2,3,3,4] would return True, which is correct. The sample input [1,2,2,2,3,4] returns False, which is correct.

Now, what about the case where the list is [1,2,2,3,3,3]. The code would check for counts: 3 appears three times → returns False.

So this should be handled.

Now, the code should pass all the sample tests.

But let's check the sample input:

Sample 6: [1,2,2,3,3,4] → returns True.

Sample 7: [1,2,2,2,3,4] → returns False.

Yes.

Now, the problem says to return True if the list is sorted and has no more than one duplicate of the same number. Wait, but the code checks for counts > 2. So if a number appears two times, it's allowed. So the code is correct.

So the code should work.

Now, let's check the sample inputs:

assert is_sorted([5]) == True → True.

assert is_sorted([1, 2, 3, 4, 5]) == True → True.

assert is_sorted([1, 3, 2, 4, 5]) == False → True, because the list is not sorted.

Yes.

So the code should work.

Now, the code uses the collections.Counter, which is needed. So the code is correct.

Thus, this should be the solution.
```

</details>

**Code that ran:**

```python
import collections

def is_sorted(lst):
    # Check if the list is non-decreasing
    for i in range(len(lst) - 1):
        if lst[i] > lst[i + 1]:
            return False
    # Check for elements appearing more than twice
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
