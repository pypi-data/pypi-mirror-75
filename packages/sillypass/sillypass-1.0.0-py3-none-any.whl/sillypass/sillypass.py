import random
import string
from typing import Dict, Mapping, Optional


LETTERS = string.ascii_letters
UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = string.punctuation


def create_password(counts: Mapping[str, int], rng: random.Random) -> str:
    """
    Randomly generate a string containing the given counts of characters.

    The `counts` parameter maps groups of characters to the exact number of
    times a character from that group should appear in the password. For
    example:

      count={"abc": 5, "de": 1}

    means the generated string should have 6 characters, 5 of which are chosen
    from "a", "b", or "c", and 1 of which is chosen from "d" or "e".
    """

    password = []

    for group in counts:
        count = counts[group]
        password += rng.choices(group, k=count)

    rng.shuffle(password)

    return ''.join(password)


def create_counts(
        length: int = 24,
        min_letters: int = 0,
        min_upper: int = 0,
        min_lower: int = 0,
        min_digits: int = 0,
        min_symbols: int = 0,
        symbols: str = SYMBOLS,
        remainder: Optional[str] = None,
) -> Dict[str, int]:
    """
    Given the specified minimum counts of each character group, return a data
    structure that can be passed to `create_password` as its `counts` argument.

    This is a convenience function that covers the requirements of the majority
    of services that place silly constraints on their passwords.

    `length` is the total length of the password. If the sum of the minimum
    counts is less than `length`, then the `remainder` character group pads the
    password to `length`. If `remainder` isn't provided, it defaults to the
    union of letters, digits, and symbols.
    """

    if length < 0:
        raise ValueError("`length` argument is negative")
    if min_letters < 0:
        raise ValueError("`min_letters` argument is negative")
    if min_upper < 0:
        raise ValueError("`min_upper` argument is negative")
    if min_lower < 0:
        raise ValueError("`min_lower` argument is negative")
    if min_digits < 0:
        raise ValueError("`min_digits` argument is negative")
    if min_symbols < 0:
        raise ValueError("`min_symbols` argument is negative")
    if min_symbols > 0 and symbols == "":
        raise ValueError("No characters provided in `symbols` argument.")

    min_length = (
        min_letters
        + min_upper
        + min_lower
        + min_digits
        + min_symbols
    )
    if min_length > length:
        raise ValueError(
            "Password length is not large enough to accommodate sum of minimum "
            f"counts: {length} < {min_length}."
        )

    counts = {}

    if min_letters > 0:
        counts[LETTERS] = min_letters
    if min_upper > 0:
        counts[UPPERCASE] = min_upper
    if min_lower > 0:
        counts[LOWERCASE] = min_lower
    if min_digits > 0:
        counts[DIGITS] = min_digits
    if min_symbols > 0:
        counts[symbols] = min_symbols

    if remainder is None:
        remainder = ''.join(set(LETTERS + DIGITS + symbols))

    min_remainder = length - min_length
    if min_remainder > 0:
        counts[remainder] = length - min_length

    return counts
