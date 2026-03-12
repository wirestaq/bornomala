"""Bangla Unicode normalization and script detection utilities."""

import unicodedata

# Bangla Unicode block: U+0980 – U+09FF
_BANGLA_START = "\u0980"
_BANGLA_END = "\u09ff"

# Characters that are acceptable alongside Bangla in "pure Bangla" text
_ALLOWED_NON_BANGLA = frozenset(" \t\n\r।,;:!?-–—()[]\"'""''৳")


def normalize(text):
    # type: (str) -> str
    """Normalize Bangla Unicode text.

    Applies the following fixes in order:

    1. **NFC normalization** — canonical composition (the standard form for
       storing and comparing Unicode text).
    2. **Danda fix** — replaces the ASCII pipe ``|`` (a common OCR artefact in
       scanned Bangla documents) with the proper Bangla danda ``।``
       *only* when it appears in an otherwise-Bangla context (surrounded by
       Bangla characters or whitespace).
    3. **Whitespace normalisation** — collapses multiple consecutive spaces
       (including no-break spaces U+00A0) into a single regular space, and
       strips leading/trailing whitespace.

    Returns the cleaned string.

    Examples::

        >>> normalize("আমার  সোনার  বাংলা")   # extra spaces
        'আমার সোনার বাংলা'
        >>> normalize("এক|দুই")               # pipe → danda
        'এক।দুই'
    """
    # 1. NFC
    text = unicodedata.normalize("NFC", text)

    # 2. Replace ASCII pipe | → danda । when flanked by Bangla/whitespace
    if "|" in text:
        result = []
        for i, ch in enumerate(text):
            if ch == "|":
                prev_ok = i == 0 or _is_bangla_or_space(text[i - 1])
                next_ok = i == len(text) - 1 or _is_bangla_or_space(text[i + 1])
                result.append("।" if (prev_ok and next_ok) else ch)
            else:
                result.append(ch)
        text = "".join(result)

    # 3. Collapse whitespace (including \u00a0) and strip ends
    import re
    text = re.sub(r"[ \t\u00a0]+", " ", text).strip()

    return text


def _is_bangla_or_space(ch):
    return ch.isspace() or is_bangla_char(ch) or ch == "।"


def is_bangla_char(ch):
    # type: (str) -> bool
    """Return ``True`` if *ch* is a single Bangla Unicode character."""
    return _BANGLA_START <= ch <= _BANGLA_END


def is_bangla(text):
    # type: (str) -> bool
    """Return ``True`` if *text* contains at least one Bangla Unicode character.

    Examples::

        >>> is_bangla("আমি")
        True
        >>> is_bangla("hello")
        False
        >>> is_bangla("hello আমি")
        True
    """
    return any(_BANGLA_START <= ch <= _BANGLA_END for ch in text)


def is_pure_bangla(text):
    # type: (str) -> bool
    """Return ``True`` if *text* contains only Bangla characters and
    allowed punctuation/whitespace (no Latin letters, Arabic digits, etc.).

    Examples::

        >>> is_pure_bangla("আমার বাংলা।")
        True
        >>> is_pure_bangla("hello আমি")
        False
        >>> is_pure_bangla("আমি ১০ জন।")   # Bangla digits are fine
        True
    """
    if not text.strip():
        return False
    for ch in text:
        if ch in _ALLOWED_NON_BANGLA:
            continue
        if _BANGLA_START <= ch <= _BANGLA_END:
            continue
        return False
    return True


def bangla_char_count(text):
    # type: (str) -> int
    """Return the number of Bangla Unicode characters in *text*.

    Examples::

        >>> bangla_char_count("hello আমি")
        3
        >>> bangla_char_count("hello")
        0
    """
    return sum(1 for ch in text if _BANGLA_START <= ch <= _BANGLA_END)
