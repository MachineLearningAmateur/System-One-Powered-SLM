# HumanEval/81, attempt 0

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`HumanEval/81/a0/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 8192 (hit the 8,192-token cap). Answer tokens: 236.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called numerical_letter_grade that takes a list of GPAs and returns a list of corresponding letter grades based on the given table. Let me think about how to approach this.

First, I should understand the grading scale. The table says that for each GPA, there's a range. For example, if the GPA is 4.0, it's A+. Then for values greater than 3.7, it's A, and so on. So the key is to check each GPA against these ranges.

The steps I need to take are:

1. Iterate through each GPA in the input list.
2. For each GPA, determine which letter grade it falls into.
3. Collect all the letter grades in a list and return it.

Let me think about the conditions. The ranges are:

- A+ is for 4.0 and above, but wait, the table says "4.0 is A+", and then " > 3.7 is A". So the A+ is for exactly 4.0. Wait, the first condition is 4.0, then the next is >3.7. So the A+ is only for 4.0. Then A is for anything above 3.7, but not including 4.0? Wait, no. Let me check the table again.

The table says:

GPA | Letter grade
4.0 | A+
>3.7 | A
>3.3 | A-
>3.0 | B+
>2.7 | B
>2.3 | B-
>2.0 | C+
>1.7 | C
>1.3 | C-
>1.0 | D+
>0.7 | D
>0.0 | D-
0.0 | E

Wait, so the A+ is only for 4.0. Then, for example, if a GPA is 3.7, it's A. But if it's 3.7, then it's not A+ but A. So the conditions are:

For each GPA, check if it's >=4.0 → A+.

Else, check if it's >3.7 → A.

But wait, the first condition is 4.0. So for 4.0, it's A+. Then for values greater than 3.7, but less than 4.0, it's A. So the conditions need to be ordered correctly.

So the order of checking is important. For example, if a GPA is 3.7, it's A. But if it's 3.7, then the next condition is >3.7, which is not true. So the code needs to check in order.

So the logic would be:

For each GPA in the list:

if GPA >=4.0 → A+

elif GPA >3.7 → A

elif GPA >3.3 → A-

... and so on.

Wait, but the conditions are in order. For example, the first condition is 4.0. Then, if it's not that, check if it's >3.7, then >3.3, etc.

So the code can be structured with a list of thresholds and their corresponding grades. For example, the thresholds are in descending order, and for each GPA, we check if it's in the range for that threshold.

Alternatively, we can create a list of tuples where each tuple contains the threshold and the grade. Then, for each GPA, we check from the highest threshold down to the lowest.

Wait, but the thresholds are in a specific order. Let me list them in order of highest to lowest:

4.0 → A+

3.7 → A

3.3 → A-

3.0 → B+

2.7 → B

2.3 → B-

2.0 → C+

1.7 → C

1.3 → C-

1.0 → D+

0.7 → D

0.0 → D-

-0.0 → E?

Wait, the last entry is 0.0 → E. So the order is:

The thresholds are 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

So for each GPA, we check if it's >=4.0 → A+.

If not, check if it's >3.7 → A.

If not, check if it's >3.3 → A-.

And so on.

So the code can have a list of thresholds and their corresponding grades, ordered from highest to lowest.

So, perhaps we can create a list of tuples where each tuple is (threshold, grade), and then for each GPA, we check in order.

Alternatively, we can create a list of conditions.

Let me think about how to structure the conditions.

Let me list the thresholds in order:

thresholds = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]

grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'E']

Wait, but the order of the thresholds is from highest to lowest. So for each GPA, we check if it's >= threshold, and if so, take the corresponding grade.

So for example, for a GPA of 4.0, it's in the first threshold, so grade is A+.

For a GPA of 3.7, it's in the second threshold (since 3.7 is >3.7? No, wait. Wait, the first condition is 4.0. So if the GPA is 3.7, then it's not >=4.0, so we check if it's >3.7. But 3.7 is not greater than 3.7. So the next condition is 3.7? Wait, no. Let me think again.

The thresholds are ordered as:

4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

So the first condition is 4.0. If the GPA is 4.0, it's >=4.0 → A+.

If it's less than 4.0, then check if it's >3.7. For example, if the GPA is 3.7, then it's not greater than 3.7. So the next condition is 3.3. So if the GPA is 3.7, then it's not greater than 3.3, but it's greater than 3.3? Wait, 3.7 is greater than 3.3. So the condition would be: if the GPA is greater than 3.3, then it's A-.

Wait, the table says:

>3.3 → A-.

So for GPA 3.7, it's in the A- category.

So the code needs to check each threshold in order. So for each GPA, we check if it's >=4.0 → A+.

If not, check if it's >3.7 → A.

If not, check if it's >3.3 → A-.

And so on.

So the code can be structured as follows:

for each gpa in grades:

    if gpa >=4.0:

        add 'A+'

    elif gpa >3.7:

        add 'A'

    elif gpa >3.3:

        add 'A-'

    elif gpa >3.0:

        add 'B+'

    elif gpa >2.7:

        add 'B'

    elif gpa >2.3:

        add 'B-'

    elif gpa >2.0:

        add 'C+'

    elif gpa >1.7:

        add 'C'

    elif gpa >1.3:

        add 'C-'

    elif gpa >1.0:

        add 'D+'

    elif gpa >0.7:

        add 'D'

    else:

        add 'E'

Wait, but what about the 0.0 case? For example, if the GPA is 0.0, then it's E. So the else part would be for the case where all previous conditions are false. So the code would check each condition in order.

But let's see. Let's take the example given in the problem.

Example:

grade_equation([4.0, 3, 1.7, 2, 3.5]) ==> ['A+', 'B', 'C-', 'C', 'A-']

Let's check each GPA:

4.0 → A+ → correct.

3 → 3 is not >=4.0. Then check if it's >3.7? 3 is not. Then check if it's >3.3? 3 is not. Then check if it's >3.0? 3 is equal to 3.0. So the next condition is if it's >3.0? Wait, the code is:

elif gpa >3.0 → B+?

Wait, the code is:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

Wait, but 3.0 is the next threshold. So for a GPA of 3.0, it's >3.0? No. Wait, 3.0 is equal to 3.0. So the condition is gpa >3.0 → which is false. So the code would check if it's >3.0, which is false. Then check the next condition.

Wait, the code is:

for each GPA:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

etc.

So for a GPA of 3.0, it's not >=4.0, not >3.7, not >3.3. Then check if it's >3.0. So 3.0 is equal to 3.0, so the condition is false. So the next condition is gpa >2.7 → which is 3.0>2.7 → yes. So the code would add 'B'.

But according to the example, the GPA of 3 is 'B'. So that's correct.

Then for 3.5, which is between 3.0 and 3.3? Wait, 3.5 is greater than 3.3. So the code would check if it's >3.3. So yes. So the code would add 'A-'.

So the example's 3.5 is 'A-'.

So the example's input is [4.0, 3, 1.7, 2, 3.5], which would be:

4.0 → A+

3 → check if >3.7? No. Then >3.3? No. Then >3.0? No. Then >2.7? 3>2.7 → yes. So 'B'.

1.7 → check if >3.7? No. Then >3.3? No. Then >3.0? No. Then >2.7? 1.7 is not. Then >2.3? 1.7 is not. Then >2.0? 1.7 is not. Then >1.7? 1.7 is equal to 1.7, so the condition is false. Then check >1.3? 1.7>1.3 → yes. So 'C'.

Wait, the example says for 1.7, the grade is 'C'. So that's correct.

Then 2.0 → check if it's >3.7? No. Then >3.3? No. Then >3.0? No. Then >2.7? 2.0>2.7? No. Then >2.3? 2.0>2.3? No. Then >2.0? 2.0 is equal to 2.0, so the condition is false. Then check >1.7? 2.0>1.7 → yes. So 'C'.

Wait, but according to the example, the 2 is 'C'. So that's correct.

So the code seems to handle that.

So the code structure would be:

def numerical_letter_grade(grades):
    result = []
    for gpa in grades:
        if gpa >=4.0:
            result.append('A+')
        elif gpa >3.7:
            result.append('A')
        elif gpa >3.3:
            result.append('A-')
        elif gpa >3.0:
            result.append('B+')
        elif gpa >2.7:
            result.append('B')
        elif gpa >2.3:
            result.append('B-')
        elif gpa >2.0:
            result.append('C+')
        elif gpa >1.7:
            result.append('C')
        elif gpa >1.3:
            result.append('C-')
        elif gpa >1.0:
            result.append('D+')
        elif gpa >0.7:
            result.append('D')
        else:
            result.append('E')
    return result

Wait, but what about the case where a GPA is exactly 3.0? Let's see. For example, if a GPA is 3.0, then the code checks if it's >3.0? No. Then the next condition is >2.7. 3.0>2.7 → yes. So it would append 'B+'.

But according to the table, the 3.0 is B+.

Yes, that's correct.

Another example: the input [1.2] → output ['D+'].

Let's see. 1.2 is not >=4.0, not >3.7. Then check if it's >3.3? No. Then >3.0? No. Then >2.7? No. Then >2.3? No. Then >2.0? No. Then >1.7? 1.2>1.7? No. Then >1.3? No. Then >1.0? 1.2>1.0 → yes. So append 'D+'.

Which is correct.

Another example: [0.5] → output 'D-'.

0.5 is not >=4.0. Then check if it's >3.7? No. Then >3.3? No. ... Then check if it's >0.7? 0.5>0.7? No. So else clause, append 'E'? Wait, no. Wait, the code says:

else: append 'E'.

But according to the table, 0.0 is E. So for 0.5, which is greater than 0.0, but less than 0.7. So the code would check if it's >0.7? 0.5>0.7? No. So the else clause is executed, which appends 'E'.

But the example says that [0.5] should be ['D-'].

Wait, that's a problem. Because according to the table, the 0.0 is E. But 0.5 is in the D- category. Wait, the table says:

>0.0 → D-

So for a GPA of 0.5, which is greater than 0.0, it's in the D- category.

But according to the code above, the code checks:

elif gpa >0.7 → D.

But 0.5 is not >0.7. So the code would go to the else clause, which appends 'E'.

But that's wrong.

So there's a problem here.

Wait, the code's conditions are:

The code checks:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

else → E

But for a GPA of 0.5, which is greater than 0.0, but less than 0.7, the code would check if it's >0.7? No. So the else clause is executed, appending 'E'.

But according to the table, 0.0 is E, and 0.0 to 0.7 is D-?

Wait, the table says:

>0.0 → D+ ?

No, let me check again.

The table says:

>0.0 → D-

Wait, the table says:

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

Wait, the last line says 0.0 is E. So the D- is for >0.7?

Wait, the table says:

>0.7 → D.

>0.0 → D-.

But then, what about the 0.0? It's E.

So for a GPA of 0.5, which is between 0.0 and 0.7, it's in the D- category.

But according to the code's current structure, the code checks for >0.7 first. So 0.5 is not >0.7, so it goes to the else clause, which is E.

But that's wrong. So the code's conditions are wrong.

Ah, here's the problem. The code's conditions are not ordered correctly. The code checks for >0.7, but the D- is for >0.0, but the code is not handling that.

So the code's conditions are not in the correct order. Let me re-express the conditions.

The correct order of the thresholds is:

The thresholds are:

4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But the code's conditions are:

Check for 4.0, then 3.7, then 3.3, then 3.0, then 2.7, then 2.3, then 2.0, then 1.7, then 1.3, then 1.0, then 0.7, then 0.0.

But for the D- and E, the code's current conditions are:

After checking for >0.7, the next is else → E.

But according to the table, the D- is for >0.7?

No. Let me recheck the table:

The table says:

>0.7 → D.

>0.0 → D-.

0.0 → E.

So the D- is for >0.0, but <=0.7?

Wait, the table says:

>0.0 → D-.

But the next condition is >0.7 → D.

Wait, that's not possible. Because the D- is for >0.0, but the D is for >0.7.

So the code's conditions are not ordered correctly. The D- is for >0.0, but the code's current conditions check for >0.7 first. So for a GPA of 0.5, which is between 0.0 and 0.7, the code would check:

Is it >0.7? No. So the code would go to the else clause, which is E.

But according to the table, 0.5 is D-.

So the code's conditions are wrong.

So the code needs to be adjusted.

The correct order of the conditions should be:

Check for the highest thresholds first, then lower ones.

So the correct order is:

4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But the code's current conditions are:

Check for 4.0, then 3.7, then 3.3, then 3.0, then 2.7, then 2.3, then 2.0, then 1.7, then 1.3, then 1.0, then 0.7, then else.

But the D- is for >0.0, but the code's condition for >0.7 is after that. So for a GPA of 0.5, which is >0.0 and <0.7, the code would check if it's >0.7 (no) and then else → E. But according to the table, it should be D-.

So the code's conditions are not ordered correctly.

So the code needs to be adjusted to have the D- and D conditions in the right order.

So the correct order of conditions should be:

Check for 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But for the D- and D, the code should check for >0.7 first, then D, then E.

Wait, no. Let me re-express the table:

The D- is for >0.0, but <=0.7.

Wait, the table says:

>0.0 → D-

But the code's current conditions have:

elif gpa >0.7 → D.

So the code is checking for >0.7 first, which is not correct.

So the correct order is:

The D- is for >0.0, and the D is for >0.7.

So the code's conditions are wrong. The D- should be checked before the D.

So the code's conditions need to be ordered such that:

The D- is checked before the D.

So the correct order is:

Check for 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But for the D- and D, the code should check for >0.0, then >0.7.

So the code's current conditions are:

After checking for >0.7, the else is E.

But for the D- and D, the code should have:

Check if the GPA is >0.0 → D-.

Then check if it's >0.7 → D.

But how to structure that.

So the code's conditions need to be:

Check for 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But the D- is for >0.0, and D is for >0.7.

So the code's conditions should be:

Check for 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But the D- is for >0.0, but the code's current conditions check for >0.7 first. So the code needs to have:

After checking for >0.7, the code would check for >0.0, but that's not the case.

Wait, perhaps the code's conditions are ordered in the wrong way. Let me think again.

The correct order of the conditions is:

The highest thresholds first, then lower ones.

So the code's conditions should be:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

elif gpa >0.0 → D-

else → E

Wait, but that's not correct. Because the D- is for >0.0, but the code's current conditions check for >0.7 first. So if the GPA is 0.5, which is >0.0 and <0.7, then it would check if it's >0.7 (no), then go to else → E, which is wrong.

So the code needs to have the D- and D conditions in the right order.

So the correct order is:

Check for >0.7 → D.

Check for >0.0 → D-.

But how?

Wait, the D- is for >0.0, and the D is for >0.7. So the code should check for >0.7 first, then >0.0. But that's not possible because 0.7 is higher than 0.0.

Wait, no. The D- is for >0.0, and the D is for >0.7. So the code's conditions need to check for >0.7 first, then for >0.0.

But that would be:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But that's not possible. Because the code is checking for >0.7 first, and then for >0.0. But the code would have to check for >0.7 first, then check if it's >0.0.

Wait, but if the GPA is 0.5, which is >0.0, then the code would check for >0.7 first (no), then check for >0.0 (yes). So the code would append D-.

But how to structure that.

So the code's conditions should be:

Check for 4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

But the D- is for >0.0, and the D is for >0.7.

So the code's conditions should be:

After checking for >0.7, then check for >0.0.

But how to structure that.

Let me re-express the code's conditions with the correct order.

The correct order of conditions is:

Check for the highest thresholds first.

So the list of thresholds is:

4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0.

So the code's conditions should be:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

elif gpa >0.0 → D-

else → E

Wait, but in this case, the D- is for >0.0. So if the GPA is 0.5, which is >0.0, then the code would check if it's >0.7 (no) and then check if it's >0.0 (yes). So the code would append D-.

But in the code, the conditions are ordered as:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But that's not possible. Because in the code, the conditions are checked in order. So the code would check if the GPA is >0.7 first. If not, then check if it's >0.0.

So the code would have:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

elif gpa >0.0 → D-

else → E

Wait, but in this case, the code would check for >0.7, then for >0.0. So for a GPA of 0.5, which is >0.0, but <0.7, it would check if it's >0.7 (no), then check if it's >0.0 (yes), so append D-.

But in the code, the conditions are written as:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But that's not possible, because in the code, the conditions are checked in order. So the code would check if the GPA is >0.7 first. If not, then check if it's >0.0.

So the code would have:

for each GPA:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

elif gpa >0.0 → D-

else → E

But the code is written as:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But in the code, the order is important. So the code would check for >0.7 first, then >0.0.

So for a GPA of 0.5, which is >0.0, but <0.7, the code would check if it's >0.7 (no), then check if it's >0.0 (yes). So the code would append D-.

But in the code, the 'elif gpa >0.7' is checked before 'elif gpa >0.0', so the code would append D-.

So the code would have:

for the condition:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But that's not possible, because the code would have to check for >0.7 first, then for >0.0.

But in the code, the conditions are written as:

elif gpa >0.7 → D

elif gpa >0.0 → D-

But in the code, the 'elif gpa >0.0' is after the 'elif gpa >0.7' condition.

So in the code, for a GPA of 0.5, which is not >0.7, the code checks if it's >0.0 (yes), so appends D-.

But in the code, the conditions are:

After checking for >0.7, then check for >0.0.

So the code would have:

if gpa >=4.0 → A+

elif gpa >3.7 → A

elif gpa >3.3 → A-

elif gpa >3.0 → B+

elif gpa >2.7 → B

elif gpa >2.3 → B-

elif gpa >2.0 → C+

elif gpa >1.7 → C

elif gpa >1.3 → C-

elif gpa >1.0 → D+

elif gpa >0.7 → D

elif gpa >0.0 → D-

else → E

But in this case, the code would check for >0.7 first, then for >0.0.

So the code is correct.

So the code's conditions are:

For a GPA of 0.5, which is >0.0, but <0.7:

- Not >=4.0, not >3.7, etc.

- Check if >0.7? No.

- Check if >0.0? Yes → append D-.

Which is correct.

So the code needs to have the conditions ordered as:

After checking for the higher thresholds, then the D- and D conditions.

So the code's conditions are:

The list of conditions is:

Check for 4.0, then 3.7, then 3.3, then 3.0, then 2.7, then 2.3, then 2.0, then 1.7, then 1.3, then 1.0, then 0.7, then 0.0.

So the code's conditions are:

if gpa >=4.0:

    A+

elif gpa >3.7:

    A

elif gpa >3.3:

    A-

elif gpa >3.0:

    B+

elif gpa >2.7:

    B

elif gpa >2.3:

    B-

elif gpa >2.0:

    C+

elif gpa >1.7:

    C

elif gpa >1.3:

    C-

elif gpa >1.0:

    D+

elif gpa >0.7:

    D

elif gpa >0.0:

    D-

else:

    E

So the code should have these conditions.

Now, the code in Python would be written as:

def numerical_letter_grade(grades):
    result = []
    for gpa in grades:
        if gpa >= 4.0:
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

Now, let's test the example.

Test case 1: [4.0, 3, 1.7, 2, 3.5]

For 4.0 → A+.

3 → check if >3.7? No. >3.3? No. >3.0? 3 is equal to 3.0, so no. Then check >2.7 → 3>2.7 → yes → B.

1.7 → check >3.7? No. >3.3? No. >3.0? No. >2.7? 1.7>2.7? No. >2.3? No. >2.0? No. >1.7? 1.7>1.7? No. >1.3? Yes → C.

2 → check >3.7? No. >3.3? No. >3.0? No. >2.7? 2>2.7? No. >2.3? No. >2.0? 2>2.0 → yes → C.

3.5 → check if >3.7? No. >3.3? 3.5>3.3 → yes → A-.

So the output
```

</details>

**Code that ran:**

```python
def numerical_letter_grade(grades):
    result = []
    for gpa in grades:
        if gpa >= 4.0:
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
