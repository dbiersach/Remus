# fen.py

Reads and writes FEN, the one-line description of a position.

First appears in `Day 07 - Play full games in En Croissant`.

## What it does

`rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1` is the start position.
The six fields are the pieces (rank 8 first, digits for runs of empty squares), the
side to move, the castling rights, the en passant square, the halfmove clock, and the
fullmove number.

## Program flow

`state_from_fen` splits the text on spaces and fills the state dict field by field;
`board_from_placement` expands each digit into that many `"."` squares.
`state_to_fen` runs the other way through `fen_placement`. Tests, puzzles, and the UCI
adapter all set up positions through `state_from_fen`.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `fen_placement` | 7 | Return the piece-placement field of FEN for a board. |
| `board_from_placement` | 7 | Build a board from the piece-placement field of FEN. |
| `state_from_fen` | 7 | Build a game state from a full FEN string. |
| `state_to_fen` | 7 | Write a game state as a full FEN string. |

## Try it

From inside a Day folder that has the file:

```bash
uv run fen.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 7.1.
