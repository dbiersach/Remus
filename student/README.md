# Student code

This folder is where you write Remus. It has one folder for each day of the
workshop, the same as `instructor/`, and each Day folder has four period folders,
`period1` to `period4`.

Each period folder starts with working code from the periods before. Its
`README.md` lists what you will learn and how you will show it, the files that are
new or growing, a paragraph on every change you make and why, and a table of the
functions left for you to write, with the line where each one starts. Each of those
functions keeps its name, its docstring, and its type hints. Its body is a stub:

```python
    # Day 1, period 4: write this function.
    # The docstring above says what it must do; the tests check it.
    raise NotImplementedError("Day 1 P4: write square_name()")
```

The first three periods of Day 1 hold Python labs instead: `python_setup.py`,
`python_strings.py`, and `python_lists.py`. In a lab file, each line that holds only
a `#` is one line for you to type.

## How to work on a function

1. Read the period's `README.md`, then the page for the file in `docs/scripts/`,
   such as `docs/scripts/board.md`.
2. Read the function's docstring. It says what the function must do.
3. Delete the two stub comments and the `raise` line, and write the body.
4. Run the tests from inside the period folder: `uv run pytest`.
5. Run the file itself, such as `uv run board.py`, and compare with the expected answers.

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
| 9 | 4 | `mate_solver.py` | `mating_move` |
| 10 | 1 | `hidden_peak.py` | `candidate_squares` |
| 10 | 1 | `hidden_peak.py` | `score_candidate` |
| 10 | 1 | `hidden_peak.py` | `choose_next_measurement` |
| 10 | 2 | `beam_time.py` | `estimate` |
| 10 | 2 | `beam_time.py` | `expected_wrong_calls` |
| 10 | 3 | `beam_time.py` | `gain` |
| 10 | 3 | `beam_time.py` | `choose_next_sample` |

On Day 9, periods 2 and 3, each pair also writes the functions of its color station in `Stations/`, listed in `docs/stations.md`.

The finished versions are in `instructor/`. Try on your own first.
