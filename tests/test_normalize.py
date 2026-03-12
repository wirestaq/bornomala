import pytest
from bornomala import normalize, is_bangla, is_pure_bangla, bangla_char_count


# ── normalize ─────────────────────────────────────────────────────────────────

def test_normalize_nfc():
    # NFD decomposed 'ক' (ka + combining nukta) should round-trip through NFC
    import unicodedata
    nfd = unicodedata.normalize("NFD", "বাংলা")
    assert normalize(nfd) == "বাংলা"


def test_normalize_collapses_spaces():
    assert normalize("আমার  সোনার  বাংলা") == "আমার সোনার বাংলা"


def test_normalize_strips_ends():
    assert normalize("  বাংলা  ") == "বাংলা"


def test_normalize_pipe_to_danda_between_bangla():
    assert normalize("এক|দুই") == "এক।দুই"


def test_normalize_pipe_not_replaced_in_latin_context():
    # pipe between Latin chars should stay
    assert normalize("a|b") == "a|b"


def test_normalize_nbsp():
    assert normalize("এক\u00a0দুই") == "এক দুই"


def test_normalize_empty():
    assert normalize("") == ""


def test_normalize_already_clean():
    text = "আমার সোনার বাংলা।"
    assert normalize(text) == text


# ── is_bangla ─────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("আমি", True),
    ("hello", False),
    ("hello আমি", True),
    ("১২৩", True),          # Bangla digits are in the Bangla block
    ("123", False),
    ("", False),
])
def test_is_bangla(text, expected):
    assert is_bangla(text) == expected


# ── is_pure_bangla ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("আমার বাংলা।", True),
    ("hello আমি", False),
    ("আমি ১০ জন।", True),     # Bangla digits OK
    ("আমি 10 জন।", False),    # Arabic/Western digits not OK
    ("", False),
    ("   ", False),
])
def test_is_pure_bangla(text, expected):
    assert is_pure_bangla(text) == expected


# ── bangla_char_count ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("text, expected", [
    ("আমি", 3),
    ("hello", 0),
    ("hello আমি", 3),
    ("", 0),
    ("আমার বাংলা", 9),
])
def test_bangla_char_count(text, expected):
    assert bangla_char_count(text) == expected
