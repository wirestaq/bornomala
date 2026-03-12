"""bornomala — Bangla text toolkit."""

from ._digits import to_bangla_digits, to_western_digits
from ._num_to_words import BanglaWords, num_to_words
from ._words_to_num import words_to_num
from ._ordinal import to_bangla_ordinal
from ._currency import format_currency
from ._datetime import (
    BanglaDate,
    BanglaDatetime,
    bangla_strftime,
    timezone,
    timedelta,
    FMT_DATE_LONG,
    FMT_DATE_SHORT,
    FMT_DATE_WEEKDAY,
    FMT_DATETIME_LONG,
    FMT_DATETIME_SHORT,
    FMT_TIME_12H,
    FMT_TIME_24H,
)
from ._calendar import (
    BanglaCalendarDate,
    gregorian_to_bangla,
    bangla_to_gregorian,
    BANGLA_CAL_MONTHS,
    BANGLA_SEASONS,
)
from ._normalize import (
    normalize,
    is_bangla,
    is_pure_bangla,
    bangla_char_count,
)

__version__ = "0.1.0"
__all__ = [
    # numbers
    "BanglaWords",
    "num_to_words",
    "words_to_num",
    # digits
    "to_bangla_digits",
    "to_western_digits",
    # ordinals & currency
    "to_bangla_ordinal",
    "format_currency",
    # dates (Gregorian)
    "BanglaDate",
    "BanglaDatetime",
    "bangla_strftime",
    "timezone",
    "timedelta",
    "FMT_DATE_LONG",
    "FMT_DATE_SHORT",
    "FMT_DATE_WEEKDAY",
    "FMT_DATETIME_LONG",
    "FMT_DATETIME_SHORT",
    "FMT_TIME_12H",
    "FMT_TIME_24H",
    # Bangla calendar
    "BanglaCalendarDate",
    "gregorian_to_bangla",
    "bangla_to_gregorian",
    "BANGLA_CAL_MONTHS",
    "BANGLA_SEASONS",
    # text utilities
    "normalize",
    "is_bangla",
    "is_pure_bangla",
    "bangla_char_count",
]
