# attacks.py

Decides whether a square is attacked and whether a king is in check.

First appears in `instructor/Day 04 - Keep only legal moves`.

## What it does

In the start position, White's knight on g1 and pawns on e2 and g2 attack f3, and no
Black piece does. `is_square_attacked(board, (5, 5), "w")` returns `True`.

## Two versions in one file

Version 1, `is_attacked_by_scanning`, asks every enemy piece "do you attack this
square?" by generating its moves. Turbo GameWorks Chess works this way, and the idea
is easy to trust.

Version 2, `is_square_attacked`, stands on the square and looks outward like a "super
piece": along rook lines and bishop lines with `first_piece`, and at the nearby
knight, pawn, and king squares. Version 2 looks at a few dozen squares instead of
generating every enemy move, so Remus uses it. `main()` compares both versions on
every square of a test position.

## Program flow

`in_check(state, color)` finds the king with `find_king` and asks whether the opponent
attacks its square. `legal_moves.py` calls `in_check` after every trial move.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `is_attacked_by_scanning` | 4 | Version 1: ask every enemy piece whether it attacks the square. |
| `attacked_by_knight` | 4 | Return True if a knight of by_color is one knight jump away. |
| `attacked_by_king` | 4 | Return True if the king of by_color is one step away. |
| `attacked_by_pawn` | 4 | Return True if a pawn of by_color attacks the square. |
| `first_piece` | 4 | Return the first piece met walking from the square in a direction, or EMPTY. |
| `attacked_along_lines` | 4 | Return True if a rook, bishop, or queen of by_color attacks along a line. |
| `is_square_attacked` | 4 | Version 2: look outward from the square for any attacker of by_color. |
| `find_king` | 4 | Return the (row, col) of the king of the given color. |
| `in_check` | 4 | Return True if the king of the given color is attacked. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run attacks.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 4.1, 4.2.
