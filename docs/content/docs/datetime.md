---
title: "Date & Time"
weight: 6
---

# Date & Time

Bangla-aware wrappers for Python's `datetime.date` and `datetime.datetime`. Same constructors, same methods — all text output in Bangla.

```python
from bornomala import BanglaDate, BanglaDatetime, bangla_strftime
from bornomala import FMT_DATE_LONG, FMT_DATE_SHORT, FMT_DATE_WEEKDAY
from bornomala import FMT_DATETIME_LONG, FMT_DATETIME_SHORT
from bornomala import FMT_TIME_12H, FMT_TIME_24H
from bornomala import timezone, timedelta
```

---

## `BanglaDate`

A wrapper for `datetime.date` that returns Bangla text from `strftime` and `__str__`.

### Construction

All three forms are equivalent:

```python
from datetime import date
from bornomala import BanglaDate

BanglaDate(2026, 3, 12)           # year, month, day
BanglaDate(date(2026, 3, 12))     # wrap an existing date
BanglaDate.fromisoformat("2026-03-12")
BanglaDate.fromtimestamp(1741737600)
BanglaDate.today()
```

### `strftime(fmt)`

```python
bd = BanglaDate(2026, 3, 12)

bd.strftime("%e %B %Y")           # '১২ মার্চ ২০২৬'
bd.strftime("%A, %e %B %Y")       # 'বৃহস্পতিবার, ১২ মার্চ ২০২৬'
bd.strftime("%d/%m/%Y")           # '১২/০৩/২০২৬'
bd.strftime("%b %Y")              # 'মার্চ ২০২৬'
```

### `__str__`

Defaults to `FMT_DATE_LONG` (`%e %B %Y`):

```python
str(BanglaDate(2026, 3, 12))     # '১২ মার্চ ২০২৬'
str(BanglaDate(2026, 1, 1))      # '১ জানুয়ারি ২০২৬'
```

### Attributes & methods

```python
bd = BanglaDate(2026, 3, 12)

bd.year           # 2026
bd.month          # 3
bd.day            # 12
bd.weekday()      # 3  (0=Monday … 6=Sunday)
bd.isoweekday()   # 4  (1=Monday … 7=Sunday)
bd.month_name()   # 'মার্চ'
bd.weekday_name() # 'বৃহস্পতিবার'
bd.isoformat()    # '2026-03-12'
```

---

## `BanglaDatetime`

Extends `BanglaDate` with time support. Wraps `datetime.datetime`.

### Construction

```python
from datetime import datetime, date
from bornomala import BanglaDatetime

BanglaDatetime(2026, 3, 12, 10, 30)            # year, month, day, hour, minute
BanglaDatetime(datetime(2026, 3, 12, 10, 30))  # wrap existing datetime
BanglaDatetime(date(2026, 3, 12))              # promote date → midnight
BanglaDatetime(date(2026, 3, 12), hour=9, minute=15)  # promote with time

BanglaDatetime.now()
BanglaDatetime.utcnow()
BanglaDatetime.fromisoformat("2026-03-12T10:30:45")
BanglaDatetime.fromtimestamp(1741737600)
```

### Timezone support

```python
from bornomala import timezone, timedelta

# UTC
BanglaDatetime.now(tz=timezone.utc)

# Bangladesh Standard Time (UTC+6)
bst = timezone(timedelta(hours=6))
BanglaDatetime(2026, 3, 12, 10, 30, tzinfo=bst)

# Promote a date to a timezone-aware datetime
BanglaDatetime.from_date(date(2026, 3, 12), tzinfo=timezone.utc)
```

### `__str__`

Defaults to `FMT_DATETIME_LONG` (`%A, %e %B %Y, %H:%M`):

```python
str(BanglaDatetime(2026, 3, 12, 10, 30))
# 'বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০'
```

### Time attributes

```python
bdt = BanglaDatetime(2026, 3, 12, 10, 30, 45, 123456)

bdt.hour         # 10
bdt.minute       # 30
bdt.second       # 45
bdt.microsecond  # 123456
bdt.tzinfo       # None (or tzinfo object if set)

bdt.date()       # BanglaDate(2026, 3, 12)
bdt.time_str()   # '১০:৩০:৪৫'  (FMT_TIME_24H by default)
bdt.time_str(FMT_TIME_12H)  # '১০:৩০ পূর্বাহ্ন'
```

---

## `bangla_strftime(dt, fmt)`

Format any `datetime.date` or `datetime.datetime` object with Bangla output, without wrapping it in `BanglaDate`.

```python
from datetime import date
from bornomala import bangla_strftime

bangla_strftime(date(2026, 3, 12), "%e %B %Y")  # '১২ মার্চ ২০২৬'
```

---

## Format codes

| Code | Output | Example |
|------|--------|---------|
| `%Y` | 4-digit year | `২০২৬` |
| `%y` | 2-digit year | `২৬` |
| `%m` | Month, zero-padded | `০৩` |
| `%d` | Day, zero-padded | `০১` |
| `%e` | Day, no leading zero | `১` |
| `%B` | Full month name | `মার্চ` |
| `%b` | Abbreviated month name | `মার্চ` |
| `%A` | Full weekday name | `বৃহস্পতিবার` |
| `%a` | Abbreviated weekday name | `বৃহ` |
| `%H` | Hour, 24h zero-padded | `১০` |
| `%I` | Hour, 12h zero-padded | `১০` |
| `%M` | Minute, zero-padded | `৩০` |
| `%S` | Second, zero-padded | `৪৫` |
| `%p` | AM/PM | `পূর্বাহ্ন` / `অপরাহ্ন` |
| `%%` | Literal `%` | `%` |

Unknown codes (e.g. `%Z`) pass through unchanged.

---

## Predefined format presets

| Constant | Pattern | Example output |
|----------|---------|----------------|
| `FMT_DATE_LONG` | `%e %B %Y` | `১২ মার্চ ২০২৬` |
| `FMT_DATE_SHORT` | `%d/%m/%Y` | `১২/০৩/২০২৬` |
| `FMT_DATE_WEEKDAY` | `%A, %e %B %Y` | `বৃহস্পতিবার, ১২ মার্চ ২০২৬` |
| `FMT_DATETIME_LONG` | `%A, %e %B %Y, %H:%M` | `বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০` |
| `FMT_DATETIME_SHORT` | `%d/%m/%Y %H:%M` | `১২/০৩/২০২৬ ১০:৩০` |
| `FMT_TIME_12H` | `%I:%M %p` | `১০:৩০ পূর্বাহ্ন` |
| `FMT_TIME_24H` | `%H:%M:%S` | `১০:৩০:৪৫` |

```python
from bornomala import BanglaDatetime, FMT_TIME_12H, FMT_DATETIME_SHORT

bdt = BanglaDatetime(2026, 3, 12, 10, 30, 45)

bdt.strftime(FMT_TIME_12H)       # '১০:৩০ পূর্বাহ্ন'
bdt.strftime(FMT_DATETIME_SHORT) # '১২/০৩/২০২৬ ১০:৩০'
```

---

## Month names

| # | Full | Short |
|---|------|-------|
| 1 | জানুয়ারি | জানু |
| 2 | ফেব্রুয়ারি | ফেব্র |
| 3 | মার্চ | মার্চ |
| 4 | এপ্রিল | এপ্রি |
| 5 | মে | মে |
| 6 | জুন | জুন |
| 7 | জুলাই | জুলা |
| 8 | আগস্ট | আগ |
| 9 | সেপ্টেম্বর | সেপ্টে |
| 10 | অক্টোবর | অক্টো |
| 11 | নভেম্বর | নভে |
| 12 | ডিসেম্বর | ডিসে |

## Weekday names

| `weekday()` | Full | Short |
|-------------|------|-------|
| 0 | সোমবার | সোম |
| 1 | মঙ্গলবার | মঙ্গল |
| 2 | বুধবার | বুধ |
| 3 | বৃহস্পতিবার | বৃহ |
| 4 | শুক্রবার | শুক্র |
| 5 | শনিবার | শনি |
| 6 | রবিবার | রবি |
