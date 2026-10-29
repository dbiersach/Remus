# Student Edit Plan: Who Writes What, Period by Period

`make_student_folders.py` writes this page from the code, so it always matches the folders. For every period it names the files that arrive or grow, which the teacher writes, and the functions the pairs write, which are stubs in each `student` folder and finished in the `instructor` folder beside it. Each period's goals file, such as `Day 03 Period 02 Goals.md`, has the same list with line numbers and the tests that check each function.

## Day 01 - Draw the board

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Welcome and setup | `python_setup_instructor.py` | None | The lab `python_setup.py` (6 lines) |
| P2 | Python lab 1: scripts, strings, ord and chr, f-strings | `python_strings_instructor.py` | None | The lab `python_strings.py` (13 lines) |
| P3 | Python lab 2: lists and nested lists | `python_lists_instructor.py` | None | The lab `python_lists.py` (25 lines) |
| P4 | board.py: the board and its square names | `board.py`, `run_tests.py`, `show_board.py`, `test_board.py` | None | `print_board()` in `board.py` (6 lines); `square_name()` in `board.py` (1 line); `parse_square()` in `board.py` (5 lines); `piece_at()` in `board.py` (2 lines) |

## Day 02 - Make and undo moves

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Python lab 3: functions, type hints, tuples, assert, pytest | `python_functions_instructor.py` | None | The lab `python_functions.py` (16 lines) |
| P2 | Python lab 4: dicts, dataclasses, aliasing, copying | `python_dicts_instructor.py` | None | The lab `python_dicts.py` (18 lines) |
| P3 | game_state.py and moves.py: a game state and a move record | `game_state.py`, `moves.py`, `test_make_move.py` | `board.py` | `is_white()` in `game_state.py` (1 line); `color_of()` in `game_state.py` (5 lines); `move_to_uci()` in `moves.py` (4 lines); `move_from_uci()` in `moves.py` (6 lines) |
| P4 | make_move.py: make and undo ordinary moves | `make_move.py` | `test_make_move.py` | `make_move()` in `make_move.py` (23 lines); `undo_move()` in `make_move.py` (9 lines) |

## Day 03 - Generate piece moves

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Python lab 5: while, break, direction tuples | `python_loops_instructor.py` | None | The lab `python_loops.py` (14 lines) |
| P2 | Jumping pieces: knights and kings | `move_generation.py`, `test_move_generation.py` | `show_board.py` | `king_moves()` in `move_generation.py` (1 line) |
| P3 | Sliding pieces: rooks, bishops, and queens | None | `move_generation.py`, `test_move_generation.py` | `slide()` in `move_generation.py` (14 lines) |
| P4 | Pawns | None | `move_generation.py`, `test_move_generation.py` | `pawn_pushes()` in `move_generation.py` (11 lines) |

## Day 04 - Keep only legal moves

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Python lab 6: modules, imports, __main__ | `python_modules_instructor.py` | None | The lab `python_modules.py` (11 lines) |
| P2 | Attacks | `attacks.py`, `test_legal_moves.py` | None | `piece_at_offsets()` in `attacks.py` (6 lines); `attacked_by_pawn()` in `attacks.py` (3 lines); `attacked_by_king()` in `attacks.py` (2 lines) |
| P3 | Check and the legal filter | `legal_moves.py` | `attacks.py`, `test_legal_moves.py` | `in_check()` in `attacks.py` (2 lines); `legal_moves()` in `legal_moves.py` (8 lines) |
| P4 | Practice positions | `demo_practice_positions_instructor.py` | `test_legal_moves.py` | The demo `demo_practice_positions.py` (14 lines) |

## Day 05 - Add castling, en passant, and promotion

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Python lab 7: sets, in, string replacement | `python_sets_instructor.py` | None | The lab `python_sets.py` (14 lines) |
| P2 | Castling | `test_special_moves.py` | `legal_moves.py`, `make_move.py` | `update_castling_rights()` in `make_move.py` (4 lines) |
| P3 | En passant and the double step | None | `make_move.py`, `move_generation.py`, `test_special_moves.py` | `en_passant_victim_square()` in `make_move.py` (1 line) |
| P4 | Promotion, and Remus plays in Lucas Chess | `demo_promotion_instructor.py`, `remus.bat`, `uci_engine.py` | `make_move.py`, `test_special_moves.py` | The demo `demo_promotion.py` (12 lines) |

## Day 06 - Count positions and read FEN

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Python lab 8: recursion | `python_recursion_instructor.py` | None | The lab `python_recursion.py` (11 lines) |
| P2 | Perft | `perft.py` | None | `perft()` in `perft.py` (8 lines) |
| P3 | Perft against python-chess, and bug hunt | `test_perft.py` | None | The fixes for the planted bugs in `bug_hunt/` (3 lines) |
| P4 | Python lab 9 and FEN | `fen.py`, `python_fen_fields_instructor.py`, `test_game.py` | `test_perft.py` | `fen_placement()` in `fen.py` (18 lines); `board_from_placement()` in `fen.py` (14 lines); the lab `python_fen_fields.py` (8 lines) |

## Day 07 - Play full games and score positions

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Ending the game | `game_end.py` | `fen.py`, `game_state.py`, `make_move.py`, `test_game.py` | `insufficient_material()` in `game_end.py` (18 lines); `game_result()` in `game_end.py` (12 lines) |
| P2 | SAN and the console game | `console_game.py`, `notation.py`, `python_input_output_instructor.py` | `test_game.py` | `parse_san()` in `notation.py` (5 lines); the lab `python_input_output.py` (16 lines) |
| P3 | First brains and the GUI | `play_match.py`, `search.py` | `console_game.py`, `test_game.py`, `uci_engine.py` | `random_move()` in `search.py` (1 line); `greedy_move()` in `search.py` (10 lines) |
| P4 | What makes a position good? Material and piece-square tables | `evaluation.py`, `test_search.py` | None | `material()` in `evaluation.py` (10 lines) |

## Day 08 - Search ahead with alpha-beta

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Minimax, negamax, and mates | None | `console_game.py`, `search.py`, `test_search.py`, `uci_engine.py` | `negamax()` in `search.py` (17 lines) |
| P2 | Python lab 11 and alpha-beta | `compare_search.py`, `mate_puzzles.epd`, `python_sorting_instructor.py` | `search.py`, `test_search.py` | `alpha_beta()` in `search.py` (16 lines); the lab `python_sorting.py` (19 lines) |
| P3 | The horizon effect and quiescence | None | `search.py`, `test_search.py` | `quiescence()` in `search.py` (15 lines) |
| P4 | Move ordering | `move_ordering.py` | `search.py`, `test_search.py` | `mvv_lva_score()` in `move_ordering.py` (8 lines) |

## Day 09 - Add the clock and build enhanced engines

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Iterative deepening, the clock, and UCI info | None | `console_game.py`, `search.py`, `test_game.py`, `test_search.py`, `uci_engine.py` | `think()` in `search.py` (17 lines) |
| P2 | Python lab 12 and the color versions | `python_caches_instructor.py` | None | The lab `python_caches.py` (7 lines); their color version's functions, in the table below |
| P3 | Color versions: test and measure | None | None | Their color version's functions, in the table below |
| P4 | Color battles | `demo_results_instructor.py` | None | The demo `demo_results.py` (13 lines) |

## Day 10 - Solve a science problem using chess AI

| Period | Title | New files | Files that grow | Pairs write |
| --- | --- | --- | --- | --- |
| P1 | Science AI: hidden_peak.py | `hidden_peak.py`, `run_tests.py`, `test_hidden_peak.py` | None | `candidate_squares()` in `hidden_peak.py` (6 lines); `score_candidate()` in `hidden_peak.py` (4 lines); `choose_next_measurement()` in `hidden_peak.py` (9 lines) |
| P2 | The phase hunt: score a guess, and the greedy agent | `phase_hunt.py`, `test_phase_hunt.py` | None | `score()` in `phase_hunt.py` (11 lines); `greedy_phases()` in `phase_hunt.py` (17 lines) |
| P3 | The phase hunt: search every set, and verify | None | `phase_hunt.py`, `test_phase_hunt.py` | `search()` in `phase_hunt.py` (13 lines) |
| P4 | Science results, take-home, and wrap-up | None | None | Nothing: a demo or teacher code |

## Color versions (Day 9, periods 2 and 3)

Each pair writes the functions of one color version in `period2/student/engines`.

| Color version | Pairs write |
| --- | --- |
| 10 RED - Transposition table | `store()` in `transposition_table.py` (3 lines); `probe()` in `transposition_table.py` (11 lines); `test_transposition_table_bounds()` in `test_upgrades.py` (13 lines) |
| 08 GREEN - Opening book | `load_book()` in `opening_book.py` (24 lines); `book_move()` in `opening_book.py` (2 lines) |
| 09 BLUE - Killer moves | `remember_killer()` in `search.py` (6 lines); `order_moves()` in `move_ordering.py` (16 lines); `test_killers_keep_two_quiet_moves()` in `test_upgrades.py` (5 lines) |
| 04 PINK - Principal variation search | `search_later_move()` in `search.py` (6 lines); `test_pvs_search_agrees_with_alpha_beta()` in `test_upgrades.py` (7 lines); `test_a_null_window_answers_only_better_or_not()` in `test_upgrades.py` (5 lines) |
| 02 YELLOW - Draw sense | `is_draw_in_search()` in `search.py` (2 lines); `test_draw_sense_search_agrees_with_alpha_beta()` in `test_upgrades.py` (7 lines); `test_a_repeated_position_is_a_draw()` in `test_upgrades.py` (5 lines); `test_the_fifty_move_limit_is_a_draw()` in `test_upgrades.py` (2 lines) |
| 07 PURPLE - Pawn structure | `pawn_structure()` in `evaluation.py` (29 lines) |
| 03 CYAN - Mating bonus | `mating_bonus()` in `evaluation.py` (24 lines) |
| 05 ORANGE - Null-move pruning | `make_null_move()` in `search.py` (5 lines); `undo_null_move()` in `search.py` (3 lines); `test_null_move_and_undo_restore_the_state()` in `test_upgrades.py` (6 lines); `test_null_move_search_saves_work_and_keeps_the_state()` in `test_upgrades.py` (9 lines) |
| 06 BROWN - Late move reductions | `reduction()` in `search.py` (3 lines); `test_only_late_quiet_moves_are_reduced()` in `test_upgrades.py` (6 lines); `test_reduced_search_saves_work_and_keeps_the_state()` in `test_upgrades.py` (9 lines) |
| 01 GRAY - King safety | `king_safety()` in `evaluation.py` (24 lines) |
