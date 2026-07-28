#!/usr/bin/env python3
"""Check whether a string is a palindrome."""

import argparse
import sys


def is_palindrome(text, ignore_case=True, alnum_only=True):
    """Return True if `text` reads the same forwards and backwards.

    ignore_case: fold case before comparing.
    alnum_only:  ignore spaces, punctuation, and other non-alphanumerics.
    """
    chars = text
    if alnum_only:
        chars = [c for c in chars if c.isalnum()]
    if ignore_case:
        chars = [c.lower() for c in chars]
    else:
        chars = list(chars)
    return chars == chars[::-1]


def main():
    parser = argparse.ArgumentParser(description="Check whether a string is a palindrome.")
    parser.add_argument("text", nargs="?", help="string to check (prompted if omitted)")
    parser.add_argument("--case-sensitive", action="store_true", help="do not ignore case")
    parser.add_argument("--strict", action="store_true", help="compare all characters, including spaces/punctuation")
    args = parser.parse_args()

    text = args.text if args.text is not None else input("Enter a string: ")

    result = is_palindrome(text, ignore_case=not args.case_sensitive, alnum_only=not args.strict)
    print(f"{text!r} is {'a palindrome' if result else 'not a palindrome'}")
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
