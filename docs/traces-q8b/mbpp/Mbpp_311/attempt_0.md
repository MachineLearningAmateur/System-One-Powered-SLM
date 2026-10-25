# Mbpp/311, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/311/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 67.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called set_left_most_unset_bit that takes an integer and returns the number with the leftmost unset bit set. Let's think about how to approach this.

First, let me understand the problem. For example, the input is 10, which is 1010 in binary. The leftmost unset bit here is the third bit from the right (since the bits are counted starting from 0 maybe?), wait, wait. Wait, let's think about the binary representation of 10. Let me write it out:

10 in binary is 1010. Let's list the bits from left to right. Wait, the leftmost bit is the highest bit. So for 10, which is 8+2, the binary is 1010. So the bits are positions 3, 2, 1, 0. So the bits are 1 (position 3), 0 (position 2), 1 (position 1), 0 (position 0). Wait, but the leftmost unset bit here is the bit at position 2 (since it's 0). Wait, but the leftmost unset bit would be the first 0 when looking from the left. Wait, maybe I need to think about the leftmost unset bit as the highest bit that is 0. So for 10 (binary 1010), the leftmost unset bit is the second bit from the left (the third position if counting from 0). Wait, maybe I need to find the position of the first 0 when looking from the left (highest bit to lowest). Wait, but how do I find that?

Alternatively, perhaps the leftmost unset bit is the highest bit that is not set. For example, for 10 (binary 1010), the highest bit is set (the 8's place), but then the next bit is 0. Wait, but the leftmost unset bit would be the highest bit that is 0. Wait, but in 1010, the highest bit is set. So maybe the leftmost unset bit is the first 0 when looking from the left. So for 10, the bits are 1 0 1 0. So the leftmost unset bit is the second bit (the first 0 from the left). But how do I find that?

Alternatively, perhaps the leftmost unset bit is the highest bit that is 0. Wait, but for numbers that are not all ones, there must be some 0s. For example, 10 is 1010. So the highest bit is 8 (bit 3). Then the next bit is 0 (bit 2). So the leftmost unset bit is bit 2. So setting that would give 1110, which is 14. Which matches the sample input.

So the task is to find the leftmost (highest) bit that is 0, and set it to 1.

So how to find that bit?

Let me think. Let's consider that the leftmost unset bit is the first 0 in the binary representation when read from left to right. So for example, 10 is 1010. So the leftmost unset is the second bit (bit 2). How to find that?

One approach is to find the position of the highest bit that is 0. So for a given number, we can find the position of the highest set bit, then check if there are any 0s to the right of that. Wait, but if the number is all ones, then there's no unset bit. But the problem probably assumes that the input has at least one unset bit.

Wait, but the function is supposed to set the leftmost unset bit. So for numbers that are all ones (like 3, which is 11 in binary), there are no unset bits. But maybe the function can return the same number? Or maybe the problem assumes that the input has at least one unset bit. But the sample input 10 has an unset bit.

So how to find the leftmost unset bit?

Let me think about the steps.

First, find the position of the highest set bit. For example, for 10 (binary 1010), the highest set bit is at position 3 (since 8 is 2^3). Then, the next bit is position 2, which is 0. So the leftmost unset bit is position 2. So setting that bit would give 1010 | (1 << 2) = 1010 | 0100 = 1110, which is 14.

So how to find that position?

Another approach: The leftmost unset bit is the first 0 in the binary representation, starting from the highest bit. So, for example, the number 10 is 1010. The highest bit is set. Then the next bit is 0. So that's the leftmost unset.

So the steps could be:

1. Find the position of the highest set bit in the number. Let's call that position m.

2. Then, check the bits from position m down to 0 to find the first 0. But wait, since the highest set bit is m, then the bits from m down to 0 may have some 0s. Wait, but the highest set bit is m, so the bits to the left of m are all 0s. Wait, no. Wait, the highest set bit is the leftmost 1. So for example, 10 is 1010. The highest bit is 8 (position 3). So the bits to the left of that (higher positions) are all 0. So the leftmost unset bit is the first 0 to the left of the highest set bit? Wait, no. Because the highest set bit is the leftmost bit. So the bits to the left of that are zeros. So the leftmost unset bit is the highest bit (which is set), but that's not. Wait, no. Wait, the leftmost bit is set, so the leftmost unset bit is the next bit. Wait, perhaps the leftmost unset bit is the first 0 in the binary representation, starting from the highest bit. So for example, 10 is 1010. The highest bit is 1, then next is 0. So the leftmost unset is that 0.

So how to find that?

An alternative approach: For the given number, find the first 0 in the binary representation when read from left to right. But how to do that programmatically.

Another way: The leftmost unset bit is the position where the number is not all ones up to that position. So, perhaps we can find the position of the first 0 in the binary representation.

Let me think about how to compute this.

Another approach: For the given number, find the position of the highest bit that is 0. Let me think. Let's take the number 10 (binary 1010). The highest bit is 8 (position 3). The next bit is 0 (position 2). So the leftmost unset bit is position 2. So how to find that position?

Wait, if I take the number and compute (number | (number + 1)) ?

Wait, perhaps not. Let me think of another way. Let's think of the number as a binary string. For example, for 10, it's '1010'. We need to find the first '0' from the left. Then set that bit to 1.

But how to find that position.

Alternatively, the leftmost unset bit is the first 0 in the binary representation when read from left to right. So for example, for 10 (binary 1010), the first 0 is at position 1 (if we count from 0 starting at the right). Wait, maybe I need to think about the positions properly.

Wait, the binary of 10 is 1010. Let's write it as 1 0 1 0. So positions from left to right are 3, 2, 1, 0. So the leftmost unset bit is at position 2. So the mask would be 1 << 2, which is 4. Adding that to 10 gives 14.

So how to find that position.

Another approach: The leftmost unset bit is the position where the bit is 0 and all higher bits are 1. Wait, no. For example, in 10 (binary 1010), the leftmost unset bit is at position 2. The higher bits (position 3) are set. So maybe the leftmost unset bit is the first 0 when you look from the highest bit down.

So here's an idea: find the position of the first 0 in the binary representation, starting from the highest bit.

So for a given number, we can find the highest bit that is set. Then, check if that bit is the leftmost. Wait, but the leftmost bit is set, so the first 0 would be the next bit. But how to find that.

Alternatively, here's a way: the leftmost unset bit is the highest bit that is 0. But how to find that. Wait, perhaps the number is not all ones. So the leftmost unset bit is the first 0 in the binary representation when read from left to right.

Another approach: Let's find the position of the leftmost 0 in the binary representation. For example, for 10 (binary 1010), the leftmost 0 is at position 2. How to compute that?

Let me think of the binary representation as a string. For example, 10 is '1010'. So the first 0 is at index 1 (if we start from 0). But how to find that in code.

But converting to binary and checking each bit may not be efficient for large numbers. But for the purpose of this problem, perhaps it's manageable.

But perhaps there's a better way using bitwise operations.

Another idea: The leftmost unset bit is the position where the number is not all ones up to that position. For example, for 10 (binary 1010), the leftmost unset bit is the first 0 in the binary string. So, the mask for that bit is (1 << (position)).

So, perhaps we can find the position of the leftmost 0 by finding the position where the number has a 0, and all higher bits are 1. Wait, not sure.

Alternatively, think of the leftmost unset bit as the position where (number & (1 << pos)) is 0, and for all higher positions (pos +1, etc.), the bits are 1. But how to find that.

Wait, here's a method. Let's find the highest bit that is 0. For example, for 10 (binary 1010), the highest bit is 8 (position 3). Then, the next bit is 0. So the highest bit that is 0 is position 2. How to find that.

Another approach: Let's compute the next power of two after the highest set bit. Wait, perhaps not. Let me think.

Let me think of the number as x. Let's find the position of the highest set bit. Let's say that is m. Then, the leftmost unset bit is the first 0 in the binary representation starting from the highest bit. But since the highest bit is set, the next bit (m-1) could be 0 or 1. So if that bit is 0, then that's the leftmost unset. If it's 1, then check the next bit, and so on.

So the algorithm would be:

1. Find the highest set bit position m.

2. Starting from m-1 down to 0, check each bit. The first 0 found is the leftmost unset bit.

So for example, for x=10 (binary 1010), m is 3 (since 2^3=8 is the highest set bit). Then check position 2: (x & (1 << 2)) is 0, so that's the leftmost unset.

So how to implement this.

First, find m. How to find the highest set bit. In Python, for x, the highest set bit can be found with x.bit_length() -1. For example, 10.bit_length() is 4, so the highest bit is 3 (since 2^3 is 8, which is part of 10).

So m = x.bit_length() -1.

Once we have m, then we can iterate from m-1 down to 0, and check if the bit is 0. The first such bit is the leftmost unset.

Once we find that position, say pos, then the result is x | (1 << pos).

But wait, for example, if x is 10, then m is 3. We check position 2. (x & (1 << 2)) is 0, so we set that bit. So the result is 10 | 4 = 14.

Another example: let's say x is 12 (binary 1100). The highest bit is 3. Then check position 2: (12 & 4) is 4 (non-zero), so check position 1: (12 & 2) is 0. So the leftmost unset bit is position 1. So setting that gives 12 | 2 = 14 (binary 1110). Wait, but the leftmost unset bit in 12 is the first 0 in the binary representation. Let's see: 12 is 1100. The leftmost bit is 1, then next is 1, then 0, then 0. So the leftmost unset is the third bit (position 2). Wait, but according to the algorithm, m is 3 (bit length is 4, so m=3). Then we check position m-1 (2) first. For x=12, (1 << 2) is 4. 12 & 4 is 4 (non-zero), so we check position 1. (1 << 1) is 2. 12 & 2 is 0. So the leftmost unset is position 1. So the result is 12 | 2 = 14. But the leftmost unset bit is position 2? Or position 1? Wait, the binary is 1100. The leftmost unset bit is the first 0 from the left. So the first 0 is at position 2 (since the bits are 1 1 0 0). So the leftmost unset bit is position 2. But according to the algorithm, it's checking position m-1 (which is 2) first. But x & (1 << 2) is 4, which is non-zero. So the algorithm would check position 1 next. But that's a 0. So according to the algorithm, the leftmost unset bit is position 1. But that's not correct. Because the first 0 from the left is position 2. Wait, what's the problem here?

Wait, in the example of 12 (binary 1100), the leftmost unset bit is the first 0 when looking from the left. Let's look at the bits:

Position 3: 1 (bit 3 is 8)
Position 2: 1 (bit 2 is 4)
Position 1: 0 (bit 1 is 2)
Position 0: 0 (bit 0 is 1)

So the leftmost unset bit is position 2? Or position 1?

Wait, the leftmost unset bit is the first 0 when looking from the left. So for binary 1100, the leftmost bit is 1, then next is 1, then 0. So the first 0 is at position 2. So the algorithm's approach is wrong here. Because in this case, the algorithm would check position m-1 (which is 3-1=2). The bit at position 2 is 1. So the algorithm would then check position 1. But that's a 0. So according to the algorithm, the leftmost unset bit is position 1. But that's not correct. Because the first 0 is at position 2. Wait, but why is that?

Wait, perhaps I have a misunderstanding of the positions. Let me clarify:

The positions are numbered from 0 (LSB) to higher. So for 12 (binary 1100), the bits are:

bit 3: 1 (8)
bit 2: 1 (4)
bit 1: 0 (2)
bit 0: 0 (1)

So the binary is 1100. So the leftmost bit is bit 3. The leftmost unset bit is the first 0 when scanning from left to right. So in this case, the first 0 is at bit 2. Wait, no. Wait, the bits are written as 1 (bit3), 1 (bit2), 0 (bit1), 0 (bit0). So when you look from left to right, the first 0 is at bit2. But according to the algorithm, we check from m-1 down to 0. For m=3, the code would check position 2 (bit2) first. But in this case, the bit is 1. So the code would check position 1 (bit1), which is 0. But that's not the leftmost unset bit. So the algorithm is wrong here.

So the algorithm's approach is incorrect. So why? Because the code is looking for the first 0 starting from the highest bit (m-1) down. But in this example, the first 0 is at position 2 (bit2), but the code is checking position 2 and finds it's set. So the code would proceed to check lower positions.

So this suggests that the algorithm is incorrect. So what's the problem here?

Ah, I think I made a mistake in how I'm calculating the highest bit. Let me re-examine. For x=12, the binary is 1100. The bit_length is 4, so the highest set bit is 3 (since 2^3 = 8). So the highest bit is position 3. Then, the code checks position m-1 (which is 3-1=2). The bit at position 2 is 1 (since 4 is part of 12). So the code would check that. Then, check position 1 (bit1), which is 0. So the code would return that. But that's not the leftmost unset bit. So the code's approach is wrong.

So the problem is that the code is checking from the highest bit (m) down to 0, but the leftmost unset bit is the first 0 in the binary representation when read from left to right. So for 12, the first 0 is at position 2, but the code is not finding it. Wait, why? Because the code is checking from m-1 (which is 2) down to 0. Wait, for m=3 (highest set bit), the code starts checking position m-1 (which is 2). For x=12, that bit is set. So the code proceeds to check position 1. So the code is looking for the first 0 in the positions from m-1 down to 0. But that's not the same as the leftmost unset bit. Because the leftmost unset bit is the first 0 when reading from left to right, which would be the first 0 in the highest positions. So in this case, the code is missing that.

So how to find the first 0 in the binary representation when read from left to right.

Another idea: The leftmost unset bit is the highest position where the bit is 0. So for example, for 12 (binary 1100), the highest position where the bit is 0 is position 1. But that's not correct. Wait, no. Because the leftmost unset bit is the first 0 when scanning from left to right. For binary 1100, the leftmost 0 is at position 2 (bit2). But that's not the case. Wait, the binary is 1100. So the leftmost bit is 1, then next is 1, then 0, then 0. So the first 0 is at position 2 (the third bit from the left). But according to the code's approach, it's not finding that. So why?

Because the code is checking positions starting from m-1 (position 2). For x=12, the bit at position 2 is 1. So the code would check lower positions. So the code is not finding the first 0 in the leftmost positions.

So this suggests that the algorithm is incorrect.

So how to find the leftmost unset bit.

Alternative approach: For the given number, the leftmost unset bit is the first position where the bit is 0, starting from the highest bit. So for example, in 12 (binary 1100), the highest bit is 3 (position 3). The next bit (position 2) is 1, then position 1 is 0. So the leftmost unset bit is position 1. But that's not correct. Because the first 0 in the left to right scan is at position 2. Wait, no. Wait, the binary is 1100. So the leftmost bit is position 3 (1), then position 2 (1), then position 1 (0), then position 0 (0). So the first 0 is at position 1. Wait, no! Because the left to right scan would see the first 0 at position 2? Or position 1?

Wait, the binary representation is 1100. So the bits are:

bit 3 (value 8): 1

bit 2 (value 4): 1

bit 1 (value 2): 0

bit 0 (value 1): 0

So when you read the binary from left to right, the first 0 is the third bit (bit 2). Wait, no. The binary is 1100. The first two bits are 1s, then 0s. So the first 0 is the third bit (bit 2). Wait, but that's the second position from the left. So the leftmost unset bit is the third bit (bit 2). But according to the code's approach, the code is checking position m-1 (which is 3-1=2), which is bit 2. But in this case, the bit is 1. So the code would check lower positions. So the code is not finding the correct position.

So why is that? Because the code is looking for the first 0 in the positions from m-1 down to 0, but in this case, the first 0 is in position 2, but the code is checking that position and finds it's set. So why?

Because the code's logic is wrong. The problem is that the highest set bit is m, but the bits to the left of that are not considered. Wait, but the highest set bit is m, so the bits higher than m are zero. So for example, in the case of 12 (binary 1100), the highest set bit is m=3. So the bits higher than m are zero, but the bits from m down to 0 are 1, 1, 0, 0. So the leftmost unset bit is the first 0 in the sequence of bits starting from the highest set bit. So for 12, the first 0 is at position 2 (bit2). But the code's approach checks position m-1 (which is 2), which is 1, so it proceeds to check lower positions. So the code is not finding the correct position. Hence, the algorithm is incorrect.

So what is wrong here? The algorithm is trying to find the first 0 in the positions from m-1 down to 0. But for the example of 12, the first 0 is at position 2, but the code is checking position 2 and finds it's set, so proceeds to check lower positions. Hence, the code is wrong.

Ah, I see now. The code is looking for the first 0 in the positions from m-1 down to 0. But in this example, the first 0 is at position 2. However, the code is checking position m-1 (which is 2) and sees that the bit is 1. So it proceeds to check lower positions. So the code is missing the correct position.

So why is the bit at position 2 set in this case? Because 12 is 1100. So 1 << 2 is 4, and 12 & 4 is 4, which is not zero. So the code is correct in that the bit is set. So the first 0 is not at position 2, but lower. So the code is correct. But that contradicts the earlier assumption that the first 0 is at position 2.

Wait, this suggests that the earlier assumption about the leftmost unset bit was incorrect. So what is the correct leftmost unset bit in this case?

For x=12 (binary 1100), the leftmost unset bit is the first 0 when reading from left to right. Let's look at the binary: 1 1 0 0. The first 0 is the third bit (position 2). But in the code's approach, the bit at position 2 is set. So that's not possible. So there's a mistake here.

Wait, no. Let me calculate the value of the bit at position 2 for x=12. 12 is 8+4=12. So the bits are 8 (bit3), 4 (bit2), 2 (bit1), 1 (bit0). So for 12, bit2 is 1 (since 4 is part of 12). So the binary is 1100. So the first 0 is at bit1. So the leftmost unset bit is bit1. So the code is correct. So earlier assumption was wrong. So the leftmost unset bit is the first 0 when scanning from left to right. For 12 (1100), the first 0 is at position 1 (the third bit from the right). So the code's approach is correct.

But then why did I think that the first 0 is at position 2? Because I was counting the positions incorrectly. So the code is correct. So for 12, the leftmost unset bit is position 1. So the code would set that bit, resulting in 12 | 2 = 14 (binary 1110). Which is correct.

So the algorithm is correct. So the earlier confusion was due to a mistake in counting positions.

So the algorithm is:

Find the highest set bit m.

Check from position m-1 down to 0 for the first 0. Once found, set that bit.

So the steps are:

For a given x:

1. Find m = x.bit_length() - 1.

2. For pos in range(m-1, -1, -1):

   if (x & (1 << pos)) == 0:

       return x | (1 << pos)

So for x=10 (binary 1010), m is 3. Check pos 2: 10 & (1<<2) is 4, which is non-zero. So check pos 1: 10 & (1<<1) is 2, non-zero. Check pos 0: 10 & 1 is 0. So the first 0 is at pos 0. So the result is 10 | 1 = 11 (binary 1011). But this contradicts the sample input. Wait, what? Because the sample input says set_left_most_unset_bit(10) == 14. But according to this algorithm, the result is 10 | 1 = 11. So there's a problem here.

Wait, this suggests that the algorithm is incorrect. So why?

Wait, let's re-examine the sample input. The sample input is 10 (binary 1010). The sample output is 14 (binary 1110). So the leftmost unset bit is the second bit from the left (bit 2). But according to the algorithm, the code would check positions m-1 down to 0, which for m=3 is 2, 1, 0.

Let's see:

For x=10, which is 1010 in binary:

m = 3 (bit_length is 4, so 4-1=3).

Check pos=2: 1 << 2 is 4. 10 & 4 = 4 != 0 → continue.

Check pos=1: 1 << 1 is 2. 10 & 2 = 2 != 0 → continue.

Check pos=0: 1 << 0 is 1. 10 & 1 = 0 → found. So set that bit. Result is 10 | 1 = 11. But the sample expects 14. So the algorithm is wrong.

But according to the sample input, the correct answer is 14. So what's wrong here?

Ah, this suggests that the algorithm is incorrect. So what is the correct way to find the leftmost unset bit?

Let me re-examine the sample input. For x=10 (binary 1010), the leftmost unset bit is the second bit (bit2). So setting that bit would give 1010 | 0100 = 1110 (14). So the algorithm must find that bit. But according to the previous algorithm, it is not finding it. So why?

Because in the previous algorithm, the code is checking from m-1 down to 0. For m=3, the code checks pos=2, which is 1 (bit2 is set), then pos=1 (bit1 is set), then pos=0 (bit0 is 0). So the algorithm is finding the leftmost unset bit as pos=0, but that's not the case. So why is the algorithm not finding the correct position?

Ah! Oh no! Because the leftmost unset bit is the first unset bit when reading from left to right. For x=10 (binary 1010), the leftmost unset bit is the second bit (bit2). But according to the algorithm, it's checking from pos=2 down to 0. The bit at pos=2 is set, so the algorithm continues to check lower positions. But the leftmost unset bit is at pos=2. So why is it set?

Wait, no. For x=10 (binary 1010), the bit at pos=2 is 0. Wait, no! Wait, 10 in binary is 1010. Let's break it down:

bit3 (8) is 1.

bit2 (4) is 0.

bit1 (2) is 1.

bit0 (1) is 0.

Ah! So the binary is 1 0 1 0. So the leftmost unset bit is at pos=2 (bit2). So why is the algorithm not finding it?

Because when the code checks pos=2, it checks if (x & (1 << pos)) == 0. For x=10, (1 << 2) is 4. 10 & 4 is 4, which is not zero. So the algorithm thinks that bit2 is set, but it's actually 0. Wait, this is a contradiction. What's the actual value of 10 in binary?

Let me compute 10 in binary. 10 divided by 2 is 5 remainder 0. 5 divided by 2 is 2 remainder 1. 2 divided by 2 is 1 remainder 0. 1 divided by 2 is 0 remainder 1. So the binary is 1010. So bits are:

bit3: 1 (8)

bit2: 0 (4)

bit1: 1 (2)

bit0: 0 (1)

So 10 is 1010. So the bit at position 2 is 0. So why is (10 & (1 << 2)) equal to 4?

Because 1 << 2 is 4. 10 & 4 is 4. But 4 is not zero. So this suggests that the bit is set. But according to the binary, it's 0. What's wrong here?

Ah! Oh no! I think I have a misunderstanding of the bit positions. Let me clarify:

The value of (1 << pos) is 2^pos. So for pos=2, it's 4. The bit at position 2 is the third bit from the right. For example, for the binary 1010, the bits are:

pos 3: 1 (8)

pos 2: 0 (4)

pos 1: 1 (2)

pos 0: 0 (1)

So when we do 10 & (1 << 2) = 10 & 4 = 4. But since the bit at position 2 is 0, why is the result 4?

Wait, this is a contradiction. What is 10 in binary? Let's compute it.

10 in binary is 1010. So the bits are:

bit3: 1 (8)

bit2: 0 (4)

bit1: 1 (2)

bit0: 0 (1)

So the value of bit2 is 0. So (x & (1 << 2)) should be 0. But 10 & 4 is 4. What's going on here?

Wait, no! Wait, 10 in binary is 1010. Let me calculate 10 & 4:

4 is 0100 in binary. 10 is 1010. AND is 0000? No, 1010 & 0100 is 0000? Or 0010? Wait, no. Let me do the binary AND:

1010 (10)

0100 (4)

AND is 0000? No, because the bits are:

1st bit: 1 & 0 = 0

2nd bit: 0 & 1 = 0?

Wait, no. Let me write it properly.

Let me write the binary numbers aligned:

10 is 1010 (binary)

4 is 0100 (binary)

So the AND is:

1 0 1 0

0 1 0 0

AND:

0 0 0 0 → which is 0. So 10 & 4 is 0. So why did I think earlier that 10 & 4 is 4?

Ah! I made a mistake in the calculation. So for x=10, (x & (1 << 2)) is 0. So the code would find that the bit at pos=2 is 0. So the algorithm would return that. So the code would set that bit, giving 10 | 4 = 14. Which matches the sample.

So where did the earlier mistake occur? When I said that 10 & 4 is 4. That was incorrect. The correct calculation is 10 & 4 = 0.

So this suggests that the algorithm is correct.

Let me re-calculate for x=10.

m = x.bit_length() - 1 → 4-1=3.

Then, for pos in range(m-1, -1, -1):

pos=2: check if (10 & (1<<2)) == 0 → 10 & 4 → 0 → yes. So return 10 | (1<<2) = 10 +4=14. Which is correct.

So the earlier mistake was due to a miscalculation of 10 & 4. So the algorithm is correct.

So the algorithm works for the sample input.

Let me recheck for x=12 (binary 1100). m is 3. So check pos=2: 12 & 4 → 4 != 0 → continue. pos=1: 12 & 2 → 0. So set that bit. Result is 12 | 2 = 14 (binary 1110). Which is correct. The leftmost unset bit is pos=1.

So the algorithm is correct.

So the steps are:

1. Find m as x.bit_length() -1.

2. Iterate from pos = m-1 down to 0:

   if (x & (1 << pos)) == 0:

       return x | (1 << pos)

3. If no such pos is found (which should not happen for numbers with at least one unset bit), return x.

So the code can be written as follows.

Now, the code:

def set_left_most_unset_bit(x):
    m = x.bit_length() - 1
    for pos in range(m-1, -1, -1):
        if (x & (1 << pos)) == 0:
            return x | (1 << pos)
    return x  # if all bits are set, but
```

</details>

**Code that ran:**

```python
def set_left_most_unset_bit(x):
    m = x.bit_length() - 1
    for pos in range(m - 1, -1, -1):
        if (x & (1 << pos)) == 0:
            return x | (1 << pos)
    return x
```

**Visible-test report:**

```text
PASS    assert set_left_most_unset_bit(10) == 14
1 of 1 visible tests passed
```
