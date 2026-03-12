---
title: "Numbers"
weight: 2
---

# Numbers

Convert integers, floats, and numeric strings to Bangla words and back.

```python
from bornomala import num_to_words, words_to_num
```

---

## `num_to_words(n)`

Convert a number to its Bangla word representation (কথায়).

**Signature**

```python
def num_to_words(n: int | float | str) -> BanglaWords
```

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `n` | `int`, `float`, or `str` | The number to convert. Strings may contain Western (0–9) or Bangla (০–৯) digits. |

**Returns** — a [`BanglaWords`](#banglawords) instance (subclass of `str`).

### Examples

#### Integers

```python
num_to_words(0)          # 'শূন্য'
num_to_words(1)          # 'এক'
num_to_words(10)         # 'দশ'
num_to_words(100)        # 'একশত'
num_to_words(1000)       # 'এক হাজার'
num_to_words(100000)     # 'এক লক্ষ'
num_to_words(10000000)   # 'এক কোটি'
num_to_words(1234567)    # 'বারো লক্ষ চৌত্রিশ হাজার পাঁচশত সাতষট্টি'
```

#### Negative numbers

```python
num_to_words(-1)     # 'ঋণাত্মক এক'
num_to_words(-42)    # 'ঋণাত্মক বিয়াল্লিশ'
num_to_words(-1000)  # 'ঋণাত্মক এক হাজার'
```

#### Decimals

```python
num_to_words("3.14")    # 'তিন দশমিক এক চার'
num_to_words("0.5")     # 'শূন্য দশমিক পাঁচ'
num_to_words("-2.5")    # 'ঋণাত্মক দুই দশমিক পাঁচ'
num_to_words("1.005")   # 'এক দশমিক শূন্য শূন্য পাঁচ'
```

#### Bangla digit string input

```python
num_to_words("১২৩৪")   # 'এক হাজার দুইশত চৌত্রিশ'
num_to_words("০")      # 'শূন্য'
```

#### Place value reference

| Number | Words |
|--------|-------|
| 100 | একশত |
| 1,000 | এক হাজার |
| 10,000 | দশ হাজার |
| 1,00,000 | এক লক্ষ |
| 10,00,000 | দশ লক্ষ |
| 1,00,00,000 | এক কোটি |
| 10,00,00,000 | দশ কোটি |
| 1,00,00,00,000 | এক হাজার কোটি |

---

## `BanglaWords`

`num_to_words` returns a `BanglaWords` — a `str` subclass with chainable suffix methods.

### Modifier

| Method | Appends | Example |
|--------|---------|---------|
| `.only()` | ` মাত্র` | `num_to_words(500).taka().only()` → `'পাঁচশত টাকা মাত্র'` |

### Currency

| Method | Appends | Usage |
|--------|---------|-------|
| `.taka()` | ` টাকা` | Amount in BDT |
| `.paisa()` | ` পয়সা` | Fractional taka |

### People / object counters

| Method | Appends | Usage |
|--------|---------|-------|
| `.jon()` | ` জন` | Person counter |
| `.ti()` | ` টি` | Generic inanimate counter |
| `.ta()` | ` টা` | Informal generic counter |

### Weight & volume

| Method | Appends |
|--------|---------|
| `.gram()` | ` গ্রাম` |
| `.kilo()` | ` কিলোগ্রাম` |
| `.liter()` | ` লিটার` |

### Distance

| Method | Appends |
|--------|---------|
| `.meter()` | ` মিটার` |
| `.kilo_meter()` | ` কিলোমিটার` |

### Misc

| Method | Appends |
|--------|---------|
| `.percent()` | ` শতাংশ` |
| `.din()` | ` দিন` |
| `.ghonta()` | ` ঘণ্টা` |

### Chaining examples

```python
num_to_words(500).taka().only()     # 'পাঁচশত টাকা মাত্র'
num_to_words(3).jon()               # 'তিন জন'
num_to_words(45).ti()               # 'পঁয়তাল্লিশ টি'
num_to_words(10).kilo()             # 'দশ কিলোগ্রাম'
num_to_words(7).ghonta()            # 'সাত ঘণ্টা'
num_to_words(25).percent()          # 'পঁচিশ শতাংশ'
num_to_words(100).meter()           # 'একশত মিটার'
```

---

## `words_to_num(text)`

Convert a Bangla word string back to a number.

**Signature**

```python
def words_to_num(text: str) -> int | float
```

**Returns** `int` when there is no fractional part; `float` otherwise.

**Raises** `ValueError` for unrecognised tokens or malformed input.

### Examples

```python
words_to_num("শূন্য")                             # 0
words_to_num("এক হাজার দুইশত চৌত্রিশ")           # 1234
words_to_num("ঋণাত্মক বিয়াল্লিশ")               # -42
words_to_num("তিন দশমিক এক চার")                 # 3.14
words_to_num("বারো লক্ষ চৌত্রিশ হাজার পাঁচশত সাতষট্টি")  # 1234567
words_to_num("এক কোটি")                           # 10000000
```

### Error cases

```python
words_to_num("")                      # ValueError: Empty input
words_to_num("hello")                 # ValueError: Unrecognised token
words_to_num("এক দশমিক")             # ValueError: Nothing after দশমিক
words_to_num("ঋণাত্মক")              # ValueError: Nothing after ঋণাত্মক
words_to_num("হাজার")                 # ValueError: Place word with no coefficient
words_to_num("তিন দশমিক ত্রিশ")      # ValueError: ত্রিশ is not a single digit word
```

### Round-trip guarantee

```python
from bornomala import num_to_words, words_to_num

for n in [0, 1, 42, 100, 1234, 99999, 1234567, 10000000]:
    assert words_to_num(num_to_words(n)) == n   # always holds
```
