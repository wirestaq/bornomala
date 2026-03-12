---
title: "Currency"
weight: 5
---

# Currency

Format monetary amounts as cheque-style Bangla strings — the kind you see on bank drafts and official receipts.

```python
from bornomala import format_currency
```

---

## `format_currency(amount, unit, paisa_unit)`

**Signature**

```python
def format_currency(
    amount: int | float | str,
    unit: str = "টাকা",
    paisa_unit: str = "পয়সা",
) -> str
```

**Parameters**

| Parameter | Default | Description |
|-----------|---------|-------------|
| `amount` | — | The monetary amount. Accepts `int`, `float`, or numeric string (Western or Bangla digits). |
| `unit` | `"টাকা"` | Main currency unit label. |
| `paisa_unit` | `"পয়সা"` | Fractional unit label (1/100 of main unit). |

**Returns** a `str` of the form:
```
<main amount in words> <unit> [<paisa amount in words> <paisa_unit>] মাত্র
```

Fractional digits beyond two decimal places are **truncated** (not rounded).

---

## Examples

### Integer amounts

```python
format_currency(0)       # 'শূন্য টাকা মাত্র'
format_currency(1)       # 'এক টাকা মাত্র'
format_currency(100)     # 'একশত টাকা মাত্র'
format_currency(500)     # 'পাঁচশত টাকা মাত্র'
format_currency(1000)    # 'এক হাজার টাকা মাত্র'
format_currency(96250)   # 'ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা মাত্র'
format_currency(10000000)  # 'এক কোটি টাকা মাত্র'
```

### Fractional amounts

```python
format_currency("1234.56")  # 'এক হাজার দুইশত চৌত্রিশ টাকা ছাপান্ন পয়সা মাত্র'
format_currency("0.50")     # 'শূন্য টাকা পঞ্চাশ পয়সা মাত্র'
format_currency("100.01")   # 'একশত টাকা এক পয়সা মাত্র'
format_currency("10.99")    # 'দশ টাকা নিরানব্বই পয়সা মাত্র'
format_currency("50.00")    # 'পঞ্চাশ টাকা মাত্র'   ← zero paisa omitted
```

### Custom currency units

```python
# US Dollar
format_currency(1250, unit="ডলার", paisa_unit="সেন্ট")
# 'এক হাজার দুইশত পঞ্চাশ ডলার মাত্র'

format_currency("9.99", unit="ডলার", paisa_unit="সেন্ট")
# 'নয় ডলার নিরানব্বই সেন্ট মাত্র'

# British Pound
format_currency("1.50", unit="পাউন্ড", paisa_unit="পেনি")
# 'এক পাউন্ড পঞ্চাশ পেনি মাত্র'

# Euro
format_currency(750, unit="ইউরো")
# 'সাতশত পঞ্চাশ ইউরো মাত্র'
```

### Bangla digit string input

```python
format_currency("৫০০")        # 'পাঁচশত টাকা মাত্র'
format_currency("১২৩৪.৫০")   # 'এক হাজার দুইশত চৌত্রিশ টাকা পঞ্চাশ পয়সা মাত্র'
```

---

## Real-world use cases

### Bank cheque

```python
amount = 96250.75
line = format_currency(amount)
print(f"মোট পরিমাণ: {line}")
# মোট পরিমাণ: ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা পঁচাত্তর পয়সা মাত্র
```

### Invoice total

```python
items = [("বই", 450), ("কলম", 30), ("খাতা", 75)]
total = sum(price for _, price in items)
print(f"মোট: {format_currency(total)}")
# মোট: পাঁচশত পঞ্চান্ন টাকা মাত্র
```

### Salary slip

```python
salary  = 35000
tax     = 3500
net     = salary - tax

print(f"মূল বেতন:  {format_currency(salary)}")
print(f"কর কর্তন: {format_currency(tax)}")
print(f"নিট বেতন: {format_currency(net)}")
# মূল বেতন:  পঁয়ত্রিশ হাজার টাকা মাত্র
# কর কর্তন: তিন হাজার পাঁচশত টাকা মাত্র
# নিট বেতন: একত্রিশ হাজার পাঁচশত টাকা মাত্র
```

---

## Notes

- Zero পয়সা is silently omitted from the output.
- The function calls `num_to_words` internally, so the full range of large numbers (কোটি and beyond) is supported.
- Fractional digits beyond two places are truncated: `"1.999"` → taka=1, paisa=99.
