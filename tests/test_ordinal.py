import pytest
from bornomala import to_bangla_ordinal


@pytest.mark.parametrize("n, expected", [
    (1,   "১ম"),
    (2,   "২য়"),
    (3,   "৩য়"),
    (4,   "৪র্থ"),
    (5,   "৫ম"),
    (6,   "৬ষ্ঠ"),
    (7,   "৭ম"),
    (8,   "৮ম"),
    (9,   "৯ম"),
    (10,  "১০ম"),
    (11,  "১১তম"),
    (12,  "১২তম"),
    (20,  "২০তম"),
    (21,  "২১তম"),
    (100, "১০০তম"),
    (999, "৯৯৯তম"),
])
def test_ordinals(n, expected):
    assert to_bangla_ordinal(n) == expected


def test_ordinal_zero_raises():
    with pytest.raises(ValueError):
        to_bangla_ordinal(0)


def test_ordinal_negative_raises():
    with pytest.raises(ValueError):
        to_bangla_ordinal(-1)


def test_ordinal_float_truncated():
    # float is cast to int
    assert to_bangla_ordinal(3.9) == "৩য়"
