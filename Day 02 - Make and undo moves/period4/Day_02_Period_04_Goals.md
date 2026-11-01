# Day 2, Period 4: make_move.py: make and undo ordinary moves

## Learning objectives

By the end of this period, each student pair can:

- Make a move and take it back exactly. **Measured by:** The make and undo tests pass, and ten moves made and undone leave the same state as the start, clocks and rights included.
- Explain why undo needs a record of what the move changed. **Measured by:** The student pair names what a capture destroys (the captured piece) and where the undo record keeps it.

## The files

New files this period:

- `make_move.py`

Files that grow this period. The new code in them is given code, already in the folder when the class opens it:

- `test_make_move.py`: 4 new tests

Functions the student pairs write this period:

- `make_move()` in `make_move.py`
- `undo_move()` in `make_move.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `make_move()` in `make_move.py`

Moves a piece and empties the square it left, then updates the clocks and gives the turn to the other side. Before changing anything, it writes down every value the move will destroy, such as the captured piece and the old clocks, in an undo record. That record is the only way to take the move back, and a search in Remus makes and undoes thousands of moves for every move it plays.

### `undo_move()` in `make_move.py`

Puts back everything a move changed, using the undo record that `make_move()` saved: the moved piece, the captured piece, the side to move, and the clocks and rights. The search will make and undo millions of moves, so undo must restore the position exactly, or Remus slowly corrupts its own board.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 3:00 to 3:15 | Unplugged warm-up, "Undo from the card": one partner makes three moves with sticky-note pieces and writes an undo card for each. The other partner restores the start position from the cards alone. |
| 3:15 to 3:25 | Slides: what a move destroys (the captured piece, the clocks, the side to move) and the undo record that saves it. The teacher shows `state_snapshot()` and the "make ten, undo ten, compare" test. |
| 3:25 to 4:15 | Student pairs write `make_move()` and `undo_move()` in `make_move.py` until the tests pass. |
| 4:15 to 4:30 | Show and choose for `make_move()`, then the checkpoint: ten moves made and undone give back the exact start state. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `make_move.py` | `make_move()` | 13 | 23 | `test_make_move.py::test_e2e4_changes_board_and_turn`, `test_make_move.py::test_knight_move_counts_toward_fifty_moves`, `test_make_move.py::test_capture_and_undo`, `test_make_move.py::test_ten_moves_made_and_undone_return_the_start` |
| `make_move.py` | `undo_move()` | 58 | 9 | `test_make_move.py::test_capture_and_undo`, `test_make_move.py::test_ten_moves_made_and_undone_return_the_start` |

Lines to type in all: 32. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `make_move()` in `make_move.py`

**Where:** lines 30 to 55 of `make_move.py`, inside `make_move()`, in place of the stub below the docstring. The tests call it directly.

```python
13 | def make_move(state: dict, move: Move) -> dict:
14 |     """
     ...
28 |         and the old values of every state field the move changes.
29 |     """
30 +     board = state["board"]
31 +     piece = piece_at(board, move.from_square)
32 +     captured = piece_at(board, move.to_square)
33 +     undo = {
34 +         "move": move,
35 +         "piece": piece,
36 +         "captured": captured,
37 +         "castling": state["castling"],
38 +         "en_passant": state["en_passant"],
39 +         "halfmove_clock": state["halfmove_clock"],
40 +         "fullmove_number": state["fullmove_number"],
41 +     }
42 +
43 +     set_piece(board, move.to_square, piece)
44 +     set_piece(board, move.from_square, EMPTY)
45 +
46 +     # The fifty-move clock restarts after a capture or a pawn move
47 +     if captured != EMPTY or piece.upper() == "P":
48 +         state["halfmove_clock"] = 0
49 +     else:
50 +         state["halfmove_clock"] += 1
51 +     if state["turn"] == BLACK:
52 +         state["fullmove_number"] += 1
53 +     state["en_passant"] = None
54 +     state["turn"] = opponent(state["turn"])
55 +     return undo
56 |
57 |
58 | def undo_move(state: dict, undo: dict) -> None:
```

**How it works:** First the function reads the moving piece and whatever stands on the landing square. Before anything changes, it records the old values in the `undo` dict: the move, both pieces, the castling rights, the en passant target, and both clocks. Next `set_piece` puts the piece on its new square and empties the old one. A capture or a pawn move resets the halfmove clock to 0, and any other move adds 1. The fullmove number grows after Black moves. Finally the turn passes to the opponent, and the function returns the undo record.

### `undo_move()` in `make_move.py`

**Where:** lines 69 to 77 of `make_move.py`, inside `undo_move()`, in place of the stub below the docstring. The tests call it directly.

```python
58 | def undo_move(state: dict, undo: dict) -> None:
59 |     """
     ...
67 |         The record make_move returned for this move.
68 |     """
69 +     board = state["board"]
70 +     move = undo["move"]
71 +     set_piece(board, move.from_square, undo["piece"])
72 +     set_piece(board, move.to_square, undo["captured"])
73 +     state["turn"] = opponent(state["turn"])
74 +     state["castling"] = undo["castling"]
75 +     state["en_passant"] = undo["en_passant"]
76 +     state["halfmove_clock"] = undo["halfmove_clock"]
77 +     state["fullmove_number"] = undo["fullmove_number"]
78 |
79 |
80 | def state_snapshot(state: dict) -> str:
```

**How it works:** The undo record holds everything the move changed. The piece goes back to its starting square, and the landing square gets back what stood there before: the captured piece, or `EMPTY` for a quiet move. The turn flips back, and the castling rights, en passant target, and both clocks are copied from the record.
