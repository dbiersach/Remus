# Student guide

You write Remus in the `student` folders. The top of the Remus folder has one
folder for each day of the workshop, and each Day folder has four period folders,
`period1` to `period4`. Each period folder holds a `student` folder, where you work,
and an `instructor` folder with the finished code. The syllabus at the top of each
Day folder, such as `Day 01 Syllabus.md`, shows the whole day: what you will learn, and what happens in each
period, from 8:30 to 4:30.

Each `student` folder starts with working code from the periods before. The goals
file beside it, such as `Day 03 Period 02 Goals.md`, lists what you will learn and how you will show it, the files that are
new or growing, a paragraph on every change you make and why, the steps of the
period with their times, and a table of the
functions left for you to write, with the line where each one starts. Each of those
functions keeps its name, its docstring, and its type hints. Its body is a stub:

```python
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write square_name()")
```

Thirteen periods hold a Python lab (`python_*.py`), such as `python_lists.py` on Day 1
or `python_recursion.py` on Day 6, and three hold a demo (`demo_*.py`), such as
`demo_promotion.py` on Day 5. In a lab or demo file, each line that holds only a `#`
is one line for you to type. On Day 6, period 3 the `bug_hunt` folder holds a copy
of Remus with three planted bugs for you to find and fix.

## How to work on a function

1. Read the period's goals file, then the page for the file in `misc/docs/code/`,
   such as `misc/docs/code/board.md`.
2. Read the function's docstring. It says what the function must do.
3. Delete the two stub comments and the `raise` line, and write the body.
4. Run the tests from inside the `student` folder: `uv run pytest`.
5. Run the file itself, such as `board.py`, with VS Code's Run Python File button,
   and compare with the expected answers.

A test that fails with `NotImplementedError` points to a function you have not
written yet.

## The functions you write

| Day | Period | File | Function |
| --- | --- | --- | --- |
| 1 | 4 | `board.py` | `print_board` |
| 1 | 4 | `board.py` | `square_name` |
| 1 | 4 | `board.py` | `parse_square` |
| 1 | 4 | `board.py` | `piece_at` |
| 2 | 3 | `game_state.py` | `is_white` |
| 2 | 3 | `game_state.py` | `color_of` |
| 2 | 3 | `moves.py` | `move_to_uci` |
| 2 | 3 | `moves.py` | `move_from_uci` |
| 2 | 4 | `make_move.py` | `make_move` |
| 2 | 4 | `make_move.py` | `undo_move` |
| 3 | 2 | `move_generation.py` | `king_moves` |
| 3 | 3 | `move_generation.py` | `slide` |
| 3 | 4 | `move_generation.py` | `pawn_pushes` |
| 4 | 2 | `attacks.py` | `attacked_by_knight` |
| 4 | 2 | `attacks.py` | `attacked_by_pawn` |
| 4 | 2 | `attacks.py` | `attacked_by_king` |
| 4 | 3 | `attacks.py` | `in_check` |
| 4 | 3 | `legal_moves.py` | `legal_moves` |
| 5 | 2 | `make_move.py` | `update_castling_rights` |
| 5 | 3 | `make_move.py` | `en_passant_victim_square` |
| 6 | 2 | `perft.py` | `perft` |
| 6 | 4 | `fen.py` | `fen_placement` |
| 6 | 4 | `fen.py` | `board_from_placement` |
| 7 | 1 | `game_end.py` | `insufficient_material` |
| 7 | 1 | `game_end.py` | `game_result` |
| 7 | 2 | `notation.py` | `parse_san` |
| 7 | 3 | `search.py` | `random_move` |
| 7 | 3 | `search.py` | `greedy_move` |
| 7 | 4 | `evaluation.py` | `material` |
| 8 | 1 | `search.py` | `negamax` |
| 8 | 2 | `search.py` | `alpha_beta` |
| 8 | 3 | `search.py` | `quiescence` |
| 8 | 4 | `move_ordering.py` | `mvv_lva_score` |
| 9 | 1 | `search.py` | `think` |
| 10 | 1 | `hidden_peak.py` | `candidate_squares` |
| 10 | 1 | `hidden_peak.py` | `score_candidate` |
| 10 | 1 | `hidden_peak.py` | `choose_next_measurement` |
| 10 | 2 | `phase_hunt.py` | `score` |
| 10 | 2 | `phase_hunt.py` | `greedy_phases` |
| 10 | 3 | `phase_hunt.py` | `search` |

On Day 9, periods 2 and 3, each pair also writes the functions of its color version
in the Day 9 `period2/student/engines` folder, listed in
[`remus_versions.md`](../engines/remus_versions.md).

The finished versions are in the `instructor` folder beside each `student` folder.
Try on your own first.
