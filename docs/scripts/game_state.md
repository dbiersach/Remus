# game_state.py

Holds everything about a game that the board alone does not show.

First appears in `instructor/Day 02 - Make and undo moves`. Grows on Day 7.

## What it does

Two positions can show the same pieces and still differ: in one, White may castle; in
the other, the king has already moved. The game state records those facts beside the
board.

## Data structure

```python
{"board": board, "turn": "w", "castling": "KQkq", "en_passant": None,
 "halfmove_clock": 0, "fullmove_number": 1, "history": [key]}
```

`history` arrives on Day 7. It lists the `position_key` of every position so far, so
`game_end.py` can count repetitions.

## Program flow

`new_game()` builds the start state. `color_of`, `is_white`, and `opponent` answer the
small questions every other module asks. `position_key(state)` writes the pieces, side
to move, castling rights, and en passant square as one string. It includes the en
passant square only when a capture there is possible, because the repetition rule
treats two positions as the same unless a player could make a different move.

## Functions

| Function | Day | What it does |
| --- | --- | --- |
| `new_game` | 2 | Return the state of a new game. |
| `is_white` | 2 | Return True if the piece is White (an uppercase letter). |
| `color_of` | 2 | Return "w" or "b" for a piece, or None for an empty square. |
| `opponent` | 2 | Return the other side's color. |
| `position_key` | 7 | Return text that is the same for two positions exactly when the repetition rule treats them as the same position. |

## Try it

From inside a Day folder in `instructor/` that has the file:

```bash
uv run game_state.py
```

The script prints each result next to the expected answer.

## Slides

See [`slide_plan.md`](../slide_plan.md): slides 2.1, 7.4.
