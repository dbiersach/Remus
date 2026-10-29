# Day 8, Period 2: Python lab 11 and alpha-beta

## Learning objectives

By the end of this period, each student pair can:

- Explain an alpha-beta cutoff. **Measured by:** "Fewest flips": the student pair reaches the right move while turning fewer cards than the whole tree.
- Show that alpha-beta keeps the answer and saves work. **Measured by:** The `alpha_beta` tests pass, and running `compare_search.py` prints the same scores as negamax with fewer nodes.
- Keep a list in order with `insert()`, start a best value at minus infinity, and time code. **Measured by:** `python_sorting.py` puts the queen first, finds the best victim, and prints the run time of `perft(3)`.

## The files

The lab is `python_sorting.py` in the `student` folder, with the answers in `python_sorting_instructor.py` in the `instructor` folder beside it. Open `python_sorting.py` in VS Code and run it with the Run Python File button (the triangle at the top right of the editor).

New files this period:

- `compare_search.py`
- `mate_puzzles.epd`

Files that grow this period:

- `search.py`
- `test_search.py`

Functions the student pairs write this period:

- `alpha_beta()` in `search.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

The student pairs fill in the blanks of `python_sorting.py`. Each `#` line in the student file stands for one line to type, and the answer sits on the same line of `python_sorting_instructor.py`.

Part #1 sorts captures by the value of the piece they take: each new piece steps past every piece worth at least as much and is inserted there. `order_moves()` in period 4 sorts moves the same way.

Part #2 starts the best value at minus infinity, so the first real value always replaces it. `alpha_beta()` starts its alpha the same way, below any score a move can get.

Part #3 times `perft(3)` with `time.perf_counter()`, the clock that `compare_search.py` uses to show how much time alpha-beta saves.

### `alpha_beta()` in `search.py`

Does the same work as negamax, but carries two numbers: alpha, the score the mover is already sure of, and beta, the score the opponent will not allow. As soon as one move scores beta or more, the opponent would never let this position happen, so the other moves are skipped. The answer is the same as negamax, and far fewer positions are visited, so Remus can look deeper in the same time.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `board.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 10:30 to 10:45 | Unplugged warm-up, "Fewest flips": the same tree as face-down cards. Student pairs turn a card only when the answer could still change. |
| 10:45 to 10:55 | Slides: alpha and beta, and the cutoff. |
| 10:55 to 11:25 | Student pairs write `alpha_beta()` beside `negamax()` and run `compare_search.py`: the same score, fewer nodes. |
| 11:25 to 12:00 | Student pairs work through `python_sorting.py`: `insert()` puts the biggest victim first, `float("inf")`, and timing a perft run. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `search.py` | `alpha_beta()` | 197 | 16 | `test_search.py::test_alpha_beta_matches_negamax_with_fewer_positions` |

Lines to type in all: 16. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `alpha_beta()` in `search.py`

**Where:** lines 226 to 241 of `search.py`, inside `alpha_beta()`, in place of the stub below the docstring. It is called by `main()` in `compare_search.py`.

```python
197 | def alpha_beta(
198 |     state: dict, depth: int, ply: int, alpha: int, beta: int, info: SearchInfo
      ...
224 |         The same score negamax returns at this depth.
225 |     """
226 +     info.nodes += 1
227 +     if depth == 0:
228 +         return evaluate(state)
229 +     moves = legal_moves(state)
230 +     if not moves:
231 +         return -(MATE_SCORE - ply) if in_check(state, state["turn"]) else 0
232 +     for move in moves:
233 +         undo = make_move(state, move)
234 +         try:
235 +             score = -alpha_beta(state, depth - 1, ply + 1, -beta, -alpha, info)
236 +         finally:
237 +             undo_move(state, undo)
238 +         if score >= beta:
239 +             return score  # Cutoff: the opponent will not allow this
240 +         alpha = max(alpha, score)
241 +     return alpha
242 |
243 |
244 | def main():
```

**How it works:** The body is negamax with a window. `alpha` is the best score this side is already sure of, and `beta` is the most the opponent will allow. Each child is searched with the window flipped, `-beta` and `-alpha`. A score at or above `beta` is a cutoff: the opponent will never let the game reach this position, so the remaining moves are skipped. Otherwise a better score raises `alpha`, and the function returns `alpha`.

### Part #1 - insert() Puts the Biggest Victim First

```python
26 |     victims = ["p", "r", "q", "n"]
27 |     # Step past every piece worth at least as much, then insert the new piece there
28 +     ordered = []
29 +     for piece in victims:
30 +         value = victim_value(piece)
31 +         place = 0
32 +         while place < len(ordered) and victim_value(ordered[place]) >= value:
33 +             place += 1
34 +         ordered.insert(place, piece)
35 +     print(f"Victims, best first: {ordered}  (expected ['q', 'r', 'n', 'p'])")
36 |
37 |     print("Part #2 - Start the Best at Minus Infinity")
```

**How it works:** The list `ordered` starts empty. For each victim the `while` loop steps past every piece worth at least as much, and `insert(place, piece)` puts the new piece there. The list stays sorted from the most valuable down after each insert.

### Part #2 - Start the Best at Minus Infinity

```python
37 |     print("Part #2 - Start the Best at Minus Infinity")
38 |     # Every real value beats minus infinity, so the first victim always becomes best
39 +     best_value = -float("inf")
40 |     best_piece = ""
41 +     for piece in victims:
42 +         if victim_value(piece) > best_value:
43 +             best_value = victim_value(piece)
44 +             best_piece = piece
45 +     print(f"Best victim: {best_piece}, worth {best_value}  (expected q, worth 9)")
46 |
47 |     print("Part #3 - Time a perft Run")
```

**How it works:** `-float("inf")` is minus infinity, a number smaller than any real value. Starting the best there means the first victim always replaces it, so no special case is needed.

### Part #3 - Time a perft Run

```python
46 |
47 |     print("Part #3 - Time a perft Run")
48 +     start = time.perf_counter()
49 +     count = perft(new_game(), 3)
50 +     elapsed = time.perf_counter() - start
51 +     print(f"perft(3) = {count:,}  (expected 8,902)")
52 +     print(f"Total run time (sec): {elapsed:.3f}")
53 |
54 |
```

**How it works:** `time.perf_counter()` reads a precise clock. Reading it before and after `perft` and subtracting gives the seconds the count took.

## What you edit in the lab

Open `python_sorting.py` in the `student` folder. Under each `Part` heading, every line that holds only a `#` is one line of code to type. Replace the `#` with the code, keeping its indent. The printed text next to each step says what the line must produce.

Lines to type in all: 19. Check the work by running `python_sorting.py` with the Run Python File button (the triangle at the top right of the editor), and compare each printed result with the expected value beside it.
