"""Bangla-aware date and datetime wrappers.

Mirrors the Python ``datetime.date`` / ``datetime.datetime`` API but returns
Bangla text from ``strftime`` and ``__str__``.

Predefined format constants::

    FMT_DATE_LONG      "%e %B %Y"              ->  "১২ মার্চ ২০২৬"
    FMT_DATE_SHORT     "%d/%m/%Y"              ->  "১২/০৩/২০২৬"
    FMT_DATE_WEEKDAY   "%A, %e %B %Y"         ->  "বৃহস্পতিবার, ১২ মার্চ ২০২৬"
    FMT_DATETIME_LONG  "%A, %e %B %Y, %H:%M"  ->  "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"
    FMT_DATETIME_SHORT "%d/%m/%Y %H:%M"        ->  "১২/০৩/২০২৬ ১০:৩০"
    FMT_TIME_12H       "%I:%M %p"              ->  "১০:৩০ পূর্বাহ্ন"
    FMT_TIME_24H       "%H:%M:%S"              ->  "১০:৩০:৪৫"
"""

from datetime import date as _date
from datetime import datetime as _datetime
from datetime import timezone as _timezone
from datetime import timedelta as _timedelta

# Re-export for convenience: `from bornomala._datetime import timezone, timedelta`
timezone = _timezone
timedelta = _timedelta
from typing import Optional, Union

from ._digits import to_bangla_digits

# ── Month names ───────────────────────────────────────────────────────────────

BANGLA_MONTHS = {
    1: "জানুয়ারি",
    2: "ফেব্রুয়ারি",
    3: "মার্চ",
    4: "এপ্রিল",
    5: "মে",
    6: "জুন",
    7: "জুলাই",
    8: "আগস্ট",
    9: "সেপ্টেম্বর",
    10: "অক্টোবর",
    11: "নভেম্বর",
    12: "ডিসেম্বর",
}

BANGLA_MONTHS_SHORT = {
    1: "জানু",
    2: "ফেব্র",
    3: "মার্চ",
    4: "এপ্রি",
    5: "মে",
    6: "জুন",
    7: "জুলা",
    8: "আগ",
    9: "সেপ্টে",
    10: "অক্টো",
    11: "নভে",
    12: "ডিসে",
}

# ── Weekday names (Python weekday(): 0=Monday … 6=Sunday) ────────────────────

BANGLA_WEEKDAYS = {
    0: "সোমবার",
    1: "মঙ্গলবার",
    2: "বুধবার",
    3: "বৃহস্পতিবার",
    4: "শুক্রবার",
    5: "শনিবার",
    6: "রবিবার",
}

BANGLA_WEEKDAYS_SHORT = {
    0: "সোম",
    1: "মঙ্গল",
    2: "বুধ",
    3: "বৃহ",
    4: "শুক্র",
    5: "শনি",
    6: "রবি",
}

# ── Predefined format strings ─────────────────────────────────────────────────

FMT_DATE_LONG = "%e %B %Y"               # "১২ মার্চ ২০২৬"
FMT_DATE_SHORT = "%d/%m/%Y"              # "১২/০৩/২০২৬"
FMT_DATE_WEEKDAY = "%A, %e %B %Y"        # "বৃহস্পতিবার, ১২ মার্চ ২০২৬"
FMT_DATETIME_LONG = "%A, %e %B %Y, %H:%M"   # "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"
FMT_DATETIME_SHORT = "%d/%m/%Y %H:%M"    # "১২/০৩/২০২৬ ১০:৩০"
FMT_TIME_12H = "%I:%M %p"               # "১০:৩০ পূর্বাহ্ন"
FMT_TIME_24H = "%H:%M:%S"               # "১০:৩০:৪৫"


# ── Core formatter ────────────────────────────────────────────────────────────

def bangla_strftime(dt, fmt):
    # type: (Union[_date, _datetime], str) -> str
    """Format a :class:`datetime.date` or :class:`datetime.datetime` using
    *fmt*, replacing all standard ``strftime`` codes with Bangla equivalents.

    Supported codes
    ---------------
    ``%Y``  4-digit year in Bangla digits
    ``%y``  2-digit year in Bangla digits
    ``%m``  zero-padded month number
    ``%d``  zero-padded day number
    ``%e``  day number without leading zero  (cross-platform alternative to ``%-d``)
    ``%B``  full Bangla month name
    ``%b``  abbreviated Bangla month name
    ``%A``  full Bangla weekday name
    ``%a``  abbreviated Bangla weekday name
    ``%H``  24-hour hour, zero-padded
    ``%I``  12-hour hour, zero-padded
    ``%M``  minute, zero-padded
    ``%S``  second, zero-padded
    ``%p``  পূর্বাহ্ন / অপরাহ্ন  (AM / PM)
    ``%%``  literal ``%``

    Any unrecognised ``%x`` code is passed through unchanged.

    Examples::

        >>> from datetime import date
        >>> bangla_strftime(date(2026, 3, 12), "%e %B %Y")
        '১২ মার্চ ২০২৬'
        >>> bangla_strftime(date(2026, 3, 12), FMT_DATE_WEEKDAY)
        'বৃহস্পতিবার, ১২ মার্চ ২০২৬'
    """
    result = []
    i = 0
    n = len(fmt)
    while i < n:
        ch = fmt[i]
        if ch == "%" and i + 1 < n:
            code = fmt[i + 1]
            i += 2

            if code == "Y":
                result.append(to_bangla_digits(dt.year))
            elif code == "y":
                result.append(to_bangla_digits(str(dt.year)[-2:]))
            elif code == "m":
                result.append(to_bangla_digits(str(dt.month).zfill(2)))
            elif code == "d":
                result.append(to_bangla_digits(str(dt.day).zfill(2)))
            elif code == "e":
                # Day without leading zero (cross-platform %-d alternative)
                result.append(to_bangla_digits(dt.day))
            elif code == "B":
                result.append(BANGLA_MONTHS[dt.month])
            elif code == "b":
                result.append(BANGLA_MONTHS_SHORT[dt.month])
            elif code == "A":
                result.append(BANGLA_WEEKDAYS[dt.weekday()])
            elif code == "a":
                result.append(BANGLA_WEEKDAYS_SHORT[dt.weekday()])
            elif code == "H":
                result.append(to_bangla_digits(str(dt.hour).zfill(2)))  # type: ignore[union-attr]
            elif code == "I":
                h = dt.hour % 12 or 12  # type: ignore[union-attr]
                result.append(to_bangla_digits(str(h).zfill(2)))
            elif code == "M":
                result.append(to_bangla_digits(str(dt.minute).zfill(2)))  # type: ignore[union-attr]
            elif code == "S":
                result.append(to_bangla_digits(str(dt.second).zfill(2)))  # type: ignore[union-attr]
            elif code == "p":
                result.append("পূর্বাহ্ন" if dt.hour < 12 else "অপরাহ্ন")  # type: ignore[union-attr]
            elif code == "%":
                result.append("%")
            else:
                result.append("%" + code)
        else:
            result.append(ch)
            i += 1

    return "".join(result)


# ── BanglaDate ────────────────────────────────────────────────────────────────

class BanglaDate(object):
    """Wraps :class:`datetime.date`; ``strftime`` and ``__str__`` return Bangla text.

    Accepts the same arguments as :class:`datetime.date` **or** an existing
    :class:`datetime.date` instance::

        >>> BanglaDate(2026, 3, 12)           # year, month, day
        BanglaDate('2026-03-12')
        >>> from datetime import date
        >>> BanglaDate(date(2026, 3, 12))      # wrap existing date
        BanglaDate('2026-03-12')
        >>> str(BanglaDate(2026, 3, 12))
        '১২ মার্চ ২০২৬'
        >>> BanglaDate.today().strftime(FMT_DATE_WEEKDAY)
        'বৃহস্পতিবার, ১২ মার্চ ২০২৬'
    """

    def __init__(self, year_or_date, month=None, day=None):
        # type: (Union[int, _date], Optional[int], Optional[int]) -> None
        if isinstance(year_or_date, _date):
            self._d = year_or_date
        else:
            if month is None or day is None:
                raise TypeError("BanglaDate requires year, month, day or a date object")
            self._d = _date(year_or_date, month, day)

    # ── Constructors (mirror datetime.date) ───────────────────────────────────

    @classmethod
    def today(cls):
        # type: () -> BanglaDate
        """Return today's date as a :class:`BanglaDate`."""
        return cls(_date.today())

    @classmethod
    def fromtimestamp(cls, t):
        # type: (float) -> BanglaDate
        """Construct from a POSIX timestamp."""
        return cls(_date.fromtimestamp(t))

    @classmethod
    def fromisoformat(cls, s):
        # type: (str) -> BanglaDate
        """Construct from an ISO 8601 date string (``"YYYY-MM-DD"``)."""
        return cls(_date.fromisoformat(s))

    @classmethod
    def from_date(cls, d):
        # type: (_date) -> BanglaDate
        """Wrap an existing :class:`datetime.date`."""
        return cls(d)

    # ── Attributes (mirror datetime.date) ────────────────────────────────────

    @property
    def year(self):
        # type: () -> int
        return self._d.year

    @property
    def month(self):
        # type: () -> int
        return self._d.month

    @property
    def day(self):
        # type: () -> int
        return self._d.day

    def weekday(self):
        # type: () -> int
        """Return the day of the week as an integer (0=Monday, 6=Sunday)."""
        return self._d.weekday()

    def isoweekday(self):
        # type: () -> int
        """Return the day of the week as an integer (1=Monday, 7=Sunday)."""
        return self._d.isoweekday()

    def isoformat(self):
        # type: () -> str
        """Return the date as an ISO 8601 string (``"YYYY-MM-DD"``)."""
        return self._d.isoformat()

    def timetuple(self):
        return self._d.timetuple()

    def toordinal(self):
        # type: () -> int
        return self._d.toordinal()

    # ── Bangla output ─────────────────────────────────────────────────────────

    def strftime(self, fmt):
        # type: (str) -> str
        """Format the date using *fmt* with Bangla text output.

        All ``strftime`` codes are replaced by their Bangla equivalents.
        See :func:`bangla_strftime` for the full list of supported codes.
        """
        return bangla_strftime(self._d, fmt)

    def month_name(self):
        # type: () -> str
        """Return the full Bangla month name (e.g. ``"মার্চ"``)."""
        return BANGLA_MONTHS[self._d.month]

    def weekday_name(self):
        # type: () -> str
        """Return the full Bangla weekday name (e.g. ``"বৃহস্পতিবার"``)."""
        return BANGLA_WEEKDAYS[self._d.weekday()]

    # ── Dunder ────────────────────────────────────────────────────────────────

    def __str__(self):
        # type: () -> str
        return bangla_strftime(self._d, FMT_DATE_LONG)

    def __repr__(self):
        # type: () -> str
        return "BanglaDate('{}')".format(self._d.isoformat())

    def __eq__(self, other):
        if isinstance(other, BanglaDate):
            return self._d == other._d
        if isinstance(other, _date):
            return self._d == other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, BanglaDate):
            return self._d < other._d
        if isinstance(other, _date):
            return self._d < other
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, BanglaDate):
            return self._d <= other._d
        if isinstance(other, _date):
            return self._d <= other
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, BanglaDate):
            return self._d > other._d
        if isinstance(other, _date):
            return self._d > other
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, BanglaDate):
            return self._d >= other._d
        if isinstance(other, _date):
            return self._d >= other
        return NotImplemented

    def __hash__(self):
        return hash(self._d)


# ── BanglaDatetime ────────────────────────────────────────────────────────────

class BanglaDatetime(BanglaDate):
    """Wraps :class:`datetime.datetime`; ``strftime`` and ``__str__`` return Bangla text.

    Accepts the same arguments as :class:`datetime.datetime`, **or** an existing
    :class:`datetime.datetime` / :class:`datetime.date` instance::

        >>> BanglaDatetime(2026, 3, 12, 10, 30)          # year … minute
        BanglaDatetime('2026-03-12T10:30:00')
        >>> from datetime import datetime, date
        >>> BanglaDatetime(datetime(2026, 3, 12, 10, 30)) # wrap existing datetime
        BanglaDatetime('2026-03-12T10:30:00')
        >>> BanglaDatetime(date(2026, 3, 12))             # promote date → datetime (midnight)
        BanglaDatetime('2026-03-12T00:00:00')
        >>> str(BanglaDatetime.now())
        'বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০'
        >>> BanglaDatetime.now().strftime(FMT_TIME_12H)
        '১০:৩০ পূর্বাহ্ন'

    Timezone support::

        >>> import datetime
        >>> utc = BanglaDatetime.now(tz=datetime.timezone.utc)
        >>> utc.tzinfo
        datetime.timezone.utc
    """

    def __init__(
        self,
        year_or_dt,
        month=None,
        day=None,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
    ):
        if isinstance(year_or_dt, _datetime):
            # wrap datetime directly (tzinfo preserved as-is)
            self._d = year_or_dt  # type: ignore[assignment]
        elif isinstance(year_or_dt, _date):
            # promote date → datetime at midnight; optionally attach tzinfo
            self._d = _datetime(  # type: ignore[assignment]
                year_or_dt.year,
                year_or_dt.month,
                year_or_dt.day,
                hour,
                minute,
                second,
                microsecond,
                tzinfo,
            )
        else:
            # called as BanglaDatetime(year, month, day, ...)
            if month is None or day is None:
                raise TypeError(
                    "BanglaDatetime requires year, month, day "
                    "or a date/datetime object"
                )
            self._d = _datetime(  # type: ignore[assignment]
                year_or_dt, month, day, hour, minute, second, microsecond, tzinfo
            )

    # ── Constructors ──────────────────────────────────────────────────────────

    @classmethod
    def now(cls, tz=None):
        # type: (Optional[object]) -> BanglaDatetime
        """Return the current local date and time.

        Pass ``tz=datetime.timezone.utc`` (or any :class:`datetime.tzinfo`) to
        get an aware datetime::

            >>> import datetime
            >>> BanglaDatetime.now(tz=datetime.timezone.utc).tzinfo
            datetime.timezone.utc
        """
        return cls(_datetime.now(tz))  # type: ignore[arg-type]

    @classmethod
    def utcnow(cls):
        # type: () -> BanglaDatetime
        """Return the current UTC date and time (timezone-aware)."""
        return cls(_datetime.now(_timezone.utc))

    @classmethod
    def fromtimestamp(cls, t, tz=None):  # type: ignore[override]
        # type: (float, Optional[object]) -> BanglaDatetime
        """Construct from a POSIX timestamp, optionally in a given timezone."""
        return cls(_datetime.fromtimestamp(t, tz))  # type: ignore[arg-type]

    @classmethod
    def fromisoformat(cls, s):  # type: ignore[override]
        # type: (str) -> BanglaDatetime
        """Construct from an ISO 8601 datetime string (timezone offset preserved)."""
        return cls(_datetime.fromisoformat(s))

    @classmethod
    def from_datetime(cls, dt):
        # type: (_datetime) -> BanglaDatetime
        """Wrap an existing :class:`datetime.datetime`."""
        return cls(dt)

    @classmethod
    def from_date(cls, d, hour=0, minute=0, second=0, tzinfo=None):  # type: ignore[override]
        # type: (_date, int, int, int, Optional[object]) -> BanglaDatetime
        """Promote a :class:`datetime.date` to a :class:`BanglaDatetime`.

        Time defaults to midnight; pass *hour*, *minute*, *second* to override.
        Pass *tzinfo* to attach a timezone::

            >>> import datetime
            >>> BanglaDatetime.from_date(
            ...     datetime.date(2026, 3, 12),
            ...     tzinfo=datetime.timezone.utc,
            ... ).tzinfo
            datetime.timezone.utc
        """
        return cls(d, hour=hour, minute=minute, second=second, tzinfo=tzinfo)  # type: ignore[arg-type]

    # ── Time attributes ───────────────────────────────────────────────────────

    @property
    def hour(self):
        # type: () -> int
        return self._d.hour  # type: ignore[union-attr]

    @property
    def minute(self):
        # type: () -> int
        return self._d.minute  # type: ignore[union-attr]

    @property
    def second(self):
        # type: () -> int
        return self._d.second  # type: ignore[union-attr]

    @property
    def microsecond(self):
        # type: () -> int
        return self._d.microsecond  # type: ignore[union-attr]

    @property
    def tzinfo(self):
        return self._d.tzinfo  # type: ignore[union-attr]

    def date(self):
        # type: () -> BanglaDate
        """Return the date part as a :class:`BanglaDate`."""
        return BanglaDate(self._d.date())  # type: ignore[union-attr]

    def time_str(self, fmt=FMT_TIME_24H):
        # type: (str) -> str
        """Return the time as a Bangla-formatted string.

        Defaults to ``FMT_TIME_24H`` (``"%H:%M:%S"``).
        """
        return bangla_strftime(self._d, fmt)

    # ── Bangla output ─────────────────────────────────────────────────────────

    def __str__(self):
        # type: () -> str
        return bangla_strftime(self._d, FMT_DATETIME_LONG)

    def __repr__(self):
        # type: () -> str
        return "BanglaDatetime('{}')".format(self._d.isoformat())  # type: ignore[union-attr]
