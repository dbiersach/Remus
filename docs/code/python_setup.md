# python_setup.py: Is the laptop ready?

*Day 1, period 1. The lab file is `student/Day 01 - Draw the board/period1/python_setup.py`, and the answers are in `instructor/Day 01 - Draw the board/period1/python_setup_instructor.py`.*

## The big picture

Before a pair writes any chess code, the laptop has to run Python. This lab checks
that, and it is the pair's first program: it prints a greeting with the team name and
picks the king out of White's back rank.

## Where this piece fits

The lab does not import Remus, and no Remus file imports it. The skills it practices,
variables, f-strings, and indexing a string, show up in `board.py` on Day 1, period 4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](board.md)

## Words to know

- **variable:** a name for a value, such as `team_name = "Knight Riders"`.
- **string:** text in quotes, such as `"RNBQKBNR"`.
- **f-string:** a string that starts with `f` and puts values inside `{ }` into the text.
- **index:** the position of one character. The first character has index 0.

## How it works

1. Part #1 (written for you) prints the Python version and whether python-chess is installed.
2. Part #2: store the team name, print a greeting, and count its characters with `len()`.
3. Part #3: store White's back rank as one string and print `back_rank[4]`, the king.

The pair types 6 lines.

## Try it

Open `python_setup.py` in `student/Day 01 - Draw the board/period1` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: Python 3.14 or later, `python-chess installed: True`, and `K` for the king.

## Puzzle questions

1. Why is the king at index 4 and not index 5?
2. What does `len("Knight Riders")` print, and does the space count?
