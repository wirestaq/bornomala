---
title: "Ordinals"
weight: 4
---

# Ordinals

Generate Bangla ordinal strings — ১ম, ২য়, ৪র্থ, ১১তম, and so on.

```python
from bornomala import to_bangla_ordinal
```

---

## `to_bangla_ordinal(n)`

**Signature**

```python
def to_bangla_ordinal(n: int) -> str
```

**Parameters**

| Parameter | Type | Description |
|-----------|------|-------------|
| `n` | `int` | A positive integer. Floats are truncated via `int()`. |

**Raises** `ValueError` for zero or negative input.

---

## Suffix rules

| Range | Suffix | Example |
|-------|--------|---------|
| 1 | ম | ১ম |
| 2 | য় | ২য় |
| 3 | য় | ৩য় |
| 4 | র্থ | ৪র্থ |
| 5 | ম | ৫ম |
| 6 | ষ্ঠ | ৬ষ্ঠ |
| 7 | ম | ৭ম |
| 8 | ম | ৮ম |
| 9 | ম | ৯ম |
| 10 | ম | ১০ম |
| 11+ | তম | ১১তম, ১০০তম … |

---

## Full reference table (1–20)

| n | Ordinal | Meaning |
|---|---------|---------|
| 1 | ১ম | প্রথম (first) |
| 2 | ২য় | দ্বিতীয় (second) |
| 3 | ৩য় | তৃতীয় (third) |
| 4 | ৪র্থ | চতুর্থ (fourth) |
| 5 | ৫ম | পঞ্চম (fifth) |
| 6 | ৬ষ্ঠ | ষষ্ঠ (sixth) |
| 7 | ৭ম | সপ্তম (seventh) |
| 8 | ৮ম | অষ্টম (eighth) |
| 9 | ৯ম | নবম (ninth) |
| 10 | ১০ম | দশম (tenth) |
| 11 | ১১তম | একাদশ (eleventh) |
| 12 | ১২তম | দ্বাদশ (twelfth) |
| 13 | ১৩তম | ত্রয়োদশ |
| 14 | ১৪তম | চতুর্দশ |
| 15 | ১৫তম | পঞ্চদশ |
| 20 | ২০তম | বিংশ |

---

## Examples

```python
to_bangla_ordinal(1)     # '১ম'
to_bangla_ordinal(2)     # '২য়'
to_bangla_ordinal(3)     # '৩য়'
to_bangla_ordinal(4)     # '৪র্থ'
to_bangla_ordinal(6)     # '৬ষ্ঠ'
to_bangla_ordinal(10)    # '১০ম'
to_bangla_ordinal(11)    # '১১তম'
to_bangla_ordinal(21)    # '২১তম'
to_bangla_ordinal(100)   # '১০০তম'
to_bangla_ordinal(999)   # '৯৯৯তম'
```

### In practice

```python
# Class rankings
students = ["রাফি", "সিয়াম", "নাফিসা", "তাহমিনা"]
for i, name in enumerate(students, 1):
    print(f"{to_bangla_ordinal(i)} স্থান: {name}")
# ১ম স্থান: রাফি
# ২য় স্থান: সিয়াম
# ৩য় স্থান: নাফিসা
# ৪র্থ স্থান: তাহমিনা

# Exam question numbers
questions = range(1, 6)
for q in questions:
    print(f"{to_bangla_ordinal(q)} প্রশ্ন")
# ১ম প্রশ্ন … ৫ম প্রশ্ন
```

### Error handling

```python
to_bangla_ordinal(0)    # ValueError: requires a positive integer
to_bangla_ordinal(-5)   # ValueError: requires a positive integer
```
