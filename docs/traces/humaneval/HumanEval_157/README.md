# HumanEval/157

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 2819 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 1628 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2147 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 1236 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 1463 | 0 |

## Prompt shown to the model (round 1)

```python

def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is right angle or 
    90 degree.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''

Visible tests:
assert right_angle_triangle(3, 4, 5) == True
assert right_angle_triangle(1, 2, 3) == False
assert right_angle_triangle(10, 6, 8) == True
```

## Visible tests

```python
assert right_angle_triangle(3, 4, 5) == True
assert right_angle_triangle(1, 2, 3) == False
assert right_angle_triangle(10, 6, 8) == True
```
