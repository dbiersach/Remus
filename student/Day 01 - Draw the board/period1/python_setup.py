#!/usr/bin/env -S uv run
"""python_setup.py

Day 1, period 1: check that the laptop is ready for the workshop, and say hello.
Replace each line that holds only # with one line of code, then run the file.
"""

import importlib.util
import platform


def main():
    print("Part #1 - Check the Laptop")
    print(f"Python version: {platform.python_version()}  (expected 3.14 or later)")
    has_chess = importlib.util.find_spec("chess") is not None
    print(f"python-chess installed: {has_chess}  (expected True)")

    print("Part #2 - Say Hello")
    # Store your team name, then print a greeting that uses it
    #
    #
    # len() counts the characters in a string, spaces included
    #

    print("Part #3 - Your First Chess Line")
    # White's back rank, from the a-file to the h-file, as one string
    #
    #
    #


if __name__ == "__main__":
    main()
