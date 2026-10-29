# Day 10, Period 1: Science AI: hidden_peak.py

## Learning objectives

By the end of this period, each student pair can:

- Map the chess engine's loop onto a measurement problem. **Measured by:** The student pair fills in the chess-to-science table: legal moves, evaluation, and greedy move each have a science partner.
- Balance exploring and exploiting. **Measured by:** The student pair's `choose_next_measurement()` beats random guessing on the 100-grid benchmark, and the student pair names the explore weight it chose.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the teacher's `engines/instructor/11 GOLD - All enhancements` folder. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

New files this period:

- `hidden_peak.py`
- `test_hidden_peak.py`

Functions the student pairs write this period:

- `candidate_squares()` in `hidden_peak.py`
- `score_candidate()` in `hidden_peak.py`
- `choose_next_measurement()` in `hidden_peak.py`

In the `student` folder these functions raise `NotImplementedError` until a student pair writes them. In the `instructor` folder they are finished.

## The changes and why

### `candidate_squares()` in `hidden_peak.py`

Lists every square not measured yet. These are the "legal moves" of the science problem: the places the AI could measure next.

### `score_candidate()` in `hidden_peak.py`

Scores a square by its predicted value plus a bonus for being far from earlier readings. The first part exploits what the AI knows, and the second explores where it knows little.

### `choose_next_measurement()` in `hidden_peak.py`

Returns the candidate with the highest score, just as `greedy_move()` returns the best capture. The same generate, score, and choose loop now runs on a science problem.

Check the work with the tests: open `run_tests.py` in the `student` folder in VS Code and click the Run Python File button (the triangle at the top right of the editor). It runs every test in the folder. To run one file on its own, such as `hidden_peak.py`, open it and click the same button.

## The period step by step

| Time | Activity |
| --- | --- |
| 8:30 to 8:45 | Unplugged warm-up, "Find the hidden peak": a 10x10 grid hides a hot spot, and each student pair gets five measurements to find it. |
| 8:45 to 8:55 | Slides: the map from chess to science. Legal moves become squares not yet measured, and the evaluation becomes predicted value plus distance to the nearest reading. |
| 8:55 to 9:35 | Student pairs write `candidate_squares()`, `score_candidate()`, and `choose_next_measurement()` in `hidden_peak.py`. |
| 9:35 to 10:00 | Student pairs tune `explore_weight` and post their 100-grid benchmark average on the board, next to random guessing. |

## What you edit this period

Every other function is finished. Change only these, and only below each docstring:

| File | Function | Starts at line | Lines to type | Tests that check it |
| --- | --- | --- | --- | --- |
| `hidden_peak.py` | `candidate_squares()` | 85 | 6 | `test_hidden_peak.py::test_greedy_ai_measures_where_it_looks_hot` |
| `hidden_peak.py` | `score_candidate()` | 107 | 4 | `run_tests.py` |
| `hidden_peak.py` | `choose_next_measurement()` | 136 | 9 | `test_hidden_peak.py::test_greedy_ai_measures_where_it_looks_hot`, `test_hidden_peak.py::test_greedy_ai_beats_random_guessing` |

Lines to type in all: 19. Each stub is two comment lines that start with `# Day ...` and a `raise NotImplementedError` statement. Delete them and write the body in their place.

## The code you type

Each block below shows the code to type with a few lines around it, so you can find the spot. A line marked `+` is one you type; a line marked `|` is already in the file. Type the code without the number and the mark, and keep the indent shown. Lines that start with `#` are comments: they explain the code, and typing them is optional.

The number at the left of each line is its line number once the code is typed. When one file holds two functions to write, type the higher one first: until it is typed, the stub of a function lower down sits a few lines higher than these numbers say.

### `candidate_squares()` in `hidden_peak.py`

**Where:** lines 99 to 104 of `hidden_peak.py`, inside `candidate_squares()`, in place of the stub below the docstring. It is called by `random_strategy()` in `hidden_peak.py`, `expectimax_choice()` in `hidden_peak.py`.

```python
 85 | def candidate_squares(readings: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
 86 |     """
      ...
 97 |         The unmeasured squares, row by row.
 98 |     """
 99 +     squares = []
100 +     for row in range(SIZE):
101 +         for col in range(SIZE):
102 +             if (row, col) not in readings:
103 +                 squares.append((row, col))
104 +     return squares
105 |
106 |
107 | def score_candidate(
```

**How it works:** The two loops visit every square of the grid, row by row, and keep each one that has no reading yet. Like `legal_moves` in Remus, this lists the choices at the current step.

### `score_candidate()` in `hidden_peak.py`

**Where:** lines 130 to 133 of `hidden_peak.py`, inside `score_candidate()`, in place of the stub below the docstring. It is called by `expectimax_choice()` in `hidden_peak.py`.

```python
107 | def score_candidate(
108 |     square: tuple[int, int], readings: dict[tuple[int, int], int], explore_weight: float
      ...
128 |         nearest reading (explore).
129 |     """
130 +     nearest = math.inf  # Farther than any real square
131 +     for measured in readings:
132 +         nearest = min(nearest, math.dist(square, measured))
133 +     return predicted_value(square, readings) + explore_weight * nearest
134 |
135 |
136 | def choose_next_measurement(
```

**How it works:** `nearest` starts at infinity, and the loop lowers it to the distance from the square to the closest square already measured. The score adds two parts: `predicted_value`, how hot the square looks from the readings nearby (exploit), and `explore_weight` times that distance, a reward for trying somewhere new (explore).

### `choose_next_measurement()` in `hidden_peak.py`

**Where:** lines 140 to 148 of `hidden_peak.py`, inside `choose_next_measurement()`, in place of the stub below the docstring. The tests call it directly.

```python
136 | def choose_next_measurement(
137 |     readings: dict[tuple[int, int], int], explore_weight: float = EXPLORE_WEIGHT
138 | ) -> tuple[int, int]:
139 |     """Return the unmeasured square with the highest score, like greedy_move()."""
140 +     candidates = candidate_squares(readings)
141 +     best_square = candidates[0]
142 +     best_score = score_candidate(best_square, readings, explore_weight)
143 +     for square in candidates:
144 +         score = score_candidate(square, readings, explore_weight)
145 +         if score > best_score:
146 +             best_square = square
147 +             best_score = score
148 +     return best_square
149 |
150 |
151 | def random_strategy(readings: dict[tuple[int, int], int]) -> tuple[int, int]:
```

**How it works:** This is `greedy_move` again, aimed at a science problem. The function lists the unmeasured squares, scores each one, and keeps the best so far in a loop. The square with the highest score is the next one to measure.
