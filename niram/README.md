# Niram-GOLD: Remus-GOLD in Rust

Niram-GOLD is Remus-GOLD rewritten in Rust. Remus echoes Rimush, the son of Sargon of
Akkad; Niram shortens Naram-Sin, Sargon's grandson, the next heir in the family line.

Niram-GOLD keeps the exact rules, evaluation, and search of
`instructor/Stations/GOLD - All enhancements`: the same board of 64 characters, the
same move order, the same five evaluation terms, and the same `upgraded_search` with
its transposition table, killer moves, principal variation search, draw sense,
null-move pruning, and late move reductions. Given the same position and depth, both
engines visit the same number of positions and choose the same move. Only the
language changes, so the benchmark below measures the language alone.

Niram is a teacher's experiment, not part of the course. Students write Remus in
Python.

## Files

Each Rust file matches the Python file of the same name, with the same function names:

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
| `search.rs` | `search.py` | Quiescence, `upgraded_search`, and `think` |
| `fen.rs`, `notation.rs` | `fen.py`, `notation.py` | FEN and SAN |
| `opening_book.rs` | `opening_book.py` | Book moves from `opening_book.txt` |
| `uci_engine.rs` | `uci_engine.py` | The UCI conversation with Lucas Chess |
| `main.rs` | `perft.py` and this benchmark | `bench`, `perft`, and the tests |

Remus-GOLD's teaching steps that `think` never calls (random, greedy, minimax, negamax,
plain alpha-beta, and version 1 of the attack test) stay in Python only.

## Run it

Rust and Cargo come from [rustup](https://rustup.rs). From inside `niram/`:

```bash
cargo test --release            # perft counts, and the same node count as Remus-GOLD
cargo run --release -- bench    # Time the search on ten positions, depth 4
cargo run --release -- bench 6  # The same at depth 6
cargo run --release -- perft 5  # 4,865,609 from the start position
```

The matching Python benchmark runs from the repository folder:

```bash
uv run niram/remus_benchmark.py      # Depth 4
uv run niram/remus_benchmark.py 6    # Depth 6
```

To play Niram in Lucas Chess, run `cargo build --release` and add
`niram/target/release/niram.exe` as a UCI engine, the same way the
[Lucas Chess guide](../docs/lucas_chess_guide.md) adds Remus. It needs no batch file.

## Benchmark

Both programs search the ten positions of `compare_search.py` the way `think()` does,
one depth at a time with no clock. A "node" is one call of `upgraded_search` or
`quiescence`, which both engines count the same way.

The first run took place in a cloud Linux container (Python 3.14.6, Rust 1.97.0):

| Depth | Nodes (both engines) | Remus-GOLD time | Niram-GOLD time | Remus nodes/s | Niram nodes/s | Speedup |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | 22,001 | 5.67 s | 0.11 s | 3,879 | 196,270 | 51x |
| 4 | 84,812 | 19.74 s | 0.36 s | 4,296 | 236,019 | 55x |
| 5 | 228,133 | 51.00 s | 1.14 s | 4,473 | 200,699 | 45x |

At every depth the two engines visit the same number of positions and pick the same
best move with the same score in all ten positions, so the speedup is the language
alone: 45 to 55 times faster.

Niram-GOLD stays a direct copy, so it keeps Remus's slow parts: a board of characters,
a new list of moves at every node, a position key built as text after every move, and
a repetition test that reads the whole game history. A Rust engine written for speed
(bitboards, a numeric hash key, moves without heap memory) runs many times faster again,
but it would no longer search the same tree as Remus.
