# Day 4, Period 2: Attacks

## Learning objectives

By the end of this period, each pair can:

- Decide whether a knight, pawn, or king attacks a square. **Measured by:** The attack tests in `test_legal_moves.py` pass for all three pieces.
- Explain that a pawn attacks diagonally but moves straight. **Measured by:** The pair marks the two squares a White pawn on e4 attacks (d5, f5) on the printed board.

## The files

New files this period:

- `attacks.py`
- `test_legal_moves.py`

Functions the pairs write this period:

- `piece_at_offsets()` in `attacks.py`
- `attacked_by_pawn()` in `attacks.py`
- `attacked_by_king()` in `attacks.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `piece_at_offsets()` in `attacks.py`

Stands on the square and looks at each offset for one piece, such as an enemy knight. Attacks work backward: instead of asking where every enemy piece can go, the test looks out from the square. A knight attacks e5 from exactly the squares a knight on e5 could jump to, so the knight, the king, and the pawn all share this one loop, the way `jump_moves()` serves both the knight and the king.

### `attacked_by_pawn()` in `attacks.py`

Looks diagonally for an enemy pawn on the row behind the square, from the attacker's point of view. A pawn captures diagonally even though it moves straight, so its two offsets differ from its push, and they depend on its color.

### `attacked_by_king()` in `attacks.py`

Looks one step away in all eight directions for the enemy king, with the same `KING_STEPS` the king moves by. Kings can never stand next to each other, and this check is what stops a king from walking up to the other king.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
