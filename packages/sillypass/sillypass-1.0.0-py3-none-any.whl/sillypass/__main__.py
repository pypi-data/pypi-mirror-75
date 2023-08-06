import argparse
import secrets

from sillypass import SYMBOLS, create_counts, create_password


# main() is defined as a separate function so that it can be reached from the
# console script installed by the package.
def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    counts = create_counts(
        length=args.length,
        min_letters=args.min_letters,
        min_upper=args.min_upper,
        min_lower=args.min_lower,
        min_digits=args.min_digits,
        min_symbols=args.min_symbols,
        symbols=args.symbols,
    )
    print(create_password(counts, secrets.SystemRandom()))


def count(value: str) -> int:
    """
    Cast the value to a count (in other words, a nonnegative integer) and
    return the count.

    This function is intended to be used as an argparse type.
    """

    try:
        int_value = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} is not an integer")

    if int_value < 0:
        raise argparse.ArgumentTypeError(f"{value} is negative")

    return int_value


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate random passwords meeting minimum character "
        "requirements.",
    )
    parser.add_argument(
        "--length", "-l",
        type=count,
        default=24,
        help="Number of characters to include in the password. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--min-letters",
        type=count,
        default=0,
        help="Minimum number of letters (upper or lowercase) to include in the "
        "password. Default: %(default)s",
    )
    parser.add_argument(
        "--min-upper",
        type=count,
        default=0,
        help="Minimum number of uppercase letters to include in the password. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--min-lower",
        type=count,
        default=0,
        help="Minimum number of lowercase letters to include in the password. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--min-digits",
        type=count,
        default=0,
        help="Minimum number of numeric digits to include in the password. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--min-symbols",
        type=count,
        default=0,
        help="Minimum number of symbols to include in the password. "
        "Default: %(default)s",
    )
    parser.add_argument(
        "--symbols",
        default=SYMBOLS,
        help="Symbols that are allowed to appear in the password. "
        "Default: %(default)s",
    )

    return parser


if __name__ == "__main__":
    main()
