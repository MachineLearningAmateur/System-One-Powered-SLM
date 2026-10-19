# HumanEval/99, attempt 1

1 round; visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking).

## Round 1 (`HumanEval/99/a1/r1`)

Visible tests: **pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 686.

<details><summary>Thinking</summary>

```text
Okay, I need to solve this problem where the function closest_integer takes a string representing a number and returns the closest integer. But if it's equidistant between two integers, I have to round away from zero. Let me think about how to approach this.

First, I need to parse the input string. The input could be something like "10", "15.3", "-14.5", etc. So I need to convert this string into a float. Then, I have to find the closest integer. But how?

Let me think about the steps:

1. Convert the input string to a float. For example, "15.3" becomes 15.3.
2. Find the closest integer. The closest integer would be the integer part if the decimal is less than 0.5, or the next integer if it's 0.5 or more. But wait, there's a catch when the number is exactly halfway between two integers. For example, 14.5 should round to 15, and -14.5 should round to -15.

So, the standard rounding rules are: if the fractional part is less than 0.5, round down. If it's 0.5 or more, round up. But when it's exactly 0.5, we need to round away from zero. So for positive numbers, if it's exactly 0.5, round up. For negative numbers, if it's exactly 0.5, round down (since -0.5 would be -1, but wait, no. Wait, for example, -14.5: the distance to -14 is 0.5, and to -15 is 0.5. So according to the note, we should round away from zero. So for -14.5, the closest is -15. So how to handle that?

So the key is that when the fractional part is exactly 0.5, we round away from zero. So for positive numbers, if the fractional part is 0.5, round up. For negative numbers, if the fractional part is 0.5, round down (since that's away from zero). Wait, but for -14.5, the distance to -15 is 0.5, and to -14 is 0.5. So the correct choice is -15. So for negative numbers, when the fractional part is 0.5, we round down (towards negative infinity), but for positive numbers, round up (towards positive infinity).

So how to implement this?

Let me think about the steps again. Let's take the value as a float. Let's compute the integer part and the fractional part.

For example, for 14.5, the integer part is 14, fractional part is 0.5. So we need to round up to 15.

For -14.5, the integer part is -14, fractional part is 0.5. So we need to round down to -15.

So, how to compute that?

One approach is to check if the fractional part is 0.5. If so, then round up or down based on the sign.

But how to compute the fractional part? Well, in Python, we can do something like:

value = float(input_str)

integer_part = int(value)
fractional_part = value - integer_part

But wait, for example, 14.5 would have fractional_part as 0.5. So, if fractional_part is exactly 0.5, then we need to round away from zero.

So, the steps would be:

- Check if the fractional part is exactly 0.5. If yes, then round up if positive, down if negative.

But how to handle that?

Another approach is to compute the rounded value as follows:

If the value is positive, then if the fractional part is 0.5, round up. Else, round normally.

If the value is negative, then if the fractional part is 0.5, round down. Else, round normally.

Wait, but how to compute the rounded value?

Alternatively, we can use the built-in round function, but with a twist. Because the standard round function rounds to the nearest even integer when the fractional part is exactly 0.5. For example, round(14.5) is 14, round(15.5) is 16, round(-14.5) is -14, round(-15.5) is -16. But according to the problem statement, when the number is exactly halfway between two integers, we need to round away from zero. So for 14.5, round up to 15, and for -14.5, round down to -15.

So the standard round function is not sufficient here. So we need to handle that case manually.

So, here's the plan:

1. Convert the input string to a float.
2. Check if the fractional part is exactly 0.5. If yes, then round away from zero.
3. Otherwise, round normally.

But how to check if the fractional part is exactly 0.5?

Let me think. For example, for 14.5, the fractional part is 0.5. For 14.5, the value is 14.5. So, when we subtract the integer part, we get 0.5. So, if the fractional part is 0.5, then we need to round away from zero.

So, the code steps:

value = float(input_str)

integer_part = int(value)

fractional_part = value - integer_part

if fractional_part == 0.5:

   if value > 0:

       return integer_part + 1

   else:

       return integer_part - 1

else:

   if fractional_part < 0.5:

       return integer_part

   else:

       return integer_part + 1

Wait, but for example, if the value is 14.5, then integer_part is 14, fractional_part is 0.5. So we add 1, giving 15. For -14.5, integer_part is -14, fractional_part is 0.5. So we subtract 1, giving -15. That's correct.

But what about numbers like 14.499999999999999? Then fractional_part is 0.499999999999999, which is less than 0.5. So we round down. But if it's 14.5, then we round up.

But how to handle the case where the value is exactly halfway between two integers. For example, 14.5 and -14.5.

So, the code would be:

def closest_integer(value):

    # convert to float

    val = float(value)

    integer_part = int(val)

    fractional_part = val - integer_part

    if fractional_part == 0.5:

        if val > 0:

            return integer_part + 1

        else:

            return integer_part - 1

    else:

        if fractional_part < 0.5:

            return integer_part

        else:

            return integer_part + 1

Wait, but what if the value is something like 14.5? Let's test.

For val = 14.5, integer_part is 14, fractional_part is 0.5. So returns 15. Correct.

For val = -14.5, integer_part is -14, fractional_part is 0.5. So returns -15. Correct.

What about val = 15.5? Then, returns 16. Correct.

What about val = 15.4? fractional_part is 0.4, so returns 15. Correct.

What about val = 15.6? fractional_part is 0.6, returns 16. Correct.

But what about when the value is something like 15.5? Then, returns 16. Correct.

But what about when the value is 15.5, but the integer part is 15. So, the code would check fractional_part is 0.5, then return 16. Correct.

But what about when the value is 0.5? Then, integer_part is 0, fractional_part is 0.5. So returns 0 +1 = 1. Which is correct.

But wait, for 0.5, the code returns 1. Which is correct. Because 0.5 is exactly between 0 and 1. So round away from zero, which is 1.

But what about for -0.5? Then, integer_part is -1, fractional_part is 0.5. So returns -1 -1 = -2. Which is correct, since -0.5 is equidistant between -1 and 0. So round away from zero, which is -1? Wait, no. Wait, -0.5 is exactly between -1 and 0. So according to the problem statement, the correct answer is -1? Or -2?

Wait, the problem says that if the number is equidistant from two integers, round away from zero. So for -0.5, the distance to -1 is 0.5, and to 0 is 0.5. So the correct choice is -1 (since that's the one further from zero). Wait, no. Wait, the distance from -0.5 to -1 is 0.5, and to 0 is 0.5. So the two integers are -1 and 0. The one further from zero is 0. So the correct answer is 0? But according to the note, for -14.5, the correct answer is -15. So for -0.5, the correct answer is 0? But according to the problem statement, the note says that for -14.5, the answer is -15. So for -0.5, the answer would be 0. But according to the code, when val is -0.5, integer_part is -1, fractional_part is 0.5. So code returns integer_part -1, which is -1 -1 = -2. Which is wrong.

Wait, that's a problem. So the code as written would return -2 for -0.5, but the correct answer should be 0.

So, what's wrong here?

Ah, because in the code, when the fractional part is 0.5, we check the sign of the value. For positive numbers, we round up, for negative numbers, we round down. But for -0.5, the code would return integer_part -1, which is -1 -1 = -2. But the correct answer is 0.

Wait, but according to the problem statement, the note says that for -14.5, the answer is -15. So for -0.5, the answer is 0. So the code as written would return -2, which is wrong.

So, there's a mistake here. How to fix this?

The problem is that the code's logic for negative numbers is not correct. Let's think again.

The code says: if fractional_part is 0.5, then:

if val > 0: round up.

else: round down.

But for val = -0.5, which is -0.5, the code returns integer_part -1, which is -1 -1 = -2. But the correct answer is 0.

So, the code's logic is incorrect for negative numbers.

So, what's the correct way to round away from zero when the fractional part is 0.5?

For example, for -0.5, the two integers are -1 and 0. The distance from -0.5 to -1 is 0.5, and to 0 is 0.5. So the correct choice is the one that is further from zero. Which is 0. So the code should return 0.

But how to handle that?

So, the problem is that for negative numbers, when the fractional part is 0.5, we need to round to the integer that is further from zero. So for -0.5, the correct answer is 0. For -14.5, the correct answer is -15.

So, how to adjust the code?

The code needs to check if the value is positive or negative, and then decide whether to round up or down. But for negative numbers, when the fractional part is 0.5, we need to round down (towards negative infinity) if the value is negative. Wait, but for -0.5, the correct answer is 0. So, how to get that?

Wait, perhaps the code should round away from zero, which for negative numbers would be to round towards negative infinity. But how?

Alternatively, for any value that is exactly halfway between two integers, the code should round to the integer that is further from zero. So for positive numbers, that's up. For negative numbers, that's down. Wait, no. For -0.5, the further from zero is 0. So for negative numbers, when the fractional part is 0.5, the code should round to the integer that is further from zero. So for -0.5, that's 0. For -14.5, that's -15. So how to compute that?

So, the code should check the sign of the value. If the value is positive, then round up. If the value is negative, round down. But how does that work?

Wait, for -0.5, the code would round down (since it's negative) to -1. But that's not correct. So that's not the right approach.

Wait, maybe the correct approach is to round away from zero. For positive numbers, that's up. For negative numbers, that's down. But for -0.5, that's down, but the correct answer is 0. So that's not correct.

Hmm, this is a problem. How to handle this case?

Alternative approach: when the fractional part is exactly 0.5, then the correct rounding is to round to the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. But how to compute that?

So, for example, for a value of -0.5, the two integers are -1 and 0. The one further from zero is 0. So the code should return 0. For -14.5, the code returns -15.

So, for a value that is exactly halfway between two integers, the code should return the integer that is further from zero.

So, how to compute that?

Let me think. For any value, the two integers are floor(val) and ceil(val). For example, 14.5's floor is 14, ceil is 15. For -14.5, floor is -15, ceil is -14.

So, the code can compute the two integers, and then check which one is further from zero.

But how to do that?

So, for a given value, the two integers are:

integer_floor = int(val) if val is not integer, else val.

But wait, for example, val = 14.5, integer_floor is 14, and integer_ceil is 15.

So, the code can compute the two integers, then check which one is further from zero.

But how to compute that in code.

Alternatively, for a value that is exactly halfway between two integers, the code can check the sign of the value and round accordingly.

But how to handle that.

Let me think again. For a value that is exactly halfway between two integers, the code should round to the one that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer.

So, for example:

val = 14.5 → higher integer is 15 → correct.

val = -14.5 → lower integer is -15 → correct.

val = -0.5 → lower integer is -1 → but that's not correct. Wait, but -0.5 is exactly between -1 and 0. So the code should return 0. So the lower integer is -1, but that's not the one further from zero. So this approach is not working.

Wait, the problem is that for -0.5, the two integers are -1 and 0. The one further from zero is 0. So the code should return 0.

So how to handle this?

So, the code needs to check if the value is positive or negative, and then decide whether to round up or down. But for the case where the value is exactly halfway, the code must choose the direction that is away from zero.

So, for positive numbers, if the fractional part is 0.5, round up. For negative numbers, if the fractional part is 0.5, round down. But in the case of -0.5, that would round down to -1, but the correct answer is 0. So this approach is not working.

So what's the problem here?

Ah, because for -0.5, the code would round down (since it's negative) to -1, but the correct answer is 0. So the code's logic is wrong here.

So, what's the correct way to handle this?

The key is that when the value is exactly halfway between two integers, the code should round to the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. But for -0.5, the lower integer is -1, but that's not further from zero. So this approach is not correct.

Wait, no. For -0.5, the two integers are -1 and 0. The distance from -0.5 to -1 is 0.5, and to 0 is 0.5. So the one further from zero is 0. So the code should return 0.

So, for negative numbers, when the value is exactly halfway between two integers, the code should round to the integer that is further from zero. Which is the same as the integer that is closest to zero. So for negative numbers, when the value is exactly halfway between two integers, the code should round to the one that is closer to zero. Wait, but that's the opposite of what the problem says.

Wait, the problem says that when the value is equidistant from two integers, round away from zero. So for -0.5, the code should round away from zero. Which is to round to the integer that is further from zero. But for -0.5, the further from zero is 0, which is the correct answer. So how to find that?

So, for any value that is exactly halfway between two integers, the code should round to the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. Wait, no. For -0.5, the lower integer is -1, which is further from zero than 0? No. Wait, -0.5 is 0.5 away from -1 and 0.5 away from 0. So the further from zero is 0. So the code should return 0.

So, for negative numbers, when the value is exactly halfway between two integers, the code should round to the integer that is further from zero. Which is the one that is closer to zero. So for -0.5, the code should return 0.

But how to compute that.

So, for any value that is exactly halfway between two integers, the code should return the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. Wait, but for -0.5, the lower integer is -1, which is further from zero than 0. No, that's not right. -1 is further from zero than 0? No. Wait, the distance from -0.5 to -1 is 0.5, and to 0 is 0.5. So the two integers are equally distant. So the code needs to choose the one that is further from zero. Which is 0. So for negative numbers, when the value is exactly halfway between two integers, the code should round to the integer that is closer to zero. Which is the one that is further from zero? No. Wait, the code needs to round away from zero. So for -0.5, the code should round to the integer that is further from zero. Which is 0. So how to determine that.

This is getting complicated. Maybe there's a better way to handle this.

Alternative approach: for any value, the code can compute the nearest integer, but if it's exactly halfway, then round away from zero. So, for example, for 14.5, the code rounds to 15. For -14.5, rounds to -15. For -0.5, rounds to 0. How to do that?

So, the code can check if the fractional part is exactly 0.5. If so, then:

if the value is positive, round up.

if the value is negative, round down.

But for -0.5, this would round down to -1, but the correct answer is 0. So this approach is not correct.

Wait, but maybe the code should check if the value is positive or negative, and if the fractional part is 0.5, then round up if positive, round down if negative, but for negative numbers, when the fractional part is 0.5, the code should round to the integer that is further from zero. Which for -0.5 is 0.

So how to compute that.

Another idea: when the value is exactly halfway between two integers, the code should round to the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. Wait, but for -0.5, the lower integer is -1, which is further from zero than 0? No, because -0.5 is 0.5 away from -1 and 0.5 away from 0. So the further from zero is 0. So the code should return 0. But how to get that.

So, for a value that is exactly halfway between two integers, the code should return the integer that is further from zero. So, for positive numbers, the higher integer. For negative numbers, the lower integer. Wait, but that's not correct. For example, -0.5 is exactly halfway between -1 and 0. The further from zero is 0. So the code should return 0. But according to this logic, the lower integer is -1, which is further from zero than 0? No. Wait, the distance from 0 to -0.5 is 0.5. The distance from -1 to -0.5 is 0.5. So both are equally distant. So the code should return the one that is further from zero, which is 0.

So, how to compute that.

Maybe the code can check if the value is positive or negative, and then decide based on that.

For example:

if the value is positive, and the fractional part is 0.5, round up.

if the value is negative, and the fractional part is 0.5, round down.

But for -0.5, this would round down to -1, which is not correct. So this approach is not working.

Alternative approach: when the value is exactly halfway between two integers, the code should round to the integer that is further from zero. So, for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. But how to compute that.

So, for example, for -0.5, the lower integer is -1. But that's not further from zero. So this approach is not correct.

Wait, perhaps the code should round to the integer that is further from zero. So for any value that is exactly halfway between two integers, the code should return the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. But how to compute that.

So, for a value that is exactly halfway between two integers, the code can compute the two integers and choose the one that is further from zero.

So, for example, for 14.5, the two integers are 14 and 15. 15 is further from zero, so return 15.

For -14.5, the two integers are -15 and -14. -15 is further from zero, so return -15.

For -0.5, the two integers are -1 and 0. 0 is further from zero, so return 0.

So, how to implement this in code.

So, the code can compute the two integers (floor and ceil), and then compare which one is further from zero.

But how to compute floor and ceil.

In Python, for a float value, the floor is int(value) if the value is not integer, but for example, 14.5's floor is 14. The ceil is 15.

So, for any value, the floor is int(val) if val is not integer, else val. But how to compute floor and ceil.

Alternatively, the code can use math.floor and math.ceil.

So, for a given value, compute floor_val = math.floor(val), ceil_val = math.ceil(val).

Then, compare which of the two is further from zero.

But how to compute that.

For example, for val = 14.5:

floor_val = 14, ceil_val = 15. 15 is further from zero, so return 15.

For val = -14.5:

floor_val = -15, ceil_val = -14. -15 is further from zero (since it's more negative), so return -15.

For val = -0.5:

floor_val = -1, ceil_val = 0. 0 is further from zero, so return 0.

So, the code can do this:

import math

def closest_integer(value):

    val = float(value)

    floor_val = math.floor(val)

    ceil_val = math.ceil(val)

    if val == floor_val + 0.5:

        # exactly halfway between floor_val and ceil_val

        if val > 0:

            return ceil_val

        else:

            return floor_val if val < 0 else ceil_val

    else:

        if val < floor_val:

            # val is between floor_val and floor_val + 1, but not exactly halfway

            # so round to floor_val if fractional part is < 0.5, else ceil_val

            if val - floor_val < 0.5:

                return floor_val

            else:

                return ceil_val

        else:

            # val is between ceil_val and ceil_val - 1?

            # not sure, but perhaps the code can check if the fractional part is 0.5.

            # but this is getting complicated.

Wait, maybe this approach is better. So, for any value, if it is exactly halfway between two integers, then return the one that is further from zero. Else, round normally.

But how to check if it's exactly halfway.

So, for example, val = 14.5, then val - floor_val = 0.5. So, check if the fractional part is exactly 0.5.

So, the code can check if the fractional part is 0.5. If so, then return the one that is further from zero. Otherwise, round normally.

But how to compute the fractional part.

So, the code can compute:

fractional_part = val - floor_val

if fractional_part == 0.5:

    if val > 0:

        return ceil_val

    else:

        return floor_val if val < 0 else ceil_val

But wait, for val = -0.5, floor_val is -1, ceil_val is 0. So, val is -0.5. So, the code returns floor_val if val < 0? No, because val is -0.5, which is less than 0. So, the code returns floor_val, which is -1. But that's not correct. So the code would return -1 for -0.5, but the correct answer is 0.

So, this approach is not working.

Hmm. This is really tricky.

Alternative idea: when the value is exactly halfway between two integers, the code should round away from zero. So, for positive numbers, round up. For negative numbers, round down. But for -0.5, that would round down to -1, which is not correct. But according to the problem statement, for -14.5, the code rounds to -15, which is correct.

Wait, but for -0.5, the code rounds to -1, which is not the correct answer. So why is that?

Ah, because the problem statement says that when the number is equidistant from two integers, round away from zero. So for -0.5, which is equidistant between -1 and 0, the code should round away from zero. Which would be to round to -1 (since that's the one away from zero? No. Wait, the away from zero would mean the direction that is not zero. So for -0.5, the away from zero would be to round to -1 or 0? Which one is further from zero?

The distance from -0.5 to -1 is 0.5, and to 0 is 0.5. So the away from zero is the one that is further from zero. So for -0.5, the correct answer is 0. So the code should return 0.

But according to the problem statement, the note says that for -14.5, the code should return -15. So for -14.5, which is equidistant between -15 and -14, the code rounds away from zero, which is -15.

So, for -0.5, the code should return 0.

So, how to handle this case.

Maybe the code should check if the value is positive or negative, and if it's exactly halfway, then round to the direction that is away from zero. For positive numbers, that's up. For negative numbers, that's down. But for -0.5, this would round down to -1, which is not correct.

So, what's the correct way to handle this?

Maybe the code should round to the direction that is away from zero, regardless of the sign. For example, if the value is exactly halfway between two integers, round away from zero. So, for -0.5, the code should round to the integer that is further from zero. Which is 0.

So, how to compute that.

Another idea: for any value that is exactly halfway between two integers, the code should round to the integer that is further from zero. So, for positive numbers, the higher integer. For negative numbers, the lower integer. Wait, but for -0.5, the lower integer is -1, which is further from zero than 0? No, the distance from 0 to -0.5 is 0.5, and from -1 to -0.5 is 0.5. So the further from zero is 0. So the code should return 0.

So, the code should round to the integer that is further from zero. So for positive numbers, that's the higher integer. For negative numbers, that's the lower integer. But for -0.5, the lower integer is -1, which is further from zero than 0? No. So this is not correct.

This is really challenging. Maybe I should look for a way to implement the rounding correctly.

Another approach: the code can check if the value is exactly halfway between two integers, and then round to the integer that is further from zero. So, for example:

def closest_integer(value):

    val = float(value)

    floor_val = int(val)

    if val - floor_val == 0.5:

        # exactly halfway between floor_val and floor_val + 1

        if val > 0:

            return floor_val + 1

        else:

            return floor_val - 1

    else:

        if val - floor_val < 0.5:

            return floor_val

        else:

            return floor_val + 1

Wait, but for val = -0.5, this would return floor_val -1, which is -1 -1 = -2. But the correct answer is 0.

So, this code is not working for this case.

Hmm. What's the issue here? The problem is that for val = -0.5, the code is returning floor_val -1, which is -1 -1 = -2, but the correct answer is 0.

So, how to handle this case?

Maybe the code should check if the value is positive or negative, and if it's exactly halfway between two integers, then return the integer that is further from zero.

So, for example:

if val > 0 and is halfway: return ceil_val

if val < 0 and is halfway: return floor_val if val is negative?

No, for val = -0.5, the floor_val is -1, and the ceil_val is 0. So the code should return 0.

So, for val < 0 and is halfway, return the ceil_val (which is the one that is further from zero).

Wait, but for val = -0.5, the ceil_val is 0, which is further from zero than -1. So the code should return 0.

So, for val < 0 and is halfway, return ceil_val.

But how to compute that.

So, the code can be:

def closest_integer(value):

    val = float(value)

    floor_val = int(val)

    if val - floor_val == 0.5:

        if val > 0:

            return floor_val + 1

        else:

            return floor_val if val < 0 else ceil_val

    else:

        if val - floor_val < 0.5:

            return floor_val

        else:

            return floor_val + 1

Wait, but how to get the ceil_val.

Ah, in Python, the ceil function is math.ceil. So, for val = -0.5, math.ceil(val) is 0.

So, in code:

import math

def closest_integer(value):

    val = float(value)

    floor_val = int(val)

    if val - floor_val == 0.5:

        if val > 0:

            return floor_val + 1

        else:

            return math.ceil(val)

    else:

        if val - floor_val < 0.5:

            return floor_val

        else:

            return floor_val + 1

Wait, let's test this code for val = -0.5.

val = -0.5

floor_val = -1

val - floor_val = 0.5, so it's exactly halfway.

So, the code returns math.ceil(val), which is 0. Correct.

For val = 14.5, returns floor_val + 1 = 14 +1 = 15. Correct.

For val = -14.5, returns math.ceil(val) = -14.5's ceil is -14? No, math.ceil(-14.5) is -14, because it rounds up to the next integer. Wait, no. The math.ceil function returns the smallest integer greater than or equal to the value. So for -14.5, math.ceil(-14.5) is -14, because -14 is greater than -14.5. So, for val = -14.5, the code returns -14, which is not correct. Because the correct answer is -15.

Wait, this is a problem. So for val = -14.5, the code would return math.ceil(val) = -14, but the correct answer is -15.

So, what's wrong here?

Ah, because for val = -14.5, the floor_val is -14, and the code is checking if val - floor_val is 0.5. So, val - floor_val is 0.5, so it enters the if clause. Then, since val is negative, it returns math.ceil(val), which is -14. But the correct answer is -15.

So this code is not working for this case.

So, what's the problem here?

For val = -14.5, the floor_val is -14, and the ceil_val is -14.5's ceil is -14? No, math.ceil(-14.5) is -14, because -14 is greater than -14.5. So, the code returns -14, which is incorrect.

But according to the problem statement, the correct answer is -15.

So, what's the issue here?

The code for val = -14.5 would return math.ceil(val) = -14, but the correct answer is -15.

So, the code is not handling this case correctly.

So, what's the correct way to handle this?

For val = -14.5, the two integers are -14 and -15. The code should return -15, because it's further from zero.

So, for negative numbers, when the value is exactly halfway between two integers, the code should return the integer that is further from zero. Which for -14.5 is -15, which is further from zero than -14.

So, the code should return the integer that is further from zero. So, for negative numbers, when the value is exactly halfway between two integers, return the integer that is further from zero. Which is the
```

</details>

**Code that ran:**

```python
import math

def closest_integer(value):
    """
    Returns the closest integer to the given value. If the value is equidistant
    from two integers, rounds away from zero.
    
    Args:
        value (str): A string representing a number.
    
    Returns:
        int: The closest integer to the input value.
    """
    val = float(value)
    floor_val = math.floor(val)
    ceil_val = math.ceil(val)
    
    if val - floor_val == 0.5:
        if val > 0:
            return ceil_val
        else:
            return floor_val if val < 0 else ceil_val
    else:
        if val - floor_val < 0.5:
            return floor_val
        else:
            return floor_val + 1
```

**Visible-test report:**

```text
PASS    assert closest_integer("10") == 10
PASS    assert closest_integer("15.3") == 15
2 of 2 visible tests passed
```
