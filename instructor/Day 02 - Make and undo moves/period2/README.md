# Day 2, Period 2: Python lab 4: dicts, dataclasses, aliasing, copying

## Learning objectives

By the end of this period, each pair can:

- Store named facts in a dict and read them back. **Measured by:** The lab's state dict answers whose turn it is and the castling rights.
- Explain aliasing: two names for one list. **Measured by:** The pair predicts, then shows, that `b2 = board` changes both boards, and that a copy does not.
- Describe a record with a `dataclass`. **Measured by:** The pair makes a small `dataclass` and prints one of its fields.

## The files

The lab is `python_dicts.py` in `student/`, with the answers in `python_dicts_instructor.py` in `instructor/`. Run it with `uv run python_dicts.py`.

The Remus code here is the same as at the end of the period before.

## The changes and why

The pairs fill in the blanks of `python_dicts.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_dicts_instructor.py`.

Part #1 keeps the facts of a game in a dict and reads them by key, the way `new_game()` in `game_state.py` holds the board, the side to move, and the castling rights.

Part #2 shows aliasing: `b2 = board` makes a second name for the same board, so a pawn put on e4 through `b2` shows up in `board` too. This is the most common surprise in a chess program that changes its board in place.

Part #3 makes a real copy with `deepcopy()`, which copies every row. The copy changes alone, and `==` compares the two boards square by square.

Part #4: you write a `dataclass` with two fields and print one of them. Remus's `Move` in `moves.py` is the same record with a third field for the promotion piece.

Check the work from inside this folder with `uv run pytest`, and run any file on its own, such as `uv run board.py`.
