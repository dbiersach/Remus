# move_generation.py

Lists every move the pieces can make by their movement rules.

First appears in `instructor/Day 03 - Generate piece moves`. Grows on Day 5.

## What it does

A rook on d4 of an empty board has 14 moves; a knight on a1 has 2. This module finds
them by walking direction tables, before any check for the king's safety. Such moves
are called pseudo-legal: they follow how the pieces move, but some may leave the king
in check.

## Data structures

Directions are `(row change, col change)` pairs. `ROOK_DIRECTIONS` holds four,
`BISHOP_DIRECTIONS` four, and `QUEEN_DIRECTIONS` all eight. `KNIGHT_JUMPS` and
`KING_STEPS` hold fixed offsets. Row 0 is rank 8, so a White pawn moves with a row
change of -1 and a Black pawn with +1.

## Program flow

`pseudo_legal_moves(state)` visits all 64 squares. For each piece of the side to move,
`piece_moves` picks a helper by the piece letter:

- knights and kings use `jump_moves`;
- rooks, bishops, and queens use `slider_moves`, which calls `slide` once per
  direction until it meets the edge or a piece;
- pawns use `pawn_pushes` and `pawn_captures`, and `pawn_moves_to` turns a move to
  the last rank into four promotion moves.

Day 5 adds `en_passant_captures(state)`, which needs the state's en passant square,
not just the board.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `on_board` | 3 | Return True if (row, col) is one of the 64 squares. |
| `jump_moves` | 3 | Return the moves of a piece that jumps by fixed offsets (a knight or a king). |
| `knight_moves` | 3 | Return the moves of a knight on the square. |
| `king_moves` | 3 | Return the one-step moves of a king on the square (castling comes later). |
| `slide` | 3 | Walk from a square in one direction and return the moves along the way. |
| `slider_moves` | 3 | Return the moves of a rook, bishop, or queen, one direction at a time. |
| `pawn_moves_to` | 3 | Return a pawn move, or the four promotion moves if it reaches the last rank. |
| `pawn_pushes` | 3 | Return a pawn's forward moves: one step, or two steps from its starting rank. |
| `pawn_captures` | 3 | Return a pawn's diagonal captures of enemy pieces. |
| `piece_moves` | 3 | Return the pseudo-legal moves of whatever piece stands on the square. |
| `en_passant_captures` | 5 | Return the en passant captures for the side to move. |
| `pseudo_legal_moves` | 3 | Return every pseudo-legal move for the side to move. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run move_generation.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 3.1, 3.2, 3.3, 3.4, 3.5.
