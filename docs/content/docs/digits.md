---
title: "Digits"
weight: 3
---

# Digits

Convert between Western ASCII digits (`0`–`9`) and Bangla Unicode digits (`০`–`৯`).

```python
from bornomala import to_bangla_digits, to_western_digits
```

---

## Digit mapping

| Western | Bangla |
|---------|--------|
| 0 | ০ |
| 1 | ১ |
| 2 | ২ |
| 3 | ৩ |
| 4 | ৪ |
| 5 | ৫ |
| 6 | ৬ |
| 7 | ৭ |
| 8 | ৮ |
| 9 | ৯ |

---

## `to_bangla_digits(n)`

Convert Western digits in `n` to Bangla Unicode digits. Non-digit characters are left unchanged.

**Signature**

```python
def to_bangla_digits(n: int | float | str) -> str
```

### Examples

```python
to_bangla_digits(0)         # '০'
to_bangla_digits(2026)      # '২০২৬'
to_bangla_digits(3.14)      # '৩.১৪'
to_bangla_digits(-42)       # '-৪২'
to_bangla_digits("3.14")    # '৩.১৪'
to_bangla_digits("abc")     # 'abc'   ← non-digits unchanged
to_bangla_digits("year 2026")  # 'year ২০২৬'
```

### Use in formatting

```python
# Bangla page numbers
pages = [1, 2, 3, 10, 11]
bangla_pages = [to_bangla_digits(p) for p in pages]
# ['১', '২', '৩', '১০', '১১']

# Bangla phone number
phone = "01712-345678"
to_bangla_digits(phone)   # '০১৭১২-৩৪৫৬৭৮'

# Bangla year in text
f"সাল: {to_bangla_digits(2026)}"   # 'সাল: ২০২৬'
```

---

## `to_western_digits(text)`

Convert Bangla Unicode digits in `text` to Western ASCII digits. Non-digit characters are left unchanged.

**Signature**

```python
def to_western_digits(text: str) -> str
```

### Examples

```python
to_western_digits("০")          # '0'
to_western_digits("২০২৬")      # '2026'
to_western_digits("৩.১৪")      # '3.14'
to_western_digits("-৪২")        # '-42'
to_western_digits("abc")        # 'abc'
to_western_digits("১2৩")       # '123'   ← mixed digits normalised
```

---

## Round-trip guarantee

```python
from bornomala import to_bangla_digits, to_western_digits

for i in range(10000):
    assert to_western_digits(to_bangla_digits(i)) == str(i)
```

---

## Notes

- Both functions operate via Unicode translation tables and run in **O(n)** time with no allocations beyond the output string.
- Only the ten Bangla digit codepoints (U+09E6–U+09EF) are translated; all other characters pass through unchanged.
- Bangla digits are used throughout bornomala in all formatted output — `strftime`, `to_bangla_ordinal`, `format_currency`, etc.
