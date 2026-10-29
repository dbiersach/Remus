# Day 4, Period 3: Check and the legal filter

## Learning objectives

By the end of this period, each student pair can:

- Tell whether a king is in check. **Measured by:** The `in_check` tests pass in check and out of check.
- Keep only legal moves by making each move, testing the king, and undoing it. **Measured by:** The legal-move tests pass: 20 moves from the start, only escapes in check, and no moves for a pinned knight.

## The files

New files this period:

- `legal_moves.py`

Files that grow this period:

- `attacks.py`
- `test_legal_moves.py`

Functions the student pairs write this period:

- `in_check()` in `attacks.py`
- `legal_moves()` in `legal_moves.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `in_check()` in `attacks.py`

Finds the king of one piece color and asks whether the other piece color attacks its square. Check decides which moves are legal, whether a game is over, and later how deep the search looks.

### `legal_moves()` in `legal_moves.py`

Tries every pseudo-legal move: makes it, keeps it if the mover's king is not in check, and undoes it. Testing after the move catches pins and discovered checks without any special rules, which is why the code is so short.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Unplugged warm-up, "Pin hunt": on four printed positions, student pairs cross out every move that leaves the mover's king attacked. |
| 1:15 to 1:25 | Slides: a move is legal only if the mover's king is safe after the move. Make it, test the king, undo it. |
| 1:25 to 2:05 | Student pairs write `in_check()` and `legal_moves()` until the tests pass. |
| 2:05 to 2:15 | Student pairs compare Remus's answers with their pin hunt worksheets. |
| 2:15 to 2:30 | Show and choose for `legal_moves()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `attacks.py` | `in_check()` | 179 | 2 | `test_legal_moves.py::test_rook_check` |
| `legal_moves.py` | `legal_moves()` | 16 | 8 | `test_legal_moves.py::test_king_cannot_step_next_to_the_other_king`, `test_legal_moves.py::test_legal_moves_leave_the_state_unchanged` |

Lines to type in all: 10. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `in_check()` in `attacks.py`

**Where:** lines 195 to 196 of `attacks.py`, inside `in_check()`, in place of the stub below the docstring. The tests call it directly.

```python
179 | def in_check(state: dict, color: str) -> bool:
180 |     """
      ...
193 |         True if that king stands on a square the other side attacks.
194 |     """
195 +     board = state["board"]
196 +     return is_square_attacked(board, find_king(board, color), opponent(color))
197 |
198 |
199 | def main():
```

**How it works:** `find_king` finds the king of `color` on the board, and `opponent` gives the other side. A king is in check when the other side attacks its square, so one call to `is_square_attacked` answers the question.

### `legal_moves()` in `legal_moves.py`

**Where:** lines 30 to 37 of `legal_moves.py`, inside `legal_moves()`, in place of the stub below the docstring. The tests call it directly.

```python
16 | def legal_moves(state: dict) -> list[Move]:
17 |     """
     ...
28 |         The pseudo-legal moves that do not leave the mover's king in check.
29 |     """
30 +     mover = state["turn"]
31 +     moves = []
32 +     for move in pseudo_legal_moves(state):
33 +         undo = make_move(state, move)
34 +         if not in_check(state, mover):
35 +             moves.append(move)
36 +         undo_move(state, undo)
37 +     return moves
38 |
39 |
40 | def main():
```

**How it works:** The function remembers whose move it is in `mover`, because `make_move` passes the turn. For each pseudo-legal move it makes the move, asks whether the mover's own king is now in check, and keeps the move only if it is not. `undo_move` puts the position back before the next move is tried. This one test catches pins, moves into check, and en passant captures that expose the king.
