# make_move.py

Makes a move on the game state and undoes it exactly.

First appears in `instructor/Day 02 - Make and undo moves`. Grows on Day 5, Day 7.

## What it does

`make_move(state, move)` changes the state in place and returns an undo record.
`undo_move(state, undo)` uses that record to put back every square, right, and clock.
Search depends on this pair: it makes thousands of moves on one live state and must
leave that state exactly as it found it.

## Data structure: the undo record

```python
{"move": move, "piece": "P", "captured": ".",
 "castling": "KQkq", "en_passant": None,
 "halfmove_clock": 0, "fullmove_number": 1,
 "rook_move": None,           # (from, to) of the rook when castling (Day 5)
 "en_passant_victim": None}   # Square of the pawn removed en passant (Day 5)
```

## Program flow

1. Save everything the move can change in the undo record.
2. Move the piece; on Day 5, also move the castling rook, remove the en passant
   victim, or swap in the promotion piece.
3. Update the clocks, the en passant target, the castling rights
   (`update_castling_rights`), and the side to move.
4. From Day 7, append the new `position_key` to `history`.

`undo_move` runs the same steps backward. `state_snapshot(state)` writes the whole
state as text, so a test can check `before == after` in one comparison.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `update_castling_rights` | 5 | Return the castling rights left after a move. |
| `en_passant_victim_square` | 5 | Return the square of the pawn an en passant capture removes. |
| `castling_rook_move` | 5 | Return the (from, to) squares of the rook in a castling move. |
| `make_move` | 2 | Make any move, including castling, en passant, and promotion, and return the record needed to undo it. |
| `undo_move` | 2 | Take back the move described by an undo record. |
| `state_snapshot` | 2 | Return the whole state as text, so two states can be compared with ==. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run make_move.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 2.3, 2.4, 2.5, 5.2, 5.3, 5.4.
