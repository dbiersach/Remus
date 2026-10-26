# board.py

Holds the chessboard and converts square names such as e2 to (row, col) tuples.

First appears in `instructor/Day 01 - Draw the board`. Grows on Day 2.

## What it does

At the start of a game, the White pawn on e2 sits at `board[6][4]`. Row 6 is rank 2,
because row 0 is rank 8, and column 4 is file e, because column 0 is file a. The board
prints rank 8 at the top, the way a player sees it from White's side.

## Data structure

The board is a list of 8 rows; each row is a list of 8 one-character strings.
Uppercase letters are White pieces, lowercase letters are Black pieces, and `EMPTY`
(`"."`) is an empty square. `BOARD_FILES` (`"abcdefgh"`) gives the file letter of each
column, and `BOARD_RANKS` (`"87654321"`) gives the rank digit of each row, so
`BOARD_FILES[4] + BOARD_RANKS[6]` is `"e2"`. `START_ROWS` spells out the start position one row at a
time, so students can read it like a picture.

## Program flow

`square_name(row, col)` and `parse_square(name)` are mirror images: `"e2"` becomes
`(6, 4)`, and `(6, 4)` becomes `"e2"`. `parse_square` raises `ValueError` for text
such as `"z9"`, so a typing mistake stops at the boundary instead of reaching the
engine. Every later module reads and writes squares through `piece_at` and
`set_piece`.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `new_board` | 1 | Return a fresh board set up in the starting position. |
| `print_board` | 1 | Print the board with rank numbers on the left and file letters below. |
| `square_name` | 1 | Convert board coordinates to an algebraic square name. |
| `parse_square` | 1 | Convert an algebraic square name to (row, col) coordinates. |
| `piece_at` | 1 | Return the piece on a (row, col) square, or EMPTY. |
| `set_piece` | 2 | Put a piece (or EMPTY) on a (row, col) square. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run board.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 1.3, 1.4, 1.5.
