# Student code

This folder is where you write Remus. It has one folder for each day of the
workshop, the same as `instructor/`, and each Day folder has four period folders,
`period1` to `period4`.

Each period folder starts with working code from the periods before. Its
`README.md` names the files that are new or growing, and the functions left for
you to write. Each of those functions keeps its name, its docstring, and its
type hints. Its body is one line:

```python
raise NotImplementedError("Day 1 P4: write square_name()")
```

## How to work on a function

1. Open the page for the file in `docs/scripts/`, such as `docs/scripts/board.md`.
2. Read the function's docstring. It says what the function must do.
3. Delete the `raise` line and write the body.
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
| 2 | 4 | `make_move.py` | `undo_move` |
| 2 | 4 | `make_move.py` | `state_snapshot` |
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
| 7 | 1 | `fen.py` | `fen_placement` |
| 7 | 1 | `fen.py` | `board_from_placement` |
| 7 | 2 | `game_end.py` | `insufficient_material` |
| 7 | 2 | `game_end.py` | `game_result` |
| 7 | 3 | `notation.py` | `parse_san` |
| 7 | 4 | `search.py` | `random_move` |
| 7 | 4 | `search.py` | `greedy_move` |
| 8 | 1 | `evaluation.py` | `material` |
| 9 | 2 | `search.py` | `capture_moves` |
| 9 | 3 | `move_ordering.py` | `mvv_lva_score` |
| 9 | 4 | `search.py` | `format_info` |
| 10 | 1 | `mate_solver.py` | `mating_move` |
| 10 | 2 | `hidden_peak.py` | `candidate_squares` |
| 10 | 2 | `hidden_peak.py` | `score_candidate` |
| 10 | 2 | `hidden_peak.py` | `choose_next_measurement` |

The finished versions are in `instructor/`. Try on your own first.
