# Mbpp/762, attempt 1

1 round; visible pass; final code on the hidden tests: ✅ pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/762/a1/r1`)

Visible tests: **pass**. Hidden tests: **✅ pass**. Thinking tokens: 819. Answer tokens: 29.

<details><summary>Thinking</summary>

```text
Okay, I need to write a Python function called check_monthnumber_number that takes a month number (from 1 to 12) and returns True if that month has 30 days, else False. Let's think about how to approach this.

First, I remember that not all months have 30 days. For example, February has 28 or 29 days, April has 30, June has 30, etc. So I need to create a list or a dictionary that maps each month to the number of days it has.

Wait, but the problem is specifically checking if the month has exactly 30 days. So let's list out the months and their days:

- January: 31
- February: 28 (or 29, but the problem probably considers non-leap years)
- March: 31
- April: 30
- May: 31
- June: 30
- July: 31
- August: 31
- September: 30
- October: 31
- November: 30
- December: 31

So the months with exactly 30 days are April (4), June (6), September (9), November (11). So the function should return True for these months, and False otherwise.

So the approach is: create a set containing those four months. Then check if the input month is in that set. If yes, return True; else, False.

Wait, but the problem says the input is a number from 1 to 12. So the function can be as simple as checking if the month is 4, 6, 9, or 11.

So the code can be:

def check_monthnumber_number(month):
    return month in {4, 6, 9, 11}

Wait, but what about February? For example, if the input is 2, the function returns False, which is correct because February has 28 days (assuming non-leap year). So that's correct.

Let me test the sample assertion. The sample says check_monthnumber_number(6) should return True. Since 6 is in the set, that's correct.

So that's the solution. But wait, maybe the problem expects to handle leap years? But the problem says "given month number contains 30 days". So regardless of leap years, February has 28 days, so the answer for month 2 is False. So the code is correct.

So the function is straightforward. Let me write that.

But wait, the function name in the assert is check_monthnumber_number. Wait, maybe that's a typo? Like maybe it's supposed to be check_month_number? But the user wrote the assert as check_monthnumber_number(6)==True. So the function name is check_monthnumber_number. So I need to make sure the function is named correctly.

So the code would be:

def check_monthnumber_number(month):
    return month in {4, 6, 9, 11}

But maybe the user wants to have a list or a dictionary. But the set approach is the simplest.

So the code is correct. Let me check the sample input. For 6, which is June, returns True. Correct.

So that's the solution. Now, the code needs to be written with proper syntax. Also, the function needs to be defined. So the complete code would be:

def check_monthnumber_number(month):
    return month in {4, 6, 9, 11}

But wait, what if the input is not an integer? Well, the problem says that the input is given as a number from 1 to 12. So the function can assume that the input is valid. So no need for error checking.

So the code is correct. Let me write that as the answer.
```

</details>

**Code that ran:**

```python
def check_monthnumber_number(month):
    return month in {4, 6, 9, 11}
```

**Visible-test report:**

```text
PASS    assert check_monthnumber_number(6)==True
1 of 1 visible tests passed
```
