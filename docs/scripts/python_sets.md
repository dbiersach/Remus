# python_sets.py: Castling rights as letters

*Day 5, period 1. The lab file is `student/Day 05 - Add castling, en passant, and promotion/period1/python_sets.py`, and the answers are in `instructor/Day 05 - Add castling, en passant, and promotion/period1/python_sets_instructor.py`.*

## The big picture

Remus keeps the castling rights as the string `"KQkq"`: K is White's king side, q
is Black's queen side. When a king or a rook leaves its home square, its letters go
away for the rest of the game. This lab practices the Python tools for that job: sets,
`in`, dict lookups, and `replace()`.

## Where this piece fits

The lab does not import Remus. On Day 5, period 2, `update_castling_rights()` in
`make_move.py` removes letters with `replace()` exactly as Part #4 does.

- **Uses:** nothing from Remus
- **Used by:** nothing; it is practice for [`make_move.py`](make_move.md)

## Words to know

- **set:** a collection that holds each item once, such as the squares pieces have left.
- **in:** asks whether an item is in a set, a dict, or a string, and answers True or False.
- **replace():** gives back a new string with one piece of text swapped for another, such as "K" for "".

## How it works

1. Part #1: add h1, e1, and h1 again to a set, and count the squares.
2. Part #2: ask with `in` which rooks have moved.
3. Part #3: look up the rights a home square guards in a dict.
4. Part #4: remove letters from `"KQkq"` with `replace()`, one at a time.

The pair types 14 lines.

## Try it

Open `python_sets.py` in `student/Day 05 - Add castling, en passant, and promotion/period1` in VS Code, and click the Run Python File button (the
triangle at the top right of the editor).

You should see: 2 squares, True and False, K, then the rights Qkq and Q.

## Puzzle questions

1. Which letters must go when the White king moves from e1?
2. A Black rook is captured on h8. Which letter must go, and why?
