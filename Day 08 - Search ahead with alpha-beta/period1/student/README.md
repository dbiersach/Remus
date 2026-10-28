# Day 8, Period 1: Minimax, negamax, and mates

## Learning objectives

By the end of this period, each pair can:

- Back up scores through a tree with minimax. **Measured by:** Paper minimax: the pair's best move matches `minimax()` on the same tree.
- Score checkmate so that a faster mate wins. **Measured by:** The negamax tests pass: `negamax()` finds every mate in 1, and the root state is unchanged after each search.

## The files

Files that grow this period:

- `console_game.py`
- `search.py`
- `test_search.py`
- `uci_engine.py`

Functions the pairs write this period:

- `negamax()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `negamax()` in `search.py`

Looks `depth` moves ahead. At depth 0 it returns the evaluation; with no legal moves it returns a mate score or 0 for stalemate. Otherwise it makes each move, asks for the opponent's score of the position, and flips its sign, because a position good for the opponent is bad for the mover. The best of those flipped scores is the score of the position. This one idea, calling itself on every reply, is the heart of every chess engine.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `board.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).

## What you edit this period

Every other function in this folder is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `negamax()` | 114 | 17 | `test_search.py::test_negamax_finds_mate_in_one`, `test_search.py::test_minimax_and_negamax_agree`, `test_search.py::test_stalemate_scores_zero` |

Lines to type in all: 17. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.
