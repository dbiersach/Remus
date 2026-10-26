# move_generation.py: Every move the pieces can make

*First appears in `instructor/Day 03 - Generate piece moves`.*

## The big picture

Each piece moves in its own way. This file lists every move each piece could make.

It does not check whether the king is safe yet. Those moves are called pseudo-legal.
The next file, legal_moves.py, throws out the unsafe ones.

## Where this piece fits

move_generation.py uses board.py, game_state.py, and moves.py. attacks.py and legal_moves.py use it.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`moves.py`](moves.md)
- **Used by:** [`attacks.py`](attacks.md), [`legal_moves.py`](legal_moves.md)

## Words to know

- **pseudo-legal:** follows how the pieces move, but might leave your own king in check.
- **direction:** a step written as (row change, column change). Up the board is (-1, 0).
- **slider:** a rook, bishop, or queen. It slides until something blocks it.
- **jumper:** a knight or a king. It moves by fixed steps.

## What it stores

Directions are pairs of numbers:

```text
(-1,-1)  (-1, 0)  (-1, 1)        up-left    up     up-right
( 0,-1)    piece  ( 0, 1)        left      piece   right
( 1,-1)  ( 1, 0)  ( 1, 1)        down-left  down   down-right
```

Rooks use the four straight directions. Bishops use the four diagonals. The queen
uses all eight. A knight on a1 has only two jumps that stay on the board.

## How it works

1. `pseudo_legal_moves()` visits all 64 squares.
2. For each piece of the side to move, `piece_moves()` picks a helper by its letter.
3. Knights and kings use `jump_moves()`.
4. Rooks, bishops, and queens use `slider_moves()`, which calls `slide()` for each direction.
5. Pawns use `pawn_pushes()` and `pawn_captures()`. On the last rank, one pawn move becomes four promotion moves.
6. `en_passant_captures()` adds the special pawn capture.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
pseudo_legal_moves()
    en_passant_captures()
        on_board()
        piece_at()  [board.py]
    color_of()  [game_state.py]
    piece_moves()
        piece_at()  [board.py]
        color_of()  [game_state.py]
        knight_moves()
            jump_moves()
                on_board()
                color_of()  [game_state.py]
                piece_at()  [board.py]
        king_moves()
            jump_moves()
                on_board()
                color_of()  [game_state.py]
                piece_at()  [board.py]
        slider_moves()
            slide()
                on_board()
                piece_at()  [board.py]
                color_of()  [game_state.py]
        pawn_pushes()
            on_board()
            pawn_moves_to()
            piece_at()  [board.py]
        pawn_captures()
            on_board()
            color_of()  [game_state.py]
            piece_at()  [board.py]
            pawn_moves_to()
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `on_board` | Says True if (row, col) is one of the 64 squares. | 3 |
| `jump_moves` | Lists the moves of a piece that jumps by fixed steps. | 3 |
| `knight_moves` | Lists a knight's moves. | 3 |
| `king_moves` | Lists a king's one-step moves. | 3 |
| `slide` | Walks one way until it hits the edge or a piece. | 3 |
| `slider_moves` | Lists a rook's, bishop's, or queen's moves. | 3 |
| `pawn_moves_to` | Makes one pawn move, or four if the pawn promotes. | 3 |
| `pawn_pushes` | Lists a pawn's forward moves: one step, or two from the start. | 3 |
| `pawn_captures` | Lists a pawn's diagonal captures. | 3 |
| `piece_moves` | Picks the right helper for the piece on a square. | 3 |
| `en_passant_captures` | Lists en passant captures, if any. | 5 |
| `pseudo_legal_moves` | Lists every move for the side to move, before the king-safety check. | 3 |

## How the file grows

- **Day 3:** `on_board`, `jump_moves`, `knight_moves`, `king_moves`, `slide`, `slider_moves`, `pawn_moves_to`, `pawn_pushes`, `pawn_captures`, `piece_moves`, `pseudo_legal_moves`
- **Day 5:** `en_passant_captures`

## Try it

From inside a Day folder that has the file, run:

```bash
uv run move_generation.py
```

You should see: `Pseudo-legal moves from the start: 20`, a knight on a1 with 2 moves, and a rook on d4 with 14.

## Puzzle questions

1. A rook on d4 of an empty board has 14 moves. Can you list them?
2. Why does a White pawn move with a row change of -1?

## Slides

Slides 3.1, 3.2, 3.3, 3.4, 3.5 in the [slide plan](../slide_plan.md).
