# Day 7, Period 1: Ending the game

## Learning objectives

By the end of this period, each student pair can:

- Name every way a game ends: checkmate, stalemate, insufficient material, repetition, and the fifty-move rule. **Measured by:** Six-position quiz: each student pair gets at least five right.
- Detect the end of a game in code. **Measured by:** The game-end tests in `test_game.py` pass for all five endings.

## The files

New files this period:

- `game_end.py`

Files that grow this period:

- `fen.py`
- `game_state.py`
- `make_move.py`
- `test_game.py`

Functions the student pairs write this period:

- `insufficient_material()` in `game_end.py`
- `game_result()` in `game_end.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `insufficient_material()` in `game_end.py`

Returns True when neither side can ever checkmate: kings alone, a king with one bishop or knight, or bishops that all stand on light squares, or all on dark squares. A square is light or dark by (row + col) % 2.

### `game_result()` in `game_end.py`

Checks every way a game ends, in order: no legal moves (checkmate or stalemate), insufficient material, threefold repetition, and the fifty-move rule. It returns the result and the reason, so the console and the GUI can say why a game is over.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:50 | Chess refresher: stalemate, repetition, the fifty and 75-move rules, and insufficient material, with a six-position quiz. |
| 8:50 to 9:00 | Slides: the halfmove clock and `position_key()`, which the teacher writes. |
| 9:00 to 9:45 | Student pairs write `insufficient_material()` and `game_result()` in `game_end.py`. |
| 9:45 to 10:00 | Student pairs check their answers on the quiz positions, then show and choose. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `game_end.py` | `insufficient_material()` | 17 | 18 | `test_game.py::test_insufficient_material` |
| `game_end.py` | `game_result()` | 57 | 12 | `test_game.py::test_checkmate_and_stalemate`, `test_game.py::test_threefold_repetition_and_undo`, `test_game.py::test_fifty_move_rule` |

Lines to type in all: 30. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `insufficient_material()` in `game_end.py`

**Where:** lines 32 to 49 of `game_end.py`, inside `insufficient_material()`, in place of the stub below the docstring. The tests call it directly.

```python
17 | def insufficient_material(board: Board) -> bool:
18 |     """
     ...
30 |         against king, and kings with bishops that all stand on squares of one color.
31 |     """
32 +     pieces = []
33 +     bishop_square_colors = set()
34 +     for row in range(8):
35 +         for col in range(8):
36 +             piece = board[row][col]
37 +             if piece == EMPTY or piece.upper() == "K":
38 +                 continue
39 +             pieces.append(piece.upper())
40 +             if piece.upper() == "B":
41 +                 bishop_square_colors.add((row + col) % 2)
42 +     if not pieces:
43 +         return True
44 +     if len(pieces) == 1 and pieces[0] in "BN":
45 +         return True
46 +     for piece in pieces:
47 +         if piece != "B":
48 +             return False  # A knight beside other pieces, or any pawn, rook, or queen
49 +     return len(bishop_square_colors) == 1
50 |
51 |
52 | def repetition_count(state: dict) -> int:
```

**How it works:** The loops collect every piece except the kings in `pieces`, in uppercase. For each bishop they add the color of its square: `(row + col) % 2` is 0 on one color and 1 on the other. Kings alone, or a king with one bishop or one knight, cannot mate, so the answer is True. Any other piece besides bishops can mate, so the answer is False. When only bishops are left, mate is impossible only if they all stand on squares of one color.

### `game_result()` in `game_end.py`

**Where:** lines 72 to 83 of `game_end.py`, inside `game_result()`, in place of the stub below the docstring. The tests call it directly.

```python
57 | def game_result(state: dict) -> tuple[str, str] | None:
58 |     """
     ...
70 |         ("1-0", "checkmate").
71 |     """
72 +     if not legal_moves(state):
73 +         if in_check(state, state["turn"]):
74 +             winner = "0-1" if state["turn"] == "w" else "1-0"
75 +             return winner, "checkmate"
76 +         return "1/2-1/2", "stalemate"
77 +     if insufficient_material(state["board"]):
78 +         return "1/2-1/2", "insufficient material"
79 +     if repetition_count(state) >= 3:
80 +         return "1/2-1/2", "threefold repetition"
81 +     if state["halfmove_clock"] >= 100:
82 +         return "1/2-1/2", "fifty-move rule"
83 +     return None
84 |
85 |
86 | def main():
```

**How it works:** The checks run in order. With no legal move, the game is over: checkmate if the side to move is in check, and the other side wins; stalemate if not. Next come the three draws: too little material to mate, the same position three times, and 100 half-moves with no capture or pawn move. If none applies, the game goes on and the function returns None.
