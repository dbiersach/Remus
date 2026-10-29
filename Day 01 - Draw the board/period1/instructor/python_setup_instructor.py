#!/usr/bin/env -S uv run
"""python_setup_instructor.py

Day 1, period 1: check that the laptop is ready for the workshop, and say hello.
The student file python_setup.py leaves one # line for each line the student pair types.
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
    team_name = "Knight Riders"
    print(f"Hello from team {team_name}!")
    # len() counts the characters in a string, spaces included
    print(f"Our team name has {len(team_name)} characters")

    print("Part #3 - Your First Chess Line")
    # White's back rank, from the a-file to the h-file, as one string
    back_rank = "RNBQKBNR"
    print(f"White's back rank: {back_rank}  (expected RNBQKBNR)")
    print(f"The king stands on the e-file: {back_rank[4]}  (expected K)")


if __name__ == "__main__":
    main()
