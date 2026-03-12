---
title: "Text Utilities"
weight: 8
---

# Text Utilities

Unicode normalisation, script detection, and character utilities for Bangla text.

```python
from bornomala import normalize, is_bangla, is_pure_bangla, bangla_char_count
```

---

## `normalize(text)`

Clean and normalise Bangla Unicode text. Applies three fixes in order:

1. **NFC normalisation** — canonical Unicode composition (the standard form for storing and comparing Bangla text).
2. **Danda repair** — replaces the ASCII pipe `|` with the Bangla danda `।` when it appears in a Bangla context. This is a common OCR artefact in scanned documents.
3. **Whitespace collapse** — collapses consecutive spaces (including no-break spaces U+00A0) to a single space, and strips leading/trailing whitespace.

**Signature**

```python
def normalize(text: str) -> str
```

### Examples

```python
# Collapse extra spaces
normalize("আমার  সোনার  বাংলা")   # 'আমার সোনার বাংলা'

# Strip leading/trailing whitespace
normalize("  বাংলা  ")            # 'বাংলা'

# Pipe → danda (Bangla context)
normalize("এক|দুই")              # 'এক।দুই'

# Pipe NOT replaced in Latin context
normalize("a|b")                  # 'a|b'

# No-break space → regular space
normalize("এক\u00a0দুই")         # 'এক দুই'

# NFC normalisation (NFD → NFC)
import unicodedata
nfd = unicodedata.normalize("NFD", "বাংলা")
normalize(nfd) == "বাংলা"        # True

# Already clean text is returned unchanged
normalize("আমার সোনার বাংলা।")  # 'আমার সোনার বাংলা।'
```

### Common use cases

```python
# Clean user input before processing
user_input = request.POST.get("name", "").strip()
clean_name = normalize(user_input)

# Normalise before comparison
def names_match(a, b):
    return normalize(a) == normalize(b)

names_match("রাফি  আহমেদ", "রাফি আহমেদ")  # True

# Pre-process OCR output
ocr_text = "বাংলাদেশ|ভারত|মিয়ানমার"
clean = normalize(ocr_text)
# 'বাংলাদেশ।ভারত।মিয়ানমার'
```

---

## `is_bangla(text)`

Return `True` if `text` contains at least one character in the Bangla Unicode block (U+0980–U+09FF).

**Signature**

```python
def is_bangla(text: str) -> bool
```

### Examples

```python
is_bangla("আমি")           # True
is_bangla("hello")          # False
is_bangla("hello আমি")     # True
is_bangla("১২৩")           # True  ← Bangla digits are in the Bangla block
is_bangla("123")            # False
is_bangla("")               # False
```

### Use cases

```python
# Route language-specific processing
def process(text):
    if is_bangla(text):
        return normalize(text)
    return text.strip()

# Filter mixed lists
texts = ["hello", "আমি", "world", "বাংলা"]
bangla_only = [t for t in texts if is_bangla(t)]
# ['আমি', 'বাংলা']
```

---

## `is_pure_bangla(text)`

Return `True` if `text` contains **only** Bangla characters, Bangla digits, standard punctuation (`। , ; : ! ? - – — ( ) [ ] " ' " " ' '`), and whitespace — no Latin letters, Arabic digits, or other scripts.

**Signature**

```python
def is_pure_bangla(text: str) -> bool
```

### Examples

```python
is_pure_bangla("আমার বাংলা।")    # True
is_pure_bangla("hello আমি")      # False  ← Latin letters
is_pure_bangla("আমি ১০ জন।")    # True   ← Bangla digits OK
is_pure_bangla("আমি 10 জন।")    # False  ← Arabic/Western digits
is_pure_bangla("")               # False
is_pure_bangla("   ")            # False
```

### Use case: content validation

```python
def validate_bangla_field(value):
    if not value.strip():
        raise ValueError("Field cannot be empty")
    if not is_pure_bangla(value):
        raise ValueError("Field must contain only Bangla text")
    return normalize(value)
```

---

## `bangla_char_count(text)`

Count the number of Bangla Unicode characters (U+0980–U+09FF) in `text`. Spaces, punctuation, and other scripts are not counted.

**Signature**

```python
def bangla_char_count(text: str) -> int
```

### Examples

```python
bangla_char_count("আমি")         # 3
bangla_char_count("hello")       # 0
bangla_char_count("hello আমি")  # 3
bangla_char_count("")            # 0
bangla_char_count("আমার বাংলা") # 9  ← space not counted
bangla_char_count("১২৩")        # 3  ← Bangla digits are counted
```

### Use cases

```python
# Enforce minimum Bangla content
def has_enough_bangla(text, min_chars=10):
    return bangla_char_count(text) >= min_chars

# Text statistics
def text_stats(text):
    total  = len(text)
    bangla = bangla_char_count(text)
    return {
        "total_chars":  total,
        "bangla_chars": bangla,
        "bangla_ratio": bangla / total if total else 0,
    }

stats = text_stats("আমার বাংলা — my language")
# {'total_chars': 24, 'bangla_chars': 9, 'bangla_ratio': 0.375}
```

---

## Combining utilities

```python
from bornomala import normalize, is_bangla, is_pure_bangla, bangla_char_count

def process_bangla_input(raw: str) -> dict:
    """Full pipeline: clean → validate → analyse."""
    clean = normalize(raw)
    return {
        "text":         clean,
        "has_bangla":   is_bangla(clean),
        "pure_bangla":  is_pure_bangla(clean),
        "bangla_chars": bangla_char_count(clean),
    }

process_bangla_input("  আমার  সোনার  বাংলা।  ")
# {
#   'text':         'আমার সোনার বাংলা।',
#   'has_bangla':   True,
#   'pure_bangla':  True,
#   'bangla_chars': 17,
# }
```
