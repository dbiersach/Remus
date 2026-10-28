# mate_solver.py: Solve mate-in-two puzzles

*First appears in `instructor/Day 09 - Add the clock and build the stations/period4`.*

## The big picture

`tests/mate_puzzles.epd` holds ten puzzles: White to play and mate in 2 or 3 moves.
This file solves all ten.

It asks a yes-or-no question instead of giving scores. Is there a White move where
every Black reply still loses to mate?

## Where this piece fits

mate_solver.py uses legal_moves.py, make_move.py, attacks.py, and notation.py. It reads the puzzles from tests/mate_puzzles.epd.

- **Uses:** [`attacks.py`](attacks.md), [`legal_moves.py`](legal_moves.md), [`make_move.py`](make_move.md), [`moves.py`](moves.md)
- **Uses only in its self-check:** [`fen.py`](fen.md), [`notation.py`](notation.md)
- **Used by:** no other Remus file

## Words to know

- **mate in 2:** White moves, Black replies, and White's second move is checkmate.
- **forced:** it works no matter what the other side does.
- **EPD:** a file format like FEN, with extra fields such as the best move.

## What it stores

The search is a tree of "some" and "every":

```text
White: is there SOME move...
   Black: ...where EVERY reply...
      White: ...still has SOME mating move?
```

## How it works

1. `mating_move()` tries each White move.
2. On White's last allowed move, it skips moves that do not give check. Only a check can be mate.
3. If Black has no legal reply and is in check, that is mate.
4. Otherwise `defense_fails()` must be True for every Black reply.
5. `defense_fails()` makes the reply and asks `mating_move()` again, one move shorter.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
read_puzzles()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `mating_move` | Finds a move that forces mate in the given number of moves, or None. | Day 9, period 4 |
| `defense_fails` | Says True if White still mates after this Black reply. | Day 9, period 4 |
| `read_puzzles` | Reads the puzzles and their answers from the EPD file. | Day 9, period 4 |

## Try it

Open `mate_solver.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Each puzzle, the move found, the expected move, and the time. MATE.008, a mate in 3, takes about 6 seconds.

## Puzzle questions

1. Why does skipping non-checking moves on the last move never miss a mate?
2. What would happen if the solver forgot that stalemate is not a win?

## Slides

Slides 9.17 in the [slide plan](../slide_plan.md).
