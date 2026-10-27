# Remus Slide Plan

These are the PowerPoint slides the workshop needs to picture Remus's data structures
and program flow. Slides are numbered by day: slide 4.2 is the second slide of Day 4.
Each script page in [`scripts/`](scripts/) lists the slides that go with it.

Most slides follow one pattern: a small position or tree the class can trace by hand,
the state before and after, and the few lines of code that do the work. Keep code on a
slide to 12 lines or fewer; the full function lives in the Day folder.

## Day 1: Draw the board

| Slide | Title | What it shows |
| --- | --- | --- |
| 1.1 | Remus at a glance | The four boundaries as boxes: engine, console, UCI adapter, En Croissant. Arrows show that only moves and text cross a boundary |
| 1.2 | The module map | Every module of Day 10 as a box, arranged bottom to top in the order it is built (board, game_state, moves, make_move, move_generation, attacks, legal_moves, ...), with import arrows |
| 1.3 | The board is a list of lists | An 8x8 grid with `board[row][col]` indexes on one side and rank and file labels on the other. Highlight `board[6][4]` = e2 = `"P"` |
| 1.4 | Square names and coordinates | `"e2"` to `(6, 4)` and back: `col = "abcdefgh".index("e")`, `row = 8 - 2`. Three worked examples: a8, e2, h1 |
| 1.5 | Piece letters | The 12 letters plus `"."`: uppercase White, lowercase Black, with piece icons |
| 1.6 | Your board as a picture | `show_board.py` side by side: the printed letters on the left, the browser picture on the right. python-chess only draws; Remus keeps the board |

## Day 2: Make and undo moves

| Slide | Title | What it shows |
| --- | --- | --- |
| 2.1 | The game state dict | One box per key (`board`, `turn`, `castling`, `en_passant`, two clocks), each with a start-position value |
| 2.2 | The `Move` record | `Move((6, 4), (4, 4))` drawn as an arrow on the board, and its UCI text `e2e4` |
| 2.3 | Make, then undo | Three panels: the state before, the undo record `make_move` returns, the state after. A return arrow shows `undo_move` restoring the first panel |
| 2.4 | The two clocks | A timeline of six moves showing when `halfmove_clock` resets (capture or pawn move) and when `fullmove_number` goes up (after Black) |
| 2.5 | Proving undo is exact | `state_snapshot` before and after a make and undo, compared with `==` |

## Day 3: Generate piece moves

| Slide | Title | What it shows |
| --- | --- | --- |
| 3.1 | Directions as numbers | A compass of `(row change, col change)` pairs: rook four, bishop four, queen eight. Row 0 is rank 8, so "up the board" is `-1` |
| 3.2 | Knight and king jumps | A knight on d4 with its eight `KNIGHT_JUMPS`; a knight on a1 with only two |
| 3.3 | Sliding along a ray | A rook on d4: `slide` walks each direction, stops before its own piece, stops on an enemy piece and includes the capture. 14 moves on an empty board |
| 3.4 | Pawns are different | White moves toward row 0, Black toward row 7; one step, two from the start row, diagonal captures, and one move becoming four at promotion |
| 3.5 | `pseudo_legal_moves` flow | Loop over 64 squares, `piece_moves` dispatches by letter to `knight_moves`, `king_moves`, `slider_moves`, `pawn_pushes`, `pawn_captures` |
| 3.6 | See your moves | The start position with one arrow per move from `show_moves()`: four knight arrows, then all 20 pseudo-legal moves |

## Day 4: Keep only legal moves

| Slide | Title | What it shows |
| --- | --- | --- |
| 4.1 | Two ways to ask "is f3 attacked?" | Left: version 1 asks every enemy piece. Right: version 2 stands on f3 and looks outward like a super piece |
| 4.2 | Looking outward | From one square: rays for rooks and queens, diagonals for bishops and queens, knight squares, pawn squares, king squares. `first_piece` stops at the first piece on each ray |
| 4.3 | The legal filter | Make the move, ask `in_check` for the mover, undo the move. Keep it only if the king is safe |
| 4.4 | Three positions one rule catches | A pinned knight, a discovered check, and a king stepping into check, all rejected by the same filter |

## Day 5: Add castling, en passant, and promotion

| Slide | Title | What it shows |
| --- | --- | --- |
| 5.1 | When castling is allowed | A checklist: right still held, squares between empty, king not in check, king does not pass through or land on an attacked square. One row of the `CASTLES` table matched to the board |
| 5.2 | Castling rights shrink | `CASTLING_SQUARES`: moving from or capturing on e1, h1, a1, e8, h8, a8 removes letters from `"KQkq"`. A sample game drawn as the string changes |
| 5.3 | En passant | The double step sets the target square; the capture lands on the target but removes the pawn beside it (`en_passant_victim_square`) |
| 5.4 | The full undo record | The undo dict with `rook_move` and `en_passant_victim` filled in for a castle and an en passant capture |
| 5.5 | Promotion and underpromotion | One pawn move becomes four: `e7e8q`, `e7e8r`, `e7e8b`, `e7e8n` |
| 5.6 | Remus plays in En Croissant | Register `remus.bat` from `Day 05 .../period4`. The GUI sends `position startpos moves e2e4 ...` and `go`; Remus answers `bestmove` with a random legal move. Day 7 explains every line |

## Day 6: Count positions with perft

| Slide | Title | What it shows |
| --- | --- | --- |
| 6.1 | The move tree | Start position: 20 moves, 400 positions, 8,902, 197,281. A tree whose branch count explodes |
| 6.2 | `perft` in eight lines | The recursive count with make, recurse, undo |
| 6.3 | `divide` finds the bug | A table of root moves with Remus's count against the reference count; the one row that differs points to the bug |

## Day 7: Play full games in En Croissant

| Slide | Title | What it shows |
| --- | --- | --- |
| 7.1 | Anatomy of FEN | The start FEN split into its six fields, each labeled |
| 7.2 | Anatomy of SAN | `Nbd2`, `exd5`, `O-O`, `e8=Q+`, with each part labeled |
| 7.3 | Reading SAN the simple way | Write the SAN of every legal move, then pick the one that matches what the player typed |
| 7.4 | Positions remember the past | `position_key` text and the `history` list; the same key three times means a repetition draw |
| 7.5 | Is the game over? | The decision flow of `game_result`: no legal moves (mate or stalemate), insufficient material, repetition, fifty-move rule |
| 7.6 | The UCI conversation | A sequence diagram: En Croissant sends `uci`, `isready`, `position`, `go`; Remus answers `uciok`, `readyok`, `bestmove` |
| 7.7 | Two first brains | `random_move` and `greedy_move` on the same position; the greedy brain takes the queen |

## Day 8: Evaluate and search ahead

| Slide | Title | What it shows |
| --- | --- | --- |
| 8.1 | Centipawns | Piece values 100, 300, 300, 500, 900, and a material count for a sample position |
| 8.2 | Piece-square tables | The knight table as a heat map: +20 in the center, -50 in the corners. Black reads the table upside down |
| 8.3 | Minimax by hand | A depth-2 tree with leaf scores; White takes the maximum, Black the minimum, and the numbers move up the tree |
| 8.4 | Negamax: one function | The same tree with one rule, "my score is the negative of my opponent's best" |
| 8.5 | Scoring checkmate | `MATE_SCORE - ply`: a mate in 1 beats a mate in 3, and both beat any material count |

## Day 9: Search faster with alpha-beta

| Slide | Title | What it shows |
| --- | --- | --- |
| 9.1 | Alpha-beta cutoffs | The Day 8 tree with branches crossed out once a refutation is found; the window `(alpha, beta)` written beside each node |
| 9.2 | Same answer, less work | A bar chart from `compare_search.py`: alpha-beta visits less than a fifth of the positions negamax visits, with equal scores |
| 9.3 | The horizon effect | A queen captures a pawn at depth 0 and is lost one move later. Quiescence keeps searching captures until the position is quiet |
| 9.4 | Move ordering | An MVV-LVA grid: victim across, attacker down. Pawn takes queen first, queen takes pawn last |
| 9.5 | Iterative deepening | A timeline of depth 1, 2, 3, 4 with the clock running out during depth 5; the best move from depth 4 is played |
| 9.6 | Stopping safely | `SearchTimeout` unwinding the recursion; each `finally` undoes its move, so the root position is intact |
| 9.7 | Thinking in a thread | The UCI loop and the search thread side by side, with the stop event between them |
| 9.8 | The principal variation | An `info depth 4 score cp 35 pv ...` line drawn as moves on the board |

## Day 10: Upgrade Remus and add Science AI

| Slide | Title | What it shows |
| --- | --- | --- |
| 10.1 | The upgrade stations | The eight stations with the GameWorks idea each one echoes |
| 10.2 | Transpositions | 1. Nf3 Nf6 2. Nc3 and 1. Nc3 Nf6 2. Nf3 reach one position. A table entry: depth, score, bound, best move |
| 10.3 | Exact, lower, upper | Three number lines showing what a stored bound proves for a new `(alpha, beta)` window |
| 10.4 | Killer moves | Two slots per ply; a quiet move that caused a cutoff jumps the queue in sibling positions |
| 10.5 | Principal variation search | The first move gets the full window; the rest get a null window `(alpha, alpha + 1)` and a re-search only on a surprise |
| 10.6 | Pawn structure | Doubled, isolated, and passed pawns on one diagram with their points |
| 10.7 | Finishing a won endgame | The `mating_bonus` heat map: the losing king pushed to the edge, the winning king closing in |
| 10.8 | The opening book | Book lines in SAN turned into a dict from `position_key` to moves, drawn as a small tree |
| 10.9 | The mate solver | An AND/OR tree: the attacker needs one move that works, the defender's every reply must fail. MATE.008 solved in about 6 seconds |
| 10.10 | The round robin | The circle method for 10 entrants: one fixed, the rest rotate; 9 rounds, 45 games |
| 10.11 | From chess to science | The map table: legal moves to unmeasured squares, evaluation to predicted value plus exploration, minimax to expectimax |
| 10.12 | The hidden peak | A 10x10 grid with readings so far, the predicted values, and the square the AI chooses next |
| 10.13 | Explore against exploit | Three runs with explore weight 0, 8, and 40 and their average measurements |
| 10.14 | The benchmark | A bar chart: random guessing about 54 measurements, greedy AI about 9 |
| 10.15 | The real thing | The NSLS-II autonomous agent runs the same loop with a Gaussian process instead of the hand-built score |
