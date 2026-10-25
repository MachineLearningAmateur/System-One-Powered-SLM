# HumanEval/81, attempt 2

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/81/a2/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 7578. Answer tokens: 255.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called numerical_letter_grade that takes a list of GPAs and returns the corresponding letter grades based on the given table. Let me think about how to approach this.

First, I should look at the grading table. The conditions are in descending order. For example, 4.0 is A+, then anything above 3.7 but less than or equal to 4.0? Wait, no. Wait the table says for GPA 4.0 it's A+. Then for >3.7 it's A. So the order is important. So I need to check the GPA against these thresholds in the correct order to avoid overlapping conditions.

Let me list out the conditions in order from highest to lowest:

- If GPA is 4.0 → A+
- If GPA >3.7 → A
- If GPA >3.3 → A-
- If GPA >3.0 → B+
- If GPA >2.7 → B
- If GPA >2.3 → B-
- If GPA >2.0 → C+
- If GPA >1.7 → C
- If GPA >1.3 → C-
- If GPA >1.0 → D+
- If GPA >0.7 → D
- If GPA >0.0 → D-
- If GPA is 0.0 → E

Wait, but the way the table is written, for example, the first entry is 4.0, then >3.7 is A. So for a GPA of 3.8, it's A. But for 3.7, it's A? Wait no, the table says for >3.7, which would be 3.7 and above? Wait no, the way the table is written, the first entry is 4.0, then the next is >3.7. So for example, 4.0 is A+, then any GPA greater than 3.7 (but less than 4.0?) would be A. Wait, but how does that work? Let me check the example given.

The example input is [4.0, 3, 1.7, 2, 3.5]. The output is ['A+', 'B', 'C-', 'C', 'A-'].

Let's see for 3.5. The example output is A-. Let's check the conditions. For 3.5, which is greater than 3.3 (so A-), but less than 3.7. So that's correct. So the order of checking is important. So the function needs to check in order from highest to lowest, so that once a condition is met, it returns the corresponding grade.

So the approach is to check each GPA against these thresholds in order. Let me think about how to structure the conditions.

So for each GPA in the input list, we need to determine which category it falls into.

Let me think of the conditions in order:

Check if GPA is equal to 4.0 → A+

Else if GPA > 3.7 → A

Else if GPA > 3.3 → A-

Else if GPA > 3.0 → B+

Else if GPA > 2.7 → B

Else if GPA > 2.3 → B-

Else if GPA > 2.0 → C+

Else if GPA > 1.7 → C

Else if GPA > 1.3 → C-

Else if GPA > 1.0 → D+

Else if GPA > 0.7 → D

Else if GPA > 0.0 → D-

Else if GPA is 0.0 → E

Wait, but the last condition is for GPA equal to 0.0, which is E. So for example, if the GPA is 0.0, it's E. If it's 0.5, then it's D- because 0.5 is greater than 0.0. So the order is important. So the conditions must be checked in order from highest to lowest, starting with 4.0, then 3.7, etc.

So the code for each GPA would be something like:

for gpa in grades:

    if gpa == 4.0:

        append 'A+'

    elif gpa > 3.7:

        append 'A'

    elif gpa > 3.3:

        append 'A-'

    elif gpa > 3.0:

        append 'B+'

    elif gpa > 2.7:

        append 'B'

    elif gpa > 2.3:

        append 'B-'

    elif gpa > 2.0:

        append 'C+'

    elif gpa > 1.7:

        append 'C'

    elif gpa > 1.3:

        append 'C-'

    elif gpa > 1.0:

        append 'D+'

    elif gpa > 0.7:

        append 'D'

    elif gpa > 0.0:

        append 'D-'

    else:

        append 'E'

Wait, but what about the case where GPA is exactly 0.0? Because the last condition is else, which would be for GPA <=0.0. But the table says that 0.0 is E. So the else would capture that. But the code above checks for GPA >0.0 first. Wait, let me think:

The code checks for GPA >0.7, then GPA>0.0. So for example, if GPA is 0.0, then all the previous conditions are false. So the code would hit the 'elif gpa >0.0' which is false, so then it goes to else, which is 'E'.

Wait, no. Let me think again. Let's take the case where GPA is 0.0. Let's walk through the code:

Check if gpa ==4.0 → no.

Check if gpa>3.7 → no.

... all the way down to the elif gpa>0.7 → no.

Then check elif gpa>0.0 → 0.0 is not greater than 0.0 → no.

Then else: append 'E'.

Which is correct.

Another example: GPA is 0.5. So:

Check all the conditions up to the elif gpa>0.7 → no. Then the elif gpa>0.0 → yes. So append 'D'.

Which is correct. Because 0.5 is greater than 0.0, so D.

Another example: GPA is 0.7. Then, the code would check if it's >0.7? No. Then check if it's >0.0 → yes. So append D. But according to the table, GPA >0.7 is D. So for 0.7, it's D? Wait, the table says:

>0.7 → D. So for GPA exactly 0.7, it's D? Wait, the table says:

The line for D is:

>0.7 → D. So for example, if GPA is 0.8, then it's D. But if GPA is 0.7, then it's D? Because the condition is >0.7. Wait, no. The table says:

The line for D is >0.7 → D. So, for example, a GPA of 0.8 would be D. But what about 0.7? According to the table, the next line is >0.0 → D-.

So for GPA 0.7, it's in the D category? Let me check the table again.

The table says:

>0.7 → D

>0.0 → D-

So, for GPA of 0.7, it's not greater than 0.7, so it would fall into the next condition, which is >0.0 → D-.

Wait, but the code checks for >0.7 first. So for GPA 0.7, the code would check:

Is it >0.7? No. Then check if it's >0.0 → yes. So append D-.

But according to the table, the D is for >0.7. So for GPA 0.7, it's not in D, but in D-? Because the D- is for >0.0. Wait, the table's lines are:

The line for D is >0.7 → D.

The line for D- is >0.0 → D-.

So for GPA 0.7, it's not greater than 0.7, so it's not D. So it's in the next condition, which is >0.0 → D-.

But according to the table, the D- is for >0.0. So for example, GPA 0.5 would be D-.

So the code is correct here.

But let me check the example given. For instance, the first example: [4.0, 3, 1.7, 2, 3.5] → output is ['A+', 'B', 'C-', 'C', 'A-'].

Let's take 3.5. So:

Check 4.0? No. >3.7? No. >3.3? Yes. So it's A-.

Which matches the example.

Another example: [1.2] → output is D+.

Let's see. 1.2 is >1.0? Yes. So the code would check:

Is it >1.0? Yes. So append D+.

Which is correct.

Another example: [0.5] → D-.

Yes, because 0.5 is >0.0 → D-.

So the code seems to handle that.

So the code structure would be:

def numerical_letter_grade(grades):
    result = []
    for gpa in grades:
        if gpa == 4.0:
            result.append('A+')
        elif gpa > 3.7:
            result.append('A')
        elif gpa > 3.3:
            result.append('A-')
        elif gpa > 3.0:
            result.append('B+')
        elif gpa > 2.7:
            result.append('B')
        elif gpa > 2.3:
            result.append('B-')
        elif gpa > 2.0:
            result.append('C+')
        elif gpa > 1.7:
            result.append('C')
        elif gpa > 1.3:
            result.append('C-')
        elif gpa > 1.0:
            result.append('D+')
        elif gpa > 0.7:
            result.append('D')
        elif gpa > 0.0:
            result.append('D-')
        else:
            result.append('E')
    return result

Wait, but what about the case where GPA is exactly 3.7? For example, if a GPA is 3.7, then it's in the A category, because the condition is >3.7. So for 3.7, it's not greater than 3.7, so the code would check the next condition. Wait, let me think:

If GPA is 3.7, then:

Check if it's 4.0 → no.

Check if >3.7 → no. Then check if >3.3 → yes. So it would be A-? But according to the table, the A is for >3.7. So for GPA 3.7, it's not >3.7, so it would fall into the next condition, which is >3.3. Which would be A-.

But according to the table, the A is for >3.7. So what's the correct letter for 3.7?

Wait, the table says:

The first row is 4.0 → A+.

Then, the next row is >3.7 → A.

So, for a GPA of 3.7, which is not greater than 3.7, it's not in that category. So the next condition is >3.3 → which is A-.

But according to the table, the A is for >3.7. So 3.7 is not in the A category. So the code is correct here. Because the code would assign A- to 3.7.

But wait, the example given in the problem: the input [3] is in the example. Let me check the example. The example input is [4.0, 3, 1.7, 2, 3.5]. The output is ['A+', 'B', 'C-', 'C', 'A-'].

So for 3.0, the code would check:

Is it 4.0? No. >3.7? No. >3.3? No. >3.0? Yes. So it would append B+? But in the example, the 3.0 is in the list, but the output for that is 'B'? Wait, wait the example input is [4.0, 3, 1.7, 2, 3.5]. The output is ['A+', 'B', 'C-', 'C', 'A-'].

Wait, the second element is 3.0. Let me see:

For GPA 3.0, according to the code:

Check if it's 4.0 → no.

Check if >3.7 → no.

Check if >3.3 → 3.0 is not greater than 3.3 → no.

Check if >3.0 → yes. So append B+.

But according to the example, the output for 3 is 'B'. Wait, that's conflicting. Wait the example input is [4.0, 3, 1.7, 2, 3.5]. The output is ['A+', 'B', 'C-', 'C', 'A-'].

Wait, the second element is 3.0. So according to the code, the code would assign B+ to it. But the example shows it as 'B'. So that's a problem. So there's a mistake here.

Wait, what's the correct letter grade for GPA 3.0?

Looking back at the table:

The table says:

>3.0 → B+.

So for GPA 3.0, the condition is not greater than 3.0. So the code would check the next condition. Let me re-examine the code.

Let me think again. The code for GPA 3.0:

Check if it's 4.0 → no.

Check if >3.7 → no.

Check if >3.3 → 3.0 is not greater than 3.3 → no.

Check if >3.0 → yes. So append B+.

But according to the example, the 3.0 is mapped to 'B'.

Wait, this suggests that the code is wrong. Because according to the example, the input 3 is mapped to 'B'.

Wait, the example says:

numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) returns ['A+', 'B', 'C-', 'C', 'A-'].

So the 3 is mapped to 'B'.

But according to the code, 3.0 would be B+.

So there's a problem here. So what's wrong with the code?

Ah! Oh, wait, the problem is that the code checks for >3.0, but according to the table, the B+ is for >3.0. So for a GPA of 3.0, it's not greater than 3.0, so the code would check the next condition. Let me check the code again.

Let me re-express the conditions:

The code's conditions for GPA 3.0:

- Check if GPA is 4.0 → no.

- Check if GPA >3.7 → no.

- Check if GPA>3.3 → no (3.0 is less than 3.3).

- Check if GPA>3.0 → yes. So append B+.

But according to the example, when the GPA is 3, the output is 'B'.

So this suggests that the code is wrong. So where's the mistake?

Ah! Oh, the problem is that the example has a GPA of 3.0, which is mapped to B. But according to the table, the B+ is for >3.0. So for 3.0, it's not in B+.

So what's the correct letter grade for 3.0?

Looking back at the table:

The table says:

>3.0 → B+.

So for GPA exactly 3.0, it's not in that category. So what is the next condition?

The next condition is >2.7 → B.

So for GPA 3.0, the code would check:

After checking all the higher conditions, the code would check:

>3.0 → yes, so B+.

But according to the example, the GPA 3.0 is mapped to B. So that's a contradiction.

Wait, this indicates that the code is incorrect. So what's wrong here?

Wait, the example says that the input [3] is mapped to 'B'. Let me check the table again.

The table:

The GPA ranges are:

- 4.0 → A+

- >3.7 → A

- >3.3 → A-

- >3.0 → B+

- >2.7 → B

So for GPA 3.0, which is equal to 3.0, it's not in any of the >3.0, so it would fall into the next condition, which is >2.7 → B.

So the code is incorrect. Because the code checks for >3.0, but the GPA 3.0 is not greater than 3.0. So the code would append B+ for 3.0, but according to the example, it should be B.

So the code's conditions are wrong. So what's the correct way to structure the conditions?

Ah! Oh, I think I made a mistake in the order of the conditions. Because the code checks for >3.0, but the GPA 3.0 is not in that category. So the code should check for >=3.0? Or maybe the conditions are not properly ordered.

Wait, the table says:

>3.0 → B+

So for GPA 3.0, it's not in this category. So the next condition is for >2.7 → B.

So for GPA 3.0, it's not in >3.0, so the code would check the next condition, which is >2.7 → yes. So append B.

But how can that be?

Wait, the code's current structure for GPA 3.0 would be:

Check if it's 4.0 → no.

Check if >3.7 → no.

Check if >3.3 → no.

Check if >3.0 → yes. So append B+.

But according to the example, the GPA 3.0 should be B.

So there's a contradiction here. So what's wrong with the conditions?

Ah! Oh, I think I have the conditions in the wrong order. For example, the B+ is for >3.0. So the code's condition for B+ is correct. But then, the code for GPA 3.0 would be in B+.

But according to the example, the GPA 3 is mapped to B. So that suggests that the code is wrong. So why is the example expecting B for GPA 3.0?

Let me recheck the example:

The example input is [4.0, 3, 1.7, 2, 3.5]. The output is ['A+', 'B', 'C-', 'C', 'A-'].

So the second element is 3.0. The output is 'B'.

So according to the table, what is the correct grade for 3.0?

Let me recheck the table:

The table:

GPA       |    Letter grade
4.0                A+
> 3.7                A 
> 3.3                A- 
> 3.0                B+
> 2.7                B 
> 2.3                B-
> 2.0                C+
> 1.7                C
> 1.3                C-
> 1.0                D+ 
> 0.7                D 
> 0.0                D-
0.0                E

So for GPA 3.0, the first condition that applies is the >3.0 → B+.

But according to the example, it's 'B'. So this suggests that there's a mistake in the example, or in the way I'm interpreting the table.

Wait, the example says that the input [3] returns 'B'. So what's the correct way to interpret the table?

Maybe the table is using >= instead of > for some conditions. Let me recheck the table:

The table says:

For example, the line for B+ is >3.0 → B+.

But if the GPA is exactly 3.0, then it's not greater than 3.0. So it would fall into the next condition, which is >2.7 → B.

So for GPA 3.0, the correct letter grade is B.

But according to the table, the B+ is for >3.0. So the code must be wrong.

So why is the example expecting 'B' for 3.0?

This suggests that the table's conditions are different. Let me re-examine the table's description.

The table is:

GPA       |    Letter grade
4.0                A+
> 3.7                A 
> 3.3                A- 
> 3.0                B+
> 2.7                B 
> 2.3                B-
> 2.0                C+
> 1.7                C
> 1.3                C-
> 1.0                D+ 
> 0.7                D 
> 0.0                D-
0.0                E

Wait, the line for B+ is >3.0. So, for a GPA of 3.0, it's not greater than 3.0, so it's not B+. So the next condition is >2.7 → B.

So for GPA 3.0, the letter grade is B.

But according to the code's current logic, the code would check for >3.0 and return B+.

So the code is incorrect. So why is the example expecting B for GPA 3.0?

Ah! Because the code's conditions are wrong. The code checks for >3.0, but the actual condition for B+ is >=3.0?

Wait, perhaps the table is using >= for some conditions. For example, the line for B+ is >3.0, but maybe that's a typo and it should be >=3.0. Or perhaps the conditions are meant to be inclusive.

But according to the example, the GPA 3.0 is mapped to B. So this suggests that the B+ condition is for >3.0, and the B condition is for >=2.7. So for GPA 3.0, it's not in B+ (since it's not >3.0), but it is >=2.7, so it's B.

So the code's current conditions are wrong. Let me think about the correct order of conditions.

The correct order of conditions should be:

Check for 4.0 → A+.

Else if GPA >3.7 → A.

Else if GPA >3.3 → A-.

Else if GPA >3.0 → B+.

Else if GPA >2.7 → B.

Else if GPA >2.3 → B-.

Else if GPA >2.0 → C+.

Else if GPA >1.7 → C.

Else if GPA >1.3 → C-.

Else if GPA >1.0 → D+.

Else if GPA >0.7 → D.

Else if GPA >0.0 → D-.

Else → E.

But for GPA 3.0, this would check >3.0 → no. So it would go to the next condition, which is >2.7 → yes. So append B.

Which is correct according to the example.

So why was the code earlier checking for >3.0? Because the code's current logic would append B+ for GPA 3.0. So there's a mistake in the code's conditions.

Ah! Oh, I see the mistake. The code checks for >3.0 and appends B+. But according to the example, the GPA 3.0 should be B. So the code is wrong. So the code's condition for B+ is wrong.

So the code's condition for B+ should be >=3.0? Or perhaps the code's order is wrong.

Wait, the B+ condition is for >3.0. So the GPA must be greater than 3.0 to get B+. So for GPA 3.0, it's not B+.

But the example says that for GPA 3.0, the output is B. So the code's condition for B+ is wrong. So what is the correct condition for B+?

Let me re-express the table in terms of ranges.

The table can be represented as:

4.0 → A+

3.7 < GPA < 4.0 → A

3.3 < GPA ≤ 3.7 → A-

3.0 < GPA ≤ 3.3 → B+

2.7 < GPA ≤ 3.0 → B

2.3 < GPA ≤ 2.7 → B-

2.0 < GPA ≤ 2.3 → C+

1.7 < GPA ≤ 2.0 → C

1.3 < GPA ≤ 1.7 → C-

1.0 < GPA ≤ 1.3 → D+

0.7 < GPA ≤ 1.0 → D

0.0 < GPA ≤ 0.7 → D-

0.0 → E

So the code needs to check for each GPA in this order. For example, for GPA 3.0:

It falls into the B range, because it's between 2.7 and 3.0.

Wait, no. Because the B+ is for 3.0 < GPA ≤3.3. So for GPA 3.0, it's not in B+.

So the code should check for GPA >3.0, and then for GPA >2.7, etc.

So the code's current conditions are:

if GPA >3.0 → B+.

But for GPA 3.0, this is false. So the code would check the next condition, which is >2.7 → yes. So append B.

Which matches the example.

So the code's conditions are correct. But earlier when I thought that the code would append B+ for GPA 3.0, that was a mistake. Because the code checks for >3.0. So for GPA 3.0, this condition is false. So the code proceeds to check the next condition.

So why did I think earlier that the code would append B+ for GPA 3.0?

Ah, because I made a mistake in thinking that the code checks for >3.0. Let me re-examine the code.

The code's condition for B+ is:

elif gpa > 3.0:

    append 'B+'

So for GPA 3.0, this condition is not met. So the code moves to the next condition, which is >2.7. For GPA 3.0, this is true. So append 'B'.

So the code is correct. So why did I think earlier that the code would append B+ for GPA 3.0? Because I made a mistake in thinking that the condition was >=3.0. But the code checks for >3.0.

So the code is correct. Then why did I get confused earlier?

Because I thought that the code would check for >3.0 and append B+ for 3.0. But that's not the case. So the code is correct.

Let me re-examine the example:

For the input [3], the GPA is 3.0.

The code would check:

Is it 4.0? No.

Is it >3.7? No.

Is it >3.3? No.

Is it >3.0? No. So move to next condition.

Is it >2.7? Yes. So append 'B'.

Which matches the example. So the code is correct.

Ah, I see. So earlier, I had a misunderstanding of the code's conditions. So the code is correct.

So the code should work.

Now, let's check another example. For GPA 3.5:

Check if it's 4.0? No.

>3.7? No. (3.5 <3.7)

>3.3? Yes. So append 'A-'.

Which matches the example's output for 3.5.

So the code is correct.

Another example: GPA 3.7. 

Check if it's 4.0? No.

>3.7? No. (3.7 is not greater than 3.7)

>3.3? Yes. So append 'A-'.

But according to the table, >3.7 is A. So for GPA 3.7, it's not in that category. So it's in the next condition. So the code would assign A- to 3.7. But according to the table, the A is for >3.7. So for 3.7, the code is correct.

So the code is correct.

Now, let's test the example given.

Sample input: [4.0, 3, 1.7, 2, 3.5]

Processing each GPA:

4.0 → A+.

3 → B.

1.7 → check:

>1.7? No. Next condition: >1.3? Yes. So append C-.

Wait, wait for 1.7:

Check if >1.7 → no. So next condition is >1.3 → yes. So append C-.

But according to the example, the third element is 1.7, which is mapped to C-.

Yes, which matches.

For 2.0:

Check if >2.0 → no. Next condition is >1.7 → yes. So append C.

Which matches the example.

For 3.5:

>3.3 → yes. So append A-.

So the output is ['A+', 'B', 'C-', 'C', 'A-'], which matches the example.

So the code works for the example.

Another example: [1.2] → D+.

Check:

Is it >1.0? Yes. So append D+.

Which is correct.

Another example: [0.5] → D-.

Check:

>0.7? No. >0.0? Yes. So append D-.

Which is correct.

So the code is correct.

Now, I need to write the code accordingly.

So the code is:

def numerical_letter_grade(grades):
    result = []
    for gpa in grades:
        if gpa == 4.0:
            result.append('A+')
        elif gpa > 3.7:
            result.append('A')
        elif gpa > 3.3:
            result.append('A-')
        elif gpa > 3.0:
            result.append('B+')
        elif gpa > 2.7:
            result.append('B')
        elif gpa > 2.3:
            result.append('B-')
        elif gpa > 2.0:
            result.append('C+')
        elif gpa > 1.7:
            result.append('C')
        elif gpa > 1.3:
            result.append('C-')
        elif gpa > 1.0:
            result.append('D+')
        elif gpa > 0.7:
            result.append('D')
        elif gpa > 0.0:
            result.append('D-')
        else:
            result.append('E')
    return result

Now, test the code against the sample inputs.

Another test case: [0.0] → E.

Another test case: [0.7] → D.

Because 0.7 is not greater than 0.7, so it's not in D. So check next condition: >0.0 → yes. So append D-.

Wait, no. For GPA 0.7:

Check if it's >0.7 → no. Then check if it's >0.0 → yes. So append D. Wait, no. Let me re-examine the code.

The code has:

elif gpa > 0.7 → append D.

So for GPA 0.7, it's not greater than 0.7, so the code checks the next condition: elif gpa >0.0 → yes. So append D-.

Wait, no. Let me re-examine the code.

The code has:

elif gpa > 0.7 → D.

elif gpa >0.0 → D-.

So for GPA 0.7, it's not >0.7 → so the code checks the next condition: >0.0 → yes. So append D-.

But according to the table, for GPA >0.7 → D. So for GPA 0.7, which is not >0.7, it's in the next condition, which is >0.0 → D-.

But according to the table, the D- is for >0.0. So for GPA 0.7, it's not in D, but in D-.

But the table says:

>0.7 → D.

>0.0 → D-.

So for GPA 0.7, it's not >0.7, so it's not D. It's in the next condition, which is >0.0 → D-.

So the code is correct.

Another example: GPA 0.8 → >0.7 → D.

So the code appends D.

So the code is correct.

Thus, the code should handle all cases correctly.

Now, the code needs to be written with proper indentation and syntax.

So the code is as written above.

Now, I need to write the code in Python, with the function definition, and return the list.

The code should pass all the tests.

Now, the user provided tests:

assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == ['A+', 'B', 'C-', 'C', 'A-']

assert numerical_letter_grade([1.2]) == ['D+']

assert numerical_letter_grade([0.5]) == ['D-']

Let me test the code for these.

For [1.2], the code checks:

>1.0 → yes. So append D+.

Yes.

For [0.5], code checks:

>0.7? No. >0.0 → yes → append D-.

Yes.

So the code passes these tests.

Thus, the code is correct.
```

</details>

**Code that ran:**

```python
def numerical_letter_grade(grades):
    """Convert a list of GPAs to corresponding letter grades based on a specific grading scale."""
    result = []
    for gpa in grades:
        if gpa == 4.0:
            result.append('A+')
        elif gpa > 3.7:
            result.append('A')
        elif gpa > 3.3:
            result.append('A-')
        elif gpa > 3.0:
            result.append('B+')
        elif gpa > 2.7:
            result.append('B')
        elif gpa > 2.3:
            result.append('B-')
        elif gpa > 2.0:
            result.append('C+')
        elif gpa > 1.7:
            result.append('C')
        elif gpa > 1.3:
            result.append('C-')
        elif gpa > 1.0:
            result.append('D+')
        elif gpa > 0.7:
            result.append('D')
        elif gpa > 0.0:
            result.append('D-')
        else:
            result.append('E')
    return result
```

**Visible-test report:**

```text
PASS    assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == ['A+', 'B', 'C-', 'C', 'A-']
PASS    assert numerical_letter_grade([1.2]) == ['D+']
PASS    assert numerical_letter_grade([0.5]) == ['D-']
3 of 3 visible tests passed
```
