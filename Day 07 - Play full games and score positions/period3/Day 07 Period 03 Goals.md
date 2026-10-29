# Day 7, Period 3: First brains and the GUI

Register `remus.bat` from the `student` folder in Lucas Chess again: Remus now plays greedy moves. Running `play_match.py` plays random Remus against greedy Remus.

## Learning objectives

By the end of this period, each student pair can:

- Choose a random move and a greedy move. **Measured by:** The brain tests pass: greedy Remus takes a hanging queen.
- Explain what the UCI commands do. **Measured by:** The student pair explains `position`, `go`, and `bestmove` from a printed conversation.
- Measure one brain against another. **Measured by:** Running `play_match.py` shows greedy Remus scoring more than random Remus.

## The files

New files this period:

- `play_match.py`
- `search.py`

Files that grow this period:

- `console_game.py`
- `test_game.py`
- `uci_engine.py`

Functions the student pairs write this period:

- `random_move()` in `search.py`
- `greedy_move()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `random_move()` in `search.py`

Picks any legal move at random. It is Remus's first brain: weak, but it proves the engine can play a whole game legally.

### `greedy_move()` in `search.py`

Picks the move that captures the most valuable piece, after shuffling so ties are broken at random. Greedy Remus beats random Remus, yet falls for any trap one move deep, which is why searching ahead comes next.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 1:00 to 1:10 | Slides: a brain is a function that picks a move. Random picks any legal move, and greedy takes the most valuable capture. |
| 1:10 to 1:40 | Student pairs write `random_move()` and `greedy_move()`. |
| 1:40 to 2:00 | The class reads the Day 5 `uci_engine.py` line by line. The teacher extends it with FEN positions and a choice of brains. |
| 2:00 to 2:15 | Student pairs register `remus.bat` from the `student` folder in Lucas Chess again and play greedy Remus. |
| 2:15 to 2:30 | Student pairs run `play_match.py`: random Remus against greedy Remus for 20 games, with the score at the end. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `random_move()` | 25 | 1 | `run_tests.py` |
| `search.py` | `greedy_move()` | 38 | 10 | `test_game.py::test_greedy_takes_the_queen` |

Lines to type in all: 11. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `random_move()` in `search.py`

**Where:** line 27 of `search.py`, inside `random_move()`, in place of the stub below the docstring. The tests call it directly.

```python
25 | def random_move(state: dict) -> Move:
26 |     """Return a random legal move."""
27 +     return random.choice(legal_moves(state))
28 |
29 |
30 | def capture_value(state: dict, move: Move) -> int:
```

**How it works:** `legal_moves` lists every legal move, and `random.choice` picks one. This is the simplest brain: it plays legal chess with no plan.

### `greedy_move()` in `search.py`

**Where:** lines 53 to 62 of `search.py`, inside `greedy_move()`, in place of the stub below the docstring. It is called by `main()` in `console_game.py`.

```python
38 | def greedy_move(state: dict) -> Move:
39 |     """
     ...
51 |         a random legal move.
52 |     """
53 +     moves = legal_moves(state)
54 +     random.shuffle(moves)  # Break ties between equal captures at random
55 +     best_move = moves[0]
56 +     best_value = capture_value(state, best_move)
57 +     for move in moves:
58 +         value = capture_value(state, move)
59 +         if value > best_value:
60 +             best_move = move
61 +             best_value = value
62 +     return best_move
63 |
64 |
65 | def main():
```

**How it works:** The function shuffles the legal moves, so equal captures are picked at random. It starts with the first move as the best and checks every move with `capture_value`. A move that captures more becomes the new best. A greedy brain grabs the biggest piece it can, without looking at the reply.
