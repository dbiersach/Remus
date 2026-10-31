# Day 2, Period 3: game_state.py and moves.py: a game state and a move record

## Learning objectives

By the end of this period, each student pair can:

- Tell the piece color of a piece, and handle an empty square. **Measured by:** The `is_white` and `color_of` tests in `test_make_move.py` pass, including `None` for `.`.
- Write a move as UCI text and read it back. **Measured by:** `move_to_uci` and `move_from_uci` round-trip `e2e4` and `e7e8q`.
- Name the fields of a game state. **Measured by:** Exit ticket: list the six fields of the state dict and what each holds.

## The files

New files this period:

- `game_state.py`
- `moves.py`
- `test_make_move.py`

Files that grow this period. The new code in them is given code, already in the folder when the class opens it:

- `board.py`: adds `set_piece()`

Functions the student pairs write this period:

- `is_white()` in `game_state.py`
- `color_of()` in `game_state.py`
- `move_to_uci()` in `moves.py`
- `move_from_uci()` in `moves.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `is_white()` in `game_state.py`

Returns True for an uppercase letter. Remus follows FEN, where uppercase is White and lowercase is Black, so one call to `isupper()` tells the piece colors apart.

### `color_of()` in `game_state.py`

Returns "w", "b", or None for an empty square. Move generation asks this about every square a piece might land on: a friend blocks the move, an enemy can be captured, and None means the square is free.

### `move_to_uci()` in `moves.py`

Writes a move as text such as e2e4, adding a lowercase piece letter for a promotion (e7e8q). UCI is the language Lucas Chess speaks, so this is how Remus tells the GUI which move it chose.

### `move_from_uci()` in `moves.py`

Reads text such as e7e8q back into a Move. The promotion letter becomes uppercase for White and lowercase for Black, so the new piece gets the right piece color on the board.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:15 | Slides: the game state dict in `new_game()` and the `Move` dataclass with `from_square`, `to_square`, and `promotion`. |
| 1:15 to 2:05 | Student pairs write `is_white()` and `color_of()` in `game_state.py`, then `move_to_uci()` and `move_from_uci()` in `moves.py`, running `run_tests.py` after each. |
| 2:05 to 2:15 | Student pairs run `game_state.py` and `moves.py` and compare the printouts with the expected answers. |
| 2:15 to 2:30 | Show and choose: the class picks one `move_from_uci()`, and the teacher adds its student pair's team name to `CONTRIBUTORS.md`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `game_state.py` | `is_white()` | 38 | 1 | `run_tests.py` |
| `game_state.py` | `color_of()` | 43 | 5 | `test_make_move.py::test_colors` |
| `moves.py` | `move_to_uci()` | 28 | 4 | `test_make_move.py::test_uci_round_trip` |
| `moves.py` | `move_from_uci()` | 48 | 6 | `test_make_move.py::test_uci_round_trip`, `test_make_move.py::test_move_record_holds_squares` |

Lines to type in all: 16. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `is_white()` in `game_state.py`

**Where:** line 40 of `game_state.py`, inside `is_white()`, in place of the stub below the docstring. The tests call it directly.

```python
38 | def is_white(piece: str) -> bool:
39 |     """Return True if the piece is White (an uppercase letter)."""
40 +     return piece.isupper()
41 |
42 |
43 | def color_of(piece: str) -> str | None:
```

**How it works:** `isupper()` is True for an uppercase letter. FEN writes White pieces in uppercase, so `"N".isupper()` is True and `"n".isupper()` is False.

### `color_of()` in `game_state.py`

**Where:** lines 45 to 49 of `game_state.py`, inside `color_of()`, in place of the stub below the docstring. The tests call it directly.

```python
43 | def color_of(piece: str) -> str | None:
44 |     """Return "w" or "b" for a piece, or None for an empty square."""
45 +     if piece == EMPTY:
46 +         return None
47 +     if is_white(piece):
48 +         return WHITE
49 +     return BLACK
50 |
51 |
52 | def opponent(color: str) -> str:
```

**How it works:** An empty square, the dot `EMPTY`, has no color, so the function returns None first. Every other square holds a piece: `is_white` sends White pieces to `WHITE` ("w"), and every piece left is Black.

### `move_to_uci()` in `moves.py`

**Where:** lines 42 to 45 of `moves.py`, inside `move_to_uci()`, in place of the stub below the docstring. The tests call it directly.

```python
28 | def move_to_uci(move: Move) -> str:
29 |     """
     ...
40 |         Text such as "e2e4", or "e7e8q" for a promotion (always lowercase).
41 |     """
42 +     text = square_name(*move.from_square) + square_name(*move.to_square)
43 +     if move.promotion is not None:
44 +         text += move.promotion.lower()
45 +     return text
46 |
47 |
48 | def move_from_uci(text: str, white_to_move: bool = True) -> Move:
```

**How it works:** `move.from_square` is a tuple such as (6, 4), and the `*` unpacks it into the two arguments `square_name` needs, giving "e2". The two names glue together into "e2e4". A promotion adds the new piece's letter in lowercase, as UCI always writes it: e7e8q.

### `move_from_uci()` in `moves.py`

**Where:** lines 64 to 69 of `moves.py`, inside `move_from_uci()`, in place of the stub below the docstring. The tests call it directly.

```python
48 | def move_from_uci(text: str, white_to_move: bool = True) -> Move:
49 |     """
     ...
62 |         The move the text describes.
63 |     """
64 +     from_square = parse_square(text[0:2])
65 +     to_square = parse_square(text[2:4])
66 +     promotion = None
67 +     if len(text) == 5:
68 +         promotion = text[4].upper() if white_to_move else text[4].lower()
69 +     return Move(from_square, to_square, promotion)
70 |
71 |
72 | def main():
```

**How it works:** `text[0:2]` is the first two characters, such as "e7", and `parse_square` turns them into a (row, col) tuple; `text[2:4]` is the landing square. A five-character move ends in a promotion letter. That letter becomes uppercase when White moves and lowercase when Black moves, so the new piece has the right piece color.
