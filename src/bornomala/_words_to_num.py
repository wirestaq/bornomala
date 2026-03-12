"""Convert Bangla words (kotha) back to numbers."""

from typing import Union

from ._data import FUSED_SHAT, ONES, PLACE_MULTIPLIERS, REVERSE_ONES
from ._digits import to_western_digits

# Single-digit words (0–9) — used to validate fractional tokens
_SINGLE_DIGIT_WORDS = frozenset(ONES[i] for i in range(10))


def words_to_num(text: str) -> Union[int, float]:
    """Convert a Bangla word string back to a number.

    Returns ``int`` when there is no fractional part, ``float`` otherwise.

    Raises ``ValueError`` for unrecognised tokens or malformed input.

    Examples::

        >>> words_to_num("শূন্য")
        0
        >>> words_to_num("এক হাজার দুইশত চৌত্রিশ")
        1234
        >>> words_to_num("ঋণাত্মক বিয়াল্লিশ")
        -42
        >>> words_to_num("তিন দশমিক এক চার")
        3.14
    """
    # Normalise Bangla digits embedded in text
    text = to_western_digits(text.strip())
    tokens = text.split()

    if not tokens:
        raise ValueError("Empty input")

    # --- Sign ---
    negative = False
    if tokens[0] == "ঋণাত্মক":
        negative = True
        tokens = tokens[1:]
        if not tokens:
            raise ValueError("Nothing after ঋণাত্মক")

    # --- Decimal split ---
    frac_part = 0.0
    has_fraction = False
    if "দশমিক" in tokens:
        idx = tokens.index("দশমিক")
        frac_tokens = tokens[idx + 1:]
        tokens = tokens[:idx]
        if not frac_tokens:
            raise ValueError("Nothing after দশমিক")
        # Each fractional token must be a single-digit word (0–9)
        frac_digits = []
        for tok in frac_tokens:
            if tok not in _SINGLE_DIGIT_WORDS:
                raise ValueError(
                    "Invalid fractional token '{}': must be a digit word"
                    " (\u09b6\u09c2\u09a8\u09cd\u09af\u2013\u09a8\u09af\u09bc)".format(tok)
                )
            frac_digits.append(str(REVERSE_ONES[tok]))
        frac_part = float("0." + "".join(frac_digits))
        has_fraction = True

    # --- Integer accumulator ---
    total = 0
    current_group = 0

    for token in tokens:
        if token in FUSED_SHAT:
            current_group += FUSED_SHAT[token]
        elif token in PLACE_MULTIPLIERS:
            if current_group == 0:
                raise ValueError(
                    "Place word '{}' with no preceding coefficient".format(token)
                )
            total += current_group * PLACE_MULTIPLIERS[token]
            current_group = 0
        elif token in REVERSE_ONES:
            current_group += REVERSE_ONES[token]
        else:
            raise ValueError("Unrecognised token: '{}'".format(token))

    total += current_group

    # --- Assemble result ---
    if has_fraction:
        result = float(total) + frac_part
    else:
        result = total

    if negative:
        result = -result

    return result
