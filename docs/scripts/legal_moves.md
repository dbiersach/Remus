# legal_moves.py: Keep only the legal moves

*First appears in `instructor/Day 04 - Keep only legal moves/period3`.*

## The big picture

Some moves break the rules because they leave your own king in check. This file
throws those moves out.

It uses one simple test. Make the move. Is your king attacked? If so, the move is
illegal. Undo it either way.

## Where this piece fits

legal_moves.py uses attacks.py, move_generation.py, and make_move.py. Almost every file above it calls `legal_moves()`.

- **Uses:** [`attacks.py`](attacks.md), [`board.py`](board.md), [`game_state.py`](game_state.md), [`make_move.py`](make_move.md), [`move_generation.py`](move_generation.md), [`moves.py`](moves.md)
- **Used by:** [`game_end.py`](game_end.md), [`mate_solver.py`](mate_solver.md), [`notation.py`](notation.md), [`perft.py`](perft.md), [`search.py`](search.md), [`uci_engine.py`](uci_engine.md)

## Words to know

- **legal move:** a move the rules allow.
- **pin:** a piece cannot move because moving it would expose its king.
- **castling:** the king moves two squares toward a rook, and the rook jumps over.

## What it stores

Each row of the castling table `CASTLES` holds one castling move:

```text
right  king from  king to  must be empty   king passes
 "K"     e1        g1       f1, g1           f1
 "Q"     e1        c1       d1, c1, b1       d1
 "k"     e8        g8       f8, g8           f8
 "q"     e8        c8       d8, c8, b8       d8
```

## How it works

1. Start with every pseudo-legal move.
2. Add castling moves that pass all the castling checks.
3. For each move: make it, test the king with `in_check()`, then undo it.
4. Keep the move only if the king was safe.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
legal_moves()
    pseudo_legal_moves()  [move_generation.py]
    castling_moves()
        opponent()  [game_state.py]
        in_check()  [attacks.py]
        is_square_attacked()  [attacks.py]
        piece_at()  [board.py]
    make_move()  [make_move.py]
    undo_move()  [make_move.py]
    in_check()  [attacks.py]
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `castling_moves` | Lists the castling moves the side to move may make right now. | Day 5, period 2 |
| `legal_moves` | Lists every legal move for the side to move. | Day 4, period 3 |

## How the file grows

- **Day 4, period 3:** `legal_moves`
- **Day 5, period 2:** `castling_moves`

## Try it

Open `legal_moves.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: `Legal moves from the start: 20  (expected 20)`.

## Puzzle questions

1. Why is it easier to test the king after the move than to look for pins first?
2. You may not castle out of check. Which line of the castling checks handles that?

## Slides

Slides 4.3, 4.4, 5.1, 5.5 in the [slide plan](../slide_plan.md).
