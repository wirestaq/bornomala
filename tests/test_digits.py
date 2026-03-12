import pytest
from bornomala import to_bangla_digits, to_western_digits

BANGLA_DIGITS = "০১২৩৪৫৬৭৮৯"
WESTERN_DIGITS = "0123456789"


@pytest.mark.parametrize("w, b", zip(WESTERN_DIGITS, BANGLA_DIGITS))
def test_to_bangla_single_digit(w, b):
    assert to_bangla_digits(w) == b


@pytest.mark.parametrize("w, b", zip(WESTERN_DIGITS, BANGLA_DIGITS))
def test_to_western_single_digit(w, b):
    assert to_western_digits(b) == w


def test_to_bangla_integer():
    assert to_bangla_digits(1234) == "১২৩৪"


def test_to_bangla_float_string():
    assert to_bangla_digits("3.14") == "৩.১৪"


def test_to_bangla_negative():
    assert to_bangla_digits(-42) == "-৪২"


def test_to_western_multidigit():
    assert to_western_digits("১২৩৪") == "1234"


def test_to_western_mixed_string():
    assert to_western_digits("১2৩") == "123"


def test_round_trip_digits():
    for i in range(1000):
        assert to_western_digits(to_bangla_digits(i)) == str(i)


def test_to_bangla_leaves_non_digits():
    assert to_bangla_digits("abc") == "abc"


def test_to_western_leaves_non_digits():
    assert to_western_digits("abc") == "abc"


def test_to_bangla_zero():
    assert to_bangla_digits(0) == "০"


def test_to_western_zero():
    assert to_western_digits("০") == "0"
