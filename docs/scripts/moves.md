# moves.py

Describes a move as a small record and converts it to and from UCI text.

First appears in `Day 02 - Make and undo moves`.

## What it does

The move e2-e4 is `Move((6, 4), (4, 4))` inside Remus and `"e2e4"` on the wire to
En Croissant. A pawn promoting on e8 is `Move((1, 4), (0, 4), "Q")`, written
`"e7e8q"`.

## Data structure

`Move` is a frozen dataclass with three fields: `from_square`, `to_square`, and
`promotion` (`None` for most moves). Frozen means a move cannot change after it is
made, so two equal moves compare equal with `==` and can sit in a set or dict.

## Program flow

`move_to_uci` writes the two square names and a lowercase promotion letter.
`move_from_uci` reads them back and makes the promotion letter uppercase for White and
lowercase for Black, matching the board's piece letters.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `Move` | 2 | One move: where the piece starts, where it lands, and any promotion. |
| `move_to_uci` | 2 | Convert a move to UCI text. |
| `move_from_uci` | 2 | Convert UCI text to a move. |

## Try it

From inside a Day folder that has the file:

```bash
uv run moves.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 2.2.
