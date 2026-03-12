"""Convert numbers to Bangla words (kotha)."""

from typing import Union

from ._data import ONES
from ._digits import to_western_digits


class BanglaWords(str):
    """A ``str`` subclass returned by :func:`num_to_words`.

    All methods return ``BanglaWords`` so they can be chained freely::

        >>> num_to_words(500).taka().only()
        'পাঁচশত টাকা মাত্র'
        >>> num_to_words(3).jon()
        'তিন জন'
    """

    def _append(self, suffix: str) -> "BanglaWords":
        return BanglaWords(self + suffix)

    # ── Modifier ──────────────────────────────────────────────────────────

    def only(self) -> "BanglaWords":
        """Append ' মাত্র' (only / exactly)."""
        return self._append(" মাত্র")

    # ── Currency ──────────────────────────────────────────────────────────

    def taka(self) -> "BanglaWords":
        """Append ' টাকা' (BDT)."""
        return self._append(" টাকা")

    def paisa(self) -> "BanglaWords":
        """Append ' পয়সা' (1/100 taka)."""
        return self._append(" পয়সা")

    # ── People / object counters ───────────────────────────────────────────

    def jon(self) -> "BanglaWords":
        """Append ' জন' (person counter)."""
        return self._append(" জন")

    def ti(self) -> "BanglaWords":
        """Append ' টি' (generic inanimate counter)."""
        return self._append(" টি")

    def ta(self) -> "BanglaWords":
        """Append ' টা' (informal generic counter)."""
        return self._append(" টা")

    # ── Weight / volume ───────────────────────────────────────────────────

    def gram(self) -> "BanglaWords":
        """Append ' গ্রাম'."""
        return self._append(" গ্রাম")

    def kilo(self) -> "BanglaWords":
        """Append ' কিলোগ্রাম'."""
        return self._append(" কিলোগ্রাম")

    def liter(self) -> "BanglaWords":
        """Append ' লিটার'."""
        return self._append(" লিটার")

    # ── Distance ──────────────────────────────────────────────────────────

    def meter(self) -> "BanglaWords":
        """Append ' মিটার'."""
        return self._append(" মিটার")

    def kilo_meter(self) -> "BanglaWords":
        """Append ' কিলোমিটার'."""
        return self._append(" কিলোমিটার")

    # ── Misc ──────────────────────────────────────────────────────────────

    def percent(self) -> "BanglaWords":
        """Append ' শতাংশ'."""
        return self._append(" শতাংশ")

    def din(self) -> "BanglaWords":
        """Append ' দিন' (days)."""
        return self._append(" দিন")

    def ghonta(self) -> "BanglaWords":
        """Append ' ঘণ্টা' (hours)."""
        return self._append(" ঘণ্টা")


def _int_to_words(n: int) -> str:
    """Convert a non-negative integer to Bangla words."""
    if n == 0:
        return ONES[0]

    if n <= 99:
        return ONES[n]

    parts = []

    # কোটি (10,000,000)
    crores = n // 10000000
    n %= 10000000
    if crores:
        # Recurse for crore-group (handles hundreds of crores etc.)
        parts.append(_int_to_words(crores) + " কোটি")

    # লক্ষ (100,000)
    lakhs = n // 100000
    n %= 100000
    if lakhs:
        parts.append(ONES[lakhs] + " লক্ষ")

    # হাজার (1,000)
    thousands = n // 1000
    n %= 1000
    if thousands:
        parts.append(ONES[thousands] + " হাজার")

    # শত (100) — fused, no space
    hundreds = n // 100
    n %= 100
    if hundreds:
        parts.append(ONES[hundreds] + "শত")

    # 1–99 remainder
    if n:
        parts.append(ONES[n])

    return " ".join(parts)


def num_to_words(n: Union[int, float, str]) -> BanglaWords:
    """Convert a number to its Bangla word representation.

    *n* may be an ``int``, ``float``, or ``str`` (with English or Bangla digits).

    Examples::

        >>> num_to_words(0)
        'শূন্য'
        >>> num_to_words(1234)
        'এক হাজার দুইশত চৌত্রিশ'
        >>> num_to_words(-42)
        'ঋণাত্মক বিয়াল্লিশ'
        >>> num_to_words("3.14")
        'তিন দশমিক এক চার'
        >>> num_to_words("১২৩৪")
        'এক হাজার দুইশত চৌত্রিশ'
    """
    # Normalise to a string of Western digits
    s = to_western_digits(str(n))

    negative = s.startswith("-")
    if negative:
        s = s[1:]

    # Split integer and fractional parts
    if "." in s:
        int_str, frac_str = s.split(".", 1)
    else:
        int_str, frac_str = s, ""

    integer_val = int(int_str) if int_str else 0

    # Build integer words
    int_words = _int_to_words(integer_val)

    # Build fractional words (digit by digit)
    if frac_str:
        frac_words = " ".join(ONES[int(d)] for d in frac_str)
        result = int_words + " দশমিক " + frac_words
    else:
        result = int_words

    if negative:
        result = "ঋণাত্মক " + result

    return BanglaWords(result)
