# Day 1, Period 1: Welcome and setup

Watch the finished Remus play in Lucas Chess, form pairs, and check that every laptop runs `uv run pytest`.

## Learning objectives

By the end of this period, each pair can:

- Start VS Code, open a Python file, and run it with the Run Python File button (the triangle at the top right of the editor). **Measured by:** Running `python_setup.py` prints Python 3.14 or later and `python-chess installed: True` on the pair's laptop.
- Store text in a variable and print it inside an f-string. **Measured by:** Part #2 of `python_setup.py` greets the pair's own team name and counts its characters correctly.
- Name the parts of a chess engine that Remus will grow: board, moves, rules, search, and evaluation. **Measured by:** Exit ticket: each student lists three of the five parts and one job of each.

## The files

This period comes before any Remus code. The lab is `python_setup.py` in `student/`, with the answers in `python_setup_instructor.py` in `instructor/`. Open `python_setup.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

## The changes and why

The pairs fill in the blanks of `python_setup.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_setup_instructor.py`.

Part #1 is already written. It prints the Python version and whether python-chess is installed, so the teacher can see at a glance that the laptop is ready.

Part #2: you store your team name in a variable and print it inside an f-string. A variable is a name for a value, and an f-string puts values into text. Remus prints every result this way.

Part #3: you store White's back rank as one string and print the letter at index 4, the king. Remus writes pieces as letters too, uppercase for White.
