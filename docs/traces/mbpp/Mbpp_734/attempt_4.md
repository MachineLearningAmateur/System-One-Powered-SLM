# Mbpp/734, attempt 4

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/734/a4/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 7920. Answer tokens: 76.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function that calculates the sum of the products of all possible sublists of a given list. The example given is that for [1,2,3], the sum is 20. Let me think about how to approach this.

First, let me understand what a sublist is. A sublist is any contiguous sequence of elements from the original list. For example, for [1,2,3], the sublists are:

- [1] → product 1
- [2] → 2
- [3] → 3
- [1,2] → 1*2=2
- [2,3] → 2*3=6
- [1,2,3] → 1*2*3=6

Adding these up: 1 + 2 + 3 + 2 + 6 + 6 = 20. Which matches the example. So the task is to compute this sum.

Now, how to compute this efficiently. Let's think about the brute force approach first. For each possible sublist, compute the product and sum them all. But for a list of size n, there are 2^n - 1 sublists. For n=10, that's 1023 sublists. For n=20, it's 1 million, which is manageable. But for larger n, this approach might be slow. However, given that the problem doesn't specify constraints on the input size, maybe the brute force is acceptable here.

But perhaps there's a smarter way. Let's think about the mathematical approach.

Let me think about the sum of products of all sublists. Let's consider each element's contribution. For example, each element contributes to the product of sublists in which it is included. But how?

Alternatively, there's a formula that can be derived. Let me think. Let's consider the sum of products of all sublists. Let's denote the list as a1, a2, ..., an.

The sum can be calculated as follows. For each element ai, how many times does it contribute to the product of sublists? Well, for each sublist that includes ai, the product includes ai. So, the total sum is the sum over all elements of ai multiplied by the sum of the products of all sublists that include ai.

Wait, maybe another approach. Let's think about the sum of products of all sublists. Let's consider that each sublist is a product of some elements. Let me think of the sum as the sum over all possible subsets (since sublists are subsets) of the product of elements in the subset.

But the problem is that for each subset, the product is multiplied. So the sum is the sum of products of all subsets.

But how to compute this sum efficiently?

There's a known formula for this. Let me recall. For example, for the sum of products of all subsets of a list, the formula is (a1 + a2 + ... + an) * (a1 + a2 + ... + an) - (sum of squares) + ...? Wait, no. Wait, let me think again.

Alternatively, consider that the sum of products of all subsets is equal to the product of (1 + ai) for each element ai. Because for each element, you can choose to include it or not. So for each element, you have a choice: include it (so multiply by ai) or not (so multiply by 1). So the total sum is the product of (1 + ai) for all i. But wait, that's the sum of products of all subsets, including the empty subset. But the problem says "all possible sublists", which includes the empty sublist. But in the example given, the sum is 20. Let's check that.

For the example [1,2,3], the product of (1+1)*(1+2)*(1+3) = 2*3*4 = 24. But the sum of products of all subsets (including empty) would be 1 (empty) + 1 + 2 + 3 + 1*2 + 1*3 + 2*3 + 1*2*3. Let's compute that:

Empty subset: 1.

Single elements: 1, 2, 3 → sum 6.

Pairs: 1*2=2, 1*3=3, 2*3=6 → sum 11.

Triple: 1*2*3=6 → sum 6.

Total sum is 1 + 6 + 11 + 6 = 24. But the problem's example is sum of non-empty sublists. So the problem's example is 20, which is 24 - 1 (the empty subset). So the problem's sum is the product of (1 + ai) for all elements, minus 1. So the formula is (product of (1 + ai) for all elements) - 1.

But wait, the problem says "all possible sublists". So the empty sublist is considered. But in the example, the sum is 20, which is 24 - 1. So the formula would be (product of (1 + ai) for all elements) - 1.

So the answer for the problem is (product of (1 + a_i) for all a_i) - 1.

Wait, let me check with the example. For [1,2,3], product is (1+1)*(1+2)*(1+3) = 2*3*4 = 24. 24-1=23? Wait no, the example says the sum is 20. Wait, there's a contradiction here. Wait, what's the correct sum?

Wait, the example says sum of products of all possible sublists. Let me re-calculate.

Original example: [1,2,3]. The sublists are:

Empty: 1 (product is 1?)

Wait, the problem says "sum of products of all possible sublists". So the empty sublist is included. But in the example, the sum is 20. Let's compute the sum of all sublists, including empty.

In the example, the sum would be:

Empty: 1.

Single elements: 1, 2, 3 → sum 6.

Pairs: 1*2=2, 1*3=3, 2*3=6 → sum 11.

Triple: 1*2*3=6 → sum 6.

Total sum: 1 + 6 + 11 + 6 = 24. So the example's sum is 20, which is 24 - 4. But according to the problem's assertion, the sum is 20. So there's a contradiction here. Wait, what's the problem's assertion? The user says:

assert sum_Of_Subarray_Prod([1,2,3]) == 20.

But according to the calculation, the sum of all sublists (including empty) is 24. So why is the example 20?

Ah, perhaps the problem considers only non-empty sublists. Because in the example, the sum is 20. Let's check that.

If the problem is to sum all non-empty sublists, then the sum is 24 - 1 (empty) = 23. But that's not 20. Wait, what's the correct sum?

Wait, the example's sum is 20. Let me re-calculate the sum of all non-empty sublists:

The sublists are:

[1], [2], [3], [1,2], [2,3], [1,2,3]. Their products are 1, 2, 3, 2, 6, 6. Sum is 1+2+3+2+6+6 = 18? Wait 1+2 is 3, +3 is 6, +2 is 8, +6 is 14, +6 is 20. Oh right! So the sum is 20. So the problem is to sum all non-empty sublists. So the formula is (product of (1 + a_i) for all a_i) - 1. Because the product includes the empty subset (which is 1) and the sum is that product minus 1.

So for the example, product is 24, 24-1=23? But the sum is 20. Wait, that's not matching. Wait, what's the product of (1 + a_i) for the example?

(1+1) * (1+2) * (1+3) = 2 * 3 * 4 = 24. So the product is 24. The sum of all subsets (including empty) is 24. So the sum of all non-empty subsets is 24 - 1 = 23. But the example says it's 20. So there's a contradiction here. What's wrong?

Wait, perhaps I made a mistake in the calculation. Let me re-calculate the sum of all non-empty sublists.

Original list [1,2,3]. The non-empty sublists:

[1] → 1

[2] → 2

[3] →3

[1,2] → 2

[2,3] →6

[1,2,3] →6

Total sum: 1 + 2 + 3 + 2 + 6 + 6 = 1 + 2 is 3, +3 is 6, +2 is 8, +6 is 14, +6 is 20. So 20. But according to the product formula, the product is 24. So 24 - 1 = 23. So why is there a discrepancy?

Ah! Wait, perhaps the product formula is not correct. Let me think again.

The product formula is the sum of products of all subsets, including the empty subset. So the sum is 1 (empty) + sum of all non-empty subsets. So the sum of non-empty subsets is product - 1.

But in the example, the sum of non-empty subsets is 20. So product -1 = 20 → product is 21. But according to the calculation, the product is 24. So something's wrong here.

Wait, perhaps my understanding of the product formula is incorrect. Let me think again.

The product of (1 + a_i) for all elements is equal to the sum of products of all subsets, including the empty subset. Let me check for the example.

For [1,2,3], the product is (1+1)*(1+2)*(1+3) = 2 * 3 *4 =24. But the sum of all subsets (including empty) is 1 (empty) + 1+2+3 + 1*2 + 1*3 + 2*3 + 1*2*3 = 1 + 6 + 11 +6 = 24. So yes, that's correct. So the sum of all subsets (including empty) is 24. So the sum of non-empty subsets is 24-1=23. But according to the example, the sum is 20. So why is there a discrepancy?

Ah! Wait, perhaps the problem counts the empty subset as not being included. But the example's assertion says that the sum is 20, which is the sum of non-empty sublists. But according to the product formula, the sum of non-empty sublists is 23. So why is the example 20?

Wait, this suggests that there's a mistake in my reasoning. Let me re-calculate the sum of all non-empty sublists again.

Wait, the sum of all non-empty sublists is:

Each non-empty subset's product. Let's list them:

Subsets:

[1] → 1

[2] → 2

[3] →3

[1,2] →2

[2,3] →6

[1,3] →3

[1,2,3] →6

Wait, wait, what about [1,3]? Oh, right! The original list is [1,2,3], so the possible sublists are:

All possible non-empty subsets. So the subsets are:

Size 1: 3 subsets.

Size 2: 3 subsets.

Size 3: 1 subset.

So total 3+3+1=7 subsets. Wait, but earlier I thought there were 6. Oh, wait, the list has 3 elements. So the number of non-empty sublists is 2^3 -1 =7. So the subsets are:

Size 1: [1], [2], [3] → products 1, 2, 3.

Size 2: [1,2], [2,3], [1,3] → products 2, 6, 3.

Wait, wait, [1,3] is a sublist. Oh, right! Because the original list is [1,2,3], so the sublists of size 2 are [1,2], [2,3], [1,3]?

Wait, no. Wait, the list is [1,2,3]. The sublists of size 2 are:

[1,2], [2,3], [1,3]? No, because the list is [1,2,3]. So the elements are in order. So the sublists of size 2 are:

[1,2], [2,3], and [1,3] is not a valid sublist. Wait, no. Because the elements are in order. So the sublists of size 2 are contiguous. So the possible sublists of size 2 are [1,2], [2,3]. So there are only two sublists of size 2. Wait, what's the correct way to count?

Ah, I think I made a mistake here. The number of sublists of size k is (n -k +1). For n=3, the number of sublists of size 1 is 3, size 2 is 2, size 3 is 1. So the total number of non-empty sublists is 3+2+1=6. So the sum is 1+2+3+2+6+3= 1+2 is 3, +3 is 6, +2 is 8, +6 is 14, +3 is 17. Wait, but that's not matching the earlier calculation. What's wrong here?

Wait, the products of the sublists:

For the list [1,2,3], the non-empty sublists are:

[1] →1

[2] →2

[3] →3

[1,2] →2

[2,3] →6

[1,2,3] →6

So the sum is 1+2+3+2+6+6 = 20. So that's correct. So where did the [1,3] come from? Oh, because the sublist [1,3] is not contiguous. So in the original list, the sublists are contiguous. So the sublists are:

For [1,2,3], the possible sublists are:

[1], [1,2], [1,2,3], [2], [2,3], [3]. So six sublists. So the sum is 1+2+3+2+6+6=20. So the sum of non-empty sublists is 20. But according to the product formula, the sum of all subsets (including empty) is 24, so the sum of non-empty is 24-1=23. But according to the actual calculation, it's 20. So there's a contradiction here. Which means that my earlier formula is wrong.

So what's wrong with the formula? Let me think again.

The formula (product of (1 + a_i)) is equal to the sum of the products of all subsets, including the empty subset. So for the example, that product is 2*3*4=24. So the sum of all subsets (including empty) is 24. So the sum of non-empty is 24-1=23. But according to the actual calculation, it's 20. So why the discrepancy?

Ah! Oh wait! Because the formula (product of (1 + a_i)) is the sum of products of all subsets, including the empty subset. But in the example, the sum of all subsets (including empty) is 24. But according to the actual calculation, the sum of non-empty is 20. So 24 - 1 = 23, but actual is 20. So this suggests that the formula is not correct. So where is the error here?

Wait, let me re-calculate the product of (1 + a_i) for the example.

The list is [1,2,3]. So the product is (1+1) * (1+2) * (1+3) = 2 * 3 * 4 = 24. But according to the actual sum of all subsets (including empty), it's 24. So the sum of all subsets (including empty) is 24. But the actual sum of non-empty is 20. So 24 - 1 (empty subset) is 23, but the actual sum is 20. So this suggests that the formula is incorrect. But why?

Wait, maybe the formula is not correct. Let me think again. Let me take a small example. Let's take a list with one element. For [a], the product is (1+a). The sum of subsets (including empty) is 1 + a. Which is correct. So for a list with one element, the sum of non-empty subsets is a. Which is (1+a) -1 = a. Which is correct. So the formula works here.

Another example: list [a, b]. The product is (1+a)(1+b) = 1 + a + b + ab. The sum of all subsets (including empty) is 1 (empty) + a (single a) + b (single b) + ab (both) → total 1 + a + b + ab. Which is correct. The sum of non-empty subsets is a + b + ab. Which is (1+a)(1+b) -1. So that's correct.

But in the case of the example [1,2,3], the sum of non-empty subsets is 20. According to the formula, it should be 24 -1 =23. But actual is 20. So why is this discrepancy?

Wait, let me calculate the sum of all subsets (including empty) for [1,2,3]. The empty subset is 1. The other subsets are:

Single elements: 1, 2, 3 → sum 6.

Pairs: 1*2=2, 2*3=6 → sum 8.

Triple: 1*2*3=6 → sum 6.

Total sum: 1 + 6 + 8 +6 = 21. Wait, but earlier I thought it was 24. What's wrong here?

Wait, the product (1+a)(1+b)(1+c) is (1+1)(1+2)(1+3) = 2 * 3 *4 = 24. But according to the sum of all subsets (including empty), it's 1 + (sum of all subsets except empty). So according to the formula, the sum of all subsets (including empty) is 24. But according to the manual calculation, it's 1 + 6 + 8 +6 = 21. So where is the mistake?

Ah! Because the formula (product of (1 + a_i)) is the sum of products of all subsets, including the empty subset. So for the example, the sum is 24. But when I manually calculated, I got 21. So there's a mistake in my manual calculation.

Let me re-calculate the sum of all subsets (including empty) for [1,2,3].

The subsets are:

Empty → 1.

Single elements:

[1] →1.

[2] →2.

[3] →3.

Sum of single elements: 1+2+3=6.

Pairs:

[1,2] →1*2=2.

[2,3] →2*3=6.

Sum of pairs: 2+6=8.

Triple:

[1,2,3] →1*2*3=6.

Sum of triple: 6.

Total sum: 1 + 6 + 8 + 6 = 21. But according to the product formula, it's 24. So there's a discrepancy here. So why?

Wait, what's the product (1+1)*(1+2)*(1+3) = 2 *3 *4 =24. But according to the manual calculation, the sum is 21. So where is the error here?

Ah! Oh! Because the formula (product of (1 + a_i)) is the sum of products of all subsets, including the empty subset. So for the example, the product is 24, which equals 1 (empty) + 1+2+3 (single elements) + 2+6 (pairs) + 6 (triple). So 1 + (1+2+3) + (2+6) +6 = 1 + 6 + 8 +6 = 21. But 24 is not equal to 21. So there's a mistake in the formula.

Wait, what's the correct value of the product? Let me compute it again. The product is (1 + 1) * (1 + 2) * (1 + 3) = 2 * 3 * 4 = 24. But according to the sum of all subsets, it's 21. So there's a contradiction. So where is the mistake?

Ah! Oh! Because the formula (product of (1 + a_i)) is the sum of the products of all subsets, including the empty subset. But in this case, the sum is 24. But according to the manual calculation, it's 21. So there's a mistake in the manual calculation.

Wait, let me re-calculate the sum of all subsets:

The product (1 + a_i) for each element is:

For a1=1: 1+1=2.

For a2=2: 1+2=3.

For a3=3: 1+3=4.

The product is 2 *3 *4 =24.

But the sum of all subsets (including empty) is 24. So the sum of all subsets is 24. So how can that be?

Let me think again. The sum of the products of all subsets is:

For each subset S, the product of elements in S.

So for the example [1,2,3], the subsets are:

Empty → 1.

[1] →1.

[2] →2.

[3] →3.

[1,2] →2.

[2,3] →6.

[1,3] →3? Wait, no, wait. The subsets are:

Wait, the subsets are all possible combinations. So the subsets are:

Empty → 1.

Single elements: [1], [2], [3] → products 1, 2, 3.

Pairs: [1,2], [2,3], [1,3] → products 2, 6, 3.

Triple: [1,2,3] →6.

So the sum is 1 + 1 + 2 + 3 + 2 + 6 + 3 + 6 = let's calculate:

1 (empty) + 1 + 2 +3 + 2 +6 +3 +6 = 1 + (1+2+3) + (2+6+3+6) = 1 +6 + 17 = 24. Oh! So earlier I missed the [1,3] subset. So the sum is 24. So the previous manual calculation was wrong because I forgot that the [1,3] is a valid subset. Oh! So the sum of all non-empty sublists is 24 - 1 (empty) = 23. But according to the example, the sum is 20. Which is not matching. But the example's assertion is that the sum of non-empty sublists is 20. So why?

Wait, but in the example, the sum of non-empty sublists is 20. But according to the formula, it's 23. So this suggests that there's a mistake in the example, or in the formula.

Wait, let me re-calculate the sum of non-empty sublists. The sum is the sum of all subsets except the empty one. Which is 24 -1 =23. But according to the example, it's 20. So this suggests that the example is wrong, or there's a misunderstanding of the problem.

Wait, the problem says: "sum of products of all possible sublists of a given list". So what's the definition of a sublist here? Is a sublist a contiguous sequence? Because if that's the case, then the previous calculation is correct. But the example says that the sum is 20, which is different from the formula's result.

Wait, the example is [1,2,3], and the sum is 20. But according to the formula, it's 23. So why is the example's assertion 20?

Let me re-calculate the sum of all non-empty contiguous sublists.

For [1,2,3], the contiguous sublists are:

[1] →1

[1,2] →2

[1,2,3] →6

[2] →2

[2,3] →6

[3] →3

So the sum is 1 + 2 +6 +2 +6 +3 = 1+2=3, +6=9, +2=11, +6=17, +3=20. Which matches the example. So the sum of non-empty contiguous sublists is 20. But according to the formula, the sum of all subsets (including empty) is 24, so the sum of non-empty contiguous sublists is 24 - 1 (empty) - (sum of other subsets that are not contiguous). Wait, but the formula (product of (1 + a_i)) includes all subsets, including non-contiguous ones. But the problem is about contiguous sublists. So the formula is not applicable here.

Ah! Oh! I see the mistake now. The formula (product of (1 + a_i)) includes all subsets, including non-contiguous ones, but the problem is only asking for contiguous sublists. So the formula is not applicable here. So my previous reasoning was wrong.

So the problem is not about all subsets, but about all contiguous sublists. Therefore, the formula (product of (1 + a_i)) is not applicable here. So I need to find another approach.

So the problem is to find the sum of products of all contiguous sublists. For example, in the case of [1,2,3], the sum is 20.

So how to compute this efficiently?

Let me think of a way to compute this sum. For each element, how much does it contribute to the total sum.

Let me think about dynamic programming. Let's consider the sum for the first i elements.

For example, for the list [a1, a2, a3], the sum of products of all contiguous sublists can be computed as follows:

The sum for the first i elements is the sum for the first i-1 elements plus the sum of the new sublists that include the i-th element.

But how to compute this.

Another approach: For each position i, we can track the sum of products of all sublists ending at i.

Let me think. Let's say we have a list of elements. For each element, we can compute the sum of products of all sublists that end at this element.

For example, for the first element a1, the only sublist is [a1], so sum is a1.

For the second element a2, the sublists ending at a2 are [a2], [a1,a2]. The sum is a2 + (a1*a2).

For the third element a3, the sublists ending at a3 are [a3], [a2,a3], [a1,a2,a3]. The sum is a3 + (a2*a3) + (a1*a2*a3).

So the total sum is the sum of all these for each element.

So the total sum is the sum of the following for each position i:

sum_{k=1 to i} (product of a_{i-k+1} ... a_i} )

So, for each i, we can compute the sum of products of all sublists ending at i.

So, for the list [a1, a2, a3], the total sum would be:

a1 + (a1*a2) + (a1*a2*a3) + a2 + (a2*a3) + a3.

Which is 1 + 2 + 6 + 2 + 6 + 3 = 20, which matches the example.

So the approach is to compute for each element, the cumulative product of the sublists ending at that element. Then, sum all these values.

But how to compute this efficiently.

Let's think about the following:

We can maintain a variable that keeps track of the current product of the sublists ending at the current position. For example, for each i, the current product is the previous product multiplied by a_i, plus a_i.

Wait, let's think. Let's say for the i-th element, the sum of products of all sublists ending at i is:

sum = a_i + (sum of products of sublists ending at i-1) * a_i.

Wait, no. Let me think again. For example, when we add a new element a_i, the new sublists ending at i are:

- the single element [a_i], which contributes a_i.

- the sublists that end at i-1 and include a_i, which are the sublists that end at i-1, and then adding a_i to them. So for example, if the previous sum for i-1 is S_prev, then the new sublists ending at i are S_prev * a_i plus a_i.

So the total sum for i is a_i + (S_prev * a_i).

But wait, the previous sum S_prev is the sum of all sublists ending at i-1. So when we add a_i, the new sublists are the previous ones extended by a_i, and the new single element. So the total sum for i is a_i + (S_prev * a_i).

But S_prev is the sum of all sublists ending at i-1. So for example, for the first element, S_prev is 0. So the sum for i=1 is a1 + 0 * a1 = a1. For i=2, the sum is a2 + (a1 * a2). For i=3, it's a3 + (a2*a3 + a1*a2*a3) ?

Wait, no. Wait, the sum of the sublists ending at i is the sum of the single element [a_i], plus the sum of the sublists that end at i-1 and are extended by a_i. So for i-th element, the sum is a_i + (sum of sublists ending at i-1) * a_i. But wait, the sum of sublists ending at i-1 is S_prev. Then the new sublists ending at i are:

- the single element [a_i], which is a_i.

- the sublists that end at i-1 and are extended by a_i. So for each sublist ending at i-1, we add a_i to it. So the sum of these is S_prev * a_i.

So the total sum for i is a_i + S_prev * a_i.

But S_prev is the sum of the sublists ending at i-1. So the total sum for i is a_i * (1 + S_prev).

But wait, for i=1, S_prev is 0. So the sum is a1 * (1 + 0) = a1. Which is correct.

For i=2, S_prev is a1. So the sum is a2 * (1 + a1) = a2 + a1*a2. Which is correct.

For i=3, S_prev is a1 + a2. So the sum is a3 * (1 + a1 + a2) = a3 + a1*a3 + a2*a3. Which is correct.

So the total sum for all sublists is the sum of the cumulative sums for each i. So for each element, we compute the current sum, and add it to the total.

So the algorithm is:

Initialize total = 0.

Initialize current_sum = 0.

For each element in the list:

    current_sum = element * (1 + current_sum)

    total += current_sum

So for example, for the list [1,2,3]:

current_sum starts at 0.

First element is 1:

current_sum = 1 * (1 + 0) = 1 → total = 1.

Second element is 2:

current_sum = 2 * (1 + 1) = 2 * 2 =4 → total = 1 +4 =5.

Third element is 3:

current_sum = 3 * (1 +4) =3 *5=15 → total =5+15=20. Which matches the example.

Yes! So this approach works.

So the code can be written as follows:

Initialize total = 0.

current_sum = 0.

for num in list:

    current_sum = num * (1 + current_sum)

    total += current_sum

return total

So this would give the correct sum for the example.

So for the list [1,2,3], the code returns 20. Which matches the example.

So this is the correct approach.

Now, the code can be written in Python.

The code would be:

def sum_Of_Subarray_Prod(lst):
    total = 0
    current_sum = 0
    for num in lst:
        current_sum = num * (1 + current_sum)
        total += current_sum
    return total

Then, the assert statement would be:

assert sum_Of_Subarray_Prod([1,2,3]) == 20

So this should work.

Let me test this with another example. For example, list [1], the code returns 1. Which is correct.

Another example: list [1,1]. The sublists are [1], [1], [1,1]. Their products are 1, 1, 1*1=1. Sum is 1+1+1=3.

Let's see:

current_sum starts at 0.

First num is 1:

current_sum = 1 * (1+0) =1 → total=1.

Second num is 1:

current_sum = 1 * (1+1) = 2 → total=1+2=3.

Which is correct.

Another example: list [2,3]. The sublists are [2], [3], [2,3]. Sum is 2 +3 +6 =11.

Code:

current_sum starts at 0.

First num is 2: current_sum = 2 *1=2 → total=2.

Second num is 3: current_sum = 3*(1+2) =3*3=9 → total=2+9=11. Correct.

Yes, this seems to work.

So the code is correct.

Now, the code needs to be written with the correct imports. But there are no imports needed. The code is just a function.

So the final code is:

def sum_Of_Subarray_Prod(lst):
    total = 0
    current_sum = 0
    for num in lst:
        current_sum = num * (1 + current_sum)
        total += current_sum
    return total

assert sum_Of_Subarray_Prod([1,2,3]) == 20

But the user wants the code in one code block, including any imports. Since there are no imports needed, the code is as above.

So the final answer is the code as written.
```

</details>

**Code that ran:**

```python
def sum_Of_Subarray_Prod(lst):
    total = 0
    current_sum = 0
    for num in lst:
        current_sum = num * (1 + current_sum)
        total += current_sum
    return total

assert sum_Of_Subarray_Prod([1, 2, 3]) == 20
```

**Visible-test report:**

```text
PASS    assert sum_Of_Subarray_Prod([1,2,3]) == 20
1 of 1 visible tests passed
```
