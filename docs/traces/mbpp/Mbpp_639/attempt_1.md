# Mbpp/639, attempt 1

1 round; visible pass; final code on the hidden tests: ❌ fail ⚠️ visible pass. Back to the [task](README.md). The prompt and the visible tests are on the task page; from round 2, the model also got its previous code and its visible-test report (never its previous thinking, and never any hidden-test result).

## Round 1 (`Mbpp/639/a1/r1`)

Visible tests: **pass**. Hidden tests: **❌ fail**. Thinking tokens: 865. Answer tokens: 44.

<details><summary>Thinking</summary>

```text
Okay, let's see. I need to write a Python function that sums the lengths of the names in a given list, but after removing those that start with a lowercase letter. The assert statement given is that the function sample_nam(['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith']) returns 16. Let me think about how to approach this.

First, the task is to sum the lengths of the names. But we have to exclude any names that start with a lowercase letter. So, for each name in the list, check if the first character is lowercase. If it is, skip it. Otherwise, add its length to the total.

Wait, but how do I check if a name starts with a lowercase letter? In Python, strings have methods like startswith(). So for each name in the list, check if name[0].islower() is True. Wait, but wait: the first character of the name. So, for example, 'sally' starts with 's', which is lowercase. So that name should be excluded. But 'Dylan' starts with 'D', which is uppercase, so it's included. Similarly, 'rebecca' starts with 'r' lowercase, so excluded. Wait, but the sample input includes 'rebecca' and 'keith' which are lowercase. Wait, the sample input is ['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'].

So the names that are to be considered are those that start with uppercase letters. So, for each name, check if the first character is uppercase. If yes, add the length of the name to the total. Otherwise, skip.

So the steps are:

1. Initialize a total sum to 0.
2. Iterate over each name in the input list.
3. For each name, check if the first character is uppercase (name[0].isupper()).
4. If yes, add the length of the name to the total.
5. After processing all names, return the total.

So the function would be something like:

def sample_nam(names):
    total = 0
    for name in names:
        if name[0].isupper():
            total += len(name)
    return total

Wait, but what about names that are empty? Well, the problem says "names of a given list of names", so perhaps the input list is non-empty, but the code should handle any names, even empty ones. But in the sample input, all names are non-empty. But the code would handle it.

Testing the sample input:

The list is ['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'].

Let's check each name:

sally: starts with 's' lowercase → excluded.

Dylan: starts with 'D' → included. Length is 5 → add 5.

rebecca: starts with 'r' lowercase → excluded.

Diana: starts with 'D' → included. Length 5 → add 5.

Joanne: starts with 'J' → included. Length 6 → add 6.

keith: starts with 'k' lowercase → excluded.

So total is 5 +5 +6 = 16. Which matches the assert statement. So the code works.

So the function is correct. Now, the code needs to be written with the correct imports. But since there are no imports needed, the code is straightforward.

So the code would be:

def sample_nam(names):
    total = 0
    for name in names:
        if name[0].isupper():
            total += len(name)
    return total

But wait, what about names that have only one character? Like 'A' → starts with uppercase, so added. For example, if the input is ['A', 'a'], then the sum would be 1 + 0 (since 'a' is lowercase) → 1.

Yes. So the code handles that.

So the code is correct. The assert statement is satisfied. So the code is correct.
```

</details>

**Code that ran:**

```python
def sample_nam(names):
    total = 0
    for name in names:
        if name and name[0].isupper():
            total += len(name)
    return total
```

**Visible-test report:**

```text
PASS    assert sample_nam(['sally', 'Dylan', 'rebecca', 'Diana', 'Joanne', 'keith'])==16
1 of 1 visible tests passed
```
