# moves.py: What a move looks like

*First appears in `instructor/Day 02 - Make and undo moves/period3`.*

## The big picture

A move needs three facts: where the piece starts, where it lands, and what a pawn
turns into if it reaches the last rank.

This file stores those facts in a small record called `Move`. It also writes moves
as text like `e2e4`, which Lucas Chess understands.

## Where this piece fits

moves.py uses board.py for square names. Every file that makes or lists moves uses it.

- **Uses:** [`board.py`](board.md)
- **Used by:** [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`mate_solver.py`](mate_solver.md), [`move_generation.py`](move_generation.md), [`move_ordering.py`](move_ordering.md), [`notation.py`](notation.md), [`opening_book.py`](opening_book.md), [`perft.py`](perft.md), [`search.py`](search.md), [`show_board.py`](show_board.md), [`transposition_table.py`](transposition_table.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **record:** a small bundle of named values. A `Move` has three.
- **dataclass:** a Python way to make a record with very little code.
- **UCI:** the language chess programs use to talk. A move looks like `e2e4`.
- **promotion:** a pawn on the last rank turns into a queen, rook, bishop, or knight.

## What it stores

```python
Move(from_square=(6, 4), to_square=(4, 4), promotion=None)   # e2 to e4
Move(from_square=(1, 4), to_square=(0, 4), promotion="Q")    # e7 to e8, becomes a queen
```

A `Move` is frozen. Once made, it cannot change. Two moves with the same three facts
are equal.

## How it works

1. `move_to_uci()` writes a move as text, such as `e2e4` or `e7e8q`.
2. `move_from_uci()` reads that text back into a `Move`.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
move_to_uci()
    square_name()  [board.py]

move_from_uci()
    parse_square()  [board.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `Move` | The record for one move: start square, end square, and promotion. | Day 2, period 3 |
| `move_to_uci` | Writes a move as UCI text, like e2e4. | Day 2, period 3 |
| `move_from_uci` | Reads UCI text like e2e4 and makes a Move. | Day 2, period 3 |

## Try it

Open `moves.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: `g1f3` turned into a `Move` and back into `g1f3`.

## Puzzle questions

1. What is the UCI text for a Black pawn on b2 promoting to a knight on b1?
2. Why does a `Move` not store which piece is moving?

## Slides

Slides 2.2 in the [slide plan](../course/slide_plan.md).
