import pytest
from bornomala import format_currency


@pytest.mark.parametrize("amount, expected", [
    (0,      "শূন্য টাকা মাত্র"),
    (1,      "এক টাকা মাত্র"),
    (100,    "একশত টাকা মাত্র"),
    (500,    "পাঁচশত টাকা মাত্র"),
    (1000,   "এক হাজার টাকা মাত্র"),
    (96250,  "ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা মাত্র"),
])
def test_integer_amounts(amount, expected):
    assert format_currency(amount) == expected


@pytest.mark.parametrize("amount, expected", [
    ("1234.56", "এক হাজার দুইশত চৌত্রিশ টাকা ছাপান্ন পয়সা মাত্র"),
    ("0.50",    "শূন্য টাকা পঞ্চাশ পয়সা মাত্র"),
    ("100.01",  "একশত টাকা এক পয়সা মাত্র"),
    ("10.99",   "দশ টাকা নিরানব্বই পয়সা মাত্র"),
])
def test_fractional_amounts(amount, expected):
    assert format_currency(amount) == expected


def test_zero_paisa_omitted():
    assert format_currency("50.00") == "পঞ্চাশ টাকা মাত্র"


def test_custom_unit():
    assert format_currency(500, unit="ডলার") == "পাঁচশত ডলার মাত্র"


def test_custom_paisa_unit():
    assert format_currency("1.50", unit="পাউন্ড", paisa_unit="পেনি") == \
        "এক পাউন্ড পঞ্চাশ পেনি মাত্র"


def test_bangla_digit_string():
    assert format_currency("৫০০") == "পাঁচশত টাকা মাত্র"


def test_frac_truncated_to_two_places():
    # 1.999 → taka=1, paisa=99 (truncated, not rounded)
    assert format_currency("1.999") == "এক টাকা নিরানব্বই পয়সা মাত্র"
