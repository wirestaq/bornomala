---
title: "Getting Started"
weight: 1
---

# Getting Started

## Installation

Install from PyPI (Python 3.5+ required, no extra dependencies):

```bash
pip install bornomala-py
```

With [uv](https://github.com/astral-sh/uv):

```bash
uv add bornomala-py
```

With Poetry:

```bash
poetry add bornomala-py
```

---

## Python version support

| Python | Supported |
|--------|-----------|
| 3.5    | ✅        |
| 3.6    | ✅        |
| 3.7    | ✅        |
| 3.8    | ✅        |
| 3.9    | ✅        |
| 3.10   | ✅        |
| 3.11   | ✅        |
| 3.12   | ✅        |
| 3.13   | ✅        |

---

## Quick tour

### Numbers in words

```python
from bornomala import num_to_words, words_to_num

num_to_words(0)        # 'শূন্য'
num_to_words(42)       # 'বিয়াল্লিশ'
num_to_words(1234)     # 'এক হাজার দুইশত চৌত্রিশ'
num_to_words(-7)       # 'ঋণাত্মক সাত'
num_to_words("3.14")   # 'তিন দশমিক এক চার'
num_to_words("১২৩")    # 'একশত তেইশ'   ← Bangla digit string accepted

words_to_num("এক হাজার দুইশত চৌত্রিশ")  # 1234
words_to_num("তিন দশমিক এক চার")        # 3.14
```

### Digit conversion

```python
from bornomala import to_bangla_digits, to_western_digits

to_bangla_digits(2026)      # '২০২৬'
to_bangla_digits(-3.14)     # '-৩.১৪'
to_western_digits("২০২৬")  # '2026'
```

### Ordinals

```python
from bornomala import to_bangla_ordinal

to_bangla_ordinal(1)    # '১ম'
to_bangla_ordinal(4)    # '৪র্থ'
to_bangla_ordinal(6)    # '৬ষ্ঠ'
to_bangla_ordinal(11)   # '১১তম'
```

### Currency

```python
from bornomala import format_currency

format_currency(500)          # 'পাঁচশত টাকা মাত্র'
format_currency("1234.50")    # 'এক হাজার দুইশত চৌত্রিশ টাকা পঞ্চাশ পয়সা মাত্র'
```

### Dates

```python
from bornomala import BanglaDate, BanglaDatetime

bd = BanglaDate(2026, 3, 12)
str(bd)                           # '১২ মার্চ ২০২৬'
bd.strftime("%A, %e %B %Y")       # 'বৃহস্পতিবার, ১২ মার্চ ২০২৬'

bdt = BanglaDatetime(2026, 3, 12, 10, 30)
str(bdt)                          # 'বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০'
```

### Bangla calendar

```python
from bornomala import gregorian_to_bangla
from datetime import date

bd = gregorian_to_bangla(date(2026, 3, 12))
str(bd)       # '২৮ ফাল্গুন ১৪৩২'
bd.season     # 'বসন্ত'
```

### Text utilities

```python
from bornomala import normalize, is_bangla, is_pure_bangla, bangla_char_count

normalize("আমার  সোনার  বাংলা")   # 'আমার সোনার বাংলা'
normalize("এক|দুই")              # 'এক।দুই'  (pipe → daari)
is_bangla("hello আমি")           # True
is_pure_bangla("আমার বাংলা।")    # True
bangla_char_count("hello আমি")   # 3
```

---

## What's next

- [Numbers →]({{< relref "numbers" >}})
- [Digits →]({{< relref "digits" >}})
- [Ordinals →]({{< relref "ordinals" >}})
- [Currency →]({{< relref "currency" >}})
- [Date & Time →]({{< relref "datetime" >}})
- [Bangla Calendar →]({{< relref "calendar" >}})
- [Text Utilities →]({{< relref "text" >}})
