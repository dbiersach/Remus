# python_fen_fields.py: The six fields of FEN

*Day 6, period 4. The lab file is `student/Day 06 - Count positions and read FEN/period4/python_fen_fields.py`, and the answers are in `instructor/Day 06 - Count positions and read FEN/period4/python_fen_fields_instructor.py`.*

## The big picture

A FEN string writes a whole position in one line of six fields, separated by
spaces. This lab cuts the start FEN apart with `split()`, prints each field with its
name, and shows how `try` and `except` catch the error that `int()` raises on text
that is not a number.

## Where this piece fits

The lab does not import Remus. Later this period `state_from_fen()` in `fen.py`
starts with the same `split()`, and `board_from_placement()` cuts the first field
into rows with `split("/")`.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`fen.py`](fen.md)

## Words to know

- **FEN:** Forsyth-Edwards Notation: the placement, the side to move, castling, en passant, and two clocks.
- **split():** cuts a string into a list at every space, or at another character you name.
- **ValueError:** the error `int()` raises when its text is not a number.
- **try and except:** run some code, and run other code instead of crashing if a named error happens.

## How it works

1. Part #1: split the start FEN and count the fields.
2. Part #2: print each field with its name.
3. Part #3: turn text into a number inside `try`, and catch `ValueError`.

The pair types 8 lines.

## Try it

Open `python_fen_fields.py` in `student/Day 06 - Count positions and read FEN/period4` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 6 fields, then each field with its name, then "x is not a number".

## Puzzle questions

1. Which field changes after every move, and which only after Black's move?
2. What should a FEN reader do with the halfmove clock `"ten"`?
