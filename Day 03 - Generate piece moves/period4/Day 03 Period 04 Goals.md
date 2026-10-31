# Day 3, Period 4: Pawns

## Learning objectives

By the end of this period, each student pair can:

- Generate pawn pushes, including the two-step first move. **Measured by:** The pawn tests pass, and the start position gives 20 pseudo-legal moves.
- Explain why White pawns move toward row 0. **Measured by:** Exit ticket: "Row 0 is rank 8, so a White pawn on row 6 moves to row ..."

## The files

Files that grow this period. The new code in them is given code, already in the folder when the class opens it:

- `move_generation.py`: adds `pawn_moves_to()`, `pawn_captures()`, `piece_moves()`, `pseudo_legal_moves()`; changes `main()`
- `test_move_generation.py`: 4 new tests

Functions the student pairs write this period:

- `pawn_pushes()` in `move_generation.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `pawn_pushes()` in `move_generation.py`

Moves a pawn one square forward if it is empty, and two squares from its starting row if both are empty. White pawns move toward row 0, because row 0 is rank 8. Pawns are the only pieces that move one way and capture another, which is why pushes get their own function.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Slides: pawns move forward toward row 0 for White, push one or two squares, and capture diagonally. The given code holds the captures and the four promotion choices. |
| 3:15 to 3:55 | Student pairs write `pawn_pushes()`: the single step and the double step from the start rank. |
| 3:55 to 4:15 | Student pairs run the tests and the arrow picture on the start position. |
| 4:15 to 4:30 | Checkpoint: `pseudo_legal_moves()` finds 20 moves from the start. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `move_generation.py` | `pawn_pushes()` | 130 | 11 | `test_move_generation.py::test_pawn_pushes_from_the_start_rank`, `test_move_generation.py::test_blocked_pawn_has_no_pushes`, `test_move_generation.py::test_pawn_promotes_to_four_pieces` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `pawn_pushes()` in `move_generation.py`

**Where:** lines 148 to 158 of `move_generation.py`, inside `pawn_pushes()`, in place of the stub below the docstring. It is called by `piece_moves()` in `move_generation.py`.

```python
130 | def pawn_pushes(board: Board, square: Square, color: str) -> list[Move]:
131 |     """
      ...
146 |         The pushes onto empty squares. A pawn never captures straight ahead.
147 |     """
148 +     row, col = square
149 +     forward = -1 if color == WHITE else 1
150 +     start_row = 6 if color == WHITE else 1
151 +     moves = []
152 +     one_step = (row + forward, col)
153 +     if on_board(*one_step) and piece_at(board, one_step) == EMPTY:
154 +         moves += pawn_moves_to(square, one_step, color)
155 +         two_steps = (row + 2 * forward, col)
156 +         if row == start_row and piece_at(board, two_steps) == EMPTY:
157 +             moves.append(Move(square, two_steps))
158 +     return moves
159 |
160 |
161 | def pawn_captures(board: Board, square: Square, color: str) -> list[Move]:
```

**How it works:** White pawns move toward row 0 (rank 8), so `forward` is -1 for White and 1 for Black, and each side's pawns start on their own row. A pawn may step one square ahead only onto an empty square. `pawn_moves_to` turns a step onto the last rank into four promotions. Only when the first square is empty, and the pawn still stands on its starting row, may it also step two squares to another empty square.
