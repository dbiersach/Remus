# Day 10, Period 1: Science AI: hidden_peak.py

## Learning objectives

By the end of this period, each pair can:

- Map the chess engine's loop onto a measurement problem. **Measured by:** The pair fills in the chess-to-science table: legal moves, evaluation, and greedy move each have a science partner.
- Balance exploring and exploiting. **Measured by:** The pair's `choose_next_measurement()` beats random guessing on the 100-grid benchmark, and the pair names the explore weight it chose.

## The files

The engine for Day 10 is Remus-GOLD, the finished Remus with all ten enhancements, in the `Remus/11 GOLD - All enhancements` folder beside the Day folders. Lucas Chess runs its `remus.bat`, and its `estimate_elo.py` rates it against Stockfish. This folder holds only the science files, which never import the engine.

New files this period:

- `hidden_peak.py`
- `test_hidden_peak.py`

Functions the pairs write this period:

- `candidate_squares()` in `hidden_peak.py`
- `score_candidate()` in `hidden_peak.py`
- `choose_next_measurement()` in `hidden_peak.py`

In `student/` these functions raise `NotImplementedError` until a pair writes them. In `instructor/` they are finished.

## The changes and why

### `candidate_squares()` in `hidden_peak.py`

Lists every square not measured yet. These are the "legal moves" of the science problem: the places the AI could measure next.

### `score_candidate()` in `hidden_peak.py`

Scores a square by its predicted value plus a bonus for being far from earlier readings. The first part exploits what the AI knows, and the second explores where it knows little.

### `choose_next_measurement()` in `hidden_peak.py`

Returns the candidate with the highest score, just as `greedy_move()` returns the best capture. The same generate, score, and choose loop now runs on a science problem.

Check the work with the tests: open a terminal in VS Code inside this folder and type `uv run pytest`. To run one file on its own, such as `hidden_peak.py`, open it in VS Code and click the Run Python File button (the triangle at the top right of the editor).
