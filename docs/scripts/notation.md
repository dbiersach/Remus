# notation.py: Moves the way people write them

*First appears in `instructor/Day 07 - Play full games in En Croissant`.*

## The big picture

People write moves like `Nf3`, `exd5`, and `O-O`. This is called SAN.

This file writes Remus's moves in SAN, and reads SAN that you type. To read SAN, it
uses a simple trick. It writes every legal move in SAN, then picks the one that
matches what you typed.

## Where this piece fits

notation.py uses board.py, attacks.py, legal_moves.py, and make_move.py. console_game.py, opening_book.py, and mate_solver.py use it.

- **Uses:** [`attacks.py`](attacks.md), [`board.py`](board.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`console_game.py`](console_game.md), [`opening_book.py`](opening_book.md)

## Words to know

- **SAN:** Standard Algebraic Notation, the way chess books write moves.
- **disambiguation:** an extra letter or number when two pieces could make the same move, as in `Nbd2`.
- **check sign:** `+` means check. `#` means checkmate.

## What it stores

Parts of a SAN move:

```text
N  b  x  d2  +
|  |  |  |   gives check
|  |  |  square it lands on
|  |  captures
|  which knight (the one on the b-file)
piece letter (no letter for a pawn)
```

## How it works

1. `move_to_san()` starts with the piece letter, or nothing for a pawn.
2. `disambiguation()` adds a file, rank, or square if two pieces could reach the same square.
3. It adds `x` for a capture, the target square, and `=Q` for a promotion.
4. It makes the move to test for `+` or `#`, then undoes it.
5. `parse_san()` matches typed text against the SAN of every legal move.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
parse_san()
    legal_moves()  [legal_moves.py]
    move_to_san()
        piece_at()  [board.py]
        square_name()  [board.py]
        make_move()  [make_move.py]
        in_check()  [attacks.py]
        undo_move()  [make_move.py]
        legal_moves()  [legal_moves.py]
        disambiguation()
            square_name()  [board.py]
            legal_moves()  [legal_moves.py]
            piece_at()  [board.py]
```

## The functions

| Function | What it does | Day |
| --- | --- | --- |
| `move_to_san` | Writes a legal move in SAN, like Nf3 or exd5. | 7 |
| `disambiguation` | Adds the letter or number that tells two pieces apart. | 7 |
| `parse_san` | Finds the legal move that matches the SAN you typed. | 7 |

## Try it

From inside a Day folder that has the file, run:

```bash
uv run notation.py
```

You should see: Every legal move of a test position in SAN, and `O-O-O` read back as a Move.

## Puzzle questions

1. Two rooks on a1 and h1 can both move to d1. What are their SAN moves?
2. Why can `parse_san()` never accept an illegal move?

## Slides

Slides 7.2, 7.3 in the [slide plan](../slide_plan.md).
