---
title: "bornomala"
type: docs
---

<div class="bornomala-hero">
  <div class="logo">বর্ণমালা</div>
  <div class="tagline">Bangla text toolkit for Python</div>
  <div class="badge-row">
    <img src="https://img.shields.io/pypi/v/bornomala?color=c0392b" alt="PyPI">
    <img src="https://img.shields.io/pypi/pyversions/bornomala?color=5b21b6" alt="Python">
    <img src="https://img.shields.io/github/license/wirestaq/bornomala" alt="License">
    <img src="https://img.shields.io/badge/coverage-100%25-brightgreen" alt="Coverage">
  </div>
</div>

**bornomala** (বর্ণমালা — *garland of letters*) is a zero-dependency Python library for working with Bangla text: numbers, digits, dates, the Bangla calendar, ordinals, currency, and Unicode utilities.

```bash
pip install bornomala-py
```

---

## Feature overview

<div class="feature-grid">
  <div class="feature-card">
    <h3>🔢 Numbers in words</h3>
    <p>Convert any number — including negatives and decimals — to natural Bangla words (কথায়), and back.</p>
  </div>
  <div class="feature-card">
    <h3>০ Digit conversion</h3>
    <p>Swap between Western ASCII digits (0–9) and Bangla Unicode digits (০–৯) in any string.</p>
  </div>
  <div class="feature-card">
    <h3>১ম Ordinals</h3>
    <p>Generate correct Bangla ordinal suffixes: ১ম, ২য়, ৪র্থ, ৬ষ্ঠ, ১১তম …</p>
  </div>
  <div class="feature-card">
    <h3>৳ Currency</h3>
    <p>Cheque-style amount words with টাকা/পয়সা, customisable for any currency.</p>
  </div>
  <div class="feature-card">
    <h3>📅 Bangla datetime</h3>
    <p>Drop-in wrappers for <code>datetime.date/datetime</code> with Bangla <code>strftime</code> and 7 format presets.</p>
  </div>
  <div class="feature-card">
    <h3>🗓 বঙ্গাব্দ Calendar</h3>
    <p>Convert Gregorian dates to the Revised Bengali Calendar and back, with month names and ঋতু seasons.</p>
  </div>
  <div class="feature-card">
    <h3>✏️ Text utilities</h3>
    <p>NFC normalisation, danda repair, whitespace cleanup, script detection, and character counting.</p>
  </div>
</div>

---

## Quick example

```python
from bornomala import (
    num_to_words, to_bangla_digits,
    to_bangla_ordinal, format_currency,
    BanglaDate, gregorian_to_bangla,
    normalize, is_bangla,
)
from datetime import date

# Numbers → words
num_to_words(1432)           # 'এক হাজার চারশত বত্রিশ'
num_to_words(3.14)           # 'তিন দশমিক এক চার'
num_to_words(-99)            # 'ঋণাত্মক নিরানব্বই'

# Digit conversion
to_bangla_digits(2026)       # '২০২৬'
to_bangla_digits("3.14")     # '৩.১৪'

# Ordinals
to_bangla_ordinal(1)         # '১ম'
to_bangla_ordinal(4)         # '৪র্থ'
to_bangla_ordinal(21)        # '২১তম'

# Currency
format_currency(96250)       # 'ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা মাত্র'
format_currency("1234.56")   # 'এক হাজার দুইশত চৌত্রিশ টাকা ছাপান্ন পয়সা মাত্র'

# Bangla date
str(BanglaDate(2026, 3, 12)) # '১২ মার্চ ২০২৬'
BanglaDate.today().strftime("%A, %e %B %Y")  # 'বৃহস্পতিবার, ১২ মার্চ ২০২৬'

# Bangla calendar
bd = gregorian_to_bangla(date(2026, 3, 12))
str(bd)        # '২৮ ফাল্গুন ১৪৩২'
bd.season      # 'বসন্ত'

# Text utilities
normalize("আমার  সোনার  বাংলা")   # 'আমার সোনার বাংলা'
is_bangla("hello আমি")            # True
```

---

## Installation

| Manager | Command |
|---------|---------|
| pip | `pip install bornomala-py` |
| uv | `uv add bornomala-py` |
| poetry | `poetry add bornomala-py` |

Requires **Python 3.5 +** with no runtime dependencies.

---

## Browse the docs

{{< columns >}}
- [**Getting started →**]({{< relref "/docs/getting-started" >}})
  Install, import, and run your first conversion in two minutes.
- [**API reference →**]({{< relref "/docs/numbers" >}})
  Complete reference for every function and class.
{{< /columns >}}
