# Day 7, Period 3: First brains and the GUI

Register `remus.bat` from the `student` folder in Lucas Chess again: Remus now plays greedy moves. Running `play_match.py` plays random Remus against greedy Remus.

## Learning objectives

By the end of this period, each pair can:

- Choose a random move and a greedy move. **Measured by:** The brain tests pass: greedy Remus takes a hanging queen.
- Explain what the UCI commands do. **Measured by:** The pair explains `position`, `go`, and `bestmove` from a printed conversation.
- Measure one brain against another. **Measured by:** Running `play_match.py` shows greedy Remus scoring more than random Remus.

## The files

New files this period:

- `play_match.py`
- `search.py`

Files that grow this period:

- `console_game.py`
- `test_game.py`
- `uci_engine.py`

Functions the pairs write this period:

- `random_move()` in `search.py`
- `greedy_move()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `random_move()` in `search.py`

Picks any legal move at random. It is Remus's first brain: weak, but it proves the engine can play a whole game legally.

### `greedy_move()` in `search.py`

Picks the move that captures the most valuable piece, after shuffling so ties are broken at random. Greedy Remus beats random Remus, yet falls for any trap one move deep, which is why searching ahead comes next.

Check the work with the tests: open a terminal in VS Code inside the `student` folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:10 | Slides: a brain is a function that picks a move. Random picks any legal move, and greedy takes the most valuable capture. |
| 1:10 to 1:40 | Pairs write `random_move()` and `greedy_move()`. |
| 1:40 to 2:00 | The class reads the Day 5 `uci_engine.py` line by line. The teacher extends it with FEN positions and a choice of brains. |
| 2:00 to 2:15 | Pairs register `remus.bat` from the `student` folder in Lucas Chess again and play greedy Remus. |
| 2:15 to 2:30 | Pairs run `play_match.py`: random Remus against greedy Remus for 20 games, with the score at the end. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `random_move()` | 25 | 1 | `uv run pytest` |
| `search.py` | `greedy_move()` | 40 | 10 | `test_game.py::test_greedy_takes_the_queen` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
