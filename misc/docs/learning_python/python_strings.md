# python_strings.py: Square names are text

*Day 1, period 2. The lab file is `Day 01 - Draw the board/period2/student/python_strings.py`, and the answers are in `Day 01 - Draw the board/period2/instructor/python_strings_instructor.py`.*

## The big picture

People name squares with text, such as `"e2"`. Remus needs numbers to find a square
on its board. This lab turns the letter of a file into a number, turns a number back
into a letter, and tells White pieces from Black ones by their case.

## Where this piece fits

The lab does not import Remus. On Day 1, period 4, `parse_square()` and
`square_name()` in `board.py` do exactly what Parts #2 and #3 practice, and on Day 2
`is_white()` in `game_state.py` is the one call from Part #4.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`board.py`](../code/board.md) and [`game_state.py`](../code/game_state.md)

## Words to know

- **ord():** gives the code number of a character. `ord("a")` is 97.
- **chr():** turns a code number back into a character. `chr(98)` is `"b"`.
- **file number:** how far a file is from the a-file, so a is 0 and e is 4.
- **isupper():** True when a letter is uppercase, which in Remus means a White piece.

## How it works

1. Part #1: pick the file letter `"e"` and rank digit `"2"` out of `"e2"` by index.
2. Part #2: `ord("e") - ord("a")` gives file number 4; `int("2")` gives rank number 2.
3. Part #3: `chr(ord("a") + 6)` gives `"g"`, and joining it with 7 gives `"g7"`.
4. Part #4: `upper()` turns `"rnbqkbnr"` into White's pieces, and `isupper()` tells them apart.

The student pair types 13 lines.

## Try it

Open `python_strings.py` in `Day 01 - Draw the board/period2/student` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: file letter e and rank digit 2, file number 4, the square g7, and `True` for `"N".isupper()`.

## Puzzle questions

1. What is the file number of h4, and of a1?
2. Why does subtracting `ord("a")` make the a-file number 0?
