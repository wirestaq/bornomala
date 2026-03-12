"""Bangla calendar (বঙ্গাব্দ) — Gregorian ↔ Bengali date conversion.

Uses the *Revised Bengali Calendar* adopted by the Bangla Academy (Bangladesh),
where every month starts on a fixed Gregorian date and the new year always
falls on 14 April.
"""

from datetime import date as _date

from ._digits import to_bangla_digits

# ── Month / season tables ─────────────────────────────────────────────────────

BANGLA_CAL_MONTHS = [
    "বৈশাখ",      # 1
    "জ্যৈষ্ঠ",    # 2
    "আষাঢ়",      # 3
    "শ্রাবণ",     # 4
    "ভাদ্র",      # 5
    "আশ্বিন",     # 6
    "কার্তিক",    # 7
    "অগ্রহায়ণ",  # 8
    "পৌষ",        # 9
    "মাঘ",        # 10
    "ফাল্গুন",    # 11
    "চৈত্র",      # 12
]

# Two consecutive Bangla months form one ঋতু (season)
BANGLA_SEASONS = {
    1: "গ্রীষ্ম",   # বৈশাখ–জ্যৈষ্ঠ   (summer)
    2: "গ্রীষ্ম",
    3: "বর্ষা",     # আষাঢ়–শ্রাবণ     (monsoon)
    4: "বর্ষা",
    5: "শরৎ",       # ভাদ্র–আশ্বিন     (autumn)
    6: "শরৎ",
    7: "হেমন্ত",    # কার্তিক–অগ্রহায়ণ (late autumn)
    8: "হেমন্ত",
    9: "শীত",       # পৌষ–মাঘ          (winter)
    10: "শীত",
    11: "বসন্ত",    # ফাল্গুন–চৈত্র    (spring)
    12: "বসন্ত",
}

# ── Gregorian start dates for each Bangla month ───────────────────────────────
# For Bangla year B the first Gregorian year is (B + 593).
# Months 9–11 and 12 fall in the *following* Gregorian year.
#
# (Gregorian month, day)
_MONTH_GREG_STARTS = [
    (4, 14),   # বৈশাখ
    (5, 15),   # জ্যৈষ্ঠ
    (6, 15),   # আষাঢ়
    (7, 16),   # শ্রাবণ
    (8, 16),   # ভাদ্র
    (9, 17),   # আশ্বিন
    (10, 17),  # কার্তিক
    (11, 16),  # অগ্রহায়ণ
    (12, 15),  # পৌষ
    (1, 14),   # মাঘ    (next Gregorian year)
    (2, 13),   # ফাল্গুন (next Gregorian year)
    (3, 14),   # চৈত্র   (next Gregorian year)
]


def _month_starts_for_bangla_year(by):
    """Return a list of 12 :class:`datetime.date` objects — the Gregorian start
    date of each Bangla month in Bangla year *by*."""
    gy = by + 593
    starts = []
    for gm, gd in _MONTH_GREG_STARTS:
        greg_year = gy if gm >= 4 else gy + 1
        starts.append(_date(greg_year, gm, gd))
    return starts


# ── BanglaCalendarDate ────────────────────────────────────────────────────────

class BanglaCalendarDate(object):
    """A date in the Bangla calendar (বঙ্গাব্দ).

    Attributes
    ----------
    year  : int  — Bangla year (e.g. 1432)
    month : int  — Bangla month 1–12
    day   : int  — day within the month
    """

    def __init__(self, year, month, day):
        # type: (int, int, int) -> None
        if not (1 <= month <= 12):
            raise ValueError("month must be 1–12, got {}".format(month))
        if day < 1:
            raise ValueError("day must be ≥ 1, got {}".format(day))
        self.year = year
        self.month = month
        self.day = day

    # ── Derived properties ────────────────────────────────────────────────────

    @property
    def month_name(self):
        # type: () -> str
        """Full Bangla month name (e.g. ``"ফাল্গুন"``)."""
        return BANGLA_CAL_MONTHS[self.month - 1]

    @property
    def season(self):
        # type: () -> str
        """The ঋতু (season) for this month (e.g. ``"বসন্ত"``)."""
        return BANGLA_SEASONS[self.month]

    def to_gregorian(self):
        # type: () -> _date
        """Convert back to a :class:`datetime.date`."""
        starts = _month_starts_for_bangla_year(self.year)
        import datetime as _dt
        return starts[self.month - 1] + _dt.timedelta(days=self.day - 1)

    # ── String output ─────────────────────────────────────────────────────────

    def __str__(self):
        # type: () -> str
        return "{} {} {}".format(
            to_bangla_digits(self.day),
            self.month_name,
            to_bangla_digits(self.year),
        )

    def __repr__(self):
        # type: () -> str
        return "BanglaCalendarDate({}, {}, {})".format(self.year, self.month, self.day)

    # ── Comparisons ───────────────────────────────────────────────────────────

    def _tuple(self):
        return (self.year, self.month, self.day)

    def __eq__(self, other):
        if isinstance(other, BanglaCalendarDate):
            return self._tuple() == other._tuple()
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, BanglaCalendarDate):
            return self._tuple() < other._tuple()
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, BanglaCalendarDate):
            return self._tuple() <= other._tuple()
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, BanglaCalendarDate):
            return self._tuple() > other._tuple()
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, BanglaCalendarDate):
            return self._tuple() >= other._tuple()
        return NotImplemented

    def __hash__(self):
        return hash(self._tuple())


# ── Public conversion functions ───────────────────────────────────────────────

def gregorian_to_bangla(gdate):
    # type: (_date) -> BanglaCalendarDate
    """Convert a :class:`datetime.date` to a :class:`BanglaCalendarDate`.

    Uses the Revised Bengali Calendar (Bangladesh / Bangla Academy standard).

    Examples::

        >>> from datetime import date
        >>> gregorian_to_bangla(date(2026, 3, 12))
        BanglaCalendarDate(1432, 11, 28)
        >>> str(gregorian_to_bangla(date(2026, 3, 12)))
        '২৮ ফাল্গুন ১৪৩২'
        >>> gregorian_to_bangla(date(2026, 4, 14))
        BanglaCalendarDate(1433, 1, 1)
        >>> str(gregorian_to_bangla(date(2026, 4, 14)))
        '১ বৈশাখ ১৪৩৩'
    """
    gm, gd = gdate.month, gdate.day

    # Determine Bangla year: new year starts on 14 April
    by = gdate.year - 593 if (gm, gd) >= (4, 14) else gdate.year - 594

    month_starts = _month_starts_for_bangla_year(by)

    # Walk backwards to find the last month whose start ≤ gdate
    bm = 1
    for i in range(11, -1, -1):
        if gdate >= month_starts[i]:
            bm = i + 1
            break

    bd = (gdate - month_starts[bm - 1]).days + 1
    return BanglaCalendarDate(by, bm, bd)


def bangla_to_gregorian(bdate):
    # type: (BanglaCalendarDate) -> _date
    """Convert a :class:`BanglaCalendarDate` to a :class:`datetime.date`.

    Examples::

        >>> bangla_to_gregorian(BanglaCalendarDate(1432, 11, 28))
        datetime.date(2026, 3, 12)
        >>> bangla_to_gregorian(BanglaCalendarDate(1433, 1, 1))
        datetime.date(2026, 4, 14)
    """
    return bdate.to_gregorian()
