# bornomala — বর্ণমালা

**Bangla text toolkit for Python.** Convert numbers to Bangla words, format dates in Bengali script, work with the বঙ্গাব্দ calendar, generate ordinals, format currency, and normalize Bangla Unicode — all with zero dependencies.

[![PyPI version](https://img.shields.io/pypi/v/bornomala?color=c0392b)](https://pypi.org/project/bornomala/)
[![Python versions](https://img.shields.io/pypi/pyversions/bornomala?color=5b21b6)](https://pypi.org/project/bornomala/)
[![License: MIT](https://img.shields.io/github/license/wirestaq/bornomala)](LICENSE)
[![Test coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/wirestaq/bornomala)
[![Tests](https://img.shields.io/badge/tests-440%20passed-brightgreen)](https://github.com/wirestaq/bornomala)

---

## What is bornomala?

**bornomala** (বর্ণমালা — *garland of letters*) is a pure-Python library for Bangla / Bengali text processing. It covers the most common needs when building Bangla-language applications: rendering numbers as words for cheques and invoices, displaying dates and times in Bengali script, converting between the Gregorian and Bengali calendar (বঙ্গাব্দ), and cleaning Bangla Unicode text.

**Key highlights:**

- ✅ **Zero runtime dependencies** — only the Python standard library
- ✅ **Python 3.5 – 3.13** tested via tox on every minor version
- ✅ **100% test coverage** — 440 tests across 10 modules
- ✅ **Type-annotated** — ships with `py.typed`
- ✅ **Revised Bengali Calendar** (Bangladesh / Bangla Academy standard)

---

## Installation

```bash
pip install bornomala
```

```bash
uv add bornomala          # uv
poetry add bornomala      # Poetry
```

---

## Features at a glance

### 🔢 Numbers in words (`num_to_words`, `words_to_num`)

Convert any integer, float, or numeric string to natural Bangla words — and back.

```python
from bornomala import num_to_words, words_to_num

num_to_words(0)           # 'শূন্য'
num_to_words(1234)        # 'এক হাজার দুইশত চৌত্রিশ'
num_to_words(10_000_000)  # 'এক কোটি'
num_to_words(-42)         # 'ঋণাত্মক বিয়াল্লিশ'
num_to_words("3.14")      # 'তিন দশমিক এক চার'
num_to_words("১২৩৪")     # 'এক হাজার দুইশত চৌত্রিশ'  ← Bangla digits accepted

words_to_num("এক হাজার দুইশত চৌত্রিশ")   # 1234
words_to_num("তিন দশমিক এক চার")          # 3.14

# Chainable suffix methods on the returned BanglaWords object
num_to_words(500).taka().only()   # 'পাঁচশত টাকা মাত্র'
num_to_words(3).jon()             # 'তিন জন'
num_to_words(10).kilo()           # 'দশ কিলোগ্রাম'
num_to_words(25).percent()        # 'পঁচিশ শতাংশ'
```

Supports numbers up to and beyond কোটি (10 million), including hundreds of crores.

---

### ০ Digit conversion (`to_bangla_digits`, `to_western_digits`)

Swap between Western ASCII digits and Bangla Unicode digits anywhere in a string.

```python
from bornomala import to_bangla_digits, to_western_digits

to_bangla_digits(2026)        # '২০২৬'
to_bangla_digits("01712-345678")  # '০১৭১২-৩৪৫৬৭৮'
to_western_digits("২০২৬")    # '2026'
to_western_digits("১2৩")     # '123'   ← mixed digits normalised
```

---

### ১ম Ordinal numbers (`to_bangla_ordinal`)

Generate correct Bangla ordinal suffixes for any positive integer.

```python
from bornomala import to_bangla_ordinal

to_bangla_ordinal(1)    # '১ম'
to_bangla_ordinal(2)    # '২য়'
to_bangla_ordinal(4)    # '৪র্থ'
to_bangla_ordinal(6)    # '৬ষ্ঠ'
to_bangla_ordinal(11)   # '১১তম'
to_bangla_ordinal(100)  # '১০০তম'
```

Rules: 1 → ম, 2–3 → য়, 4 → র্থ, 5–10 → ম, 6 → ষ্ঠ, 11+ → তম.

---

### ৳ Cheque-style currency (`format_currency`)

Format monetary amounts as Bengali word strings — perfect for bank drafts, invoices, and official documents.

```python
from bornomala import format_currency

format_currency(96250)         # 'ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা মাত্র'
format_currency("1234.56")     # 'এক হাজার দুইশত চৌত্রিশ টাকা ছাপান্ন পয়সা মাত্র'
format_currency(500, unit="ডলার")          # 'পাঁচশত ডলার মাত্র'
format_currency("9.99", unit="ডলার", paisa_unit="সেন্ট")
# 'নয় ডলার নিরানব্বই সেন্ট মাত্র'
```

---

### 📅 Bangla date & time (`BanglaDate`, `BanglaDatetime`)

Drop-in wrappers for Python's `datetime.date` / `datetime.datetime` — same constructors, same methods, all text output in Bangla.

```python
from bornomala import BanglaDate, BanglaDatetime, FMT_DATE_WEEKDAY, FMT_TIME_12H
from datetime import date

# Construction — three equivalent forms
BanglaDate(2026, 3, 12)
BanglaDate(date(2026, 3, 12))
BanglaDate.fromisoformat("2026-03-12")

str(BanglaDate(2026, 3, 12))               # '১২ মার্চ ২০২৬'
BanglaDate(2026, 3, 12).strftime(FMT_DATE_WEEKDAY)
# 'বৃহস্পতিবার, ১২ মার্চ ২০২৬'

bdt = BanglaDatetime(2026, 3, 12, 10, 30)
str(bdt)                                   # 'বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০'
bdt.strftime(FMT_TIME_12H)                 # '১০:৩০ পূর্বাহ্ন'
```

**7 ready-made format presets:** `FMT_DATE_LONG`, `FMT_DATE_SHORT`, `FMT_DATE_WEEKDAY`, `FMT_DATETIME_LONG`, `FMT_DATETIME_SHORT`, `FMT_TIME_12H`, `FMT_TIME_24H`.

**Full timezone support:**

```python
from bornomala import BanglaDatetime, timezone, timedelta

bst = timezone(timedelta(hours=6))   # Bangladesh Standard Time
BanglaDatetime.now(tz=bst)
BanglaDatetime.utcnow()
```

---

### 🗓 Bangla calendar / বঙ্গাব্দ (`gregorian_to_bangla`, `bangla_to_gregorian`)

Convert between the Gregorian calendar and the **Revised Bengali Calendar** (Bangla Academy, Bangladesh), including month names and ঋতু seasons.

```python
from bornomala import gregorian_to_bangla, bangla_to_gregorian, BanglaCalendarDate
from datetime import date

bd = gregorian_to_bangla(date(2026, 3, 12))
str(bd)          # '২৮ ফাল্গুন ১৪৩২'
bd.month_name    # 'ফাল্গুন'
bd.season        # 'বসন্ত'

gregorian_to_bangla(date(2026, 4, 14))  # পহেলা বৈশাখ → BanglaCalendarDate(1433, 1, 1)

# Round-trip
bangla_to_gregorian(BanglaCalendarDate(1433, 1, 1))  # date(2026, 4, 14)
```

The six seasons: গ্রীষ্ম · বর্ষা · শরৎ · হেমন্ত · শীত · বসন্ত

---

### ✏️ Text utilities (`normalize`, `is_bangla`, `is_pure_bangla`, `bangla_char_count`)

Clean, detect, and analyse Bangla Unicode text.

```python
from bornomala import normalize, is_bangla, is_pure_bangla, bangla_char_count

# NFC normalisation + whitespace collapse + danda repair
normalize("আমার  সোনার  বাংলা")   # 'আমার সোনার বাংলা'
normalize("এক|দুই")              # 'এক।দুই'   ← pipe → danda (OCR fix)

# Script detection
is_bangla("hello আমি")           # True
is_bangla("hello")               # False

# Purity check (no Latin/Arabic digits or other scripts)
is_pure_bangla("আমার বাংলা।")   # True
is_pure_bangla("আমি 10 জন।")    # False

# Character count (Bangla block only)
bangla_char_count("hello আমি")  # 3
```

---

## Full API reference

| Function / Class | Module | Description |
|------------------|--------|-------------|
| `num_to_words(n)` | numbers | Number → Bangla words |
| `words_to_num(text)` | numbers | Bangla words → number |
| `BanglaWords` | numbers | `str` subclass with `.taka()`, `.jon()`, `.only()` … |
| `to_bangla_digits(n)` | digits | Western → Bangla digit characters |
| `to_western_digits(text)` | digits | Bangla → Western digit characters |
| `to_bangla_ordinal(n)` | ordinals | Integer → Bangla ordinal string |
| `format_currency(amount)` | currency | Amount → cheque-style Bangla string |
| `BanglaDate` | datetime | `datetime.date` wrapper with Bangla output |
| `BanglaDatetime` | datetime | `datetime.datetime` wrapper with Bangla output |
| `bangla_strftime(dt, fmt)` | datetime | Format any date/datetime in Bangla |
| `BanglaCalendarDate` | calendar | Bangla calendar date object |
| `gregorian_to_bangla(date)` | calendar | Gregorian → বঙ্গাব্দ |
| `bangla_to_gregorian(bdate)` | calendar | বঙ্গাব্দ → Gregorian |
| `normalize(text)` | text | NFC + whitespace + danda repair |
| `is_bangla(text)` | text | Detect any Bangla characters |
| `is_pure_bangla(text)` | text | Detect exclusively Bangla text |
| `bangla_char_count(text)` | text | Count Bangla characters |

---

## Documentation

Full documentation with comprehensive examples is available at:
**[https://wirestaq.github.io/bornomala/](https://wirestaq.github.io/bornomala/)**

To run the docs locally:

```bash
cd docs
hugo server
# → http://localhost:1313/bornomala/
```

---

## Development

```bash
git clone https://github.com/wirestaq/bornomala.git
cd bornomala
uv sync
uv run pytest          # run tests
uv run tox             # test across Python 3.8 – 3.13
```

Test coverage:

```bash
uv run pytest --cov=bornomala --cov-report=term-missing
```

---

## Contributing

Issues and pull requests are welcome at [github.com/wirestaq/bornomala](https://github.com/wirestaq/bornomala).

Please open an issue before submitting a PR for new features.

---

## License

MIT © [Wirestaq](https://github.com/wirestaq)
