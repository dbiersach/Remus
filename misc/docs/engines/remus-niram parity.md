# Engine parity: Remus and Niram

`misc/scripts/engine_parity.py` checks that Niram-GOLD thinks exactly like Remus-GOLD. For every position below, both engines report the position key, the version's evaluation, the legal moves in generation order and in search order, the book moves, and a search with no clock: each depth's score, node count, and principal variation, and the best move. Niram picks the depth, the deepest search that visits at most 500,000 positions, and Remus repeats that search. Any difference in any field counts as a mismatch.

Last run: 2026-10-29, Remus-GOLD and Niram-GOLD, 49 positions, 49 searches, 0 mismatches, 8.6 minutes on 4 cores.

Run it again with `uv run misc/scripts/engine_parity.py --nodes 500000` from the repository folder.

## Versions

| Version | Positions matched | Positions searched | Deepest search | Remus time (s) |
| --- | ---: | ---: | ---: | ---: |
| GOLD | 49 of 49 | 10,640,155 | 12 | 1,548 |

## Opening book

Niram reads `Niram-GOLD/opening_book.txt`; the check compares every position and move of its book, in order, with the book Remus-GOLD loads.

| Version | Positions | Moves | Same as Niram's book | Same file |
| --- | ---: | ---: | --- | --- |
| GOLD | 285 | 328 | yes | yes |

## Positions

Each row gives the depth the search reached and the positions it visited. A search stops short of the cap when the next depth would pass it, when it reaches depth 12, or when it finds a forced mate.

| Position | What it tests | Depth | Positions searched |
| --- | --- | ---: | ---: |
| start | Opening | 9 | 301,708 |
| after-e4 | Opening | 8 | 107,572 |
| italian | Opening, in book | 6 | 101,723 |
| najdorf | Opening, in book | 7 | 367,789 |
| queens-gambit | Opening, in book | 8 | 445,567 |
| kings-indian | Opening, in book | 7 | 338,811 |
| grob | Opening, out of book | 8 | 483,645 |
| scholars-trap | Trap line, Black defends | 8 | 336,779 |
| blackburne-shilling | Trap line, White defends | 7 | 422,956 |
| trap-attacker | Trap line, attacker's turn | 6 | 101,723 |
| giuoco-middlegame | Middlegame | 7 | 460,756 |
| kiwipete | Middlegame, castling, en passant | 6 | 209,468 |
| pinned-bishops | Middlegame, pins | 7 | 283,551 |
| wac-001 | Tactic | 7 | 212,864 |
| wac-002 | Tactic, Black | 10 | 295,160 |
| wac-003 | Tactic | 8 | 347,499 |
| wac-004 | Tactic, sacrifice | 3 | 1,462 |
| wac-005 | Tactic, Black | 3 | 486 |
| in-check | Check | 2 | 14 |
| double-check | Double check | 7 | 368,123 |
| castle-both | Castling | 9 | 497,550 |
| castle-through-check | Castling across an attacked square | 9 | 387,678 |
| castle-b-file | Castling with b1 attacked | 8 | 460,482 |
| en-passant | En passant | 7 | 196,293 |
| en-passant-pinned | En passant that exposes the king | 10 | 186,562 |
| promotion | Promotion | 8 | 252,159 |
| promotion-capture | Promotion by capture | 9 | 293,553 |
| black-promotion | Promotion, Black | 8 | 223,461 |
| underpromotion | Knight promotion with check | 10 | 97,611 |
| king-and-pawn | Endgame | 12 | 34,784 |
| rook-ending | Endgame | 2 | 48 |
| lucena | Endgame | 10 | 154,438 |
| philidor | Endgame, Black | 10 | 341,168 |
| queen-vs-pawns | Endgame | 10 | 372,064 |
| pawn-race | Endgame | 12 | 153,334 |
| king-queen-king | Mating with the queen | 9 | 381,093 |
| king-rook-king | Mating with the rook | 11 | 364,588 |
| bishop-knight | Mating with bishop and knight | 10 | 411,778 |
| back-rank | Mate in one | 2 | 47 |
| mate-001 | Mate in two | 5 | 12,942 |
| mate-005 | Mate in two | 5 | 19,455 |
| mate-007 | Mate in two | 5 | 7,292 |
| mate-008 | Mate in three | 5 | 48,425 |
| repetition | Threefold repetition one move away | 8 | 314,247 |
| repetition-ahead | Repetition while ahead | 12 | 2,220 |
| fifty-moves | Fifty-move rule near | 12 | 240 |
| knight-only | Insufficient material | 12 | 238,987 |
| checkmated | Checkmate on the board | 0 | 0 |
| stalemated | Stalemate on the board | 0 | 0 |
