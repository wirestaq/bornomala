import pytest
from bornomala import num_to_words
from bornomala._data import ONES


# ── 0–99 parametrized against the ONES table ──────────────────────────────

@pytest.mark.parametrize("n, expected", list(ONES.items()))
def test_ones_table(n, expected):
    assert num_to_words(n) == expected


# ── Hundreds ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    (100, "একশত"),
    (200, "দুইশত"),
    (300, "তিনশত"),
    (500, "পাঁচশত"),
    (900, "নয়শত"),
    (101, "একশত এক"),
    (115, "একশত পনেরো"),
    (999, "নয়শত নিরানব্বই"),
])
def test_hundreds(n, expected):
    assert num_to_words(n) == expected


# ── Thousands ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    (1000, "এক হাজার"),
    (2000, "দুই হাজার"),
    (10000, "দশ হাজার"),
    (99000, "নিরানব্বই হাজার"),
    (1500, "এক হাজার পাঁচশত"),
    (1234, "এক হাজার দুইশত চৌত্রিশ"),
    (9999, "নয় হাজার নয়শত নিরানব্বই"),
])
def test_thousands(n, expected):
    assert num_to_words(n) == expected


# ── Lakhs ──────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    (100000, "এক লক্ষ"),
    (500000, "পাঁচ লক্ষ"),
    (1000000, "দশ লক্ষ"),
    (1234567, "বারো লক্ষ চৌত্রিশ হাজার পাঁচশত সাতষট্টি"),
    (9999999, "নিরানব্বই লক্ষ নিরানব্বই হাজার নয়শত নিরানব্বই"),
])
def test_lakhs(n, expected):
    assert num_to_words(n) == expected


# ── Crores ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    (10000000, "এক কোটি"),
    (100000000, "দশ কোটি"),
    (1000000000, "একশত কোটি"),
    (10000000000, "এক হাজার কোটি"),
])
def test_crores(n, expected):
    assert num_to_words(n) == expected


# ── Negatives ──────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    (-1, "ঋণাত্মক এক"),
    (-42, "ঋণাত্মক বিয়াল্লিশ"),
    (-1000, "ঋণাত্মক এক হাজার"),
    (-100, "ঋণাত্মক একশত"),
])
def test_negatives(n, expected):
    assert num_to_words(n) == expected


# ── Floats ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("n, expected", [
    ("3.14", "তিন দশমিক এক চার"),
    ("0.5", "শূন্য দশমিক পাঁচ"),
    ("-2.5", "ঋণাত্মক দুই দশমিক পাঁচ"),
    ("100.01", "একশত দশমিক শূন্য এক"),
    ("1.005", "এক দশমিক শূন্য শূন্য পাঁচ"),
])
def test_floats(n, expected):
    assert num_to_words(n) == expected


# ── String inputs ──────────────────────────────────────────────────────────

def test_string_western_digits():
    assert num_to_words("42") == "বিয়াল্লিশ"


def test_string_bangla_digits():
    assert num_to_words("১২৩৪") == "এক হাজার দুইশত চৌত্রিশ"


def test_string_zero():
    assert num_to_words("০") == "শূন্য"


# ── BanglaWords suffix methods ─────────────────────────────────────────────

def test_banglawords_is_str_subclass():
    assert isinstance(num_to_words(1), str)


@pytest.mark.parametrize("method, suffix", [
    ("only",       " মাত্র"),
    ("taka",       " টাকা"),
    ("paisa",      " পয়সা"),
    ("jon",        " জন"),
    ("ti",         " টি"),
    ("ta",         " টা"),
    ("gram",       " গ্রাম"),
    ("kilo",       " কিলোগ্রাম"),
    ("liter",      " লিটার"),
    ("meter",      " মিটার"),
    ("kilo_meter", " কিলোমিটার"),
    ("percent",    " শতাংশ"),
    ("din",        " দিন"),
    ("ghonta",     " ঘণ্টা"),
])
def test_suffix_methods(method, suffix):
    result = getattr(num_to_words(5), method)()
    assert result == "পাঁচ" + suffix


def test_suffix_chaining():
    assert num_to_words(500).taka().only() == "পাঁচশত টাকা মাত্র"


def test_suffix_returns_banglawords():
    result = num_to_words(3).jon()
    assert isinstance(result, type(num_to_words(1)))
