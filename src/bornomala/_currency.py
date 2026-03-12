"""Cheque-style Bangla currency formatting."""

from ._digits import to_western_digits
from ._num_to_words import num_to_words


def format_currency(amount, unit="টাকা", paisa_unit="পয়সা"):
    # type: (object, str, str) -> str
    """Format a monetary amount as a cheque-style Bangla string.

    *amount* may be an ``int``, ``float``, or numeric string (Western or
    Bangla digits).  Fractional cents are truncated to two decimal places.

    Examples::

        >>> format_currency(96250)
        'ছিয়ানব্বই হাজার দুইশত পঞ্চাশ টাকা মাত্র'
        >>> format_currency(1234.56)
        'এক হাজার দুইশত চৌত্রিশ টাকা ছাপান্ন পয়সা মাত্র'
        >>> format_currency(500, unit="ডলার", paisa_unit="সেন্ট")
        'পাঁচশত ডলার মাত্র'
        >>> format_currency("৫০০")
        'পাঁচশত টাকা মাত্র'
    """
    s = to_western_digits(str(amount)).strip()

    if "." in s:
        int_str, frac_str = s.split(".", 1)
        taka = int(int_str) if int_str else 0
        # Normalise to exactly 2 fractional digits
        paisa = int((frac_str + "00")[:2])
    else:
        taka = int(s)
        paisa = 0

    result = str(num_to_words(taka)) + " " + unit
    if paisa:
        result += " " + str(num_to_words(paisa)) + " " + paisa_unit
    result += " মাত্র"
    return result
