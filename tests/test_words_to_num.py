import pytest
from bornomala import num_to_words, words_to_num


# ── Direct conversion tests ────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("শূন্য", 0),
    ("এক", 1),
    ("নিরানব্বই", 99),
    ("একশত", 100),
    ("পাঁচশত", 500),
    ("নয়শত নিরানব্বই", 999),
    ("এক হাজার", 1000),
    ("এক হাজার দুইশত চৌত্রিশ", 1234),
    ("এক লক্ষ", 100000),
    ("বারো লক্ষ চৌত্রিশ হাজার পাঁচশত সাতষট্টি", 1234567),
    ("এক কোটি", 10000000),
    ("দশ কোটি", 100000000),
    ("একশত কোটি", 1000000000),
])
def test_direct(text, expected):
    assert words_to_num(text) == expected


# ── Negative numbers ───────────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("ঋণাত্মক এক", -1),
    ("ঋণাত্মক বিয়াল্লিশ", -42),
    ("ঋণাত্মক এক হাজার", -1000),
])
def test_negatives(text, expected):
    assert words_to_num(text) == expected


# ── Decimals ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("তিন দশমিক এক চার", 3.14),
    ("শূন্য দশমিক পাঁচ", 0.5),
    ("ঋণাত্মক দুই দশমিক পাঁচ", -2.5),
    ("একশত দশমিক শূন্য এক", 100.01),
])
def test_decimals(text, expected):
    assert words_to_num(text) == pytest.approx(expected)


# ── Return type ────────────────────────────────────────────────────────────

def test_returns_int_for_whole_number():
    result = words_to_num("এক হাজার")
    assert isinstance(result, int)


def test_returns_float_for_decimal():
    result = words_to_num("তিন দশমিক এক চার")
    assert isinstance(result, float)


# ── Round-trip tests ───────────────────────────────────────────────────────

@pytest.mark.parametrize("n", [
    0, 1, 9, 10, 11, 19, 20, 21, 42, 99,
    100, 101, 500, 999,
    1000, 1234, 9999,
    10000, 99999,
    100000, 1234567, 9999999,
    10000000, 99999999,
    100000000, 999999999,
])
def test_round_trip_int(n):
    assert words_to_num(num_to_words(n)) == n


@pytest.mark.parametrize("n", [-1, -42, -1000, -100000])
def test_round_trip_negative(n):
    assert words_to_num(num_to_words(n)) == n


# ── Error cases ────────────────────────────────────────────────────────────

def test_empty_input():
    with pytest.raises(ValueError):
        words_to_num("")


def test_unknown_token():
    with pytest.raises(ValueError):
        words_to_num("hello")


def test_fractional_token_too_large():
    with pytest.raises(ValueError):
        words_to_num("তিন দশমিক ত্রিশ")  # ত্রিশ=30, not a single digit


def test_nothing_after_dashamik():
    with pytest.raises(ValueError):
        words_to_num("এক দশমিক")


def test_nothing_after_rnaatmak():
    with pytest.raises(ValueError):
        words_to_num("ঋণাত্মক")


def test_place_word_without_coefficient():
    with pytest.raises(ValueError):
        words_to_num("হাজার")
