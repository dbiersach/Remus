# Niram: every Remus version in Rust

Niram is Remus rewritten in Rust. Remus echoes Rimush, the son of Sargon of Akkad;
Niram shortens Naram-Sin, Sargon's grandson, the next heir in the family line.

Niram holds one engine for each of the 12 versions in `instructor/Remus`:
Niram-WHITE with no enhancements, the ten color stations, and Niram-GOLD with all
ten. Each Niram version keeps the exact rules, evaluation, and search of the Remus
version of the same color: the same board of 64 characters, the same move order,
and the same evaluation terms and search function. Given the same position and
depth, both engines visit the same number of positions and choose the same move
with the same score. Only the language changes, so a Niram league plays the same
games as a Remus league would with about 50 times more thinking time.

Niram is a teacher's experiment, not part of the course. Students write Remus in
Python.

## Folders

The folders carry the same names as the station folders, with the same two-digit
prefix, so that both list in the order of each version's Elo over WHITE in the
10-minute Remus league:

| Folder | Program | Search | Evaluation |
| --- | --- | --- | --- |
| `00 WHITE - No enhancements` | `niram-white` | `alpha_beta_with_quiescence` | material, placement |
| `01 YELLOW - Draw sense` | `niram-yellow` | `draw_sense_search` | material, placement |
| `02 ORANGE - Null-move pruning` | `niram-orange` | `null_move_search` | material, placement |
| `03 BROWN - Late move reductions` | `niram-brown` | `reduced_search` | material, placement |
| `04 BLUE - Killer moves` | `niram-blue` | `killer_search` | material, placement |
| `05 PINK - Principal variation search` | `niram-pink` | `pvs_search` | material, placement |
| `06 RED - Transposition table` | `niram-red` | `table_search` | material, placement |
| `07 PURPLE - Pawn structure` | `niram-purple` | `alpha_beta_with_quiescence` | + pawn structure |
| `08 GRAY - King safety` | `niram-gray` | `alpha_beta_with_quiescence` | + king safety |
| `09 CYAN - Mating bonus` | `niram-cyan` | `alpha_beta_with_quiescence` | + mating bonus |
| `10 GREEN - Opening book` | `niram-green` | `alpha_beta_with_quiescence`, after the book | material, placement |
| `11 GOLD - All enhancements` | `niram-gold` | `upgraded_search`, after the book | all five terms |

Each version folder holds only what makes that version different: `evaluation.rs`
with its `evaluate`, `search.rs` with its search function, `quiescence`, and
`think`, and `main.rs`. Each station is Remus-WHITE plus exactly one enhancement,
so no station needs code from another; only GOLD combines all ten.

Everything the versions share sits in `rules/`, and each of its Rust files matches
the Python file of the same name, with the same function names:

| Rust file | Remus file | What it does |
| --- | --- | --- |
| `board.rs` | `board.py` | The 8x8 board and square names |
| `moves.rs` | `moves.py` | The `Move` record and UCI text |
| `game_state.rs` | `game_state.py` | The game state and `position_key` |
| `make_move.rs` | `make_move.py` | `make_move` and `undo_move` |
| `move_generation.rs` | `move_generation.py` | Pseudo-legal moves |
| `attacks.rs` | `attacks.py` | Attacked squares and check |
| `legal_moves.rs` | `legal_moves.py` | Castling and the legal-move filter |
| `evaluation.rs` | `evaluation.py` | Material, placement, pawns, mating, king safety |
| `move_ordering.rs` | `move_ordering.py` | MVV-LVA and killer moves |
| `transposition_table.rs` | `transposition_table.py` | The table of searched positions |
| `search_tools.rs` | `search.py` | The pieces every search shares: the node count, the clock, null moves, reductions |
| `fen.rs`, `notation.rs` | `fen.py`, `notation.py` | FEN and SAN |
| `opening_book.rs` | `opening_book.py` | Book moves from `opening_book.txt`, defend-only trap lines included |
| `uci_engine.rs` | `uci_engine.py` | The UCI conversation with Lucas Chess |
| `bench.rs` | `perft.py` and this benchmark | `bench`, `perft`, and the command line |

`opening_book.txt` is a copy of the book in `instructor/Remus/11 GOLD - All
enhancements`, read by Niram-GREEN and Niram-GOLD. The teaching steps that `think` never calls (random, greedy, minimax,
negamax, plain alpha-beta, and the scanning attack test) stay in Python only.

## Run it

Rust and Cargo come from [rustup](https://rustup.rs). From inside `Niram/`:

```bash
cargo build --release                       # All 12 programs, in target/release
cargo test --release                        # perft, the book, and each version's node count
cargo run --release -p niram-red -- bench   # Time Niram-RED on ten positions, depth 4
cargo run --release -p niram-gold -- bench 6
cargo run --release -p niram-white -- perft 5   # 4,865,609 from the start position
```

The matching Python benchmark runs from the repository folder and takes a color:

```bash
uv run scripts/remus_benchmark.py GOLD      # Remus-GOLD, depth 4
uv run scripts/remus_benchmark.py RED 3     # Remus-RED, depth 3
```

To play a Niram version in Lucas Chess, run `cargo build --release` and add
`Niram/target/release/niram-gold.exe` (or any other color) as a UCI engine, the same
way the [Lucas Chess guide](../docs/lucas_chess_guide.md) adds Remus. It needs no
batch file.

## Leagues and matches with Niram

The three station scripts take `--niram`, which plays the Niram programs in place
of the Python stations. Build the programs first. `station_match.py` runs from
`instructor/Remus`, and the other two run from the top Remus folder.

```bash
uv run station_match.py RED --niram                   # Niram-RED against Niram-WHITE
uv run scripts/station_league.py --niram --at-once 16 # the round robin of all 12
uv run scripts/station_league.py --niram --rate-only  # only the Niram ratings
uv run scripts/station_elo.py --niram --workers 16    # all 12 against Stockfish
```

Niram games carry the names Niram-WHITE to Niram-GOLD and are rated apart from the
Remus games, with Niram-WHITE pinned at 0. Leagues still use a 10-minute clock: at
about 50 times the speed of Remus, a 10-minute Niram game searches about as many
positions as a Remus game of eight hours, deep enough for every enhancement to
show what it adds.

## Same tree as Remus

Every version's test checks the depth 3 node count of its Remus twin on the ten
benchmark positions. At depths 3 and 4 the Python and Rust benchmarks also agree on
the best move and score of every position:

| Version | Nodes, depth 3 | Nodes, depth 4 | Niram nodes/s, depth 4 |
| --- | ---: | ---: | ---: |
| WHITE | 72,747 | 431,212 | 211,776 |
| YELLOW | 72,747 | 431,138 | 197,904 |
| ORANGE | 72,747 | 273,470 | 227,642 |
| BROWN | 38,545 | 162,998 | 232,309 |
| BLUE | 64,890 | 328,889 | 225,679 |
| PINK | 61,112 | 289,419 | 263,755 |
| RED | 58,531 | 243,223 | 215,312 |
| PURPLE | 79,656 | 452,398 | 189,047 |
| GRAY | 75,525 | 459,732 | 220,135 |
| CYAN | 72,692 | 425,602 | 199,903 |
| GREEN | 72,747 | 431,212 | 236,953 |
| GOLD | 22,001 | 84,812 | 219,500 |

GREEN searches the same tree as WHITE, because the benchmark searches without the
opening book. Every Remus version runs at about 4,000 positions a second on the
same cloud computer, so every Niram version is about 50 times faster.

## Benchmark of Niram-GOLD

Both programs search the ten positions of `compare_search.py` the way `think()` does,
one depth at a time with no clock. A "node" is one call of a search function or of
`quiescence`, which both engines count the same way.

The first run took place in a cloud Linux container (Python 3.14.6, Rust 1.97.0):

| Depth | Nodes (both engines) | Remus-GOLD time | Niram-GOLD time | Remus nodes/s | Niram nodes/s | Speedup |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 22,001 | 5.67 s | 0.11 s | 3,879 | 196,270 | 51x |
| 4 | 84,812 | 19.74 s | 0.36 s | 4,296 | 236,019 | 55x |
| 5 | 228,133 | 51.00 s | 1.14 s | 4,473 | 200,699 | 45x |
| 6 | 673,713 | 158.89 s | 2.67 s | 4,240 | 252,045 | 59x |

On David's PC (DABMAIN, Windows 11), with nothing else running, depth 5 gave:

| Depth | Nodes (both engines) | Remus-GOLD time | Niram-GOLD time | Remus nodes/s | Niram nodes/s | Speedup |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | 228,133 | 31.87 s | 0.55 s | 7,158 | 416,801 | 58x |

At every depth the two engines visit the same number of positions and pick the same
best move with the same score in all ten positions, so the speedup is the language
alone: 45 to 59 times faster, far past the factor of 10 that would make a Rust
version worth considering.

Every Niram version stays a direct copy, so it keeps Remus's slow parts: a board of characters,
a new list of moves at every node, a position key built as text after every move, and
a repetition test that reads the whole game history. A Rust engine written for speed
(bitboards, a numeric hash key, moves without heap memory) runs many times faster again,
but it would no longer search the same tree as Remus.

## Should the students learn Rust?

Rust would be much harder for 13-year-olds than Python. The chess ideas are no harder
in Rust; the language is. A pair meets the borrow checker (`&mut State` against
`&State`), `Option` and `Result` in place of `None` and exceptions, `as usize` casts
on every board index, and long compiler errors before the first move ever plays.
Those costs land on the class time a pair spends on make/undo, negamax, and
alpha-beta.

The speed also buys less than it seems. Alpha-beta with good move ordering needs
roughly 5 to 10 times more positions for each extra ply, so 50 times the speed lets
the same search look about 2 plies deeper in the same time.

The course stays in Python. Niram serves as a short teacher demo that answers
the question "why do real engines use compiled languages?" with a measurement: the
same engine, the same tree, the same moves, and 50 times the speed.
