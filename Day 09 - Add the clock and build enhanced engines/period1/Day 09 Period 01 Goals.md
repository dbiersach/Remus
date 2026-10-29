# Day 9, Period 1: Iterative deepening, the clock, and UCI info

## Learning objectives

By the end of this period, each student pair can:

- Search deeper one step at a time until the clock runs out. **Measured by:** `test_think_respects_its_time` passes, and Remus never loses on time in Lucas Chess.
- Report the search to the GUI with `info` lines. **Measured by:** Lucas Chess shows Remus's depth, score, and best line for each depth that `think()` finishes.

## The files

Files that grow this period:

- `console_game.py`
- `search.py`
- `test_game.py`
- `test_search.py`
- `uci_engine.py`

Functions the student pairs write this period:

- `think()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `think()` in `search.py`

Searches depth 1, then depth 2, then depth 3, and keeps the best move of the deepest search that finished. When the clock runs out in the middle of a search, the unfinished search is thrown away. Each finished depth also puts its best move first for the next depth, so alpha-beta cuts off more. This is iterative deepening, and it lets Remus play on any clock.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Slides: the clock. The teacher reads `go movetime`, `wtime`, and `btime`, turns them into a thinking time, and writes `format_info()`. |
| 8:45 to 9:25 | Student pairs write `think()` (the iterative deepening loop): depth 1, then 2, then 3, keeping the best move of the deepest search that finished. |
| 9:25 to 9:35 | Show and choose for `think()`. The chosen code makes Remus-WHITE, the Remus with none of the enhancements and the starting point of every color version. |
| 9:35 to 10:00 | The class watches Remus-WHITE play a 5-minute game against Stockfish at 1500 Elo in Lucas Chess and reads the `info` lines as it thinks. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `think()` | 427 | 17 | `test_search.py::test_think_respects_its_time` |

Lines to type in all: 17. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `think()` in `search.py`

**Where:** lines 447 to 463 of `search.py`, inside `think()`, in place of the stub below the docstring. It is called by `think_move()` in `search.py`, `main()` in `uci_engine.py`.

```text
427 | def think(state: dict, seconds: float = 2.0, max_depth: int = 64, report=None) -> Move:
      ...
445 |         The best move of the deepest search that finished.
446 |     """
447 +     info = SearchInfo(deadline=time.perf_counter() + seconds)
448 +     moves = legal_moves(state)
449 +     best = order_moves(moves, state["board"])[0]
450 +     for depth in range(1, max_depth + 1):
451 +         try:
452 +             score, pv = alpha_beta_with_quiescence(
453 +                 state, depth, 0, -MATE_SCORE - 1, MATE_SCORE + 1, info, best
454 +             )
455 +         except SearchTimeout:
456 +             break  # Keep the best move of the last depth that finished
457 +         if pv:
458 +             best = pv[0]
459 +         if report is not None:
460 +             report(format_info(depth, score, info.nodes, pv))
461 +         if abs(score) > MATE_SCORE - 1000 or len(moves) == 1:
462 +             break  # A forced mate or a single legal move needs no deeper search
463 +     return best
464 |
465 |
466 | def think_move(state: dict) -> Move:
```
