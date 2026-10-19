# HumanEval/81

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 8192 | 1 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 8192 | 1 |

## Prompt shown to the model (round 1)

```python

def numerical_letter_grade(grades):
    """It is the last week of the semester and the teacher has to give the grades
    to students. The teacher has been making her own algorithm for grading.
    The only problem is, she has lost the code she used for grading.
    She has given you a list of GPAs for some students and you have to write 
    a function that can output a list of letter grades using the following table:
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
    

    Example:
    grade_equation([4.0, 3, 1.7, 2, 3.5]) ==> ['A+', 'B', 'C-', 'C', 'A-']
    """

Visible tests:
assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == ['A+', 'B', 'C-', 'C', 'A-']
assert numerical_letter_grade([1.2]) == ['D+']
assert numerical_letter_grade([0.5]) == ['D-']
```

## Visible tests

```python
assert numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]) == ['A+', 'B', 'C-', 'C', 'A-']
assert numerical_letter_grade([1.2]) == ['D+']
assert numerical_letter_grade([0.5]) == ['D-']
```
