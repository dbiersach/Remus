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

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `attacks.py` | `attacked_by_knight()` | 63 | 7 | `uv run pytest` |
| `attacks.py` | `attacked_by_pawn()` | 85 | 8 | `uv run pytest` |
| `attacks.py` | `attacked_by_king()` | 72 | 7 | `uv run pytest` |

Lines to type in all: 22. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
