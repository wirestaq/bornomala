"""Digit conversion between Western (ASCII) and Bangla Unicode numerals."""

from typing import Union

_W2B = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
_B2W = str.maketrans("০১২৩৪৫৬৭৮৯", "0123456789")


def to_bangla_digits(n: Union[int, float, str]) -> str:
    """Convert Western digits in *n* to Bangla Unicode digits.

    Non-digit characters (``-``, ``.``, letters) are left unchanged.
    """
    return str(n).translate(_W2B)


def to_western_digits(text: str) -> str:
    """Convert Bangla Unicode digits in *text* to Western ASCII digits.

    Non-digit characters are left unchanged.
    """
    return text.translate(_B2W)
