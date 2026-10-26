# File Versions: Which Day Changes Which File

Each Day folder holds one version of each file. The folder name is the version: the
`board.py` in `Day 02 - Make and undo moves` is version 2 of `board.py`. A file that a
day does not change is copied forward as it is.

Table 1 follows each file through the days. Table 2 lists, for each day, the files
that are new or changed. Test files are listed in Table 2 only.

## Table 1: By file

| File | First day | How it changes |
| --- | --- | --- |
| `board.py` | 1: the 8x8 board, printing, square names | 2: adds `set_piece()` to write a square |
| `game_state.py` | 2: the state dict, colors | 7: adds `position_key()` for repetition |
| `moves.py` | 2: the `Move` record and UCI text | No changes |
| `make_move.py` | 2: make and undo quiet moves and captures | 5: castling, en passant, promotion, castling rights. 7: records each position in `history` and removes it on undo |
| `move_generation.py` | 3: moves of every piece | 5: adds en passant captures |
| `attacks.py` | 4: attacked squares, two versions, and `in_check()` | No changes |
| `legal_moves.py` | 4: the make, test, undo filter | 5: adds castling moves |
| `perft.py` | 6: counts positions, `divide()` | No changes |
| `fen.py` | 7: FEN in and out | No changes |
| `notation.py` | 7: SAN in and out | No changes |
| `game_end.py` | 7: mate, stalemate, draws | No changes |
| `search.py` | 7: random and greedy brains | 8: minimax, negamax, mate scores. 9: alpha-beta, quiescence, iterative deepening, `info` lines. 10: `upgraded_search()` with memory, killers, PVS, draw sense |
| `uci_engine.py` | 7: talks UCI to En Croissant | 8: negamax brain. 9: clock, thinking thread, `stop`. 10: plays book moves first |
| `console_game.py` | 7: two people play in SAN | 8: Remus plays with negamax. 9: Remus thinks on a clock. 10: Remus plays book moves first |
| `play_match.py` | 7: two brains play a match | No changes |
| `remus.bat` | 7: starts Remus for En Croissant | No changes |
| `evaluation.py` | 8: material and piece-square tables | 10: pawn structure and the mating bonus |
| `move_ordering.py` | 9: captures first by MVV-LVA | 10: killer moves |
| `compare_search.py` | 9: negamax against alpha-beta | No changes |
| `transposition_table.py` | 10: remembers searched positions | Last day |
| `opening_book.py`, `opening_book.txt` | 10: plays known openings | Last day |
| `mate_solver.py` | 10: solves the GameWorks mate puzzles | Last day |
| `hidden_peak.py` | 10: Science AI | Last day |
| `tournament.py` | 10: the class round robin | Last day |
| `remus.sh` | 10: starts Remus on a Mac or Linux computer at home | Last day |

## Table 2: By day

| Day | New files | Changed files |
| --- | --- | --- |
| 1. Draw the board | `board.py`, `test_board.py` | None |
| 2. Make and undo moves | `game_state.py`, `moves.py`, `make_move.py`, `test_make_move.py` | `board.py`: adds `set_piece()` |
| 3. Generate piece moves | `move_generation.py`, `test_move_generation.py` | None |
| 4. Keep only legal moves | `attacks.py`, `legal_moves.py`, `test_legal_moves.py` | None |
| 5. Add castling, en passant, and promotion | `test_special_moves.py` | `make_move.py`: the three special moves and castling rights. `move_generation.py`: en passant captures. `legal_moves.py`: castling moves |
| 6. Count positions with perft | `perft.py`, `test_perft.py` | None |
| 7. Play full games in En Croissant | `fen.py`, `notation.py`, `game_end.py`, `search.py`, `uci_engine.py`, `console_game.py`, `play_match.py`, `remus.bat`, `test_game.py` | `game_state.py`: `position_key()`. `make_move.py`: position history. `test_perft.py`: sets up positions with `fen.py` |
| 8. Evaluate and search ahead | `evaluation.py`, `test_search.py` | `search.py`: minimax and negamax. `uci_engine.py` and `console_game.py`: use the negamax brain |
| 9. Search faster with alpha-beta | `move_ordering.py`, `compare_search.py` | `search.py`: alpha-beta, quiescence, `think()`. `uci_engine.py`: clock, thread, `stop`. `console_game.py`: uses `think()`. `test_search.py`: tests for the new search |
| 10. Upgrade Remus and add Science AI | `transposition_table.py`, `opening_book.py`, `opening_book.txt`, `mate_solver.py`, `hidden_peak.py`, `tournament.py`, `remus.sh`, `test_upgrades.py` | `search.py`: `upgraded_search()`. `evaluation.py`: pawns and mating. `move_ordering.py`: killers. `uci_engine.py` and `console_game.py`: book moves first |
