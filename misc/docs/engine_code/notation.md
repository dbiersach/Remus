# notation.py: Moves the way people write them

*First appears in `Day 07 - Play full games and score positions/period2/instructor`.*

## The big picture

People write moves like `Nf3`, `exd5`, and `O-O`. This is called SAN.

This file writes Remus's moves in SAN, and reads SAN that you type. To read SAN, it
uses a simple trick. It writes every legal move in SAN, then picks the one that
matches what you typed.

## Where this piece fits

notation.py uses board.py, attacks.py, legal_moves.py, and make_move.py. opening_book.py uses it to read the book's SAN moves, and the tests use it to name moves.

- **Uses:** [`attacks.py`](attacks.md), [`board.py`](board.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`opening_book.py`](opening_book.md)

## Words to know

- **SAN:** Standard Algebraic Notation, the way chess books write moves.
  [Chess notation](../chess_instruction/chess_notation.md) explains how to read and
  write it: piece letters, captures, castling, promotion, check, and checkmate.
- **disambiguation:** an extra letter or number when two pieces could make the same move, as in `Nbd2`.

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

| Function | What it does | Arrives |
| --- | --- | --- |
| `move_to_san` | Writes a legal move in SAN, like Nf3 or exd5. | Day 7, period 2 |
| `disambiguation` | Adds the letter or number that tells two pieces apart. | Day 7, period 2 |
| `parse_san` | Finds the legal move that matches the SAN you typed. | Day 7, period 2 |

## Try it

Open `notation.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Every legal move of a test position in SAN, and `O-O-O` read back as a Move.

## Puzzle questions

1. Two rooks on a1 and h1 can both move to d1. What are their SAN moves?
2. Why can `parse_san()` never accept an illegal move?

## Slides

Slides 7.3, 7.4 in the [slide plan](../course/slide_plan.md).
