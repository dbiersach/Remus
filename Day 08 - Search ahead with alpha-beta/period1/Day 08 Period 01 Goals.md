# Day 8, Period 1: Minimax, negamax, and mates

## Learning objectives

By the end of this period, each student pair can:

- Back up scores through a tree with minimax. **Measured by:** Paper minimax: the student pair's best move matches `minimax()` on the same tree.
- Score checkmate so that a faster mate wins. **Measured by:** The negamax tests pass: `negamax()` finds every mate in 1, and the root state is unchanged after each search.

## The files

Files that grow this period:

- `console_game.py`
- `search.py`
- `test_search.py`
- `uci_engine.py`

Functions the student pairs write this period:

- `negamax()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `negamax()` in `search.py`

Looks `depth` moves ahead. At depth 0 it returns the evaluation; with no legal moves it returns a mate score or 0 for stalemate. Otherwise it makes each move, asks for the opponent's score of the position, and flips its sign, because a position good for the opponent is bad for the mover. The best of those flipped scores is the score of the position. This one idea, calling itself on every reply, is the heart of every chess engine.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Unplugged warm-up, "Paper minimax": student pairs back up max and min on a printed two-ply tree and circle the best move. A seven-student human tree can act it out at the front of the room. |
| 8:45 to 9:00 | The teacher writes `minimax()` to depth 2 with a node counter, and student pairs compare its answer with their worksheets. |
| 9:00 to 9:10 | Slides: negamax, the same search in one function: flip the sign, wrap make and undo in `try/finally`, and score checkmate as `-(MATE_SCORE - ply)`. |
| 9:10 to 9:50 | Student pairs write `negamax()` until the tests show it agrees with minimax and leaves the root state unchanged. |
| 9:50 to 10:00 | Show and choose for `negamax()`. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `negamax()` | 114 | 17 | `test_search.py::test_negamax_finds_mate_in_one`, `test_search.py::test_minimax_and_negamax_agree`, `test_search.py::test_stalemate_scores_zero` |

Lines to type in all: 17. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `negamax()` in `search.py`

**Where:** lines 139 to 155 of `search.py`, inside `negamax()`, in place of the stub below the docstring. It is called by `best_move()` in `search.py`.

```python
114 | def negamax(state: dict, depth: int, ply: int, info: SearchInfo) -> int:
115 |     """
      ...
137 |         The score for the side to move.
138 |     """
139 +     info.nodes += 1
140 +     if depth == 0:
141 +         return evaluate(state)
142 +     moves = legal_moves(state)
143 +     if not moves:
144 +         if in_check(state, state["turn"]):
145 +             return -(MATE_SCORE - ply)  # Checkmated: worse the sooner it happens
146 +         return 0  # Stalemate
147 +     best = -MATE_SCORE - 1
148 +     for move in moves:
149 +         undo = make_move(state, move)
150 +         try:
151 +             score = -negamax(state, depth - 1, ply + 1, info)
152 +         finally:
153 +             undo_move(state, undo)
154 +         best = max(best, score)
155 +     return best
156 |
157 |
158 | def best_move(state: dict, depth: int) -> tuple[Move, int, SearchInfo]:
```

**How it works:** Each call counts one node. At depth 0 the function stops looking ahead and returns `evaluate`. With no legal moves the game is over: a checkmated side gets a large negative score, worse the sooner the mate (`ply` counts how deep the search is), and stalemate is 0. Otherwise every move is made, searched one ply less deep, and undone; `try` and `finally` undo the move even if the search stops early. The minus sign turns the opponent's score into ours, and `best` keeps the highest.
