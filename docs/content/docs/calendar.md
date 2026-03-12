---
title: "Bangla Calendar"
weight: 7
---

# Bangla Calendar (বঙ্গাব্দ)

Convert between the Gregorian calendar and the **Revised Bengali Calendar** (শংশোধিত বাংলা পঞ্জিকা) as standardised by the Bangla Academy, Bangladesh.

```python
from bornomala import (
    BanglaCalendarDate,
    gregorian_to_bangla,
    bangla_to_gregorian,
    BANGLA_CAL_MONTHS,
    BANGLA_SEASONS,
)
from datetime import date
```

---

## Calendar overview

The Revised Bengali Calendar (১৯৮৭):

- The new year (**পহেলা বৈশাখ**) always falls on **14 April** (Gregorian).
- Months 1–5 have **31 days**; months 6–11 have **30 days**.
- Month 12 (চৈত্র) has **30 days** in regular years, **31** in leap years.
- The Bangla year = Gregorian year − 593 (on or after 14 April) or − 594 (before 14 April).

---

## Month reference

| # | Month | Season (ঋতু) | Gregorian start |
|---|-------|-------------|-----------------|
| 1 | বৈশাখ | গ্রীষ্ম | 14 April |
| 2 | জ্যৈষ্ঠ | গ্রীষ্ম | 15 May |
| 3 | আষাঢ় | বর্ষা | 15 June |
| 4 | শ্রাবণ | বর্ষা | 16 July |
| 5 | ভাদ্র | শরৎ | 16 August |
| 6 | আশ্বিন | শরৎ | 17 September |
| 7 | কার্তিক | হেমন্ত | 17 October |
| 8 | অগ্রহায়ণ | হেমন্ত | 16 November |
| 9 | পৌষ | শীত | 15 December |
| 10 | মাঘ | শীত | 14 January |
| 11 | ফাল্গুন | বসন্ত | 13 February |
| 12 | চৈত্র | বসন্ত | 14 March |

---

## `gregorian_to_bangla(gdate)`

Convert a `datetime.date` to a `BanglaCalendarDate`.

**Signature**

```python
def gregorian_to_bangla(gdate: datetime.date) -> BanglaCalendarDate
```

### Examples

```python
gregorian_to_bangla(date(2026, 4, 14))  # BanglaCalendarDate(1433, 1, 1)
str(gregorian_to_bangla(date(2026, 4, 14)))   # '১ বৈশাখ ১৪৩৩'

gregorian_to_bangla(date(2026, 3, 12))  # BanglaCalendarDate(1432, 11, 28)
str(gregorian_to_bangla(date(2026, 3, 12)))   # '২৮ ফাল্গুন ১৪৩২'

gregorian_to_bangla(date(2026, 4, 13))  # BanglaCalendarDate(1432, 12, 31)
gregorian_to_bangla(date(2025, 7, 16))  # BanglaCalendarDate(1432, 4, 1)
gregorian_to_bangla(date(2026, 1, 14))  # BanglaCalendarDate(1432, 10, 1)
```

---

## `bangla_to_gregorian(bdate)`

Convert a `BanglaCalendarDate` back to a `datetime.date`.

**Signature**

```python
def bangla_to_gregorian(bdate: BanglaCalendarDate) -> datetime.date
```

### Examples

```python
bangla_to_gregorian(BanglaCalendarDate(1433, 1, 1))
# datetime.date(2026, 4, 14)

bangla_to_gregorian(BanglaCalendarDate(1432, 11, 28))
# datetime.date(2026, 3, 12)
```

### Round-trip

```python
dates = [date(2026, 1, 1), date(2026, 4, 14), date(2026, 7, 4), date(2025, 12, 31)]
for d in dates:
    assert bangla_to_gregorian(gregorian_to_bangla(d)) == d   # always holds
```

---

## `BanglaCalendarDate`

### Construction

```python
BanglaCalendarDate(year, month, day)
BanglaCalendarDate(1432, 11, 28)   # ২৮ ফাল্গুন ১৪৩২
```

| Parameter | Range | Description |
|-----------|-------|-------------|
| `year` | any positive int | Bangla year (বঙ্গাব্দ) |
| `month` | 1–12 | Bangla month number |
| `day` | 1–31 | Day within the month |

Raises `ValueError` for invalid month or day < 1.

### Attributes

```python
bd = gregorian_to_bangla(date(2026, 3, 12))

bd.year         # 1432
bd.month        # 11
bd.day          # 28
bd.month_name   # 'ফাল্গুন'
bd.season       # 'বসন্ত'
```

### `__str__`

Returns `"{day} {month_name} {year}"` in Bangla digits:

```python
str(BanglaCalendarDate(1432, 11, 28))   # '২৮ ফাল্গুন ১৪৩২'
str(BanglaCalendarDate(1433, 1, 1))     # '১ বৈশাখ ১৪৩৩'
```

### Comparisons

```python
a = BanglaCalendarDate(1432, 1, 1)
b = BanglaCalendarDate(1432, 12, 30)

a < b    # True
a <= b   # True
b > a    # True
b >= a   # True
a == a   # True
```

---

## Seasons (ঋতু)

| Season | Months | Description |
|--------|--------|-------------|
| গ্রীষ্ম | বৈশাখ–জ্যৈষ্ঠ | Summer |
| বর্ষা | আষাঢ়–শ্রাবণ | Monsoon |
| শরৎ | ভাদ্র–আশ্বিন | Autumn |
| হেমন্ত | কার্তিক–অগ্রহায়ণ | Late autumn |
| শীত | পৌষ–মাঘ | Winter |
| বসন্ত | ফাল্গুন–চৈত্র | Spring |

```python
from bornomala import BANGLA_SEASONS

BANGLA_SEASONS[1]   # 'গ্রীষ্ম'  (বৈশাখ)
BANGLA_SEASONS[3]   # 'বর্ষা'   (আষাঢ়)
BANGLA_SEASONS[11]  # 'বসন্ত'  (ফাল্গুন)
```

---

## Practical examples

### Today in Bangla calendar

```python
from datetime import date
from bornomala import gregorian_to_bangla

today = gregorian_to_bangla(date.today())
print(f"আজ: {today}")             # e.g. আজ: ২৮ ফাল্গুন ১৪৩২
print(f"ঋতু: {today.season}")    # ঋতু: বসন্ত
```

### Bengali New Year countdown

```python
from datetime import date
from bornomala import gregorian_to_bangla, BanglaDate, to_bangla_digits

new_year = date(2026, 4, 14)  # পহেলা বৈশাখ ১৪৩৩
days_left = (new_year - date.today()).days
print(f"পহেলা বৈশাখ আর {to_bangla_digits(days_left)} দিন বাকি")
```

### Calendar header

```python
from datetime import date
from bornomala import gregorian_to_bangla, BANGLA_CAL_MONTHS

for month_num, month_name in enumerate(BANGLA_CAL_MONTHS, 1):
    print(f"{month_num:2d}. {month_name}")
# 1. বৈশাখ
# 2. জ্যৈষ্ঠ
# ...
```
