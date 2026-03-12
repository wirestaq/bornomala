"""Tests for BanglaDate, BanglaDatetime, and bangla_strftime."""

import pytest
from datetime import date, datetime, timezone, timedelta

from bornomala import (
    BanglaDate,
    BanglaDatetime,
    bangla_strftime,
    FMT_DATE_LONG,
    FMT_DATE_SHORT,
    FMT_DATE_WEEKDAY,
    FMT_DATETIME_LONG,
    FMT_DATETIME_SHORT,
    FMT_TIME_12H,
    FMT_TIME_24H,
)

# ── Reference objects ─────────────────────────────────────────────────────────

D = date(2026, 3, 12)        # Thursday / বৃহস্পতিবার
DT = datetime(2026, 3, 12, 10, 30, 45)
DT_PM = datetime(2026, 3, 12, 14, 5, 3)
D_JAN = date(2026, 1, 1)     # Thursday / বৃহস্পতিবার, single-digit day


# ── bangla_strftime codes ─────────────────────────────────────────────────────

@pytest.mark.parametrize("fmt, expected", [
    ("%Y",  "২০২৬"),
    ("%y",  "২৬"),
    ("%m",  "০৩"),
    ("%d",  "১২"),
    ("%e",  "১২"),
    ("%B",  "মার্চ"),
    ("%b",  "মার্চ"),
    ("%A",  "বৃহস্পতিবার"),
    ("%a",  "বৃহ"),
    ("%%",  "%"),
])
def test_strftime_date_codes(fmt, expected):
    assert bangla_strftime(D, fmt) == expected


@pytest.mark.parametrize("fmt, expected", [
    ("%H",  "১০"),
    ("%I",  "১০"),
    ("%M",  "৩০"),
    ("%S",  "৪৫"),
    ("%p",  "পূর্বাহ্ন"),
])
def test_strftime_time_codes_am(fmt, expected):
    assert bangla_strftime(DT, fmt) == expected


@pytest.mark.parametrize("fmt, expected", [
    ("%H",  "১৪"),
    ("%I",  "০২"),
    ("%M",  "০৫"),
    ("%S",  "০৩"),
    ("%p",  "অপরাহ্ন"),
])
def test_strftime_time_codes_pm(fmt, expected):
    assert bangla_strftime(DT_PM, fmt) == expected


def test_strftime_unknown_code_passthrough():
    assert bangla_strftime(D, "%Z") == "%Z"


def test_strftime_literal_text():
    assert bangla_strftime(D, "তারিখ: %e %B %Y") == "তারিখ: ১২ মার্চ ২০২৬"


def test_strftime_e_no_leading_zero():
    assert bangla_strftime(D_JAN, "%e") == "১"


def test_strftime_d_leading_zero():
    assert bangla_strftime(D_JAN, "%d") == "০১"


# ── Predefined format constants ───────────────────────────────────────────────

def test_fmt_date_long():
    assert bangla_strftime(D, FMT_DATE_LONG) == "১২ মার্চ ২০২৬"


def test_fmt_date_short():
    assert bangla_strftime(D, FMT_DATE_SHORT) == "১২/০৩/২০২৬"


def test_fmt_date_weekday():
    assert bangla_strftime(D, FMT_DATE_WEEKDAY) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬"


def test_fmt_datetime_long():
    assert bangla_strftime(DT, FMT_DATETIME_LONG) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"


def test_fmt_datetime_short():
    assert bangla_strftime(DT, FMT_DATETIME_SHORT) == "১২/০৩/২০২৬ ১০:৩০"


def test_fmt_time_12h():
    assert bangla_strftime(DT, FMT_TIME_12H) == "১০:৩০ পূর্বাহ্ন"


def test_fmt_time_24h():
    assert bangla_strftime(DT, FMT_TIME_24H) == "১০:৩০:৪৫"


# ── All 12 months ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("month, name", [
    (1, "জানুয়ারি"), (2, "ফেব্রুয়ারি"), (3, "মার্চ"),
    (4, "এপ্রিল"),   (5, "মে"),          (6, "জুন"),
    (7, "জুলাই"),    (8, "আগস্ট"),       (9, "সেপ্টেম্বর"),
    (10, "অক্টোবর"), (11, "নভেম্বর"),   (12, "ডিসেম্বর"),
])
def test_all_month_names(month, name):
    d = date(2026, month, 1)
    assert bangla_strftime(d, "%B") == name


# ── All 7 weekdays ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("d, name", [
    (date(2026, 3, 9),  "সোমবার"),
    (date(2026, 3, 10), "মঙ্গলবার"),
    (date(2026, 3, 11), "বুধবার"),
    (date(2026, 3, 12), "বৃহস্পতিবার"),
    (date(2026, 3, 13), "শুক্রবার"),
    (date(2026, 3, 14), "শনিবার"),
    (date(2026, 3, 15), "রবিবার"),
])
def test_all_weekday_names(d, name):
    assert bangla_strftime(d, "%A") == name


# ── BanglaDate ────────────────────────────────────────────────────────────────

def test_bangla_date_today_is_bangla_date():
    assert isinstance(BanglaDate.today(), BanglaDate)


def test_bangla_date_str():
    bd = BanglaDate.from_date(D)
    assert str(bd) == "১২ মার্চ ২০২৬"


def test_bangla_date_repr():
    bd = BanglaDate.from_date(D)
    assert repr(bd) == "BanglaDate('2026-03-12')"


def test_bangla_date_strftime():
    bd = BanglaDate.from_date(D)
    assert bd.strftime(FMT_DATE_WEEKDAY) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬"


def test_bangla_date_attributes():
    bd = BanglaDate.from_date(D)
    assert bd.year == 2026
    assert bd.month == 3
    assert bd.day == 12


def test_bangla_date_weekday():
    bd = BanglaDate.from_date(D)
    assert bd.weekday() == 3       # Thursday
    assert bd.isoweekday() == 4


def test_bangla_date_month_name():
    bd = BanglaDate.from_date(D)
    assert bd.month_name() == "মার্চ"


def test_bangla_date_weekday_name():
    bd = BanglaDate.from_date(D)
    assert bd.weekday_name() == "বৃহস্পতিবার"


def test_bangla_date_isoformat():
    bd = BanglaDate.from_date(D)
    assert bd.isoformat() == "2026-03-12"


def test_bangla_date_fromisoformat():
    bd = BanglaDate.fromisoformat("2026-03-12")
    assert str(bd) == "১২ মার্চ ২০২৬"


def test_bangla_date_fromtimestamp():
    bd = BanglaDate.fromtimestamp(0)
    assert isinstance(bd, BanglaDate)


def test_bangla_date_equality():
    bd1 = BanglaDate.from_date(D)
    bd2 = BanglaDate.from_date(D)
    assert bd1 == bd2


def test_bangla_date_comparison():
    bd1 = BanglaDate.from_date(date(2026, 1, 1))
    bd2 = BanglaDate.from_date(date(2026, 12, 31))
    assert bd1 < bd2
    assert bd2 > bd1


# ── BanglaDatetime ────────────────────────────────────────────────────────────

def test_bangla_datetime_now_is_bangla_datetime():
    assert isinstance(BanglaDatetime.now(), BanglaDatetime)


def test_bangla_datetime_str():
    bdt = BanglaDatetime.from_datetime(DT)
    assert str(bdt) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"


def test_bangla_datetime_repr():
    bdt = BanglaDatetime.from_datetime(DT)
    assert repr(bdt) == "BanglaDatetime('2026-03-12T10:30:45')"


def test_bangla_datetime_time_codes():
    bdt = BanglaDatetime.from_datetime(DT)
    assert bdt.strftime("%H:%M:%S") == "১০:৩০:৪৫"


def test_bangla_datetime_time_str_default():
    bdt = BanglaDatetime.from_datetime(DT)
    assert bdt.time_str() == "১০:৩০:৪৫"


def test_bangla_datetime_time_str_12h():
    bdt = BanglaDatetime.from_datetime(DT)
    assert bdt.time_str(FMT_TIME_12H) == "১০:৩০ পূর্বাহ্ন"


def test_bangla_datetime_time_attrs():
    bdt = BanglaDatetime.from_datetime(DT)
    assert bdt.hour == 10
    assert bdt.minute == 30
    assert bdt.second == 45


def test_bangla_datetime_date_part():
    bdt = BanglaDatetime.from_datetime(DT)
    d_part = bdt.date()
    assert isinstance(d_part, BanglaDate)
    assert str(d_part) == "১২ মার্চ ২০২৬"


def test_bangla_datetime_fromisoformat():
    bdt = BanglaDatetime.fromisoformat("2026-03-12T10:30:45")
    assert bdt.hour == 10
    assert bdt.minute == 30


def test_bangla_datetime_midnight_12h():
    # midnight: hour=0 → 12-hour display should be ১২
    bdt = BanglaDatetime.from_datetime(datetime(2026, 3, 12, 0, 0, 0))
    assert bdt.strftime("%I") == "১২"
    assert bdt.strftime("%p") == "পূর্বাহ্ন"


def test_bangla_datetime_noon_12h():
    bdt = BanglaDatetime.from_datetime(datetime(2026, 3, 12, 12, 0, 0))
    assert bdt.strftime("%I") == "১২"
    assert bdt.strftime("%p") == "অপরাহ্ন"


# ── Flexible constructors ─────────────────────────────────────────────────────

def test_bangla_date_from_ints():
    bd = BanglaDate(2026, 3, 12)
    assert bd.year == 2026
    assert bd.month == 3
    assert bd.day == 12
    assert str(bd) == "১২ মার্চ ২০২৬"


def test_bangla_date_from_date_obj():
    bd = BanglaDate(date(2026, 3, 12))
    assert str(bd) == "১২ মার্চ ২০২৬"


def test_bangla_date_missing_args_raises():
    with pytest.raises(TypeError):
        BanglaDate(2026)


def test_bangla_datetime_from_ints():
    bdt = BanglaDatetime(2026, 3, 12, 10, 30, 45)
    assert bdt.hour == 10
    assert bdt.minute == 30
    assert bdt.second == 45
    assert str(bdt) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"


def test_bangla_datetime_from_datetime_obj():
    bdt = BanglaDatetime(datetime(2026, 3, 12, 10, 30, 45))
    assert bdt.hour == 10
    assert str(bdt) == "বৃহস্পতিবার, ১২ মার্চ ২০২৬, ১০:৩০"


def test_bangla_datetime_from_date_obj_midnight():
    """Promoting a date to datetime defaults to midnight."""
    bdt = BanglaDatetime(date(2026, 3, 12))
    assert bdt.year == 2026
    assert bdt.hour == 0
    assert bdt.minute == 0
    assert bdt.second == 0


def test_bangla_datetime_from_date_obj_with_time():
    bdt = BanglaDatetime(date(2026, 3, 12), hour=10, minute=30)
    assert bdt.hour == 10
    assert bdt.minute == 30


def test_bangla_datetime_from_date_classmethod():
    bdt = BanglaDatetime.from_date(date(2026, 3, 12), hour=9, minute=15)
    assert bdt.hour == 9
    assert bdt.minute == 15


def test_bangla_datetime_missing_args_raises():
    with pytest.raises(TypeError):
        BanglaDatetime(2026)


# ── Timezone support ──────────────────────────────────────────────────────────

def test_bangla_datetime_now_utc():
    bdt = BanglaDatetime.now(tz=timezone.utc)
    assert bdt.tzinfo == timezone.utc


def test_bangla_datetime_utcnow():
    bdt = BanglaDatetime.utcnow()
    assert bdt.tzinfo == timezone.utc


def test_bangla_datetime_from_ints_with_tz():
    tz_bd = timezone(timedelta(hours=6))  # Bangladesh Standard Time UTC+6
    bdt = BanglaDatetime(2026, 3, 12, 10, 30, tzinfo=tz_bd)
    assert bdt.tzinfo == tz_bd


def test_bangla_datetime_from_date_with_tz():
    tz_bd = timezone(timedelta(hours=6))
    bdt = BanglaDatetime.from_date(date(2026, 3, 12), tzinfo=tz_bd)
    assert bdt.tzinfo == tz_bd
    assert bdt.hour == 0


def test_bangla_datetime_wrap_aware_datetime():
    tz_bd = timezone(timedelta(hours=6))
    dt = datetime(2026, 3, 12, 10, 30, tzinfo=tz_bd)
    bdt = BanglaDatetime(dt)
    assert bdt.tzinfo == tz_bd
    assert bdt.hour == 10


def test_bangla_datetime_fromtimestamp_utc():
    bdt = BanglaDatetime.fromtimestamp(0, tz=timezone.utc)
    assert bdt.tzinfo == timezone.utc
    assert bdt.year == 1970


def test_bangla_datetime_fromisoformat_with_offset():
    bdt = BanglaDatetime.fromisoformat("2026-03-12T10:30:00+06:00")
    assert bdt.hour == 10
    assert bdt.tzinfo is not None


# ── BanglaDate: comparison with native date objects ───────────────────────────

def test_bangla_date_eq_native_date():
    bd = BanglaDate.from_date(D)
    assert bd == D


def test_bangla_date_lt_native_date():
    bd = BanglaDate.from_date(date(2026, 1, 1))
    assert bd < date(2026, 12, 31)


def test_bangla_date_le_native_date():
    bd = BanglaDate.from_date(D)
    assert bd <= D
    assert bd <= date(2026, 12, 31)


def test_bangla_date_gt_native_date():
    bd = BanglaDate.from_date(date(2026, 12, 31))
    assert bd > date(2026, 1, 1)


def test_bangla_date_ge_native_date():
    bd = BanglaDate.from_date(D)
    assert bd >= D
    assert bd >= date(2026, 1, 1)


def test_bangla_date_le_between_bangla_dates():
    bd1 = BanglaDate.from_date(D)
    bd2 = BanglaDate.from_date(D)
    assert bd1 <= bd2


def test_bangla_date_ge_between_bangla_dates():
    bd1 = BanglaDate.from_date(D)
    bd2 = BanglaDate.from_date(D)
    assert bd1 >= bd2


def test_bangla_date_hash():
    bd = BanglaDate.from_date(D)
    assert hash(bd) == hash(D)


def test_bangla_date_timetuple():
    bd = BanglaDate.from_date(D)
    assert bd.timetuple().tm_year == 2026


def test_bangla_date_toordinal():
    bd = BanglaDate.from_date(D)
    assert bd.toordinal() == D.toordinal()


def test_bangla_date_comparison_not_implemented():
    bd = BanglaDate.from_date(D)
    assert bd.__eq__("not a date") is NotImplemented
    assert bd.__lt__("not a date") is NotImplemented
    assert bd.__le__("not a date") is NotImplemented
    assert bd.__gt__("not a date") is NotImplemented
    assert bd.__ge__("not a date") is NotImplemented


# ── BanglaDatetime: microsecond ───────────────────────────────────────────────

def test_bangla_datetime_microsecond():
    bdt = BanglaDatetime.from_datetime(datetime(2026, 3, 12, 10, 30, 45, 123456))
    assert bdt.microsecond == 123456
