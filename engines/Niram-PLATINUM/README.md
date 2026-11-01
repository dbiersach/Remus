# Niram-PLATINUM: Remus-PLATINUM in Rust

Niram-PLATINUM is Remus-PLATINUM rewritten in Rust, the way Niram-GOLD, in the folder beside this one, is Remus-GOLD rewritten in Rust. It is Niram-GOLD plus the ten enhancements that Remus-PLATINUM adds to Remus-GOLD, and the [Remus-PLATINUM README](<../instructor/12 Remus-PLATINUM - Ten more enhancements/README.md>) explains each one step by step, with the code. Given the same position and depth, Niram-PLATINUM and Remus-PLATINUM visit the same number of positions and choose the same move with the same score.

Niram-PLATINUM is the course designer's experiment, not part of the course.

## Files

Every file in `src/` matches the Niram-GOLD file of the same name, except for the four that hold the new code:

| Rust file | Remus-PLATINUM file | What it adds |
| --- | --- | --- |
| `exchange.rs` | `exchange.py` | Static exchange evaluation (SEE) |
| `search.rs` | `search.py` | Delta pruning and SEE in `quiescence`, futility pruning, `aspiration_search`, and time management in `think` |
| `search_tools.rs` | `search.py` | The new constants; `think` takes a planned time and a hard limit |
| `evaluation.rs` | `evaluation.py` | `game_phase`, `taper`, `tapered_terms`, `pawn_race`, `mobility`, and `piece_terms` |
| `uci_engine.rs` | `uci_engine.py` | `longest_time`, the hard limit on one move |

`taper` rounds with `div_euclid`, which rounds a negative score down the way Python's `//` does, so the two engines blend every score the same way.

## Build and run it

Install Rust as the [Niram-GOLD README](../Niram-GOLD/README.md#install-rust-on-windows) shows, then, from inside this folder:

```bash
cargo build --release                   # The program, target/release/niram-platinum.exe
cargo test --release                    # perft, SEE, and the node count of Remus-PLATINUM
cargo run --release -- bench 7          # Time Niram-PLATINUM on ten positions, depth 7
```

`.cargo/config.toml` keeps the Windows linker from writing a `.pdb` file, the same as in Niram-GOLD. To play Niram-PLATINUM in Lucas Chess, add `target/release/niram-platinum.exe` as a UCI engine.

`uv run misc/designer/engine_parity.py --version PLATINUM` checks that Niram-PLATINUM matches Remus-PLATINUM on 49 positions and writes [misc/designer/remus-niram_platinum_same_algorithms.md](../../misc/designer/remus-niram_platinum_same_algorithms.md). A change to Remus-PLATINUM's rules, evaluation, search, or opening book needs the same change here and a clean parity run.
