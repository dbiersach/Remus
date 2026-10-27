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

- `attacked_by_knight()` in `attacks.py`
- `attacked_by_pawn()` in `attacks.py`
- `attacked_by_king()` in `attacks.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `attacked_by_knight()` in `attacks.py`

Looks one knight jump away from the square for an enemy knight. Attacks work backward: instead of asking where every enemy piece can go, it stands on the square and looks out.

### `attacked_by_pawn()` in `attacks.py`

Looks diagonally for an enemy pawn on the row behind the square, from the attacker's point of view. A pawn captures diagonally even though it moves straight, so this check differs from the push.

### `attacked_by_king()` in `attacks.py`

Looks one step away in all eight directions for the enemy king. Kings can never stand next to each other, and this check is what stops a king from walking up to the other king.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
