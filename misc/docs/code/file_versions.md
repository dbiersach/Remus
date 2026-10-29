# File Versions: Which Period Changes Which File

Each period folder holds one version of each file. The folder path is the version:
the `make_move.py` in `Day 05 - Add castling, en passant, and promotion/period2` is
the version with castling and without en passant. A file that a period does not
change is copied forward as it is. `period4` of each day is the finished code of that
day, and `make_period_folders.py` builds `period1` to `period3` from it.

Table 1 follows each file through the course. Table 2 lists, for each period, the
files that are new or changed. Test files are listed in Table 2 only. "D5 P2" means
Day 5, Period 2.

## Table 1: By file

| File | First arrives | How it changes |
| --- | --- | --- |
| `board.py` | D1 P4: the 8x8 board, printing, square names | D2 P3: adds `set_piece()` to write a square |
| `show_board.py` | D1 P4: draws the board as a picture in the browser | D3 P2: draws an arrow for each move with `show_moves()` |
| `game_state.py` | D2 P3: the state dict, piece colors | D7 P1: adds `position_key()` and the position history |
| `moves.py` | D2 P3: the `Move` record and UCI text | No changes |
| `make_move.py` | D2 P4: make and undo quiet moves and captures | D5 P2: castling and castling rights. D5 P3: en passant. D5 P4: promotion. D7 P1: records each position in `history` and removes it on undo |
| `move_generation.py` | D3 P2: knight and king jumps | D3 P3: sliding pieces. D3 P4: pawns, promotion choices, `pseudo_legal_moves()`. D5 P3: en passant captures |
| `attacks.py` | D4 P2: attacked squares, two versions | D4 P3: `find_king()` and `in_check()` |
| `legal_moves.py` | D4 P3: the make, test, undo filter | D5 P2: adds castling moves |
| `uci_engine.py` | D5 P4: a first engine for Lucas Chess that plays random legal moves | D7 P3: every UCI command, FEN positions, random and greedy brains. D8 P1: negamax brain. D9 P1: clock and thinking time. Remus-GOLD: plays book moves first |
| `remus.bat` | D5 P4: starts Remus for Lucas Chess | No changes |
| `perft.py` | D6 P2: counts positions, `divide()` | No changes |
| `fen.py` | D6 P4: FEN in and out | D7 P1: starts the position history |
| `game_end.py` | D7 P1: mate, stalemate, draws | No changes |
| `notation.py` | D7 P2: SAN in and out | No changes |
| `console_game.py` | D7 P2: two people play in SAN | D7 P3: Remus plays greedy moves. D8 P1: Remus plays with negamax. D9 P1: Remus thinks on a clock. Remus-GOLD: Remus plays book moves first |
| `search.py` | D7 P3: random and greedy brains | D8 P1: minimax, negamax, and mate scores. D8 P2: alpha-beta. D8 P3: quiescence. D8 P4: move ordering, check extension, the clock. D9 P1: iterative deepening and `info` lines. Remus-GOLD: `upgraded_search()` with memory, killers, PVS, draw sense, null moves, late move reductions |
| `play_match.py` | D7 P3: two brains play a match | No changes |
| `evaluation.py` | D7 P4: material and piece-square tables | Remus-GOLD: pawn structure, the mating bonus, king safety |
| `compare_search.py` | D8 P2: negamax against alpha-beta | No changes |
| `move_ordering.py` | D8 P4: captures first by MVV-LVA | Remus-GOLD: killer moves |
| `transposition_table.py` | Remus-GOLD: remembers searched positions | Last day |
| `opening_book.py`, `opening_book.txt` | Remus-GOLD: plays known openings | Last day |
| `hidden_peak.py` | D10 P1: Science AI, the hidden peak | Last day |
| `phase_hunt.py` | D10 P2: the phase hunt: the evaluation `score()` and the greedy agent | D10 P3: the tree search `search()` and the benchmark that compares it with greedy |
| `estimate_elo.py` | Remus-GOLD: measures the Elo rating of Remus against Stockfish | Last day |
| `period2/engines/version_match.py` | D9 P2: plays one color version against Remus-WHITE, the Day 9 Remus with no enhancements, from 32 openings | Last day |
| `misc/scripts/version_league.py` | D10 P4: ranks all 12 Remus versions from every color version game | Last day |

## Table 2: By period

Lab periods and review periods change no Remus code. Their folders are copies of the
period before, so a pair can always open the newest folder. Each Python lab
(`python_*.py`) and each demo (`demo_*.py`) lives only in its own period folder; the student folder holds the file with blanks, and the
instructor folder holds the answer file `<name>_instructor.py`.

| Period | New files | Changed files |
| --- | --- | --- |
| D1 P1 to P3 | No Remus code yet. Each folder holds its Python lab: `python_setup.py` (P1), `python_strings.py` (P2), and `python_lists.py` (P3), with the answer file `<name>_instructor.py` in `instructor/` | None |
| D1 P4 | `board.py`, `show_board.py`, `test_board.py` | None |
| D2 P1 | Lab 3: `python_functions.py` | None |
| D2 P2 | Lab 4: `python_dicts.py` | None |
| D2 P3 | `game_state.py`, `moves.py`, `test_make_move.py` | `board.py`: adds `set_piece()` |
| D2 P4 | `make_move.py` | `test_make_move.py`: make and undo tests |
| D3 P1 | Lab 5: `python_loops.py` | None |
| D3 P2 | `move_generation.py`, `test_move_generation.py` | `show_board.py`: move arrows |
| D3 P3 | None | `move_generation.py`: `slide()` and `slider_moves()`. `test_move_generation.py` |
| D3 P4 | None | `move_generation.py`: pawns and `pseudo_legal_moves()`. `test_move_generation.py` |
| D4 P1 | Lab 6: `python_modules.py`, which imports `board.py` and `move_generation.py` | None |
| D4 P2 | `attacks.py`, `test_legal_moves.py` | None |
| D4 P3 | `legal_moves.py` | `attacks.py`: `find_king()` and `in_check()`. `test_legal_moves.py` |
| D4 P4 | Demo: `demo_practice_positions.py` | `test_legal_moves.py`: the practice positions |
| D5 P1 | Lab 7: `python_sets.py` | None |
| D5 P2 | `test_special_moves.py` | `make_move.py`: castling and rights. `legal_moves.py`: castling moves |
| D5 P3 | None | `make_move.py`: en passant. `move_generation.py`: en passant captures. `test_special_moves.py` |
| D5 P4 | `uci_engine.py`, `remus.bat`. Demo: `demo_promotion.py` | `make_move.py`: promotion. `test_special_moves.py` |
| D6 P1 | Lab 8: `python_recursion.py` | None |
| D6 P2 | `perft.py` | None |
| D6 P3 | `test_perft.py`. Demo: the `bug_hunt/` folder, a copy of the period's Remus with three planted bugs, and `hunt.py`, which finds them with `divide()` | None |
| D6 P4 | `fen.py`, `test_game.py`. Lab 9: `python_fen_fields.py` | `test_perft.py`: sets up positions with `fen.py` |
| D7 P1 | `game_end.py` | `game_state.py`: `position_key()`. `make_move.py` and `fen.py`: position history. `test_game.py` |
| D7 P2 | `notation.py`, `console_game.py`. Lab 10: `python_input_output.py` | `test_game.py` |
| D7 P3 | `search.py`, `play_match.py` | `uci_engine.py`: the full engine. `console_game.py`: Remus plays. `test_game.py` |
| D7 P4 | `evaluation.py`, `test_search.py` | None |
| D8 P1 | None | `search.py`: minimax and negamax. `uci_engine.py` and `console_game.py`: the negamax brain. `test_search.py` |
| D8 P2 | `compare_search.py`. Lab 11: `python_sorting.py` | `search.py`: alpha-beta. `test_search.py` |
| D8 P3 | None | `search.py`: quiescence. `test_search.py` |
| D8 P4 | `move_ordering.py` | `search.py`: ordering, check extension, clock. `test_search.py` |
| D9 P1 | None | `search.py`: `think()`. `uci_engine.py`: clock and thinking time. `console_game.py`: uses `think()`. `test_search.py` |
| D9 P2, P3 | Ten color version folders in `period2/instructor/engines` and `period2/student/engines` (see [remus_versions.md](../engines/remus_versions.md)). Lab 12 in P2: `python_caches.py` | None: from period 2 on, the Day 9 period folders hold no engine code, and Remus-WHITE stays in `period1` |
| D9 P4 | `play_battle.py` in each color version folder: color battles between pairs. Demo: `demo_results.py` | None |
| D10 P1 | `hidden_peak.py`, `test_hidden_peak.py`. The Day 10 folders hold only the science files; the engine is Remus-GOLD (`transposition_table.py`, `opening_book.py`, `upgraded_search()`, and the other enhancements) | None |
| D10 P2 | `phase_hunt.py`, `test_phase_hunt.py` | None |
| D10 P3 | None | `phase_hunt.py`: the tree search. `test_phase_hunt.py` |
| D10 P4 | None: the pairs report their science results | None |
