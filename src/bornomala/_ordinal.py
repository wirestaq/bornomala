"""Bangla ordinal numbers."""

from ._digits import to_bangla_digits

# 1–10 have unique suffixes; 11+ use the general তম suffix
_SUFFIXES = {
    1:  "ম",
    2:  "য়",
    3:  "য়",
    4:  "র্থ",
    5:  "ম",
    6:  "ষ্ঠ",
    7:  "ম",
    8:  "ম",
    9:  "ম",
    10: "ম",
}
_DEFAULT_SUFFIX = "তম"


def to_bangla_ordinal(n):
    # type: (int) -> str
    """Convert a positive integer to its Bangla ordinal string.

    Examples::

        >>> to_bangla_ordinal(1)
        '১ম'
        >>> to_bangla_ordinal(4)
        '৪র্থ'
        >>> to_bangla_ordinal(6)
        '৬ষ্ঠ'
        >>> to_bangla_ordinal(11)
        '১১তম'
        >>> to_bangla_ordinal(100)
        '১০০তম'
    """
    n = int(n)
    if n <= 0:
        raise ValueError("to_bangla_ordinal requires a positive integer, got {}".format(n))
    suffix = _SUFFIXES.get(n, _DEFAULT_SUFFIX)
    return to_bangla_digits(n) + suffix
