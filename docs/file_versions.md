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
| `game_state.py` | D2 P3: the state dict, colors | D7 P2: adds `position_key()` and the position history |
| `moves.py` | D2 P3: the `Move` record and UCI text | No changes |
| `make_move.py` | D2 P4: make and undo quiet moves and captures | D5 P2: castling and castling rights. D5 P3: en passant. D5 P4: promotion. D7 P2: records each position in `history` and removes it on undo |
| `move_generation.py` | D3 P2: knight and king jumps | D3 P3: sliding pieces. D3 P4: pawns, promotion choices, `pseudo_legal_moves()`. D5 P3: en passant captures |
| `attacks.py` | D4 P2: attacked squares, two versions | D4 P3: `find_king()` and `in_check()` |
| `legal_moves.py` | D4 P3: the make, test, undo filter | D5 P2: adds castling moves |
| `uci_engine.py` | D5 P4: a first engine for En Croissant that plays random legal moves | D7 P4: every UCI command, FEN positions, random and greedy brains. D8 P4: negamax brain. D9 P4: clock, thinking thread, `stop`. D10 P1: plays book moves first |
| `remus.bat` | D5 P4: starts Remus for En Croissant | No changes |
| `perft.py` | D6 P2: counts positions, `divide()` | No changes |
| `fen.py` | D7 P1: FEN in and out | D7 P2: starts the position history |
| `game_end.py` | D7 P2: mate, stalemate, draws | No changes |
| `notation.py` | D7 P3: SAN in and out | No changes |
| `console_game.py` | D7 P3: two people play in SAN | D7 P4: Remus plays greedy moves. D8 P4: Remus plays with negamax. D9 P4: Remus thinks on a clock. D10 P1: Remus plays book moves first |
| `search.py` | D7 P4: random and greedy brains | D8 P3: minimax. D8 P4: negamax and mate scores. D9 P1: alpha-beta. D9 P2: quiescence. D9 P3: move ordering, check extension, the clock. D9 P4: iterative deepening and `info` lines. D10 P1: `upgraded_search()` with memory, killers, PVS, draw sense, null moves, late move reductions |
| `play_match.py` | D7 P4: two brains play a match | No changes |
| `evaluation.py` | D8 P1: material | D8 P2: piece-square tables. D10 P1: pawn structure, the mating bonus, king safety |
| `compare_search.py` | D9 P1: negamax against alpha-beta | No changes |
| `move_ordering.py` | D9 P3: captures first by MVV-LVA | D10 P1: killer moves |
| `transposition_table.py` | D10 P1: remembers searched positions | Last day |
| `opening_book.py`, `opening_book.txt` | D10 P1: plays known openings | Last day |
| `mate_solver.py` | D10 P1: solves the GameWorks mate puzzles | Last day |
| `hidden_peak.py` | D10 P2: Science AI | Last day |
| `tournament.py` | D10 P3: the class round robin | Last day |
| `remus.sh` | D10 P4: starts Remus on a Mac or Linux computer at home | Last day |
| `estimate_elo.py` | D10 P4: measures the Elo rating of Remus against Stockfish | Last day |
| `Stations/station_match.py` | D10 P1: plays one enhancement station against the plain Day 9 Remus | Last day |

## Table 2: By period

Lab periods and review periods change no Remus code. Their folders are copies of the
period before, so a pair can always open the newest folder.

| Period | New files | Changed files |
| --- | --- | --- |
| D1 P1 to P3 | None: setup and Python labs, before any Remus code | None |
| D1 P4 | `board.py`, `show_board.py`, `test_board.py` | None |
| D2 P1, P2 | None: Python labs | None |
| D2 P3 | `game_state.py`, `moves.py`, `test_make_move.py` | `board.py`: adds `set_piece()` |
| D2 P4 | `make_move.py` | `test_make_move.py`: make and undo tests |
| D3 P1 | None: Python lab | None |
| D3 P2 | `move_generation.py`, `test_move_generation.py` | `show_board.py`: move arrows |
| D3 P3 | None | `move_generation.py`: `slide()` and `slider_moves()`. `test_move_generation.py` |
| D3 P4 | None | `move_generation.py`: pawns and `pseudo_legal_moves()`. `test_move_generation.py` |
| D4 P1 | None: Python lab | None |
| D4 P2 | `attacks.py`, `test_legal_moves.py` | None |
| D4 P3 | `legal_moves.py` | `attacks.py`: `find_king()` and `in_check()`. `test_legal_moves.py` |
| D4 P4 | None | `test_legal_moves.py`: the practice positions |
| D5 P1 | None: Python lab | None |
| D5 P2 | `test_special_moves.py` | `make_move.py`: castling and rights. `legal_moves.py`: castling moves |
| D5 P3 | None | `make_move.py`: en passant. `move_generation.py`: en passant captures. `test_special_moves.py` |
| D5 P4 | `uci_engine.py`, `remus.bat` | `make_move.py`: promotion. `test_special_moves.py` |
| D6 P1 | None: Python lab | None |
| D6 P2 | `perft.py` | None |
| D6 P3 | `test_perft.py` | None |
| D6 P4 | None: review | None |
| D7 P1 | `fen.py`, `test_game.py` | `test_perft.py`: sets up positions with `fen.py` |
| D7 P2 | `game_end.py` | `game_state.py`: `position_key()`. `make_move.py` and `fen.py`: position history. `test_game.py` |
| D7 P3 | `notation.py`, `console_game.py` | `test_game.py` |
| D7 P4 | `search.py`, `play_match.py` | `uci_engine.py`: the full engine. `console_game.py`: Remus plays. `test_game.py` |
| D8 P1 | `evaluation.py`, `test_search.py` | None |
| D8 P2 | None | `evaluation.py`: piece-square tables. `test_search.py` |
| D8 P3 | None | `search.py`: minimax. `test_search.py` |
| D8 P4 | None | `search.py`: negamax. `uci_engine.py` and `console_game.py`: the negamax brain. `test_search.py` |
| D9 P1 | `compare_search.py` | `search.py`: alpha-beta. `test_search.py` |
| D9 P2 | None | `search.py`: quiescence. `test_search.py` |
| D9 P3 | `move_ordering.py` | `search.py`: ordering, check extension, clock. `test_search.py` |
| D9 P4 | None | `search.py`: `think()`. `uci_engine.py`: clock, thread, `stop`. `console_game.py`: uses `think()`. `test_search.py` |
| D10 P1 | Ten station folders in `Stations/` (see [stations.md](stations.md)), `transposition_table.py`, `opening_book.py`, `opening_book.txt`, `mate_solver.py`, `test_upgrades.py` | `search.py`: `upgraded_search()`. `evaluation.py`: pawns, mating, king safety. `move_ordering.py`: killers. `uci_engine.py` and `console_game.py`: book moves first |
| D10 P2 | `hidden_peak.py` | `test_upgrades.py`: hidden-peak tests |
| D10 P3 | `tournament.py` | None |
| D10 P4 | `remus.sh`, `estimate_elo.py` | None |
