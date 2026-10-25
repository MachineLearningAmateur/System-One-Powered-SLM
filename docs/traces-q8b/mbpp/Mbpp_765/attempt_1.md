# Mbpp/765, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/765/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 83.

<details><summary>Thinking</summary>

```text
Okay, I need to find the nth polite number. Let me think about what a polite number is. Oh right, from the GeeksforGeeks link, polite numbers are numbers that can be expressed as the sum of two or more consecutive positive integers. And the problem says to find the nth one.

Wait, the example given is is_polite(7) == 11. Wait, that's confusing. Wait, the function is supposed to return the nth polite number. So when n is 7, the answer is 11? Let me check that. Let me think about the sequence of polite numbers.

Wait, the first few polite numbers are 3, 4, 5, 6, 7, 8, 9, 10, 11, etc. Wait, but wait. Wait, what's the first polite number? Let me think. The number 1 can't be expressed as sum of two or more consecutive numbers. 2 also can't. 3 is 1+2. So 3 is the first polite number. Then 4 is 1+3, or 2+2? Wait, but consecutive numbers. So 1+3 is not consecutive. Wait, 2+2 is not consecutive. Wait, 4 can be expressed as 1+2+1? No. Wait, maybe I'm misunderstanding. Wait, the definition is that a polite number can be expressed as the sum of two or more consecutive positive integers. So for example, 3 is 1+2. 4 can be 1+3? No, because they are not consecutive. Wait, 4 can be written as 1+2+1? No. Wait, maybe 4 can't be expressed as such? Wait, but then what about 4? Let me think again.

Wait, let's check the example given. The user says that is_polite(7) returns 11. So the 7th polite number is 11. Let me think about the sequence.

Wait, maybe the first few polite numbers are 3, 4, 5, 6, 7, 8, 9, 10, 11, etc. So the 7th is 9? But the example says 11. Wait, maybe I'm misunderstanding the problem. Let me check the GeeksforGeeks link.

Wait, according to the problem statement, the nth polite number. Let me check the example given. The assert is is_polite(7) == 11. Wait, maybe the function is supposed to return the nth polite number. So when n is 7, the answer is 11. So the first 7 polite numbers are 3, 4, 5, 6, 7, 8, 9? But that would make the 7th number 9, not 11. So perhaps I'm misunderstanding the problem. Wait, maybe the example is wrong? Or maybe the function is not called is_polite, but the problem says that the function is to find the nth polite number. Wait, the problem says: write a function to find the nth polite number. The assert is is_polite(7) == 11. So the function is called is_polite, and when given 7, returns 11. So that suggests that the 7th polite number is 11. So what's the sequence?

Let me think again. Let me list the polite numbers. According to the problem's example, the 7th is 11. Let me check the sequence. Let me think about the numbers and their representations.

3: 1+2 → yes.

4: 1+3? No. Wait, 1+2+1? No. Wait, 4 can be written as 1+3 (but not consecutive). Wait, maybe 4 can be written as 2+2? But consecutive numbers must be increasing. So 2 and 2 are not consecutive. So 4 can't be written as sum of consecutive numbers. Wait, but that would mean that 4 is not a polite number. But that contradicts the example. So maybe I'm missing something here.

Wait, perhaps the definition is different. Let me check the GeeksforGeeks link. Oh, the link is given, but I can't access it. But according to the problem statement, the example says that the 7th polite number is 11. So let's think about that.

Wait, maybe the polite numbers are numbers that are not powers of two. Because according to some knowledge, a number can be expressed as the sum of consecutive integers if and only if it is not a power of two. Let me check that. For example, 3 is 2^1 + 1, not a power of two. 4 is 2^2. So 4 is a power of two. So 4 is not a polite number. But then, what about 5? 5 is 2+3, so yes. So the sequence of polite numbers would be 3, 5, 6, 7, 9, 10, 11, etc. So the first polite number is 3, the second is 5, third is 6, fourth is 7, fifth is 9, sixth is 10, seventh is 11. So that would make the 7th number 11, which matches the example. So the function needs to return the nth number in this sequence.

So the problem is to find the nth number that is not a power of two. Because the polite numbers are exactly the numbers that are not powers of two. So the nth polite number is the nth number in the sequence of numbers that are not powers of two.

So how do we find the nth polite number? Well, for example, the nth polite number is n + the number of powers of two less than or equal to n. Because for each number, if it is a power of two, it's excluded. So the nth polite number is n plus the count of powers of two up to that number. Wait, but how do we compute that?

Alternatively, the nth polite number is the number that is n plus the number of powers of two less than or equal to n. Wait, perhaps not. Let me think. Let's take n=7. The 7th polite number is 11. Let's see. The numbers from 1 to 11 are:

Numbers that are not powers of two: 3,5,6,7,9,10,11. So there are 7 numbers. So the 7th is 11. So the formula is that the nth polite number is n + the number of powers of two less than or equal to n. Wait, how?

Let me think. For example, for n=7, the number of powers of two up to 7 is 3 (since 2^0=1, 2^1=2, 2^2=4, 2^3=8 which is larger than 7). So 3. Then 7 + 3 = 10. But that's not 11. Hmm. So maybe that approach is not correct. Alternatively, perhaps the nth polite number is n + the count of powers of two up to n + something. Wait, perhaps the formula is that the nth polite number is n + the number of powers of two less than or equal to n. Let me check with n=7. The count of powers of two up to 7 is 3 (1, 2, 4). So 7 + 3 = 10. But the correct answer is 11. So that's not matching. So maybe that approach is wrong.

Alternatively, perhaps the nth polite number is n + the number of powers of two less than or equal to n + 1? Let me try. For n=7, 3+1=4, 7+4=11. Which matches. Let's check for n=1. The first polite number is 3. The count of powers of two up to 1 is 1 (only 1). So 1 + 1 + 1 = 3. Yes. For n=2, the second polite number is 5. Let's see. The count of powers of two up to 2 is 2 (1, 2). So 2 + 2 + 1? No. Wait, 2 + 2 = 4. Which is not 5. Hmm. Maybe this approach is not correct. Let me think again.

Another approach: the nth polite number is the number which is n plus the number of powers of two less than or equal to n. Let me think. Let's take n=7. The count of powers of two up to 7 is 3 (1, 2, 4). So 7 + 3 = 10. But the correct answer is 11. So why is that? Because the 7th polite number is 11. So how does that fit?

Alternatively, perhaps the nth polite number is n + the number of powers of two less than or equal to n. But for n=7, the count is 3, so 7+3=10. But the correct answer is 11. So that's not matching. So perhaps that approach is incorrect.

Wait, maybe the formula is that the nth polite number is n + the number of powers of two less than or equal to n. But how does that fit with the example. Let's think for n=7. The count is 3. So 7 +3=10. But the correct answer is 11. So that's not matching. So perhaps that's not the right formula.

Wait, maybe the nth polite number is n + the number of powers of two less than or equal to (n + the number of powers of two less than or equal to n). That seems recursive and complicated. Maybe there's a better way.

Alternatively, think about the sequence of polite numbers. They are all numbers except the powers of two. So the nth polite number is the number that is n plus the number of powers of two that are less than or equal to that number. Wait, but how to find that number?

Alternatively, the nth polite number is n + the count of powers of two up to n. Let me try for n=7. Let's see: the count of powers of two up to 7 is 3 (1, 2, 4). So 7 + 3 = 10. But the correct answer is 11. So that's not matching. So what's wrong here?

Wait, maybe the formula is that the nth polite number is n + the number of powers of two that are less than or equal to (n + the number of powers of two that are less than or equal to n). But this seems circular.

Alternatively, think of the nth polite number as the number which is n plus the number of powers of two up to that number. Let me think. For example, for the 7th polite number, which is 11, how many powers of two are there up to 11? The powers are 1, 2, 4, 8. So 4. So 7 + 4 = 11. Which matches. Let me check for n=1. The first polite number is 3. How many powers of two up to 3? 1, 2. So 2. So 1 + 2 = 3. Correct. For n=2, the second polite number is 5. How many powers of two up to 5? 1, 2, 4. So 3. 2 + 3 = 5. Correct. For n=3, the third polite number is 6. How many powers up to 6? 1,2,4. 3. 3+3=6. Correct. For n=4, the fourth polite number is 7. How many powers up to 7? 1,2,4. 3. 4+3=7. Correct. For n=5, fifth polite number is 9. How many powers up to 9? 1,2,4,8. 4. 5+4=9. Correct. For n=6, sixth is 10. How many powers up to 10? 1,2,4,8. 4. 6+4=10. Correct. For n=7, 7+4=11. Correct. So the formula is that the nth polite number is n + the number of powers of two up to (n + the number of powers of two up to ...). Wait, but how do we compute this?

Wait, the formula is that the nth polite number is n plus the number of powers of two that are less than or equal to the nth polite number. But since we don't know the nth polite number, how do we compute this? However, this seems to be a recursive relationship. But perhaps there's a way to find the number of powers of two up to a certain number.

But how can we find the nth polite number? Let's think of it as the number x such that x = n + k, where k is the number of powers of two less than or equal to x. So x = n + k, where k is the count of powers of two up to x.

But how do we find x given n?

Let me think of this as a function. For example, given n, find x such that x = n + the number of powers of two up to x.

But how to compute this?

Let me think. The number of powers of two up to x is floor(log2(x)) + 1. Because the powers of two are 2^0, 2^1, ..., up to 2^m where 2^m <=x. So m is floor(log2(x)). So the count is m+1.

So the equation is x = n + (floor(log2(x)) + 1).

But solving this equation for x given n seems challenging. However, perhaps we can approximate it.

For example, for a given n, the value of x is approximately n + log2(x) + 1. But since log2(x) is small compared to x, maybe we can approximate x as n + log2(n) + 1. But this is not precise. Alternatively, we can find x by iterating.

Let me think for n=7. We want x such that x = 7 + (number of powers of two up to x). Let's try x=11. Number of powers up to 11 is 4 (1, 2, 4, 8). 7+4=11. Correct. So x=11.

For n=1, x=3. 3 = 1 + 2 (number of powers up to 3 is 2). Correct.

So the problem reduces to finding x such that x = n + (number of powers of two up to x). How can we compute this?

But how to compute x for a given n? Well, perhaps we can find x by using the formula x = n + k, where k is the number of powers of two up to x. Since k is floor(log2(x)) +1, but that depends on x.

But perhaps we can approximate x as n + log2(x) + 1. However, since x is n + something, we can approximate x as n + log2(n) + 1. But this is not precise. Alternatively, perhaps we can find x by starting from n and adding the number of powers of two up to x.

But how?

Alternatively, since the number of powers of two up to x is O(log x), which is small compared to x, perhaps x is approximately n + log(n) + 1. So for a given n, we can compute x as n + the number of powers of two up to x. But since x is not known, perhaps we can use binary search.

Alternatively, for a given n, the nth polite number is equal to n + the number of powers of two less than or equal to (n + the number of powers of two less than or equal to ...). But this seems recursive.

Alternatively, think of it as x = n + k, where k is the number of powers of two up to x. Since k is the number of powers of two up to x, which is floor(log2(x)) + 1. So x = n + floor(log2(x)) + 1.

But solving this equation for x is tricky. However, since for x, the value of floor(log2(x)) is roughly log2(x), we can approximate x as n + log2(x) + 1. But since x is n + something, perhaps we can approximate x as n + log2(n) + 1. For example, for n=7, log2(7) is about 2.8, so x would be 7 + 2.8 + 1 = 10.8, which rounds up to 11. Which is correct.

So for a given n, we can approximate x as n + log2(n) + 1, and then adjust it. But how to compute this accurately?

Alternatively, since the number of powers of two up to x is floor(log2(x)) + 1, and x is n + (number of powers up to x), perhaps we can compute x as n + (number of powers up to x). But how?

Let me think of this as x = n + (number of powers up to x). Let's denote the number of powers up to x as k. So x = n + k. And k is the number of powers of two up to x. So k = floor(log2(x)) + 1.

But since x = n + k, substituting:

k = floor(log2(n + k)) + 1.

So for a given n, we can find k by solving this equation. But how?

But since k is the number of powers of two up to x, which is up to n +k. For example, for n=7, x=11, k=4. So 4 = floor(log2(11)) +1 = 3+1=4. Correct.

So how can we find k for a given n?

Well, since k is the number of powers up to x =n +k, and since k is at most log2(n +k) +1, but this seems recursive.

But perhaps we can find k by iterating. Let's think of k as being roughly log2(n) + something. For example, for n=7, k=4. For n=1, k=2. For n=2, k=3. For n=3, k=3. For n=4, k=3. For n=5, k=4. So for each n, the k is the number of powers of two up to (n +k). But how can we compute this?

Alternatively, since the number of powers of two up to x is O(log x), and x is n + O(log n), then k is O(log n). So for a given n, we can iterate k from 1 to, say, 32 (since 2^32 is a very large number, and for n up to say 1e6, the k would be small), and find the value of k that satisfies x =n +k, and the number of powers of two up to x is k.

But how?

Alternatively, for a given n, we can compute x as n + the number of powers of two up to x. But since x is not known, perhaps we can approximate x as n + the number of powers of two up to (n + ...). But this seems complicated.

Alternatively, perhaps for any x, the number of powers of two up to x is floor(log2(x)) + 1. So for a given n, we can compute x as n + floor(log2(x)) + 1. But since x depends on log2(x), this is a bit of a loop.

But perhaps we can use a binary search approach. Let me think. Let's assume that x is approximately n + log2(n) + 1. So for example, for n=7, this gives 7 + 2.8 + 1 = 10.8, so x=11. Which is correct. So for a given n, we can start with x = n + log2(n) + 1, and then adjust.

But how to compute this accurately?

Alternatively, for a given n, we can find the x by starting with x =n and incrementing until x is not a power of two. But that's not efficient for large n. However, given that the number of powers of two up to x is small, perhaps we can find x by computing x =n + the number of powers of two up to x. But how?

Alternatively, think that the number of powers of two up to x is k. Then x = n +k. So k is the number of powers of two up to (n +k). So for example, for n=7, k=4, since 7+4=11, and the number of powers up to 11 is 4 (1,2,4,8).

So how to find k for a given n? Let's think of k as being the number of powers of two up to (n +k). But since k is the number of powers up to (n +k), which is floor(log2(n +k)) +1.

So the equation is k = floor(log2(n +k)) + 1.

But solving this equation for k is challenging. However, since k is small compared to n, we can approximate it. For example, let's assume that k is approximately log2(n) + something. So for a given n, we can compute k by iterating from 0 to some upper bound.

For example, for n=7, we can try k=4. Let's see:

n +k = 7 +4 = 11. log2(11) is about 3.459, floor is 3. 3 +1 =4. So yes.

So for a given n, we can compute k by starting with an initial guess and then adjusting.

But how to find k programmatically?

Alternatively, since the number of powers of two up to x is floor(log2(x)) +1, and x =n +k, then for a given n, we can compute k as follows:

We can start with k=0, and increment until the equation holds. But this is not efficient for large n.

Alternatively, since k is the number of powers of two up to (n +k), which is floor(log2(n +k)) +1. So for a given n, we can compute k by binary search.

But perhaps there's a simpler way. For example, since the number of powers of two up to x is m, then x is at least 2^m -1. So for x =n +k, and k = m.

So for example, m is the number of powers of two up to x. So m = floor(log2(x)) +1. So x =n + m.

But m = floor(log2(n +m)) +1.

So how to find m for a given n?

Let me think for a given n, we can try m from 0 upwards. For example, for n=7:

We can try m=3: x=7+3=10. log2(10) is ~3.32, floor is 3. So m is 3+1=4. But we assumed m=3. So not matching. Try m=4: x=7+4=11. log2(11) is ~3.459, floor is 3. 3+1=4. So m=4. So this works.

So for a given n, we can find m such that m = floor(log2(n +m)) +1.

But how to find m?

We can start with an initial guess for m. For example, m can be up to log2(n + m) +1. Since m is the number of powers of two up to x =n +m, and x is at least 2^m. So n +m >= 2^m. So m can be found by solving for m in this inequality. For example, for n=7, m=4, 2^4=16. 7+4=11 <16. So that's not possible. Wait, but x is 11, which is less than 16, but the number of powers of two up to 11 is 4 (1,2,4,8). So 2^0, 2^1, 2^2, 2^3. So m is 4. So the equation is 2^m is 16, which is larger than x=11. So the inequality is not 2^m <=x, but x >=2^{m-1}.

This seems complicated. But perhaps we can find m by iterating from 0 upwards. For a given n, we can try m starting from 0 and see if the equation holds. However, this could be time-consuming for large n. But given that m is small (since for n=1e6, m is about log2(1e6 + m) +1, which is around 20), this is manageable.

So the steps for the code could be:

For a given n, find m such that m = floor(log2(n + m)) + 1.

Once m is found, x is n + m.

But how to find m?

Let me think of m as the number of powers of two up to x =n +m. So m can be calculated as the number of powers of two up to (n +m). So for a given n, we can iterate m from 1 upwards until we find the correct value.

Alternatively, since m is the number of powers of two up to x =n +m, and x is n +m, we can compute m as follows:

We can start with m=0, and then compute x =n +m. Then compute the number of powers of two up to x, which is k. If k == m, then we have found the correct m. Otherwise, we adjust m.

But this seems like a loop.

Alternatively, for a given n, we can compute m as the number of powers of two up to (n + m). But since m is the number of powers of two up to (n +m), and m is approximately log2(n +m), we can approximate m as log2(n) + log2(1 + m/n). For large n, this is roughly log2(n). So for a given n, we can start with m = floor(log2(n)) + 1, and adjust.

But how to implement this in code?

Alternatively, since the number of powers of two up to x is floor(log2(x)) +1, and x =n + m, where m is the number of powers up to x. So m = floor(log2(n + m)) + 1.

We can solve this equation numerically. For example, we can start with an initial guess for m, say m_initial = floor(log2(n)) + 2, and then iterate until m converges.

Let me try for n=7. log2(7) is ~2.8, so m_initial is 2+2=4. Then x=7+4=11. log2(11) is ~3.459, floor is 3. So m=3+1=4. Which matches. So m=4 is correct.

For n=1, log2(1)=0, m_initial is 0+2=2. x=1+2=3. log2(3) is ~1.58, floor is 1. m=1+1=2. Which matches. So m=2.

For n=2, log2(2)=1. m_initial=1+2=3. x=2+3=5. log2(5)=2.32, floor is 2. m=2+1=3. Which matches. So m=3.

So this approach seems to work. So the steps for code would be:

For a given n, compute m_initial as floor(log2(n)) + 2. Then compute x =n +m_initial. Then compute the number of powers of two up to x, which is floor(log2(x)) +1. If this equals m_initial, then m is m_initial. Else, adjust m_initial.

But how to find m?

Alternatively, for a given n, we can compute m by iterating m from 0 upwards until the equation holds. However, since m is small, this is feasible.

But how to compute floor(log2(x))?

In Python, we can use the math module's functions. For example, math.log2(x) returns the base-2 logarithm. Then, taking the floor of that gives us the exponent.

So, for a given x, the number of powers of two up to x is floor(log2(x)) + 1. For example, x=3: log2(3)=1.58, floor is 1. 1+1=2 (powers are 1, 2).

So, the plan is:

For a given n, find m such that m = floor(log2(n + m)) + 1.

Once m is found, the nth polite number is n + m.

So, how to find m?

We can start with m = floor(log2(n)) + 1, and then iterate until the equation holds.

Let me think of a loop:

def find_m(n):
    m = floor(log2(n)) + 1
    while True:
        x = n + m
        k = floor(log2(x)) + 1
        if k == m:
            return m
        elif k < m:
            m = k
        else:
            m +=1

But I'm not sure. Let's test with n=7.

Initially, m = floor(log2(7)) +1 = 2 +1=3.

x =7+3=10. log2(10) is ~3.32, floor is 3. k=3+1=4. So k=4. Which is larger than m=3. So we increase m by 1. Now m=4.

x=7+4=11. log2(11) is ~3.45, floor is 3. k=3+1=4. Which equals m=4. So return 4. Correct.

Another test: n=1.

m_initial = floor(log2(1)) +1=0+1=1.

x=1+1=2. log2(2)=1, floor is 1. k=1+1=2. Which is larger than m=1. So m increases to 2. Now x=1+2=3. log2(3)=1.58, floor is 1. k=1+1=2. Which equals m=2. Return 2. Correct.

Another test: n=2.

m_initial = floor(log2(2)) +1 =1 +1=2.

x=2+2=4. log2(4)=2. k=2+1=3. Which is larger than m=2. So m increases to 3. x=2+3=5. log2(5)=2.32, floor 2. k=2+1=3. Which equals m=3. Return 3. Correct.

Another test: n=3.

m_initial = floor(log2(3)) +1=1+1=2. x=3+2=5. log2(5)=2.32, floor 2. k=3. Which is larger than m=2. So m increases to 3. x=3+3=6. log2(6)=2.58, floor 2. k=3. Which equals m=3. Return 3. So x=6. Which is correct.

So this approach seems to work.

So in code, for a given n, we can compute m by starting with m_initial = floor(log2(n)) +1, then iterate until the equation holds.

Once m is found, x =n +m is the nth polite number.

So the code steps are:

Implement a function to compute the nth polite number:

def nth_polite(n):
    # compute m
    import math
    m = math.floor(math.log2(n)) + 1
    while True:
        x = n + m
        k = math.floor(math.log2(x)) + 1
        if k == m:
            return x
        elif k < m:
            m = k
        else:
            m += 1

Wait, but what if the initial m is not sufficient? For example, let's take n=5. Let's see.

n=5. m_initial is floor(log2(5))=2, so m_initial=2+1=3. x=5+3=8. log2(8) is 3. k=3+1=4. Which is larger than m=3. So m increases to 4. x=5+4=9. log2(9)=3.169, floor is 3. k=3+1=4. Which equals m=4. So return x=9. Which is correct. The fifth polite number is 9.

So this works.

But what about when m_initial is too high? For example, let's say n=4.

m_initial = floor(log2(4)) +1 = 2+1=3. x=4+3=7. log2(7)=2.8, floor 2. k=3. So k=3 == m=3. Return x=7. Which is correct. The fourth polite number is 7.

So this seems to work.

Now, what about for n=100?

Let me think. The 100th polite number is 100 + number of powers of two up to that number. But how?

But according to the formula, it's x =n +m, where m is the number of powers of two up to x.

But for the code, the function will compute it correctly.

So the code for the function is as above. However, there's a problem when n is 0? Well, the problem says to find the nth polite number. Assuming n starts at 1.

Now, the problem says that the function is called is_polite, but the assert is is_polite(7) == 11. Wait, the function is supposed to return the nth polite number. So the function's name is is_polite, but that's confusing. Because the function is_polite(n) returns the nth polite number. But the example says that is_polite(7) is 11. Which matches our code.

So the code for the function is:

import math

def is_polite(n):
    m = math.floor(math.log2(n)) + 1
    while True:
        x = n + m
        k = math.floor(math.log2(x)) + 1
        if k == m:
            return x
        elif k < m:
            m = k
        else:
            m += 1

Wait, but what about cases where the initial m is not correct? Let me test for n=1.

But according to our earlier tests, it works.

But there's a possible problem with math.log2(n) when n is 0. But since n starts from 1, this is okay.

But what about when n is 1, and math.log2(1) is 0. So m_initial is 0+1=1. Then x=1+1=2. log2(2) is 1. k=1+1=2. Which is larger than m=1. So m increases to 2. x=1+2=3. log2(3) is ~1.58. floor is 1. k=1+1=2. Which equals m=2. So returns 3. Correct.

But what about when n is 0? Well, the problem probably expects n to be at least 1.

But according to the problem statement, the example is is_polite(7) == 11, which is correct.

So this code should work.

But there's another possible issue: when x is 1. For example, when n=0? Well, the problem probably doesn't require that.

Now, let's test the code for n=7.

n=7.

m_initial = floor(log2(7)) = 2 (since 2^2=4, 2^3=8). So m_initial = 2+1=3.

x =7+3=10. log2(10) is ~3.32, floor is 3. k=3+1=4. Which is larger than m=3. So m increases to 4. x=7+4=11. log2(11)=3.459, floor is 3. k=3+1=4. Which equals m=4. So return 11. Correct.

So the code works.

Now, what about when n=1?

Yes, returns 3. Correct.

Now, the code seems correct. Now, the code uses math.log2, but what if n is 0? Well, the problem probably expects n to be positive.

But for the problem's purposes, the code should handle n >=1.

But what about when n is very large? For example, n=1e6. The code should handle it.

But what about when x is 0? No, since n is at least 1,
```

</details>

**Code that ran:**

```python
import math

def is_polite(n):
    m = math.floor(math.log2(n)) + 1
    while True:
        x = n + m
        k = math.floor(math.log2(x)) + 1
        if k == m:
            return x
        elif k < m:
            m = k
        else:
            m += 1
```

**Visible-test report:**

```text
PASS    assert is_polite(7) == 11
1 of 1 visible tests passed
```
