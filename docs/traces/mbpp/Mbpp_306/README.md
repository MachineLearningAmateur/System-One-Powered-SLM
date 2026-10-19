# Mbpp/306

Benchmark: mbpp+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 3 | no visible pass after round 3 | 8192 / 3108 / 4101 | 1 |
| [Attempt 1](attempt_1.md) | 3 | no visible pass after round 3 | 8192 / 7179 / 8192 | 2 |
| [Attempt 2](attempt_2.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 3](attempt_3.md) | 3 | no visible pass after round 3 | 8192 / 8192 / 8192 | 3 |
| [Attempt 4](attempt_4.md) | 3 | no visible pass after round 3 | 8192 / 4078 / 7076 | 1 |

## Prompt shown to the model (round 1)

```python
"""
Write a function to find the maximum sum of increasing subsequence from prefix until ith index and also including a given kth element which is after i, i.e., k > i .
assert max_sum_increasing_subseq([1, 101, 2, 3, 100, 4, 5 ], 7, 4, 6) == 11
"""
```

## Visible tests

```python
assert max_sum_increasing_subseq([1, 101, 2, 3, 100, 4, 5 ], 7, 4, 6) == 11
```
