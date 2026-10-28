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

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `piece_at_offsets()` in `attacks.py`

Stands on the square and looks at each offset for one piece, such as an enemy knight. Attacks work backward: instead of asking where every enemy piece can go, the test looks out from the square. A knight attacks e5 from exactly the squares a knight on e5 could jump to, so the knight, the king, and the pawn all share this one loop, the way `jump_moves()` serves both the knight and the king.

### `attacked_by_pawn()` in `attacks.py`

Looks diagonally for an enemy pawn on the row behind the square, from the attacker's point of view. A pawn captures diagonally even though it moves straight, so its two offsets differ from its push, and they depend on its color.

### `attacked_by_king()` in `attacks.py`

Looks one step away in all eight directions for the enemy king, with the same `KING_STEPS` the king moves by. Kings can never stand next to each other, and this check is what stops a king from walking up to the other king.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `attacks.py` | `piece_at_offsets()` | 64 | 6 | `uv run pytest` |
| `attacks.py` | `attacked_by_pawn()` | 103 | 3 | `uv run pytest` |
| `attacks.py` | `attacked_by_king()` | 97 | 2 | `uv run pytest` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
