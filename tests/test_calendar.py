import pytest
from datetime import date
from bornomala import (
    BanglaCalendarDate,
    gregorian_to_bangla,
    bangla_to_gregorian,
    BANGLA_CAL_MONTHS,
    BANGLA_SEASONS,
)


# ── gregorian_to_bangla ───────────────────────────────────────────────────────

@pytest.mark.parametrize("gdate, by, bm, bd", [
    # New Year's Day
    (date(2026, 4, 14), 1433, 1,  1),   # ১ বৈশাখ ১৪৩৩
    # Day before New Year
    (date(2026, 4, 13), 1432, 12, 31),  # চৈত্র 31, 1432
    # Mid-year
    (date(2026, 3, 12), 1432, 11, 28),  # ২৮ ফাল্গুন ১৪৩২
    # January in the same Bangla year
    (date(2026, 1, 14), 1432, 10, 1),   # ১ মাঘ ১৪৩২
    (date(2026, 1, 13), 1432, 9,  30),  # পৌষ 30
    # Mid-summer
    (date(2025, 7, 16), 1432, 4,  1),   # ১ শ্রাবণ ১৪৩২
    # Bangla year 1433 start
    (date(2026, 4, 14), 1433, 1,  1),
    (date(2026, 5, 15), 1433, 2,  1),   # ১ জ্যৈষ্ঠ ১৪৩৩
])
def test_gregorian_to_bangla(gdate, by, bm, bd):
    result = gregorian_to_bangla(gdate)
    assert result.year == by
    assert result.month == bm
    assert result.day == bd


# ── bangla_to_gregorian (round-trip) ─────────────────────────────────────────

@pytest.mark.parametrize("gdate", [
    date(2026, 1, 1),
    date(2026, 3, 12),
    date(2026, 4, 13),
    date(2026, 4, 14),
    date(2026, 7, 16),
    date(2025, 12, 15),
    date(2025, 4, 14),
])
def test_round_trip(gdate):
    assert bangla_to_gregorian(gregorian_to_bangla(gdate)) == gdate


# ── BanglaCalendarDate attributes ────────────────────────────────────────────

def test_month_name():
    assert gregorian_to_bangla(date(2026, 3, 12)).month_name == "ফাল্গুন"
    assert gregorian_to_bangla(date(2026, 4, 14)).month_name == "বৈশাখ"


def test_season():
    assert gregorian_to_bangla(date(2026, 3, 12)).season == "বসন্ত"   # ফাল্গুন
    assert gregorian_to_bangla(date(2026, 4, 14)).season == "গ্রীষ্ম"  # বৈশাখ
    assert gregorian_to_bangla(date(2026, 7, 16)).season == "বর্ষা"    # শ্রাবণ


def test_str():
    bd = BanglaCalendarDate(1432, 11, 28)
    assert str(bd) == "২৮ ফাল্গুন ১৪৩২"


def test_repr():
    bd = BanglaCalendarDate(1433, 1, 1)
    assert repr(bd) == "BanglaCalendarDate(1433, 1, 1)"


def test_str_new_year():
    bd = gregorian_to_bangla(date(2026, 4, 14))
    assert str(bd) == "১ বৈশাখ ১৪৩৩"


# ── All 12 months present in BANGLA_CAL_MONTHS ───────────────────────────────

def test_month_list_length():
    assert len(BANGLA_CAL_MONTHS) == 12


def test_all_months_have_seasons():
    for m in range(1, 13):
        assert m in BANGLA_SEASONS


# ── Equality and comparison ───────────────────────────────────────────────────

def test_equality():
    assert BanglaCalendarDate(1432, 11, 28) == BanglaCalendarDate(1432, 11, 28)
    assert BanglaCalendarDate(1432, 11, 28) != BanglaCalendarDate(1432, 11, 29)


def test_ordering():
    a = BanglaCalendarDate(1432, 1, 1)
    b = BanglaCalendarDate(1432, 12, 30)
    assert a < b
    assert b > a


# ── Invalid construction ──────────────────────────────────────────────────────

def test_invalid_month():
    with pytest.raises(ValueError):
        BanglaCalendarDate(1432, 13, 1)


def test_invalid_day():
    with pytest.raises(ValueError):
        BanglaCalendarDate(1432, 1, 0)


# ── Extended comparison coverage ─────────────────────────────────────────────

def test_le_equal():
    a = BanglaCalendarDate(1432, 6, 15)
    b = BanglaCalendarDate(1432, 6, 15)
    assert a <= b


def test_le_less():
    a = BanglaCalendarDate(1432, 1, 1)
    b = BanglaCalendarDate(1432, 6, 1)
    assert a <= b


def test_ge_equal():
    a = BanglaCalendarDate(1432, 6, 15)
    b = BanglaCalendarDate(1432, 6, 15)
    assert a >= b


def test_ge_greater():
    a = BanglaCalendarDate(1432, 12, 1)
    b = BanglaCalendarDate(1432, 1, 1)
    assert a >= b


def test_gt():
    a = BanglaCalendarDate(1433, 1, 1)
    b = BanglaCalendarDate(1432, 12, 30)
    assert a > b


def test_hash_usable_in_set():
    a = BanglaCalendarDate(1432, 11, 28)
    b = BanglaCalendarDate(1432, 11, 28)
    assert len({a, b}) == 1


def test_not_implemented_eq():
    a = BanglaCalendarDate(1432, 1, 1)
    assert a.__eq__("not a date") is NotImplemented


def test_not_implemented_lt():
    a = BanglaCalendarDate(1432, 1, 1)
    assert a.__lt__("not a date") is NotImplemented


def test_not_implemented_le():
    a = BanglaCalendarDate(1432, 1, 1)
    assert a.__le__("not a date") is NotImplemented


def test_not_implemented_gt():
    a = BanglaCalendarDate(1432, 1, 1)
    assert a.__gt__("not a date") is NotImplemented


def test_not_implemented_ge():
    a = BanglaCalendarDate(1432, 1, 1)
    assert a.__ge__("not a date") is NotImplemented


# ── bangla_to_gregorian standalone ───────────────────────────────────────────

def test_bangla_to_gregorian_standalone():
    assert bangla_to_gregorian(BanglaCalendarDate(1433, 1, 1)) == date(2026, 4, 14)
    assert bangla_to_gregorian(BanglaCalendarDate(1432, 11, 28)) == date(2026, 3, 12)
