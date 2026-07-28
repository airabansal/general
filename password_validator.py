#!/usr/bin/env python3
"""Validate a password against a few simple strength rules."""

import argparse
import getpass
import sys

SPECIAL_CHARS = "!@#$%^&*()-_=+[]{};:,.<>?/|"


def is_valid_password(password):
    """Return a list of rules the password FAILS. Empty list means it's valid."""
    problems = []

    if len(password) < 8:
        problems.append("must be at least 8 characters long")
    if not any(c.islower() for c in password):
        problems.append("must contain a lowercase letter")
    if not any(c.isupper() for c in password):
        problems.append("must contain an uppercase letter")
    if not any(c.isdigit() for c in password):
        problems.append("must contain a digit")
    if not any(c in SPECIAL_CHARS for c in password):
        problems.append("must contain a special character (" + SPECIAL_CHARS + ")")
    if " " in password:
        problems.append("must not contain spaces")

    return problems


def main():
    parser = argparse.ArgumentParser(description="Validate a password against simple strength rules.")
    parser.add_argument("password", nargs="?", help="password to check (prompted securely if omitted)")
    args = parser.parse_args()

    if args.password is not None:
        password = args.password
    else:
        # Read without echoing to the screen; fall back to a plain prompt if needed.
        try:
            password = getpass.getpass("Enter a password to check: ")
        except Exception:
            password = input("Enter a password to check: ")

    problems = is_valid_password(password)

    if not problems:
        print("Strong password!")
        sys.exit(0)

    print("Weak password. It:")
    for problem in problems:
        print("  - " + problem)
    sys.exit(1)


if __name__ == "__main__":
    main()
