# evaluation.py

Scores a position in centipawns without looking ahead.

First appears in `instructor/Day 08 - Evaluate and search ahead`. Grows on Day 10.

## What it does

A centipawn is a hundredth of a pawn. With a White knight on e5 and a Black knight on
a8, material is level but White's knight attacks eight squares and Black's two, so
`placement` gives White +70.

## Data structures

`PIECE_VALUES` holds 100, 300, 300, 500, and 900 for pawn, knight, bishop, rook, and
queen. Each piece-square table is an 8x8 list of bonuses written from White's side,
row 0 (rank 8) first. A Black piece reads its table upside down: row 7 uses row 0.

## Program flow

`evaluate(state)` adds the terms with White's side positive, then flips the sign when
Black is to move, because negamax scores every position for the side to move.

| Term | Day | Idea |
| --- | --- | --- |
| `material` | 8 | Sum of piece values |
| `placement` | 8 | Piece-square tables |
| `pawn_structure` | 10 | Doubled -8, isolated -20, passed pawns up to +70 by rank |
| `mating_bonus` | 10 | With a big lead against little material, push the losing king to the edge and bring the winning king close |

`explain_evaluation(state)` prints each term, so a student can say why Remus likes a
position.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `material` | 8 | Return the material balance in centipawns, positive when White is ahead. |
| `placement` | 8 | Return the piece-square bonus in centipawns, positive when it favors White. |
| `pawn_structure` | 10 | Score the pawn structure in centipawns, positive when it favors White. |
| `mating_bonus` | 10 | Return a bonus for cornering the losing king, positive when it favors White. |
| `evaluate` | 8 | Score the position for the side to move. |
| `explain_evaluation` | 8 | Print each term of the evaluation, so Remus can say why it likes a position. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run evaluation.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 8.1, 8.2, 10.6, 10.7.
