# Remus-PLATINUM and Niram-PLATINUM: the same algorithms at two speeds

Niram-PLATINUM is Remus-PLATINUM rewritten in Rust. The two engines run the same algorithms: the same move generator, evaluation, search, and opening book. Given the same position and the same depth, they pick the same move. They differ greatly in speed, and so in playing strength: with a clock running, Niram-PLATINUM searches far more positions and reaches deeper.

`misc/designer/engine_parity.py` checks that the algorithms match. It gives both engines the same positions with no clock, so time never decides how deep a search goes. For each position, both engines report the position key, the evaluation, the legal moves in generation order and in search order, the book moves, every depth's score, node count, and principal variation, and the best move. Niram-PLATINUM picks the depth, the deepest search that visits at most 150,000 positions, and Remus-PLATINUM repeats that search. Any difference in any field counts as a mismatch.

## Result

49 of 49 positions match, with 0 mismatches. The searches visited 3,322,822 positions in all, up to depth 12. The whole check took 3.1 minutes on 4 cores.

## Speed

Both engines ran the same searches. Niram-PLATINUM ran them one after another on one core. Remus-PLATINUM ran one search per core, and its time below adds up the time of every search.

| Engine | Time for all searches (s) | Positions a second |
| --- | ---: | ---: |
| Niram-PLATINUM | 44.4 | 74,761 |
| Remus-PLATINUM | 536 | 6,198 |

Niram-PLATINUM ran the same searches 12 times as fast.

## Opening book

Niram-PLATINUM reads `engines/Niram-PLATINUM/opening_book.txt`. The check compares every position and move of that book, in order, with the book Remus-PLATINUM loads.

| Engine | Positions | Moves | Same as Niram-PLATINUM's book | Same file |
| --- | ---: | ---: | --- | --- |
| Remus-PLATINUM | 285 | 328 | yes | yes |

## Positions

Each row gives the depth the search reached and the positions it visited. A search stops short of the cap when the next depth would pass it, when it reaches depth 12, or when it finds a forced mate.

| Position | What it tests | Depth | Positions searched |
| --- | --- | ---: | ---: |
| start | Opening | 7 | 39,226 |
| after-e4 | Opening | 7 | 104,643 |
| italian | Opening, in book | 8 | 146,945 |
| najdorf | Opening, in book | 6 | 65,063 |
| queens-gambit | Opening, in book | 6 | 36,037 |
| kings-indian | Opening, in book | 6 | 55,632 |
| grob | Opening, out of book | 7 | 134,638 |
| scholars-trap | Trap line, Black defends | 7 | 70,239 |
| blackburne-shilling | Trap line, White defends | 6 | 94,524 |
| trap-attacker | Trap line, attacker's turn | 8 | 146,945 |
| giuoco-middlegame | Middlegame | 7 | 84,821 |
| kiwipete | Middlegame, castling, en passant | 6 | 56,469 |
| pinned-bishops | Middlegame, pins | 7 | 109,198 |
| wac-001 | Tactic | 7 | 125,166 |
| wac-002 | Tactic, Black | 9 | 132,667 |
| wac-003 | Tactic | 8 | 93,137 |
| wac-004 | Tactic, sacrifice | 3 | 801 |
| wac-005 | Tactic, Black | 3 | 365 |
| in-check | Check | 2 | 14 |
| double-check | Double check | 6 | 78,745 |
| castle-both | Castling | 7 | 104,563 |
| castle-through-check | Castling across an attacked square | 7 | 118,245 |
| castle-b-file | Castling with b1 attacked | 8 | 143,994 |
| en-passant | En passant | 6 | 44,931 |
| en-passant-pinned | En passant that exposes the king | 11 | 98,305 |
| promotion | Promotion | 7 | 78,368 |
| promotion-capture | Promotion by capture | 7 | 65,441 |
| black-promotion | Promotion, Black | 7 | 99,253 |
| underpromotion | Knight promotion with check | 8 | 126,993 |
| king-and-pawn | Endgame | 12 | 31,901 |
| rook-ending | Endgame | 2 | 48 |
| lucena | Endgame | 8 | 18,307 |
| philidor | Endgame, Black | 8 | 116,387 |
| queen-vs-pawns | Endgame | 7 | 39,361 |
| pawn-race | Endgame | 11 | 108,408 |
| king-queen-king | Mating with the queen | 6 | 87,063 |
| king-rook-king | Mating with the rook | 9 | 129,238 |
| bishop-knight | Mating with bishop and knight | 8 | 81,057 |
| back-rank | Mate in one | 2 | 47 |
| mate-001 | Mate in two | 5 | 8,838 |
| mate-005 | Mate in two | 5 | 19,754 |
| mate-007 | Mate in two | 5 | 6,013 |
| mate-008 | Mate in three | 5 | 28,551 |
| repetition | Threefold repetition one move away | 7 | 68,951 |
| repetition-ahead | Repetition while ahead | 12 | 1,494 |
| fifty-moves | Fifty-move rule near | 12 | 240 |
| knight-only | Insufficient material | 11 | 121,796 |
| checkmated | Checkmate on the board | 0 | 0 |
| stalemated | Stalemate on the board | 0 | 0 |

## Run it again

The course designer runs `uv run misc/designer/engine_parity.py --version PLATINUM --nodes 150000` from the top Remus folder. The script builds Niram-PLATINUM with `cargo build --release` first and rewrites this page.
