# Day 4, Period 2: Attacks

## Learning objectives

By the end of this period, each student pair can:

- Decide whether a knight, pawn, or king attacks a square. **Measured by:** The attack tests in `test_legal_moves.py` pass for all three pieces.
- Explain that a pawn attacks diagonally but moves straight. **Measured by:** The student pair marks the two squares a White pawn on e4 attacks (d5, f5) on the printed board.

## The files

New files this period:

- `attacks.py`
- `test_legal_moves.py`

Functions the student pairs write this period:

- `piece_at_offsets()` in `attacks.py`
- `attacked_by_pawn()` in `attacks.py`
- `attacked_by_king()` in `attacks.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `piece_at_offsets()` in `attacks.py`

Stands on the square and looks at each offset for one piece, such as an enemy knight. Attacks work backward: instead of asking where every enemy piece can go, the test looks out from the square. A knight attacks e5 from exactly the squares a knight on e5 could jump to, so the knight, the king, and the pawn all share this one loop, the way `jump_moves()` serves both the knight and the king.

### `attacked_by_pawn()` in `attacks.py`

Looks diagonally for an enemy pawn on the row behind the square, from the attacker's point of view. A pawn captures diagonally even though it moves straight, so its two offsets differ from its push, and they depend on its piece color.

### `attacked_by_king()` in `attacks.py`

Looks one step away in all eight directions for the enemy king, with the same `KING_STEPS` the king moves by. Kings can never stand next to each other, and this check is what stops a king from walking up to the other king.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Chess refresher on the demonstration board: check, pins, and discovered check. |
| 10:45 to 11:00 | Slides: a square is attacked if a piece could capture there. Stand on the square and look outward like a "super piece". The teacher writes `attacked_by_knight()` and the sliding-line part. |
| 11:00 to 11:40 | Student pairs write `piece_at_offsets()`, then `attacked_by_pawn()` and `attacked_by_king()` on top of it. |
| 11:40 to 11:50 | Student pairs run the attack tests and the file's self-check. |
| 11:50 to 12:00 | Show and choose for `piece_at_offsets()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `attacks.py` | `piece_at_offsets()` | 64 | 6 | `run_tests.py` |
| `attacks.py` | `attacked_by_pawn()` | 103 | 3 | `run_tests.py` |
| `attacks.py` | `attacked_by_king()` | 97 | 2 | `run_tests.py` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
