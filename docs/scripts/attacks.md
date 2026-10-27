# attacks.py: Is this square under attack?

*First appears in `instructor/Day 04 - Keep only legal moves/period2`.*

## The big picture

A king may not stay in check. To know that, Remus must answer one question: is
this square attacked?

This file answers it two ways. Version 1 asks every enemy piece. Version 2 stands on
the square and looks outward. Remus uses version 2 because it checks fewer squares.

## Where this piece fits

attacks.py uses board.py, game_state.py, and move_generation.py. legal_moves.py, game_end.py, notation.py, search.py, and mate_solver.py use it.

- **Uses:** [`board.py`](board.md), [`game_state.py`](game_state.md), [`move_generation.py`](move_generation.md)
- **Used by:** [`game_end.py`](game_end.md), [`legal_moves.py`](legal_moves.md), [`mate_solver.py`](mate_solver.md), [`notation.py`](notation.md), [`search.py`](search.md)

## Words to know

- **attacked:** an enemy piece could capture on that square.
- **check:** the king's square is attacked.
- **super piece:** pretend a piece on the square can move every way. Whatever it could capture is an attacker.
- **ray:** a straight line of squares from one square to the edge.

## What it stores

Version 2 looks outward from the square like this:

```text
   along rook lines      -> finds an enemy rook or queen
   along bishop lines    -> finds an enemy bishop or queen
   at knight jumps       -> finds an enemy knight
   at pawn squares       -> finds an enemy pawn
   at the 8 next squares -> finds the enemy king
```

## How it works

1. `in_check()` finds the king with `find_king()`.
2. It asks `is_square_attacked()` about the king's square.
3. `is_square_attacked()` checks knights, the king, pawns, and the lines in turn.
4. `first_piece()` walks along a line and stops at the first piece it meets.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
is_attacked_by_scanning()
    color_of()  [game_state.py]
    piece_moves()  [move_generation.py]

in_check()
    is_square_attacked()
        attacked_by_knight()
            on_board()  [move_generation.py]
            piece_at()  [board.py]
        attacked_by_pawn()
            on_board()  [move_generation.py]
            piece_at()  [board.py]
        attacked_by_king()
            on_board()  [move_generation.py]
            piece_at()  [board.py]
        attacked_along_lines()
            first_piece()
                on_board()  [move_generation.py]
            color_of()  [game_state.py]
    find_king()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `is_attacked_by_scanning` | Version 1: asks every enemy piece if it can reach the square. | Day 4, period 2 |
| `attacked_by_knight` | Looks for an enemy knight one jump away. | Day 4, period 2 |
| `attacked_by_king` | Looks for the enemy king one step away. | Day 4, period 2 |
| `attacked_by_pawn` | Looks for an enemy pawn that captures onto the square. | Day 4, period 2 |
| `first_piece` | Walks in one direction and returns the first piece it meets. | Day 4, period 2 |
| `attacked_along_lines` | Looks along straight and diagonal lines for a rook, bishop, or queen. | Day 4, period 2 |
| `is_square_attacked` | Version 2: looks outward from the square for any attacker. | Day 4, period 2 |
| `find_king` | Finds the square of a king. | Day 4, period 3 |
| `in_check` | Says True if that side's king is attacked. | Day 4, period 3 |

## How the file grows

- **Day 4, period 2:** `is_attacked_by_scanning`, `attacked_by_knight`, `attacked_by_king`, `attacked_by_pawn`, `first_piece`, `attacked_along_lines`, `is_square_attacked`
- **Day 4, period 3:** `find_king`, `in_check`

## Try it

From inside a period folder that has the file, run:

```bash
uv run attacks.py
```

You should see: Which side attacks f3 at the start, and `Versions 1 and 2 agree on 96 of 96 squares`.

## Puzzle questions

1. At the start, which White pieces attack f3?
2. Why can a pawn attack a square it cannot move to?

## Slides

Slides 4.1, 4.2 in the [slide plan](../slide_plan.md).
