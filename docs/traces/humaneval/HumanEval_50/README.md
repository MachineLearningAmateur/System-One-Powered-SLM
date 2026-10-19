# HumanEval/50

Benchmark: humaneval+. Run: `main-test-v1`. Back to the [index](../../README.md).

## Attempts

| Attempt | Rounds | End | Thinking tokens per round | Cap hits |
| --- | --- | --- | --- | --- |
| [Attempt 0](attempt_0.md) | 1 | visible pass | 7185 | 0 |
| [Attempt 1](attempt_1.md) | 1 | visible pass | 3955 | 0 |
| [Attempt 2](attempt_2.md) | 1 | visible pass | 2908 | 0 |
| [Attempt 3](attempt_3.md) | 1 | visible pass | 5843 | 0 |
| [Attempt 4](attempt_4.md) | 1 | visible pass | 4498 | 0 |

## Prompt shown to the model (round 1)

```python


def encode_shift(s: str):
    """
    returns encoded string by shifting every character by 5 in the alphabet.
    """
    return "".join([chr(((ord(ch) + 5 - ord("a")) % 26) + ord("a")) for ch in s])


def decode_shift(s: str):
    """
    takes as input string encoded with encode_shift function. Returns decoded string.
    """

Visible tests:
assert decode_shift('tantywccpjkimslotpzs') == 'oviotrxxkefdhngjokun'
assert decode_shift('clknfxdnox') == 'xgfiasyijs'
assert decode_shift('dtzqyosaovdbafbg') == 'youltjnvjqywvawb'
```

## Visible tests

```python
assert decode_shift('tantywccpjkimslotpzs') == 'oviotrxxkefdhngjokun'
assert decode_shift('clknfxdnox') == 'xgfiasyijs'
assert decode_shift('dtzqyosaovdbafbg') == 'youltjnvjqywvawb'
```
