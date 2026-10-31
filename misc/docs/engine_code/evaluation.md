# evaluation.py: How good is this position?

*First appears in `Day 07 - Play full games and score positions/period4/instructor`.*

## The big picture

To pick a good move, Remus needs to judge a position. This file gives each position
a score.

A positive score is good for White. The unit is the centipawn, one hundredth of a
pawn. So +100 means White is about one pawn ahead.

## Where this piece fits

evaluation.py uses board.py. search.py and move_ordering.py use its scores and piece values.

- **Uses:** [`board.py`](board.md)
- **Uses only in its self-check:** [`fen.py`](fen.md)
- **Used by:** [`move_ordering.py`](move_ordering.md), [`search.py`](search.md)

## Words to know

- **centipawn:** one hundredth of a pawn. A pawn is worth 100.
- **material:** the value of all the pieces each side has.
- **piece-square table:** an 8x8 grid of bonus points for standing on each square.
- **passed pawn:** a pawn with no enemy pawn ahead of it, on its own file or a file next to it.

## What it stores

Piece values:

| Piece | Pawn | Knight | Bishop | Rook | Queen |
| --- | --- | --- | --- | --- | --- |
| Centipawns | 100 | 300 | 300 | 500 | 900 |

The knight table gives +20 for the center and -50 for a corner. A knight in the
center reaches 8 squares. A knight in a corner reaches 2. Black reads each table
upside down.

## How it works

1. `material()` adds up White's pieces and subtracts Black's.
2. `placement()` adds the table bonus for each piece's square. The queen has no table:
   it is strong on any square, so it gets no bonus anywhere.
3. `pawn_structure()` subtracts points for weak pawns and adds points for passed pawns (Remus-PURPLE and Remus-GOLD, Day 9).
4. `mating_bonus()` helps finish a won endgame by pushing the losing king to the edge (Remus-CYAN and Remus-GOLD, Day 9).
5. `king_safety()` rewards pawns that shelter the king while the enemy queen is on the board (Remus-GRAY and Remus-GOLD, Day 9).
6. `evaluate()` adds the parts, then flips the sign if Black is to move.

## Call tree

Each function is listed with the functions it calls, indented below it.
A name in [brackets] lives in another file.

```text
explain_evaluation()
    material()
    placement()
    pawn_structure()
    mating_bonus()
    king_safety()
    evaluate()
        king_safety()
        mating_bonus()
        pawn_structure()
        material()
        placement()
```

## The functions

| Function | What it does | Arrives |
| --- | --- | --- |
| `material` | Counts the value of the pieces. Positive means White is ahead. | Day 7, period 4 |
| `placement` | Adds bonus points for pieces on good squares. | Day 7, period 4 |
| `pawn_structure` | Scores doubled, isolated, and passed pawns. | Remus-GOLD |
| `mating_bonus` | Rewards driving the losing king to the edge when far ahead. | Remus-GOLD |
| `king_safety` | Rewards pawns that shelter the king while the enemy queen is on the board. | Remus-GOLD |
| `evaluate` | Gives the score from the point of view of the side to move. | Day 7, period 4 |
| `explain_evaluation` | Prints each part of the score, so you can see why. | Day 7, period 4 |

## How the file grows

- **Day 7, period 4:** `material`, `placement`, `evaluate`, `explain_evaluation`
- **Remus-GOLD:** `pawn_structure`, `mating_bonus`, `king_safety`

## Try it

Open `evaluation.py` from a period folder that has the file in VS Code, and click the Run Python File
button (the triangle at the top right of the editor).

You should see: Every part of the score for the start (all 0), then a centered knight worth +70.

## Puzzle questions

1. White has a queen and Black has a rook. What is the material score?
2. Why does `evaluate()` flip the sign when Black is to move?

## Slides

Slides 7.7, 7.8, 9.12, 9.13, 9.14 in the [slide plan](../course/slide_plan.md).
